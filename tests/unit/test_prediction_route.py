import pytest
from fastapi.testclient import TestClient
from services.api.main import app

client = TestClient(app)

AUTH_HEADERS = {
    "X-User-Id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
    "X-User-Role": "teacher",
    "X-Campus-Scope": "MNWB,MNWG",
    "X-Teacher-Eid": "1042",
}


def test_prediction_authorized_returns_200():
    payload = {
        "target_type": "student",
        "target_id": "SYN_1001",
        "campus_code": "MNWB",
        "academic_year": 26,
        "prediction_horizon": "annual_board"
    }
    response = client.post("/api/v1/prediction", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["target_id"] == "SYN_1001"
    assert data["risk_level"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    assert 0.0 <= data["predicted_score"] <= 100.0
    assert "feature_attributions" in data
    assert "disclaimer" in data
    assert "ADVISORY NOTICE" in data["disclaimer"]


def test_prediction_cross_campus_denied_403():
    payload = {
        "target_type": "student",
        "target_id": "SYN_1001",
        "campus_code": "ATKB",
    }
    response = client.post("/api/v1/prediction", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 403
    data = response.json()
    assert data["error_code"] == "CROSS_CAMPUS_ACCESS_DENIED"


def test_prediction_unauthenticated_returns_401():
    payload = {"target_type": "student", "target_id": "SYN_1001"}
    response = client.post("/api/v1/prediction", json=payload)
    assert response.status_code == 401


def test_prediction_shap_attributions_present():
    payload = {
        "target_type": "student",
        "target_id": "SYN_1002",
        "campus_code": "MNWB"
    }
    response = client.post("/api/v1/prediction", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data["feature_attributions"]) > 0
    first_attr = data["feature_attributions"][0]
    assert "feature_name" in first_attr
    assert "shap_value" in first_attr
    assert first_attr["impact_direction"] in ["INCREASES_RISK", "DECREASES_RISK"]


def test_prediction_model_metadata_present():
    payload = {
        "target_type": "student",
        "target_id": "SYN_1001",
        "campus_code": "MNWB"
    }
    response = client.post("/api/v1/prediction", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    meta = data["model_metadata"]
    assert "model_name" in meta
    assert "mlflow_run_id" in meta
