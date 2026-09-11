"""
Unit Tests for Multi-Tier Prediction Endpoints (Students, Teachers, Subjects, Campuses)
"""

import pytest
from fastapi.testclient import TestClient
from services.api.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_student_prediction_high_risk(client):
    headers = {
        "X-User-Id": "test_user_01",
        "X-User-Role": "teacher",
        "X-Campus-Scope": "MNWB,ALL",
        "Content-Type": "application/json"
    }
    payload = {
        "target_type": "student",
        "target_id": "SYN_1001",
        "campus_code": "MNWB"
    }
    resp = client.post("/api/v1/prediction", json=payload, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["target_id"] == "SYN_1001"
    assert data["risk_level"] in ["HIGH", "CRITICAL"]
    assert data["predicted_score"] <= 55.0
    assert len(data["feature_attributions"]) > 0


def test_student_prediction_low_risk(client):
    headers = {
        "X-User-Id": "test_user_02",
        "X-User-Role": "principal",
        "X-Campus-Scope": "MNWB,ALL",
        "Content-Type": "application/json"
    }
    payload = {
        "target_type": "student",
        "target_id": "SYN_1002",
        "campus_code": "MNWB"
    }
    resp = client.post("/api/v1/prediction", json=payload, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["target_id"] == "SYN_1002"
    assert data["risk_level"] == "LOW"
    assert data["predicted_score"] >= 80.0


def test_teacher_prediction_endpoint(client):
    headers = {
        "X-User-Id": "test_user_03",
        "X-User-Role": "principal",
        "X-Campus-Scope": "DGKB,ALL",
        "Content-Type": "application/json"
    }
    payload = {
        "eid": "1042",
        "campus_code": "DGKB"
    }
    resp = client.post("/api/v1/prediction/teacher", json=payload, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "data" in data
    teacher_data = data["data"]
    assert teacher_data["eid"] == "1042"
    assert "forecasted_class_avg" in teacher_data
    assert "value_added_score" in teacher_data
    assert teacher_data["performance_tier"] in ["EXEMPLARY", "PROFICIENT", "DEVELOPING", "NEEDS_SUPPORT"]


def test_subject_prediction_endpoint(client):
    headers = {
        "X-User-Id": "test_user_04",
        "X-User-Role": "principal",
        "X-Campus-Scope": "ALL",
        "Content-Type": "application/json"
    }
    payload = {
        "subject": "MATHEMATICS",
        "class_grade": 9,
        "campus_code": "ALL"
    }
    resp = client.post("/api/v1/prediction/subject", json=payload, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "data" in data
    subj_data = data["data"]
    assert subj_data["subject"] == "MATHEMATICS"
    assert "expected_pass_pct" in subj_data
    assert "board_benchmark_pct" in subj_data
    assert "board_alignment_gap" in subj_data
    assert subj_data["bottleneck_risk_level"] in ["LOW", "MEDIUM", "HIGH"]


def test_campus_prediction_endpoint(client):
    headers = {
        "X-User-Id": "test_user_05",
        "X-User-Role": "admin",
        "X-Campus-Scope": "ALL,HSPB",
        "Content-Type": "application/json"
    }
    payload = {
        "campus_code": "HSPB"
    }
    resp = client.post("/api/v1/prediction/campus", json=payload, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "data" in data
    campus_data = data["data"]
    assert campus_data["campus_code"] == "HSPB"
    assert campus_data["national_rank"] == 1
    assert campus_data["forecasted_aggregate_gpa"] >= 90.0
    assert campus_data["standing_tier"] == "TOP_TIER"
