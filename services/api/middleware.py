"""Small, dependency-free HTTP controls for the local institutional service."""

import json
import logging
import math
import threading
import time
import uuid
from collections import defaultdict, deque
from collections.abc import Callable

from fastapi import Request
from fastapi.responses import JSONResponse, Response


logger = logging.getLogger("eduquery.http")
logger.setLevel(logging.INFO)


class FixedWindowRateLimiter:
    """Bound a single process; ingress must enforce the distributed production limit."""

    def __init__(
        self,
        max_requests: int,
        window_seconds: int = 60,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if max_requests < 1 or window_seconds < 1:
            raise ValueError("Rate-limit values must be positive.")
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.clock = clock
        self._requests: dict[str, deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()
        self._last_cleanup = self.clock()

    def allow(self, key: str) -> tuple[bool, int, int]:
        now = self.clock()
        cutoff = now - self.window_seconds
        with self._lock:
            if now - self._last_cleanup >= self.window_seconds:
                stale_keys = [
                    existing_key
                    for existing_key, timestamps in self._requests.items()
                    if not timestamps or timestamps[-1] <= cutoff
                ]
                for existing_key in stale_keys:
                    del self._requests[existing_key]
                self._last_cleanup = now
            bucket = self._requests[key]
            while bucket and bucket[0] <= cutoff:
                bucket.popleft()
            if len(bucket) >= self.max_requests:
                retry_after = max(1, math.ceil(self.window_seconds - (now - bucket[0])))
                return False, 0, retry_after
            bucket.append(now)
            return True, self.max_requests - len(bucket), 0


def add_security_headers(response: Response, request_id: str) -> None:
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Cache-Control"] = "no-store"
    # The static demo UI contains controlled inline CSS/JS. This CSP permits
    # those two local assets while blocking external scripts, fonts and egress.
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self' data:; "
        "font-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
    )


def client_key(request: Request) -> str:
    """Use the socket peer, never a spoofable forwarded header, at this layer."""
    return request.client.host if request.client else "unknown"


def log_request(request_id: str, request: Request, response: Response, elapsed_ms: int) -> None:
    logger.info(
        json.dumps(
            {
                "event": "http_request",
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "execution_time_ms": elapsed_ms,
            },
            separators=(",", ":"),
        )
    )


def rate_limit_response(request_id: str, retry_after: int) -> JSONResponse:
    response = JSONResponse(
        status_code=429,
        content={"detail": "Request rate limit exceeded.", "request_id": request_id},
    )
    response.headers["Retry-After"] = str(retry_after)
    return response
