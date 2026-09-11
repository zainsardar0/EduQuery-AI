from services.query.wren_engine import WrenEngine
from services.query.wren_semantic import plan_semantic_sql


def test_human_question_routes_to_semantic_plan():
    engine = WrenEngine()
    decision = engine.interpret_local("Show Mathematics performance for class 10")
    assert decision.kind == "query"
    assert decision.plan.intent == "subject_performance"
    assert decision.plan.class_level == 10
    assert decision.plan.subject == "MATHEMATICS"


def test_grade_level_result_question_stays_local_and_uses_class_performance():
    decision = WrenEngine().interpret_local("Give result distribution by grade level")
    assert decision.kind == "query"
    assert decision.plan.intent == "class_performance"


def test_semantic_sql_is_transformed_by_wren_mdl():
    engine = WrenEngine()
    plan = engine.interpret_local("Show attendance summary").plan
    semantic_sql, params = engine.compile(plan)
    physical_sql = plan_semantic_sql(semantic_sql)
    assert "FROM house_attendance" in semantic_sql
    assert "dbo.[House_Attendance_Daily]" in physical_sql
    assert params == []


def test_mutation_is_rejected_before_planning():
    assert not WrenEngine().is_safe_question("DROP TABLE STUDENTS_ROLL")


def test_generic_greeting_is_not_misclassified_as_analytics():
    decision = WrenEngine().interpret_local("How are you?")
    assert decision.kind == "conversation"
    assert decision.plan is None
