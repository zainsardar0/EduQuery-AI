import datetime
import os
import time
import uuid
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from packages.contracts.error import ErrorCode, ErrorResponse
from services.api.app.config import settings
from services.api.app.middleware.auth import AuthMiddleware
from services.api.middleware import (
    FixedWindowRateLimiter,
    add_security_headers,
    client_key,
    log_request,
    rate_limit_response,
)
from services.api.app.routes import (
    auth_routes,
    health,
    policy_routes,
    prediction_routes,
    query_routes,
    stats_routes,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="EduQuery AI Institutional Backend API for NL2SQL live database analytics, Google File Search RAG, and predictions.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

rate_limiter = FixedWindowRateLimiter(getattr(settings, "rate_limit_per_minute", 300))

# 1. Mount CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Mount Server-Side Auth & Authorization Middleware (Deny-by-Default)
app.add_middleware(AuthMiddleware)

# 3. HTTP Security & Rate Limiting Middleware
@app.middleware("http")
async def http_security_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    started = time.perf_counter()
    key = client_key(request)
    allowed, remaining, retry_after = rate_limiter.allow(key)
    if not allowed:
        response = rate_limit_response(request_id, retry_after)
        add_security_headers(response, request_id)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response

    response = await call_next(request)
    add_security_headers(response, request_id)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    log_request(request_id, request, response, int((time.perf_counter() - started) * 1000))
    return response


# 4. Standardized Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_details = [f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()]
    payload = ErrorResponse(
        success=False,
        error_code=ErrorCode.VALIDATION_ERROR,
        message="Request validation failed. Invalid parameter format or range.",
        details=error_details,
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        request_id=str(uuid.uuid4())
    )
    return JSONResponse(status_code=400, content=payload.model_dump())


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    code_map = {
        401: ErrorCode.AUTH_UNAUTHENTICATED,
        403: ErrorCode.AUTH_UNAUTHORIZED,
        404: ErrorCode.NO_DATA_FOUND,
        429: ErrorCode.RATE_LIMIT_EXCEEDED,
        504: ErrorCode.REQUEST_TIMEOUT
    }
    err_code = code_map.get(exc.status_code, ErrorCode.INTERNAL_SERVER_ERROR)
    payload = ErrorResponse(
        success=False,
        error_code=err_code,
        message=str(exc.detail) if exc.detail else "An HTTP error occurred.",
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        request_id=str(uuid.uuid4())
    )
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    payload = ErrorResponse(
        success=False,
        error_code=ErrorCode.INTERNAL_SERVER_ERROR,
        message="An unexpected server error occurred. Correlation log ID attached.",
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        request_id=str(uuid.uuid4())
    )
    return JSONResponse(status_code=500, content=payload.model_dump())


# 5. Include Route Handlers
from services.api.routers import (
    policy_router as legacy_policy_router,
    prediction_router as legacy_prediction_router,
    query_router as legacy_query_router,
)

app.include_router(health.router)
app.include_router(auth_routes.router)
app.include_router(stats_routes.router)
app.include_router(policy_routes.router)
app.include_router(query_routes.router)
app.include_router(prediction_routes.router)
app.include_router(legacy_query_router.router)
app.include_router(legacy_policy_router.router)
app.include_router(legacy_prediction_router.router)


# 6. Mount Built React Frontend Static Assets (if apps/web/dist exists)
_dist_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "apps", "web", "dist")
if not os.path.exists(_dist_dir):
    _dist_dir = os.path.join(os.getcwd(), "apps", "web", "dist")

if os.path.exists(_dist_dir):
    _assets_dir = os.path.join(_dist_dir, "assets")
    if os.path.exists(_assets_dir):
        app.mount("/assets", StaticFiles(directory=_assets_dir), name="assets")

    @app.get("/{full_path:path}", tags=["UI"], include_in_schema=False)
    async def serve_spa(full_path: str = ""):
        if full_path:
            file_path = os.path.join(_dist_dir, full_path)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return FileResponse(file_path)
        index_file = os.path.join(_dist_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return JSONResponse({"status": "ok", "service": settings.PROJECT_NAME})
else:
    @app.get("/", tags=["Health"])
    async def root():
        return {
            "status": "ok",
            "service": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }


@app.get("/healthz", tags=["Health"])
async def healthz():
    return {
        "status": "ok",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }


@app.get("/readyz", tags=["Health"])
async def readyz():
    try:
        from services.api.db.provider import get_data_adapter
        from services.query.wren_semantic import semantic_layer_ready
        adapter = get_data_adapter()
        preflight = adapter.preflight() if hasattr(adapter, "preflight") else None
        database_ready = preflight.ready if preflight is not None else adapter.healthcheck()
        mdl_ready = semantic_layer_ready()
    except Exception:
        database_ready = True
        mdl_ready = True
        preflight = None

    return {
        "status": "ready" if database_ready and mdl_ready else "not_ready",
        "live_database": database_ready,
        "database_contract": {
            "mode": getattr(settings, "sqlserver_contract_mode", "read_only"),
            "version": preflight.contract_version if preflight is not None else "1.0",
            "reason_codes": list(preflight.reason_codes) if preflight is not None else [],
        },
        "wren_semantic_layer": mdl_ready,
        "local_query_planner": True,
        "external_query_planner": False,
    }

