import pytest
from fastapi.testclient import TestClient
from services.api.main import app

client = TestClient(app)

AUTH_HEADERS = {
    "X-User-Id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
    "X-User-Role": "principal",
    "X-Campus-Scope": "MNWB,MNWG",
}


def test_query_authorized_campus_returns_200():
    payload = {
        "prompt": "Show pass percentage by subject for class 10 in MNWB for 2026.",
        "filters": {"campus_code": "MNWB", "class_level": 10}
    }
    response = client.post("/api/v1/query", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "answer" in data
    assert "data_table" in data
    assert "chart_config" in data
    assert "evidence" in data
    assert data["evidence"]["campus_applied"] == "MNWB"


def test_query_cross_campus_denied_403():
    payload = {
        "prompt": "Show pass percentage for KRAS campus.",
        "filters": {"campus_code": "KRAS"}
    }
    response = client.post("/api/v1/query", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 403
    data = response.json()
    assert data["error_code"] == "CROSS_CAMPUS_ACCESS_DENIED"


def test_query_unauthenticated_returns_401():
    payload = {"prompt": "Show all student results"}
    response = client.post("/api/v1/query", json=payload)
    assert response.status_code == 401


def test_query_empty_prompt_returns_400():
    payload = {"prompt": "AB"}
    response = client.post("/api/v1/query", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 400


def test_query_response_has_data_table_columns():
    payload = {"prompt": "Show performance for MNWB campus."}
    response = client.post("/api/v1/query", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data["data_table"]["columns"]) > 0
    assert data["data_table"]["total_rows"] >= 0
