from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class ErrorCode(str, Enum):
    AUTH_UNAUTHENTICATED = "AUTH_UNAUTHENTICATED"
    AUTH_UNAUTHORIZED = "AUTH_UNAUTHORIZED"
    CROSS_CAMPUS_ACCESS_DENIED = "CROSS_CAMPUS_ACCESS_DENIED"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    UNSAFE_QUERY_REJECTED = "UNSAFE_QUERY_REJECTED"
    NO_DATA_FOUND = "NO_DATA_FOUND"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    REQUEST_TIMEOUT = "REQUEST_TIMEOUT"
    DEPENDENCY_FAILURE = "DEPENDENCY_FAILURE"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"


class ErrorResponse(BaseModel):
    """
    Standardized public error payload for all service endpoints.
    Omits raw SQL text, stack traces, database credentials, or provider details.
    """
    success: bool = Field(
        default=False,
        description="Always false for error responses"
    )
    error_code: ErrorCode = Field(
        ...,
        description="Stable error classification code",
        examples=[ErrorCode.UNSAFE_QUERY_REJECTED]
    )
    message: str = Field(
        ...,
        description="Safe, user-facing summary message describing the error",
        examples=["The submitted prompt requested non-read-only data operations which are prohibited."]
    )
    details: Optional[List[str]] = Field(
        default=None,
        description="Optional list of non-sensitive validation or contextual error items",
        examples=[["Field 'prompt' must not be empty"]]
    )
    timestamp: str = Field(
        ...,
        description="ISO-8601 UTC timestamp when the error occurred",
        examples=["2026-08-03T12:05:10Z"]
    )
    request_id: str = Field(
        ...,
        description="Unique correlation identifier for server log tracing",
        examples=["9f8e7d6c-5b4a-3f2e-1d0c-9b8a7f6e5d4c"]
    )
