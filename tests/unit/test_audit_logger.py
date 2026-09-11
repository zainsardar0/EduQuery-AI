import json
from pathlib import Path
from services.api.audit.logger import AuditLogger


def test_audit_event_logged(tmp_path: Path):
    log_file = tmp_path / "test_audit.jsonl"
    logger = AuditLogger(log_path=str(log_file))

    event = logger.log_event(
        request_id="req-test-1",
        user_id="user-1",
        access_scope="all_campuses",
        prompt_family="attendance",
        sql_generated=True,
        validation_result="PASS",
        external_call_made=False,
        execution_time_ms=32,
        outcome="success",
    )

    assert event["request_id"] == "req-test-1"
    assert event["actor_scope"]["access_scope"] == "all_campuses"
    assert event["outcome"] == "success"

    # Verify log file contents
    assert log_file.exists()
    lines = log_file.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 1
    log_data = json.loads(lines[0])
    assert log_data["request_id"] == "req-test-1"


def test_audit_log_excludes_raw_prompts_and_pii(tmp_path: Path):
    log_file = tmp_path / "test_audit_privacy.jsonl"
    logger = AuditLogger(log_path=str(log_file))

    logger.log_event(
        request_id="req-test-2",
        user_id="user-2",
        access_scope="all_campuses",
        prompt_family="academic_result",
        sql_generated=True,
        validation_result="PASS",
        external_call_made=True,
        execution_time_ms=45,
        outcome="success",
    )

    content = log_file.read_text(encoding="utf-8")
    assert "prompt_text" not in content
    assert "student_name" not in content
    assert "rows" not in content
    assert "sql_query" not in content
