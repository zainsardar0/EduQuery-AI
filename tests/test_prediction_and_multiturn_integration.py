"""
Automated Integration Tests for:
1. Academic Prediction AI (ML + SHAP) routing in /api/v1/query without WrenAI NL2SQL fallthrough.
2. Google File Search API policy RAG integration.
3. WrenAI NL2SQL live query execution.
4. Model isolation and structured data outputs.
"""

import pytest
from fastapi.testclient import TestClient
from services.api.main import app
from services.api.app.routes import query_routes


@pytest.fixture
def client():
    return TestClient(app)


AUTH_HEADERS = {
    "X-User-Id": "acceptance_tester",
    "X-User-Role": "admin",
    "X-Campus-Scope": "ALL"
}


def test_prediction_ai_query_routing(client):
    """Verify that engine='prediction_ai' returns Academic Prediction and SHAP text data instead of WrenAI NL2SQL."""
    payload = {
        "prompt": "Predict students in Class 10 at high risk of failing annual board exams",
        "engine": "prediction_ai",
        "filters": {"campus_code": "ALL"}
    }
    res = client.post("/api/v1/query", headers=AUTH_HEADERS, json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    ans_lower = data["answer"].lower()
    assert "risk" in ans_lower or "forecast" in ans_lower or "academic" in ans_lower or "fail" in ans_lower
    assert "Academic Risk Prediction" in data["evidence"]["intent_category"]
    
    # Text-only default (no table or chart unless requested)
    assert data.get("chart_config") is None


def test_prediction_ai_refuses_unvalidated_class_section_future_pass_rate(client, monkeypatch):
    """A scoped future pass-rate query must not fall through to generic all-campus prose."""
    def fail_if_live_context_is_queried(*_args, **_kwargs):
        raise AssertionError("unsupported forecast must not query live student records")

    monkeypatch.setattr(
        query_routes.prediction_intelligence,
        "_gather_live_context",
        fail_if_live_context_is_queried,
    )
    payload = {
        "prompt": "what will be the pass rate of ATKB Class 10 section A in 2027",
        "engine": "prediction_ai",
        "filters": {"campus_code": "ALL"},
    }

    res = client.post("/api/v1/query", headers=AUTH_HEADERS, json=payload)

    assert res.status_code == 200
    data = res.json()
    answer = data["answer"]
    assert "cannot produce a validated 2027 pass-rate forecast" in answer
    assert "ATKB Class 10 Section A" in answer
    assert "all 20 campuses" not in answer
    assert data["data_table"] is None
    assert data["evidence"]["campus_applied"] == "ATKB"
    assert data["evidence"]["tables_queried"] == []
    assert data["evidence"]["rag_sources_used"] == []
    assert "Not Supported" in data["evidence"]["intent_category"]


def test_prediction_ai_explicit_table_request(client):
    """Verify that engine='prediction_ai' provides a data_table when explicitly requested by user."""
    payload = {
        "prompt": "Show table of students in Class 10 at high risk of failing",
        "engine": "prediction_ai",
        "filters": {"campus_code": "ALL"}
    }
    res = client.post("/api/v1/query", headers=AUTH_HEADERS, json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["data_table"] is not None
    assert len(data["data_table"]["rows"]) > 0
    assert "fail_probability" in data["data_table"]["rows"][0]


def test_google_file_search_rag_routing(client):
    """Verify that engine='google_file_search_rag' queries policy documents with source citations."""
    payload = {
        "prompt": "What are the rules regarding day scholars admission and attendance?",
        "engine": "google_file_search_rag"
    }
    res = client.post("/api/v1/query", headers=AUTH_HEADERS, json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "(Source:" in data["answer"]
    assert "Policy" in data["evidence"]["intent_category"]
    assert len(data["evidence"]["rag_sources_used"]) > 0


def test_teacher_leave_query_does_not_match_tea_guardrail(client, monkeypatch):
    """The out-of-domain keyword 'tea' must not match inside 'teachers'."""
    prompt = "how can teachers apply for leave?"

    def fake_ask_policy(query):
        assert query == prompt
        return {
            "answer": "Teachers apply through the official leave process.\n\n(Source: Leave Policy.pdf)",
            "sources": ["Leave Policy.pdf"],
            "engine": "curated_policy_fallback",
            "latency_ms": 1.0,
        }

    monkeypatch.setattr(query_routes.gemini_file_rag, "ask_policy", fake_ask_policy)
    res = client.post(
        "/api/v1/query",
        headers=AUTH_HEADERS,
        json={"prompt": prompt, "engine": "google_file_search_rag"},
    )

    assert res.status_code == 200
    data = res.json()
    assert data["evidence"]["intent_category"] == "Policy Document Retrieval (Local Curated Fallback)"
    assert data["evidence"]["rag_sources_used"] == ["Leave Policy.pdf"]


def test_teacher_leave_fallback_returns_staff_process_only(monkeypatch):
    monkeypatch.setattr(query_routes.gemini_file_rag, "is_configured", lambda: False)

    result = query_routes.gemini_file_rag.ask_policy("how can teachers apply for leave?")

    assert "through the Vice Principal for onward approval by the Principal" in result["answer"]
    assert "must be sanctioned in advance" in result["answer"]
    assert "Fitness Certificate on Return" not in result["answer"]


def test_wren_nl2sql_routing(client):
    """Verify that engine='wren_nl2sql' translates prompt to T-SQL and returns table data."""
    payload = {
        "prompt": "Show weak students in class 10",
        "engine": "wren_nl2sql",
        "filters": {"campus_code": "ATKB"}
    }
    res = client.post("/api/v1/query", headers=AUTH_HEADERS, json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["data_table"] is not None


def test_conversational_failsafe(client):
    """Verify failsafe gracefully answers odd/chitchat queries like 'how are you' or 'supp ?'."""
    for odd_prompt in ["how are you", "supp ?", "hello", "hey", "what can you do"]:
        payload = {
            "prompt": odd_prompt,
            "engine": "wren_nl2sql"
        }
        res = client.post("/api/v1/query", headers=AUTH_HEADERS, json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        assert "EduQuery AI" in data["answer"]
        assert "Conversational Guidance" in data["evidence"]["intent_category"]


def test_flag_and_feedback_endpoint(client):
    """Verify that /api/v1/query/flag and /api/v1/query/feedback log events successfully."""
    payload = {
        "query_id": "test-123",
        "question": "Which students are at risk?",
        "engine": "prediction_ai",
        "feedback_type": "flag",
        "flagged": True,
        "details": "User flagged for review"
    }
    res = client.post("/api/v1/query/flag", headers=AUTH_HEADERS, json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["flagged"] is True
    assert "event_id" in data


def test_prediction_ai_campus_overall_query(client):
    """Verify that prompt 'best performing Campus overall for all the classes' returns multi-campus forecast."""
    payload = {
        "prompt": "best performing Campus overall for all the classes",
        "engine": "prediction_ai",
        "filters": {"campus_code": "ALL"}
    }
    res = client.post("/api/v1/query", headers=AUTH_HEADERS, json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    ans = data["answer"]
    assert "Hasilpur" in ans or "HSPB" in ans
    assert "Mianwali" in ans or "MNWG" in ans
    assert "all classes" in ans.lower()


def test_prediction_ai_campus_table_query(client):
    """Verify that prompt requesting a table of campus rankings returns structured data_table."""
    payload = {
        "prompt": "show table of best performing campus overall",
        "engine": "prediction_ai",
        "filters": {"campus_code": "ALL"}
    }
    res = client.post("/api/v1/query", headers=AUTH_HEADERS, json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["data_table"] is not None
    rows = data["data_table"]["rows"]
    assert len(rows) >= 5
    assert rows[0]["rank"] == 1
    assert "forecasted_gpa" in rows[0]


def test_prediction_ai_campus_class_10_query(client):
    """Verify that prompt 'best performing campus in class 10th' returns Class 10 specific forecast."""
    payload = {
        "prompt": "best performing campus in class 10th",
        "engine": "prediction_ai",
        "filters": {"campus_code": "ALL"}
    }
    res = client.post("/api/v1/query", headers=AUTH_HEADERS, json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    ans = data["answer"]
    assert "Class 10" in ans or "Matriculation" in ans
    assert "Hasilpur" in ans or "HSPB" in ans


def test_out_of_domain_guardrail(client):
    """Verify that out-of-domain queries like 'best coffee in lahore' or 'weather today' trigger domain boundary guard."""
    for odd_prompt in ["best coffee in lahore", "where to buy pizza in multan", "cricket match score", "weather forecast tomorrow"]:
        for eng in ["prediction_ai", "wren_nl2sql", "google_file_search_rag"]:
            payload = {
                "prompt": odd_prompt,
                "engine": eng
            }
            res = client.post("/api/v1/query", headers=AUTH_HEADERS, json=payload)
            assert res.status_code == 200
            data = res.json()
            assert data["success"] is True
            assert "EduQuery AI" in data["answer"]
            assert "Punjab Daanish Schools" in data["answer"]
            assert data["evidence"]["intent_category"] == "Out-of-Domain Guardrail & Domain Boundary Enforcement"
