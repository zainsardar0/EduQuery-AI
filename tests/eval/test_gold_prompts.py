import pytest

from services.api.app.services.gemini_file_rag import gemini_file_rag
from services.api.routers.policy_router import POLICY_ARTIFACT_IDS
from services.query.wren_engine import WrenEngine
from services.query.wren_semantic import plan_semantic_sql


QUERY_GOLD = [
    ("Show student roll list for class 10", "student_roster", "student_enrollment"),
    ("Show results for roll number 12345", "individual_results", "student_result_card"),
    ("Show daily student attendance report", "attendance_summary", "house_attendance"),
    ("Show teacher performance by subject", "teacher_performance", "teacher_results"),
    ("Compare school performance across all campuses", "school_performance", "teacher_results"),
    ("Show weak students needing remedial classes", "weak_students", "consolidated_results"),
]

POLICY_GOLD = [
    ("How can siblings be given admission?", "POL-003", 3),
    ("What is the policy for late arrival of students?", "POL-005", None),
    ("What medical policy applies to students?", "POL-007", None),
    ("What are the promotion and discharge rules for students?", "POL-008", None),
]


@pytest.mark.parametrize("prompt,expected_intent,expected_model", QUERY_GOLD)
def test_gold_prompt_nl2sql_accuracy(prompt, expected_intent, expected_model):
    engine = WrenEngine()
    decision = engine.interpret_local(prompt)
    assert decision.kind == "query"
    assert decision.plan is not None and decision.plan.intent == expected_intent
    semantic_sql, params = engine.compile(decision.plan)
    assert expected_model in semantic_sql
    physical_sql = plan_semantic_sql(semantic_sql)
    assert "SELECT" in physical_sql.upper()
    assert physical_sql != semantic_sql
    assert isinstance(params, list)


@pytest.mark.parametrize("query,artifact_id,page", POLICY_GOLD)
def test_gold_prompt_policy_retrieval_recall(query, artifact_id, page):
    res = gemini_file_rag.ask_policy(query)
    sources = res.get("sources", [])
    assert len(sources) > 0
    matched_ids = [POLICY_ARTIFACT_IDS.get(s, "POL-001") for s in sources]
    assert artifact_id in matched_ids
