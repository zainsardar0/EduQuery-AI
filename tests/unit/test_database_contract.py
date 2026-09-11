import pytest
import sqlglot
from sqlglot import exp

from services.query.database_contract import (
    LIVE_WREN_OBJECTS,
    approved_objects,
    route_sql_to_contract,
)


def test_live_contract_routes_every_physical_table_into_reporting_schema():
    sql = (
        "SELECT t.SCHOOL, h.[PASS%] FROM dbo.TR_ALL AS t "
        "JOIN dbo.HOF_FRMT AS h ON h.EID = t.EID"
    )
    routed = route_sql_to_contract(sql, "live_v1")
    statement = sqlglot.parse_one(routed, read="tsql")
    references = {
        f"{table.db}.{table.name}".lower()
        for table in statement.find_all(exp.Table)
    }
    assert references == {
        "eduquery_reporting.tr_all",
        "eduquery_reporting.hof_frmt",
    }
    assert references <= LIVE_WREN_OBJECTS


def test_legacy_contract_preserves_verified_snapshot_sql():
    sql = "SELECT TOP 10 * FROM dbo.TR_ALL"
    assert route_sql_to_contract(sql, "legacy_snapshot") == sql


def test_unknown_contract_mode_fails_closed():
    with pytest.raises(ValueError):
        approved_objects("future-unapproved")
