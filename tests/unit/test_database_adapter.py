import pytest
from services.api.app.adapters.database import DatabaseAdapter, UnsafeQueryError


@pytest.fixture
def adapter():
    return DatabaseAdapter(fallback_file_path="data/semantic/demo_fallback.json")


def test_valid_select_passes(adapter):
    assert adapter.validate_sql_safety("SELECT TOP 100 * FROM vw_CONSOLIDATED_ACCURATE WHERE SCHOOL = 'MNWB'")


def test_valid_cte_passes(adapter):
    sql = "WITH ranked AS (SELECT SCHOOL, PASS_PERCENTAGE FROM vw_CONSOLIDATED_ACCURATE) SELECT * FROM ranked"
    assert adapter.validate_sql_safety(sql)


def test_insert_blocked(adapter):
    with pytest.raises(UnsafeQueryError):
        adapter.validate_sql_safety("INSERT INTO MARKS VALUES (1, 2, 95)")


def test_update_blocked(adapter):
    with pytest.raises(UnsafeQueryError):
        adapter.validate_sql_safety("UPDATE MARKS SET OBTAINED_MARKS = 100 WHERE ID = 1")


def test_delete_blocked(adapter):
    with pytest.raises(UnsafeQueryError):
        adapter.validate_sql_safety("DELETE FROM STUDENTS_ROLL WHERE ID = 1")


def test_drop_blocked(adapter):
    with pytest.raises(UnsafeQueryError):
        adapter.validate_sql_safety("DROP TABLE MARKS")


def test_exec_blocked(adapter):
    with pytest.raises(UnsafeQueryError):
        adapter.validate_sql_safety("EXEC GenerateConsolidatedView @ExamType='ANNUAL', @Year=26")


def test_system_table_blocked(adapter):
    with pytest.raises(UnsafeQueryError):
        adapter.validate_sql_safety("SELECT * FROM sys.tables")


def test_multi_statement_blocked(adapter):
    with pytest.raises(UnsafeQueryError):
        adapter.validate_sql_safety("SELECT 1; DROP TABLE MARKS")


def test_fallback_query_returns_data(adapter):
    rows, fallback_used, exec_ms = adapter.execute_query_with_fallback(
        intent_prompt="Pass percentage for MNWB",
        campus_code="MNWB",
        class_level=10
    )
    assert isinstance(rows, list)
    assert isinstance(fallback_used, bool)
    assert exec_ms >= 0


def test_fallback_prediction_returns_shap(adapter):
    pred, fallback_used, exec_ms = adapter.get_prediction(
        target_id="SYN_1001",
        campus_code="MNWB"
    )
    assert pred["target_id"] == "SYN_1001"
    assert pred["risk_level"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    assert len(pred["feature_attributions"]) > 0
