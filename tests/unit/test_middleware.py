from services.api.middleware import FixedWindowRateLimiter
from fastapi.testclient import TestClient


def test_rate_limiter_rejects_until_window_expires():
    now = [100.0]
    limiter = FixedWindowRateLimiter(2, window_seconds=60, clock=lambda: now[0])

    assert limiter.allow("client") == (True, 1, 0)
    assert limiter.allow("client") == (True, 0, 0)
    allowed, remaining, retry_after = limiter.allow("client")
    assert allowed is False
    assert remaining == 0
    assert retry_after == 60

    now[0] = 161.0
    assert limiter.allow("client") == (True, 1, 0)


def test_application_rate_limit_response_has_retry_and_security_headers(monkeypatch):
    import services.api.main as api_main

    monkeypatch.setattr(api_main, "rate_limiter", FixedWindowRateLimiter(1))
    client = TestClient(api_main.app)
    assert client.get("/").status_code == 200
    response = client.get("/")
    assert response.status_code == 429
    assert response.headers["retry-after"]
    assert response.headers["x-ratelimit-remaining"] == "0"
    assert response.headers["x-content-type-options"] == "nosniff"
