import pytest

from services.api.config import Settings
from services.query.wren_engine import LIVE_CAMPUSES, PlanError, WrenEngine
from services.query.wren_semantic import plan_semantic_sql, semantic_layer_ready


def _plan(**overrides):
    return {
        "intent": "weak_students", "campus": "ATKB", "class_level": 10,
        "section": None, "year": 26, "subject": None, "house": None,
        "threshold": 40, "limit": 25, **overrides,
    }


def test_compiler_uses_parameterized_semantic_sql_then_wren_physical_sql():
    engine = WrenEngine()
    plan = engine.validate_plan(_plan())
    semantic_sql, params = engine.compile(plan)
    physical_sql = plan_semantic_sql(semantic_sql)
    assert "FROM consolidated_results" in semantic_sql
    assert "dbo.students_result_total" in physical_sql
    assert params == ["TOTAL", 40.0, "ATKB", 10, 26]


def test_strict_wren_runtime_loads_built_mdl():
    assert semantic_layer_ready() is True


def test_all_campuses_is_default_and_explicit_filter_is_optional():
    engine = WrenEngine()
    all_plan = engine.interpret_local("Show weak students in class 10").plan
    one_plan = engine.interpret_local("Show weak students in ATKB class 10").plan
    assert all_plan.campus == "ALL"
    assert one_plan.campus == "ATKB"


def test_unknown_campus_is_rejected():
    with pytest.raises(PlanError):
        WrenEngine().validate_plan(_plan(campus="DAANISH-01"))


def test_personal_and_sql_control_prompts_never_reach_remote_planner():
    engine = WrenEngine()
    assert not engine.can_send_to_remote_planner("Show marks for student named Ali Khan")
    assert not engine.can_send_to_remote_planner("Show roll no 12345")
    assert not engine.is_safe_question("DROP TABLE MARKS")
    assert engine.is_safe_question("Show weak students in ATKB")
    assert "ATKB" in LIVE_CAMPUSES


def test_remote_planner_payload_drops_unknown_words_and_names():
    payload = WrenEngine().remote_planner_prompt(
        "Compare Ali's overall school performance with Sara in ATKB class 10"
    )
    assert "Ali" not in payload
    assert "Sara" not in payload
    assert "school" in payload
    assert "performance" in payload
    assert "ATKB" in payload
    assert '"class_level": 10' in payload


def test_production_config_fails_closed_on_demo_defaults():
    with pytest.raises(ValueError, match="ENABLE_DEMO_AUTH"):
        Settings(app_env="production")
    settings = Settings(
        app_env="production", enable_demo_auth=False,
        jwt_secret="a-secure-non-demo-secret-with-32-characters",
        jwt_issuer="institution-identity",
        allowed_origins="https://eduquery.example.edu",
        allow_privileged_demo_db_user=False,
        sqlserver_dsn=(
            "Driver={ODBC Driver 18 for SQL Server};Server=sql.daanish.edu.pk;"
            "Database=EduQueryLive;Encrypt=yes;TrustServerCertificate=no;ApplicationIntent=ReadOnly;"
        ),
        sqlserver_contract_mode="live_v1",
        sqlserver_expected_database="EduQueryLive",
        sqlserver_expected_contract_version="2026.08.16.1",
    )
    assert settings.app_env == "production"
