import pytest
from fastapi.testclient import TestClient
from services.api.main import app

client = TestClient(app)

AUTH_HEADERS = {
    "X-User-Id": "test_admin",
    "X-User-Role": "admin",
    "X-Campus-Scope": "MNWB,MNWG,ATKB,ATKG,HSPB"
}


@pytest.mark.parametrize("engine", [
    "wren_nl2sql",
    "google_file_search_rag",
    "local_rag"
])
def test_all_engines_return_valid_response(engine):
    payload = {
        "prompt": "Show Class 10 performance and statistics",
        "engine": engine
    }
    response = client.post("/api/v1/query", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["answer"]) > 0
    assert "data_table" in data
    assert "chart_config" in data
    assert "evidence" in data
