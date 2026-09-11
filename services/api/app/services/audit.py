import datetime
import json
import os
import uuid
from typing import List, Optional
from pydantic import BaseModel, Field


class AuditEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    user_id: str
    role: str
    campus_applied: str
    intent_category: str
    tables_queried: List[str]
    execution_time_ms: float
    success: bool
    error_code: Optional[str] = None
    fallback_used: bool = False


class AuditService:
    """
    Redacted audit logging service.
    Logs metadata about queries and predictions without recording raw PII,
    student names, roll numbers, or protected prompt text.
    """

    def __init__(self, log_directory: str = "logs"):
        self.log_dir = log_directory
        self.log_file = os.path.join(self.log_dir, "audit.jsonl")
        self._ensure_log_dir()

    def _ensure_log_dir(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir, exist_ok=True)

    def log_event(
        self,
        user_id: str,
        role: str,
        campus_applied: str,
        intent_category: str,
        tables_queried: List[str],
        execution_time_ms: float,
        success: bool = True,
        error_code: Optional[str] = None,
        fallback_used: bool = False
    ) -> AuditEvent:
        event = AuditEvent(
            user_id=user_id,
            role=role,
            campus_applied=campus_applied,
            intent_category=intent_category,
            tables_queried=tables_queried,
            execution_time_ms=execution_time_ms,
            success=success,
            error_code=error_code,
            fallback_used=fallback_used
        )

        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(event.model_dump()) + "\n")
        except Exception as e:
            # Fallback to stdout if logging file write fails
            print(f"[AUDIT LOG ERROR] Failed to write log: {e}. Event: {event.model_dump()}")

        return event


audit_service = AuditService()
