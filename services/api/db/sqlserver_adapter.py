"""Read-only SQL Server adapter for the versioned Daanish reporting contract."""

from dataclasses import dataclass
import time
from typing import Any, Dict, List, Optional, Sequence

import pyodbc
import sqlglot
from sqlglot import exp

from services.api.config import get_settings
from services.query.database_contract import approved_objects


class LiveDatabaseUnavailable(ValueError):
    """The configured live database cannot safely serve a query."""


@dataclass(frozen=True)
class DatabasePreflightReport:
    ready: bool
    reason_codes: tuple[str, ...]
    contract_version: str | None = None


class SQLServerAdapter:
    """Opens a short-lived, read-only connection per request.

    This adapter intentionally exposes no write method. Database credentials must
    additionally be a dedicated read-only account before any public deployment.
    """

    def __init__(self, dsn: Optional[str] = None):
        settings = get_settings()
        self.settings = settings
        self.dsn = dsn or settings.sqlserver_dsn
        self.timeout_seconds = settings.sqlserver_query_timeout_seconds
        self.max_rows = settings.sqlserver_max_rows
        self.contract_mode = settings.sqlserver_contract_mode
        self.approved_objects = approved_objects(self.contract_mode)
        self._preflight_report: DatabasePreflightReport | None = None
        self._preflight_checked_at = 0.0
        lowered = self.dsn.lower().replace(" ", "")
        if "encrypt=yes" not in lowered and "encrypt=true" not in lowered:
            raise LiveDatabaseUnavailable("SQL Server DSN must require Encrypt=True.")
        if "applicationintent=readonly" not in lowered:
            raise LiveDatabaseUnavailable("SQL Server DSN must declare ApplicationIntent=ReadOnly.")

    def _connect(self) -> pyodbc.Connection:
        try:
            connection = pyodbc.connect(self.dsn, autocommit=True, timeout=self.timeout_seconds)
            self._assert_non_privileged_principal(connection)
            return connection
        except pyodbc.Error as exc:
            raise LiveDatabaseUnavailable("Live SQL Server connection failed.") from exc

    def _assert_non_privileged_principal(self, connection: pyodbc.Connection) -> None:
        """A connection-string flag is not a substitute for database permissions."""
        cursor = connection.cursor()
        cursor.execute(
            "SELECT IS_MEMBER('db_owner') AS is_db_owner, "
            "DATABASEPROPERTYEX(DB_NAME(), 'Updateability') AS updateability"
        )
        row = cursor.fetchone()
        is_owner = bool(row and row[0] == 1)
        database_is_read_only = bool(row and str(row[1]).upper() == "READ_ONLY")
        settings = self.settings
        demo_override = settings.app_env.lower() != "production" and settings.allow_privileged_demo_db_user
        read_only_demo = settings.app_env.lower() != "production" and database_is_read_only
        if is_owner and not (demo_override or read_only_demo):
            connection.close()
            raise LiveDatabaseUnavailable(
                "Configured SQL Server identity is db_owner; a dedicated read-only login is required."
            )

    @staticmethod
    def _validate_read_only_sql(
        sql: str, allowed_objects: frozenset[str] | None = None
    ) -> None:
        """Reject anything outside one SELECT over the approved Wren physical objects."""
        try:
            statements = sqlglot.parse(sql, read="tsql")
        except sqlglot.errors.ParseError as exc:
            raise LiveDatabaseUnavailable("SQL Server query failed the read-only syntax gate.") from exc
        if len(statements) != 1 or not isinstance(statements[0], exp.Select):
            raise LiveDatabaseUnavailable("SQL Server adapter accepts one SELECT statement only.")

        statement = statements[0]
        allowed = allowed_objects or approved_objects("legacy_snapshot")
        cte_names = {cte.alias_or_name.lower() for cte in statement.find_all(exp.CTE)}
        for table in statement.find_all(exp.Table):
            if not table.db and table.name.lower() in cte_names:
                continue
            qualified = f"{table.db}.{table.name}".lower() if table.db else table.name.lower()
            if table.catalog or qualified not in allowed:
                raise LiveDatabaseUnavailable("SQL Server query references an unapproved object.")

    def _run_preflight(self, connection: pyodbc.Connection) -> DatabasePreflightReport:
        issues: list[str] = []
        cursor = connection.cursor()
        cursor.execute(
            "SELECT DB_NAME() AS database_name, "
            "DATABASEPROPERTYEX(DB_NAME(), 'Updateability') AS updateability, "
            "IS_MEMBER('db_owner') AS is_db_owner, "
            "IS_MEMBER('db_datawriter') AS is_db_datawriter, "
            "IS_SRVROLEMEMBER('sysadmin') AS is_sysadmin"
        )
        row = cursor.fetchone()
        database_name = str(row[0]) if row else ""
        database_is_read_only = bool(row and str(row[1]).upper() == "READ_ONLY")
        privileged = bool(row and any(value == 1 for value in row[2:5]))
        demo_exception = (
            self.settings.app_env.lower() != "production"
            and (self.settings.allow_privileged_demo_db_user or database_is_read_only)
        )
        if privileged and not demo_exception:
            issues.append("PRIVILEGED_DATABASE_IDENTITY")
        expected_database = self.settings.sqlserver_expected_database.strip()
        if expected_database and database_name.casefold() != expected_database.casefold():
            issues.append("UNEXPECTED_DATABASE")

        for qualified in sorted(self.approved_objects):
            cursor.execute(
                "SELECT OBJECT_ID(?), "
                "HAS_PERMS_BY_NAME(?, 'OBJECT', 'SELECT'), "
                "HAS_PERMS_BY_NAME(?, 'OBJECT', 'INSERT'), "
                "HAS_PERMS_BY_NAME(?, 'OBJECT', 'UPDATE'), "
                "HAS_PERMS_BY_NAME(?, 'OBJECT', 'DELETE'), "
                "HAS_PERMS_BY_NAME(?, 'OBJECT', 'ALTER'), "
                "HAS_PERMS_BY_NAME(?, 'OBJECT', 'CONTROL')",
                [qualified] * 7,
            )
            permission_row = cursor.fetchone()
            if not permission_row or permission_row[0] is None:
                issues.append("MISSING_REPORTING_OBJECT")
                continue
            if permission_row[1] != 1:
                issues.append("MISSING_REPORTING_SELECT")
            if any(value == 1 for value in permission_row[2:]):
                issues.append("WRITABLE_REPORTING_OBJECT")

        contract_version: str | None = None
        expected_contract = self.settings.sqlserver_expected_contract_version.strip()
        if expected_contract:
            try:
                cursor.execute(
                    "SELECT TOP (1) ContractVersion "
                    "FROM eduquery_reporting.SemanticContract "
                    "WHERE IsActive = 1 ORDER BY ActivatedAt DESC"
                )
                contract_row = cursor.fetchone()
                contract_version = str(contract_row[0]) if contract_row else None
            except pyodbc.Error:
                issues.append("MISSING_SEMANTIC_CONTRACT")
            if contract_version != expected_contract:
                issues.append("SEMANTIC_CONTRACT_MISMATCH")

        return DatabasePreflightReport(
            ready=not issues,
            reason_codes=tuple(sorted(set(issues))),
            contract_version=contract_version,
        )

    def preflight(self, *, force: bool = False) -> DatabasePreflightReport:
        now = time.monotonic()
        if (
            not force
            and self._preflight_report is not None
            and now - self._preflight_checked_at < self.settings.sqlserver_preflight_cache_seconds
        ):
            return self._preflight_report
        try:
            with self._connect() as connection:
                report = self._run_preflight(connection)
        except LiveDatabaseUnavailable:
            report = DatabasePreflightReport(False, ("DATABASE_CONNECTION_FAILED",))
        self._preflight_report = report
        self._preflight_checked_at = now
        return report

    def execute_query(self, sql: str, params: Optional[Sequence[Any]] = None) -> List[Dict[str, Any]]:
        self._validate_read_only_sql(sql, self.approved_objects)
        try:
            with self._connect() as connection:
                connection.timeout = self.timeout_seconds
                cursor = connection.cursor()
                cursor.execute(sql, params or [])
                columns = [column[0] for column in cursor.description or []]
                rows = cursor.fetchmany(self.max_rows)
                return [dict(zip(columns, row)) for row in rows]
        except LiveDatabaseUnavailable:
            raise
        except pyodbc.Error as exc:
            raise LiveDatabaseUnavailable("Live SQL Server query failed.") from exc

    def healthcheck(self) -> bool:
        return self.preflight().ready
