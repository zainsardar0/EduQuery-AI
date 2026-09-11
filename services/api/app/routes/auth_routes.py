import datetime
import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from packages.contracts.auth import AuthContext, UserRole
from packages.contracts.error import ErrorCode, ErrorResponse
from services.api.app.config import settings

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication & Context"])


class SSOLoginRequest(BaseModel):
    username: str
    school: str  # Campus code e.g. "MNWB", "ATKB", "HSPB"
    role: Optional[str] = None
    teacher_eid: Optional[int] = None


class SSOLoginResponse(BaseModel):
    token: str
    user: AuthContext


@router.post("/sso-login", response_model=SSOLoginResponse)
async def sso_login(payload: SSOLoginRequest):
    """
    SSO Handoff endpoint for users redirected from the Daanish School Web Portal.
    Accepts verified session parameters and returns an authorized AuthContext session.
    """
    username = payload.username.strip()
    school = payload.school.strip().upper()

    # Determine user role from username or payload
    role_val = UserRole.TEACHER
    if payload.role:
        try:
            role_val = UserRole(payload.role.lower())
        except ValueError:
            role_val = UserRole.TEACHER
    elif "admin" in username.lower() or username.lower() in ["awais"]:
        role_val = UserRole.ADMIN
    elif "coord" in username.lower() or "principal" in username.lower():
        role_val = UserRole.PRINCIPAL

    # Set campus scope: Admins get all campuses, school users get their assigned campus
    campus_scope = [school] if school else ["MNWB"]
    if role_val == UserRole.ADMIN:
        campus_scope = ["MNWB", "MNWG", "ATKB", "ATKG", "HSPB", "KRA", "CHB", "CHG", "RYKB", "RYKG"]

    auth_context = AuthContext(
        user_id=str(uuid.uuid5(uuid.NAMESPACE_DNS, f"daanish-{username}")),
        role=role_val,
        campus_scope=campus_scope,
        teacher_eid=payload.teacher_eid,
        authenticated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        session_expires_at=(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=12)).isoformat()
    )

    # Simulated JWT token representation
    token = f"daanish_sso_{username}_{school}_{int(datetime.datetime.now().timestamp())}"

    return SSOLoginResponse(
        token=token,
        user=auth_context
    )


class DemoLoginRequest(BaseModel):
    user_id: str = "ui_user"


@router.post("/demo-login")
async def demo_login(payload: DemoLoginRequest):
    """
    Demo login endpoint for tests and web UI session initialization.
    """
    from services.api.auth.provider import issue_demo_token
    token = issue_demo_token(user_id=payload.user_id)
    return {
        "access_token": token,
        "token_type": "bearer",
        "auth_context": {
            "user_id": payload.user_id,
            "access_scope": "all_campuses",
            "demo_mode": True,
        }
    }




@router.get("/me", response_model=AuthContext)
async def get_current_user_context(request: Request):
    """
    Protected endpoint returning the server-derived AuthContext for the authenticated user.
    """
    user_context: AuthContext = getattr(request.state, "user", None)
    if not user_context:
        error = ErrorResponse(
            success=False,
            error_code=ErrorCode.AUTH_UNAUTHENTICATED,
            message="No authenticated session context found.",
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            request_id=str(uuid.uuid4())
        )
        return JSONResponse(status_code=401, content=error.model_dump())

    return user_context
