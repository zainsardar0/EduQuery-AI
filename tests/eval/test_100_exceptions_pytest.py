"""Legacy exception corpus retained as a fail-closed compatibility gate.

Its historical table-name expectations describe the retired seed schema. Accuracy for
the approved Wren semantic model is enforced by test_wren_human_queries.py.
"""

import pytest
from fastapi.testclient import TestClient

from services.api.auth.provider import issue_demo_token
from services.api.db.provider import get_data_adapter
from services.api.main import app
from tests.eval.dataset_100_exception_prompts import EXCEPTION_PROMPT_BENCHMARK


SAFE_REFUSALS = {
    "NON_SELECT_SQL",
    "UNAPPROVED_OBJECT",
    "UNSUPPORTED_DOMAIN",
    "FORBIDDEN_MUTATION",
    "OUT_OF_SCOPE",
    "MODEL_DISABLED",
    "UNSUPPORTED_SEMANTIC_PLAN",
    "WREN_SEMANTIC_REJECTED",
}


class FakeAdapter:
    def execute_query(self, sql, params=None):
        return [{"campus": "ATKB", "record_count": 1}]

    def healthcheck(self):
        return True


@pytest.fixture(autouse=True)
def _local_database_only():
    app.dependency_overrides[get_data_adapter] = lambda: FakeAdapter()
    yield
    app.dependency_overrides.clear()


client = TestClient(app)
headers = {"Authorization": f"Bearer {issue_demo_token(user_id='exception_eval')}"}


@pytest.mark.parametrize(
    "item", EXCEPTION_PROMPT_BENCHMARK, ids=[item["id"] for item in EXCEPTION_PROMPT_BENCHMARK]
)
def test_wren_exception_prompt_handling(item):
    response = client.post(
        "/api/v1/query/execute",
        headers=headers,
        json={"prompt": item["prompt"], "include_explanation": True},
    )
    assert response.status_code == 200
    data = response.json()

    if item["expected_action"] == "refuse":
        assert data["status"] == "refused"
        assert data["reason_code"] in SAFE_REFUSALS
        return

    assert data["status"] in {"success", "refused"}
    if data["status"] == "success":
        assert data["semantic_layer"].startswith("wrenai-")
        assert data["planner_source"] == "local"
        assert data["generated_sql"]
    else:
        assert data["reason_code"] in SAFE_REFUSALS
