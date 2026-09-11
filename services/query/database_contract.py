"""Fixed physical-object routing for the versioned live reporting contract."""

from __future__ import annotations

import sqlglot
from sqlglot import exp


CONTRACT_VERSION = "2026.08.16.1"

LEGACY_WREN_OBJECTS = frozenset({
    "dbo.all_combined",
    "dbo.hof_frmt",
    "dbo.house_attendance_daily",
    "dbo.internal_exam_group_wise_performance_view",
    "dbo.internal_student_result_card_view",
    "dbo.marks",
    "dbo.prac",
    "dbo.students_roll",
    "dbo.students_roll_internal_exam",
    "dbo.students_result_total",
    "dbo.tr_all",
    "dbo.tr2_prac",
    "dbo.tr2_theory",
    "dbo.vteacher_sum_per",
    "dbo.vteacher_sum_per_board_middle",
})

LIVE_WREN_OBJECTS = frozenset(
    f"eduquery_reporting.{name.split('.', 1)[1]}" for name in LEGACY_WREN_OBJECTS
)


def approved_objects(contract_mode: str) -> frozenset[str]:
    if contract_mode == "legacy_snapshot":
        return LEGACY_WREN_OBJECTS
    if contract_mode == "live_v1":
        return LIVE_WREN_OBJECTS
    raise ValueError("Unknown SQL Server contract mode.")


def route_sql_to_contract(sql: str, contract_mode: str) -> str:
    """Move Wren's verified dbo references into the curated live schema."""
    if contract_mode == "legacy_snapshot":
        return sql
    if contract_mode != "live_v1":
        raise ValueError("Unknown SQL Server contract mode.")

    statements = sqlglot.parse(sql, read="tsql")
    if len(statements) != 1:
        raise ValueError("Expected one Wren SQL statement.")
    statement = statements[0]
    for table in statement.find_all(exp.Table):
        if table.catalog:
            raise ValueError("Catalog-qualified Wren objects are not supported.")
        qualified = f"{table.db}.{table.name}".lower() if table.db else table.name.lower()
        if qualified not in LEGACY_WREN_OBJECTS:
            continue
        table.set("db", exp.to_identifier("eduquery_reporting"))
    return statement.sql(dialect="tsql")
