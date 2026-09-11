import json
from pathlib import Path
from packages.contracts.schemas.auth import AuthContext
from packages.contracts.schemas.query import QueryRequest, QueryResponse, QueryRefusal
from packages.contracts.schemas.prediction import PredictionRequest, PredictionResponse
from packages.contracts.schemas.policy import PolicyRequest, PolicyResponse
from packages.contracts.schemas.errors import APIError


def test_auth_context_schema():
    auth = AuthContext(user_id="user123", access_scope="all_campuses", demo_mode=True)
    assert auth.user_id == "user123"
    assert auth.access_scope == "all_campuses"
    assert auth.demo_mode is True


def test_query_schemas():
    req = QueryRequest(prompt="Show grade 10 attendance")
    assert req.prompt == "Show grade 10 attendance"
    assert req.include_explanation is True

    res = QueryResponse(
        query_id="q-101",
        generated_sql="SELECT * FROM governed_attendance",
        columns=["student_id", "status"],
        rows=[{"student_id": "S101", "status": "Present"}],
        row_count=1,
        execution_time_ms=45,
    )
    assert res.status == "success"
    assert res.row_count == 1

    ref = QueryRefusal(
        query_id="q-102",
        reason_code="NON_SELECT_SQL",
        safe_message="Only SELECT queries are allowed."
    )
    assert ref.status == "refused"


def test_prediction_schemas():
    req = PredictionRequest(student_features={"gpa": 3.5, "attendance_rate": 0.92}, target="academic_risk")
    assert req.target == "academic_risk"

    res = PredictionResponse(
        prediction_id="p-101",
        risk_score=0.15,
        risk_label="low",
        mlflow_run_id="run-99",
        shap_values={"attendance_rate": -0.4}
    )
    assert res.risk_score == 0.15
    assert "advisory" in res.disclaimer.lower()


def test_policy_schemas():
    req = PolicyRequest(issue_description="Leave policy for teachers during exam week")
    assert req.issue_description.startswith("Leave policy")

    res = PolicyResponse(
        status="found",
        policy_id="pol-101",
        relevant_sections=[{"section": "4.2", "title": "Exam Leave"}],
        explanation="Teachers may apply for exam leave 7 days in advance."
    )
    assert res.status == "found"
    assert "human officers" in res.disclaimer.lower()


def test_error_schema():
    err = APIError(
        error_code="UNAUTHORIZED",
        safe_message="Authentication token missing or invalid.",
        request_id="req-555"
    )
    assert err.status == "error"
    assert err.error_code == "UNAUTHORIZED"


def test_dist_exports_exist():
    dist_dir = Path(__file__).parent.parent.parent / "packages" / "contracts" / "dist"
    assert (dist_dir / "types.d.ts").exists()
    assert (dist_dir / "schemas" / "AuthContext.json").exists()
    assert (dist_dir / "schemas" / "QueryResponse.json").exists()
