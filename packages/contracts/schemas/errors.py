from typing import Literal
from pydantic import BaseModel, Field


class APIError(BaseModel):
    status: Literal["error"] = Field("error", description="Error status marker")
    error_code: str = Field(..., description="Machine-stable error code e.g. UNAUTHORIZED, VALIDATION_FAILED")
    safe_message: str = Field(..., description="User-safe error message without sensitive stack traces")
    request_id: str = Field(..., description="Unique request tracing UUID")
