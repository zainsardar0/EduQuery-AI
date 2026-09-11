from fastapi.testclient import TestClient

from services.api.auth.provider import issue_demo_token
from services.api.db.provider import get_data_adapter
from services.api.main import app


class FakeAdapter:
    def __init__(self):
        self.calls = []

    def execute_query(self, sql, params=None):
        self.calls.append((sql, params or []))
        return [{"campus": "ATKB", "percentage": 31.5}]

    def healthcheck(self):
        return True


def _headers():
    return {"Authorization": f"Bearer {issue_demo_token()}"}


def test_local_weak_query_uses_wren_and_all_campuses():
    adapter = FakeAdapter()
    app.dependency_overrides[get_data_adapter] = lambda: adapter
    try:
        response = TestClient(app).post(
            "/api/v1/query/execute",
            json={"prompt": "Show weak students in class 10"},
            headers=_headers(),
        )
    finally:
        app.dependency_overrides.clear()
    data = response.json()
    assert data["status"] == "success"
    assert data["planner_source"] == "local"
    assert data["semantic_layer"].startswith("wrenai-0.13.")
    assert data["generated_sql"] is not None
    assert "dbo.students_result_total" in adapter.calls[0][0]
    assert adapter.calls[0][1] == ["TOTAL", 40.0, 10]


def test_conversation_never_executes_sql_or_provider():
    adapter = FakeAdapter()
    app.dependency_overrides[get_data_adapter] = lambda: adapter
    try:
        data = TestClient(app).post(
            "/api/v1/query/execute", json={"prompt": "How are you?"}, headers=_headers()
        ).json()
    finally:
        app.dependency_overrides.clear()
    assert data["status"] == "success"
    assert data["semantic_intent"] == "conversation"
    assert data["generated_sql"] is None
    assert adapter.calls == []


def test_personal_query_is_local_instead_of_remote_blocked():
    adapter = FakeAdapter()
    app.dependency_overrides[get_data_adapter] = lambda: adapter
    try:
        data = TestClient(app).post(
            "/api/v1/query/execute",
            json={"prompt": "Show results for roll number 12345"},
            headers=_headers(),
        ).json()
    finally:
        app.dependency_overrides.clear()
    assert data["status"] == "success"
    assert data["semantic_intent"] == "individual_results"
    assert data["planner_source"] == "local"
    assert adapter.calls[0][1] == ["12345"]


def test_sql_control_is_refused_before_database():
    adapter = FakeAdapter()
    app.dependency_overrides[get_data_adapter] = lambda: adapter
    try:
        data = TestClient(app).post(
            "/api/v1/query/execute", json={"prompt": "DROP TABLE MARKS"}, headers=_headers()
        ).json()
    finally:
        app.dependency_overrides.clear()
    assert data["reason_code"] == "NON_SELECT_SQL"
    assert adapter.calls == []


def test_unverified_cross_table_gold_prompt_is_safely_refused():
    adapter = FakeAdapter()
    app.dependency_overrides[get_data_adapter] = lambda: adapter
    try:
        data = TestClient(app).post(
            "/api/v1/query/execute",
            json={"prompt": "Predict whether Class 10 Mathematics Annual average will exceed last Mock"},
            headers=_headers(),
        ).json()
    finally:
        app.dependency_overrides.clear()
    assert data["reason_code"] == "GOVERNED_CAPABILITY_REQUIRED"
    assert adapter.calls == []


def test_catalog_summary_is_grounded_and_more_detailed():
    adapter = FakeAdapter()
    app.dependency_overrides[get_data_adapter] = lambda: adapter
    try:
        data = TestClient(app).post(
            "/api/v1/query/execute",
            json={"prompt": "How many students are enrolled in Class 8 this year in ATKB?"},
            headers=_headers(),
        ).json()
    finally:
        app.dependency_overrides.clear()
    assert data["status"] == "success"
    assert "read-only database" in data["explanation"]
    assert "no external model" in data["explanation"]
