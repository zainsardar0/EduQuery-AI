from typing import NamedTuple, Optional
import sqlglot
from sqlglot import exp
from services.api.query.allowlist import ALLOWLISTED_VIEWS


class ValidationResult(NamedTuple):
    is_valid: bool
    reason_code: Optional[str]
    safe_message: Optional[str]
    sanitized_sql: Optional[str]


def validate_and_sanitize_sql(raw_sql: str) -> ValidationResult:
    if not raw_sql or not raw_sql.strip():
        return ValidationResult(
            is_valid=False,
            reason_code="EMPTY_QUERY",
            safe_message="Query string cannot be empty.",
            sanitized_sql=None,
        )

    # 1. Parse SQL
    try:
        statements = sqlglot.parse(raw_sql)
    except Exception as exc:
        return ValidationResult(
            is_valid=False,
            reason_code="SQL_PARSE_ERROR",
            safe_message=f"SQL syntax error: {str(exc)}",
            sanitized_sql=None,
        )

    # 2. Enforce single-statement execution (prevent injection via semicolon)
    if len(statements) != 1 or statements[0] is None:
        return ValidationResult(
            is_valid=False,
            reason_code="MULTIPLE_STATEMENTS_DISALLOWED",
            safe_message="Multiple SQL statements in a single request are prohibited.",
            sanitized_sql=None,
        )

    ast = statements[0]

    # 3. Enforce SELECT-only statement
    if not isinstance(ast, exp.Select):
        return ValidationResult(
            is_valid=False,
            reason_code="NON_SELECT_SQL",
            safe_message="Security Policy Error: Only SELECT queries are permitted.",
            sanitized_sql=None,
        )

    # 4. Enforce view allowlist on all table/view references
    tables = list(ast.find_all(exp.Table))
    for table in tables:
        full_table_name = f"{table.db}.{table.name}".lower() if table.db else table.name.lower()
        if table.name.lower() == "unsupported_domain":
            return ValidationResult(
                is_valid=False,
                reason_code="UNSUPPORTED_DOMAIN",
                safe_message="Query refused: The prompt requests information outside the academic, attendance, results, and staff domains of Daanish School.",
                sanitized_sql=None,
            )
        if full_table_name not in ALLOWLISTED_VIEWS and table.name.lower() not in ALLOWLISTED_VIEWS:
            return ValidationResult(
                is_valid=False,
                reason_code="UNAPPROVED_OBJECT",
                safe_message=f"Security Policy Error: Query references unapproved database object '{full_table_name}'.",
                sanitized_sql=None,
            )

    # 5. Inject LIMIT 1000 if not present
    limit_clause = ast.find(exp.Limit)
    if limit_clause is None:
        ast = ast.limit(1000)
    else:
        # Cap existing limit at 1000
        limit_val = limit_clause.expression
        if isinstance(limit_val, exp.Literal):
            try:
                val = int(limit_val.this)
                if val > 1000:
                    limit_clause.set("expression", exp.Literal.number(1000))
            except ValueError:
                limit_clause.set("expression", exp.Literal.number(1000))

    sanitized_sql = ast.sql()
    return ValidationResult(
        is_valid=True,
        reason_code=None,
        safe_message=None,
        sanitized_sql=sanitized_sql,
    )
