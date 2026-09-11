from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from packages.contracts.schemas.auth import AuthContext, DemoLoginRequest, TokenResponse
from services.api.auth.dependencies import require_auth
from services.api.auth.provider import issue_demo_token
from services.api.config import get_settings

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/demo-login", response_model=TokenResponse)
async def demo_login(body: DemoLoginRequest = DemoLoginRequest()):
    """Issue a signed demo token with the same all-campus scope for every user."""
    if not get_settings().enable_demo_auth:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    token = issue_demo_token(user_id=body.user_id or "demo_user")
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        auth_context=AuthContext(
            user_id=body.user_id or "demo_user",
            access_scope="all_campuses",
            demo_mode=True,
        ),
    )


@router.get("/me", response_model=AuthContext)
async def get_current_user(auth: AuthContext = Depends(require_auth)):
    """Return the verified identity and uniform access scope."""
    return auth
