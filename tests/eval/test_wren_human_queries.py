import pytest

from services.query.wren_engine import WrenEngine
from services.query.wren_semantic import plan_semantic_sql
from tests.eval.dataset_wren_human_queries import HUMAN_QUERY_CASES


@pytest.fixture(scope="module")
def engine():
    return WrenEngine()


@pytest.mark.parametrize("case", HUMAN_QUERY_CASES, ids=lambda case: case["prompt"])
def test_one_hundred_human_queries_route_without_provider(case, engine):
    prompt = case["prompt"]
    assert engine.is_safe_question(prompt) is case["safe"]
    if not case["safe"]:
        return

    decision = engine.interpret_local(prompt)
    assert decision.kind == case["expected_kind"]
    assert engine.can_send_to_remote_planner(prompt) is case["remote_allowed"]
    if decision.kind != "query":
        return

    assert decision.plan is not None
    if case["expected_intent"] is not None:
        assert decision.plan.intent == case["expected_intent"]
    else:
        assert decision.plan.intent in {"individual_student", "individual_results", "student_attendance"}
    semantic_sql, params = engine.compile(decision.plan)
    physical_sql = plan_semantic_sql(semantic_sql)
    assert "dbo." in physical_sql
    assert physical_sql.count("?") == len(params)


def test_acceptance_set_is_exactly_one_hundred_unique_prompts():
    prompts = [case["prompt"].casefold() for case in HUMAN_QUERY_CASES]
    assert len(prompts) == 100
    assert len(set(prompts)) == 100
