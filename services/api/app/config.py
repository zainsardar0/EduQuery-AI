import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "EduQuery AI Backend API"
    VERSION: str = "1.0.0-mvp"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = os.getenv("EDUQUERY_ENV", "production")

    # Allowed CORS Origins
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://eduquery-ai.vercel.app",
        "*"
    ]

    # Auth & JWT Configuration
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "daanish_eduquery_jwt_secret_key_2026_secure")
    JWT_ALGORITHM: str = "HS256"

    # Live Production SQL Server (Daanish Schools Database)
    DB_HOST: str = os.getenv("DB_HOST", "")
    DB_PORT: str = os.getenv("DB_PORT", "1433")
    DB_NAME: str = os.getenv("DB_NAME", "")
    DB_USER: str = os.getenv("DB_USER", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_DRIVER: str = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")

    # Google Gemini API Key for Google File Search API / Gemini RAG
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

    # OpenRouter API Key for Wren / external assistance
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")

    # Force fallback toggle (default true for safe demo mode)
    FORCE_DEMO_FALLBACK: bool = os.getenv("FORCE_DEMO_FALLBACK", "true").lower() == "true"

    @property
    def database_url(self) -> str:
        """Constructs the ODBC connection string for SQL Server."""
        if os.getenv("DATABASE_URL"):
            return os.getenv("DATABASE_URL")
        return (
            f"Driver={{{self.DB_DRIVER}}};"
            f"Server={self.DB_HOST},{self.DB_PORT};"
            f"Database={self.DB_NAME};"
            f"Uid={self.DB_USER};"
            f"Pwd={self.DB_PASSWORD};"
            "Encrypt=yes;TrustServerCertificate=yes;"
        )


settings = Settings()
