from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import JWTError, jwt

from packages.contracts.schemas.auth import AuthContext
from services.api.config import get_settings


def issue_demo_token(
    user_id: str = "demo_user",
    expires_in_hours: int = 24,
    **_ignored_legacy_scope: object,
) -> str:
    """Issue one uniform all-campus identity.

    Legacy campus/role keyword arguments are ignored so an old client cannot
    recreate role restrictions or elevated privileges.
    """
    settings = get_settings()
    if not settings.enable_demo_auth:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "access_scope": "all_campuses",
        "demo_mode": True,
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=expires_in_hours)).timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def verify_token(token: str) -> AuthContext:
    settings = get_settings()
    try:
        if settings.app_env.lower() == "production" and settings.jwt_secret == "demo-secret-key-change-in-production-32bytes-min":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Production authentication is not configured",
                headers={"WWW-Authenticate": "Bearer"},
            )
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience,
            options={"require_sub": True, "require_iat": True, "require_exp": True},
        )
        user_id = payload.get("sub")
        demo_mode = bool(payload.get("demo_mode", False))
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token claims",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if demo_mode and not settings.enable_demo_auth:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Demo credentials are disabled",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return AuthContext(user_id=user_id, access_scope="all_campuses", demo_mode=demo_mode)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
