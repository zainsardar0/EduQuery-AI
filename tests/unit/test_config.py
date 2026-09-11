import pytest
from pydantic import ValidationError

from services.api.config import Settings
from services.query.database_contract import CONTRACT_VERSION


def _production_settings(**overrides):
    values = {
        "app_env": "production",
        "enable_demo_auth": False,
        "jwt_secret": "x" * 64,
        "jwt_issuer": "institution-identity",
        "jwt_audience": "eduquery-api",
        "allowed_origins": "https://eduquery.example.edu",
        "allow_privileged_demo_db_user": False,
        "sqlserver_dsn": (
            "Driver={ODBC Driver 18 for SQL Server};Server=sql.daanish.edu.pk;"
            "Database=EduQueryLive;Encrypt=yes;TrustServerCertificate=no;ApplicationIntent=ReadOnly;"
        ),
        "sqlserver_contract_mode": "live_v1",
        "sqlserver_expected_database": "EduQueryLive",
        "sqlserver_expected_contract_version": CONTRACT_VERSION,
    }
    values.update(overrides)
    return Settings(_env_file=None, **values)


def test_production_configuration_accepts_explicit_secure_identity_and_origin():
    settings = _production_settings()
    assert settings.app_env == "production"


@pytest.mark.parametrize(
    "overrides",
    [
        {"jwt_secret": "too-short"},
        {"jwt_issuer": "eduquery-demo"},
        {"allowed_origins": "http://eduquery.example.edu"},
        {"enable_demo_auth": True},
        {"sqlserver_contract_mode": "legacy_snapshot"},
        {"sqlserver_expected_database": ""},
        {"sqlserver_expected_contract_version": ""},
        {"sqlserver_dsn": "Driver={ODBC Driver 18 for SQL Server};Server=localhost;Database=EduQueryLive;Encrypt=yes;TrustServerCertificate=no;ApplicationIntent=ReadOnly;"},
        {"sqlserver_dsn": "Driver={ODBC Driver 18 for SQL Server};Server=sql.daanish.edu.pk;Database=EduQueryLive;Encrypt=yes;TrustServerCertificate=yes;ApplicationIntent=ReadOnly;"},
    ],
)
def test_production_configuration_rejects_unsafe_defaults(overrides):
    with pytest.raises(ValidationError):
        _production_settings(**overrides)
