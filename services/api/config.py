from functools import lru_cache
from pathlib import Path
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Core
    app_env: str = "demo"
    demo_mode: bool = False
    enable_demo_auth: bool = True

    # Auth
    jwt_secret: str = "demo-secret-key-change-in-production-32bytes-min"
    jwt_algorithm: str = "HS256"
    jwt_issuer: str = "eduquery-demo"
    jwt_audience: str = "eduquery-api"

    # SQL Server / backend
    data_backend: str = "sqlserver"
    sqlserver_dsn: str = "Driver={ODBC Driver 17 for SQL Server};Server=localhost;Database=EduQuery_Wren_20260713;Trusted_Connection=yes;Encrypt=yes;TrustServerCertificate=yes;ApplicationIntent=ReadOnly;"
    sqlserver_query_timeout_seconds: int = 12
    sqlserver_max_rows: int = 100
    sqlserver_contract_mode: str = "legacy_snapshot"
    sqlserver_expected_database: str = ""
    sqlserver_expected_contract_version: str = ""
    sqlserver_preflight_cache_seconds: int = 30
    allow_privileged_demo_db_user: bool = False

    # Remote model controls
    external_model_enabled: bool = False
    openrouter_api_key: str = ""

    # Local free/LanceDB RAG settings
    policy_rag_root: str = "data/policy_rag_markdown_r4"
    # Calibrated against the Markdown corpus: supported boarder-leave prompt 0.0353;
    # unsupported transport prompt -0.3508. Revalidate when the corpus changes.
    policy_rag_min_rerank_score: float = 0.0

    # OpenAI embeddings / LanceDB
    openai_api_key: str = ""
    embedding_model: str = "text-embedding-3-large"
    embedding_batch_size: int = 64
    lancedb_path: str = "./data/lancedb"

    # Local generator (ollama) settings
    ollama_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "llama2"
    generator_max_tokens: int = 512
    generator_temperature: float = 0.0

    # Admin / operational
    audit_log_path: str = "services/api/logs/audit.jsonl"
    allowed_origins: str = "http://localhost:3000,http://localhost:3001,http://localhost:8000,http://127.0.0.1:8000,http://127.0.0.1:3000"
    admin_api_key: str = "change_me_admin_key"
    rate_limit_requests_per_minute: int = 1000

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env", env_file_encoding="utf-8", extra="ignore"
    )

    @model_validator(mode="after")
    def reject_unsafe_production_defaults(self):
        if self.jwt_algorithm != "HS256":
            raise ValueError("JWT_ALGORITHM must be HS256 for the configured shared-secret verifier.")
        if not self.jwt_audience.strip():
            raise ValueError("JWT_AUDIENCE cannot be empty.")
        if self.rate_limit_requests_per_minute < 1:
            raise ValueError("RATE_LIMIT_REQUESTS_PER_MINUTE must be positive.")
        if self.sqlserver_contract_mode not in {"legacy_snapshot", "live_v1"}:
            raise ValueError("SQLSERVER_CONTRACT_MODE must be legacy_snapshot or live_v1.")
        if self.sqlserver_preflight_cache_seconds < 1:
            raise ValueError("SQLSERVER_PREFLIGHT_CACHE_SECONDS must be positive.")
        if self.app_env.lower() == "production":
            if self.enable_demo_auth:
                raise ValueError("ENABLE_DEMO_AUTH must be false in production.")
            if self.jwt_secret == "demo-secret-key-change-in-production-32bytes-min":
                raise ValueError("JWT_SECRET must be replaced in production.")
            if len(self.jwt_secret) < 32:
                raise ValueError("JWT_SECRET must contain at least 32 characters in production.")
            if not self.jwt_issuer.strip() or self.jwt_issuer == "eduquery-demo":
                raise ValueError("JWT_ISSUER must identify the production issuer.")
            if self.allow_privileged_demo_db_user:
                raise ValueError("ALLOW_PRIVILEGED_DEMO_DB_USER cannot be enabled in production.")
            origins = [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]
            if not origins or any(not origin.startswith("https://") for origin in origins):
                raise ValueError("Production ALLOWED_ORIGINS must contain only explicit HTTPS origins.")
            dsn = self.sqlserver_dsn.lower().replace(" ", "")
            if "encrypt=yes" not in dsn and "encrypt=true" not in dsn:
                raise ValueError("Production SQLSERVER_DSN must require encryption.")
            if "trustservercertificate=yes" in dsn or "trustservercertificate=true" in dsn:
                raise ValueError("Production SQLSERVER_DSN must validate the SQL Server certificate.")
            if "applicationintent=readonly" not in dsn:
                raise ValueError("Production SQLSERVER_DSN must declare ApplicationIntent=ReadOnly.")
            if "server=localhost" in dsn or "server=127.0.0.1" in dsn:
                raise ValueError("Production SQLSERVER_DSN must identify the institutional SQL endpoint.")
            if self.sqlserver_contract_mode != "live_v1":
                raise ValueError("Production requires SQLSERVER_CONTRACT_MODE=live_v1.")
            if not self.sqlserver_expected_database.strip():
                raise ValueError("SQLSERVER_EXPECTED_DATABASE is required in production.")
            if not self.sqlserver_expected_contract_version.strip():
                raise ValueError("SQLSERVER_EXPECTED_CONTRACT_VERSION is required in production.")
        if not -20 <= self.policy_rag_min_rerank_score <= 20:
            raise ValueError("POLICY_RAG_MIN_RERANK_SCORE is outside the supported range.")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
