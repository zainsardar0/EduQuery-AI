from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from jose import jwt

from packages.contracts.schemas.auth import AuthContext
from services.api.auth.dependencies import require_auth
from services.api.auth.provider import issue_demo_token
from services.api.config import get_settings

auth_test_app = FastAPI()


@auth_test_app.get("/protected")
async def protected_route(auth: AuthContext = Depends(require_auth)):
    return auth.model_dump()


client = TestClient(auth_test_app)


def test_no_token_returns_401():
    response = client.get("/protected")
    assert response.status_code == 401


def test_invalid_token_returns_401():
    response = client.get("/protected", headers={"Authorization": "Bearer invalid.token.here"})
    assert response.status_code == 401


def test_token_without_issuer_and_audience_is_rejected():
    settings = get_settings()
    now = datetime.now(timezone.utc)
    token = jwt.encode(
        {
            "sub": "wrong_context",
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=5)).timestamp()),
        },
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_every_demo_token_has_one_all_campus_scope():
    token = issue_demo_token(
        user_id="demo_user", campus_id="ATKB", role="teacher"
    )
    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {
        "user_id": "demo_user",
        "access_scope": "all_campuses",
        "demo_mode": True,
    }


def test_legacy_role_and_campus_arguments_cannot_change_access():
    first = issue_demo_token(user_id="first", campus_id="ATKB", role="teacher")
    second = issue_demo_token(user_id="second", campus_id="MNWB", role="admin")
    first_data = client.get("/protected", headers={"Authorization": f"Bearer {first}"}).json()
    second_data = client.get("/protected", headers={"Authorization": f"Bearer {second}"}).json()
    assert first_data["access_scope"] == second_data["access_scope"] == "all_campuses"
    assert "role" not in first_data and "campus_id" not in first_data


def test_auth_router_demo_login_and_me():
    from services.api.main import app

    main_client = TestClient(app)
    response = main_client.post("/api/v1/auth/demo-login", json={"user_id": "ui_user"})
    assert response.status_code == 200
    data = response.json()
    assert data["auth_context"]["access_scope"] == "all_campuses"
    me = main_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {data['access_token']}"},
    )
    assert me.status_code == 200
    assert me.json()["user_id"] == "ui_user"
