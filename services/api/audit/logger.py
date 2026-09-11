import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from services.api.config import get_settings


class AuditLogger:
    """Append-only operational audit log with no prompts, PII, or result rows."""

    def __init__(self, log_path: Optional[str] = None):
        self.log_path = Path(log_path or get_settings().audit_log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log_event(
        self,
        request_id: str,
        user_id: str,
        access_scope: str,
        prompt_family: str,
        sql_generated: bool,
        validation_result: str,
        external_call_made: bool,
        execution_time_ms: int,
        outcome: str,
        reason_code: Optional[str] = None,
    ) -> dict:
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": request_id,
            "actor_scope": {"user_id": user_id, "access_scope": access_scope},
            "prompt_family": prompt_family,
            "sql_generated": sql_generated,
            "validation_result": validation_result,
            "external_call_made": external_call_made,
            "execution_time_ms": execution_time_ms,
            "outcome": outcome,
            "reason_code": reason_code,
        }
        with open(self.log_path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(event) + "\n")
        return event
