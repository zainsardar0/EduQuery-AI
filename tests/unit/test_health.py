from fastapi.testclient import TestClient
from services.api.main import app

client = TestClient(app)


def test_health_check_public_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "EduQuery-AI Backend API"
    assert data["version"] == "1.0.0-mvp"
    assert "components" in data
    assert "database" in data["components"]


def test_health_no_auth_required():
    # Health endpoint must be publicly accessible — no auth headers needed
    response = client.get("/health")
    assert response.status_code == 200


def test_health_timestamp_present():
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "service" in data
    assert "components" in data
    assert "database" in data["components"]


def test_stats_analytics_endpoint():
    response = client.get("/api/v1/analytics/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_students" in data
    assert data["total_students"] > 0
    assert "total_campuses" in data
    assert "top_campuses" in data
