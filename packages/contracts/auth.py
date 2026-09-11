from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class UserRole(str, Enum):
    ADMIN = "admin"
    PRINCIPAL = "principal"
    TEACHER = "teacher"
    COUNSELOR = "counselor"
    AUDITOR = "auditor"


class AuthContext(BaseModel):
    """
    Server-derived authentication and authorization context.
    Computed exclusively on the institutional backend from verified JWT/session claims.
    Never trusted from client-supplied payload parameters.
    """
    model_config = ConfigDict(frozen=True)

    user_id: str = Field(
        ...,
        description="Unique identifier of the authenticated user",
        examples=["a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d"]
    )
    role: UserRole = Field(
        ...,
        description="Server-assigned institutional role governing feature and data access level",
        examples=[UserRole.TEACHER]
    )
    campus_scope: List[str] = Field(
        ...,
        description="List of 4-letter campus codes (SCHOOL) the user is authorized to access",
        examples=[["MNWB", "MNWG"]]
    )
    teacher_eid: Optional[int] = Field(
        default=None,
        description="Optional Employee ID (EID) if user is a teacher",
        examples=[1042]
    )
    authenticated_at: str = Field(
        ...,
        description="ISO-8601 UTC timestamp of authentication verification",
        examples=["2026-08-03T12:00:00Z"]
    )
    session_expires_at: str = Field(
        ...,
        description="ISO-8601 UTC timestamp of token/session expiration",
        examples=["2026-08-03T20:00:00Z"]
    )
