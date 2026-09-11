"""Regression coverage for the retired persona access model.

Legacy role and campus token arguments must not change SQL visibility. The human-query
accuracy benchmark lives in test_wren_human_queries.py.
"""

from fastapi.testclient import TestClient

from services.api.auth.provider import issue_demo_token
from services.api.db.provider import get_data_adapter
from services.api.main import app


class UniformFakeAdapter:
    def execute_query(self, sql, params=None):
        return [{"campus": "ATKB", "percentage": 32.5}]

    def healthcheck(self):
        return True


def _execute(token: str, prompt: str):
    return TestClient(app).post(
        "/api/v1/query/execute",
        headers={"Authorization": f"Bearer {token}"},
        json={"prompt": prompt, "include_explanation": True},
    ).json()


def test_legacy_persona_arguments_cannot_change_all_campus_visibility():
    teacher = issue_demo_token(user_id="teacher_maryam", campus_id="ATKB", role="teacher")
    coordinator = issue_demo_token(user_id="coord_tariq", campus_id="MNWB", role="admin")
    app.dependency_overrides[get_data_adapter] = lambda: UniformFakeAdapter()
    try:
        teacher_result = _execute(teacher, "Show weak students across all campuses")
        coordinator_result = _execute(coordinator, "Show weak students across all campuses")
    finally:
        app.dependency_overrides.clear()

    assert teacher_result["status"] == coordinator_result["status"] == "success"
    assert teacher_result["generated_sql"] == coordinator_result["generated_sql"]
    assert teacher_result["rows"] == coordinator_result["rows"]
    assert teacher_result["semantic_intent"] == coordinator_result["semantic_intent"] == "weak_students"


def test_explicit_campus_filter_is_query_content_not_token_authorization():
    token = issue_demo_token(user_id="any_authenticated_user", campus_id="MNWB", role="teacher")
    app.dependency_overrides[get_data_adapter] = lambda: UniformFakeAdapter()
    try:
        result = _execute(token, "Show weak students for ATKB campus")
    finally:
        app.dependency_overrides.clear()

    assert result["status"] == "success"
    assert result["semantic_intent"] == "weak_students"
    assert result["rows"][0]["campus"] == "ATKB"
