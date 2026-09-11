from typing import Literal, Optional

from pydantic import BaseModel, Field


class AuthContext(BaseModel):
    """Authenticated identity with one uniform database access scope."""

    user_id: str = Field(..., description="Unique authenticated identity")
    access_scope: Literal["all_campuses"] = Field(
        "all_campuses", description="Uniform EduQuery analytics scope"
    )
    demo_mode: bool = Field(False, description="Flag indicating demo-mode authentication")


class DemoLoginRequest(BaseModel):
    user_id: Optional[str] = Field("demo_user", description="Username or ID")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT bearer token")
    token_type: str = Field("bearer", description="Token type")
    auth_context: AuthContext = Field(..., description="Authenticated uniform access context")
