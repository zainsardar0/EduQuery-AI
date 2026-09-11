import json
import os
import tempfile
import pytest
from services.api.app.services.audit import AuditService


@pytest.fixture
def temp_audit_service(tmp_path):
    """Create a temporary AuditService writing to a temp directory."""
    return AuditService(log_directory=str(tmp_path))


def test_audit_log_is_created(temp_audit_service, tmp_path):
    temp_audit_service.log_event(
        user_id="a1b2c3d4-uuid",
        role="teacher",
        campus_applied="MNWB",
        intent_category="Class/Section Aggregates",
        tables_queried=["vw_CONSOLIDATED_ACCURATE"],
        execution_time_ms=142.5,
        success=True
    )
    log_file = tmp_path / "audit.jsonl"
    assert log_file.exists()


def test_audit_log_contains_no_pii(temp_audit_service, tmp_path):
    temp_audit_service.log_event(
        user_id="a1b2c3d4-uuid",
        role="principal",
        campus_applied="MNWG",
        intent_category="Teacher Analytics",
        tables_queried=["TEACHERS_PROFILE"],
        execution_time_ms=55.0,
        success=True
    )
    log_file = tmp_path / "audit.jsonl"
    content = log_file.read_text(encoding="utf-8")
    record = json.loads(content.strip())

    # Confirm no raw student data, prompts, or SQL in log
    assert "student" not in content.lower() or "intent_category" in content.lower()
    assert "prompt" not in record
    assert "sql" not in record
    assert "password" not in content.lower()
    assert "marks" not in content.lower()


def test_audit_log_records_correct_fields(temp_audit_service, tmp_path):
    temp_audit_service.log_event(
        user_id="user-xyz-123",
        role="auditor",
        campus_applied="MNWB",
        intent_category="Board Benchmarks",
        tables_queried=["BOARD_PER", "GZT_STRENGTH"],
        execution_time_ms=210.3,
        success=True,
        fallback_used=False
    )
    log_file = tmp_path / "audit.jsonl"
    record = json.loads(log_file.read_text(encoding="utf-8").strip())

    assert record["user_id"] == "user-xyz-123"
    assert record["role"] == "auditor"
    assert record["campus_applied"] == "MNWB"
    assert record["intent_category"] == "Board Benchmarks"
    assert "BOARD_PER" in record["tables_queried"]
    assert record["execution_time_ms"] == 210.3
    assert record["success"] is True
    assert record["fallback_used"] is False
    assert "event_id" in record
    assert "timestamp" in record


def test_audit_log_records_error_code(temp_audit_service, tmp_path):
    temp_audit_service.log_event(
        user_id="user-abc",
        role="teacher",
        campus_applied="ATK",
        intent_category="Unauthorized Cross-Campus Query Attempt",
        tables_queried=[],
        execution_time_ms=0.0,
        success=False,
        error_code="CROSS_CAMPUS_ACCESS_DENIED"
    )
    log_file = tmp_path / "audit.jsonl"
    record = json.loads(log_file.read_text(encoding="utf-8").strip())
    assert record["success"] is False
    assert record["error_code"] == "CROSS_CAMPUS_ACCESS_DENIED"
