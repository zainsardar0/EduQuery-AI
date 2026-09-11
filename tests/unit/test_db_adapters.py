import pytest
from services.api.db.sqlserver_adapter import LiveDatabaseUnavailable, SQLServerAdapter


class _FakeCursor:
    def __init__(self, *, writable_object=False):
        self.writable_object = writable_object
        self.query = ""

    def execute(self, query, params=None):
        self.query = query
        return self

    def fetchone(self):
        if "DB_NAME() AS database_name" in self.query:
            return ("EduQuery", "READ_ONLY", 1, 0, 0)
        if "HAS_PERMS_BY_NAME" in self.query:
            return (123, 1, int(self.writable_object), 0, 0, 0, 0)
        raise AssertionError(f"Unexpected preflight query: {self.query}")


class _FakeConnection:
    def __init__(self, *, writable_object=False):
        self.fake_cursor = _FakeCursor(writable_object=writable_object)

    def cursor(self):
        return self.fake_cursor


def test_sqlserver_adapter_encrypt_enforcement():
    # Unencrypted DSN must raise ValueError
    invalid_dsn = "Driver={ODBC Driver 18 for SQL Server};Server=localhost;Database=EduQuery;Encrypt=False;"
    with pytest.raises(ValueError) as excinfo:
        SQLServerAdapter(dsn=invalid_dsn)
    assert "Encrypt=True" in str(excinfo.value)

    # Valid DSN with Encrypt=True passes initialization check
    valid_dsn = "Driver={ODBC Driver 18 for SQL Server};Server=localhost;Database=EduQuery;Encrypt=True;ApplicationIntent=ReadOnly;"
    adapter = SQLServerAdapter(dsn=valid_dsn)
    assert adapter.dsn == valid_dsn


@pytest.mark.parametrize(
    "sql",
    [
        "DROP TABLE dbo.STUDENTS_ROLL_INTERNAL_EXAM",
        "SELECT * FROM sys.tables",
        "SELECT * FROM dbo.STUDENTS_ROLL_INTERNAL_EXAM; SELECT 1",
    ],
)
def test_sqlserver_adapter_rejects_unsafe_sql_before_connecting(sql):
    adapter = SQLServerAdapter(
        dsn="Driver={ODBC Driver 18 for SQL Server};Server=localhost;Database=EduQuery;Encrypt=True;ApplicationIntent=ReadOnly;"
    )
    with pytest.raises(LiveDatabaseUnavailable):
        adapter.execute_query(sql)


def test_database_preflight_accepts_read_only_demo_snapshot_permissions():
    adapter = SQLServerAdapter(
        dsn="Driver={ODBC Driver 18 for SQL Server};Server=localhost;Database=EduQuery;Encrypt=True;ApplicationIntent=ReadOnly;"
    )
    report = adapter._run_preflight(_FakeConnection())
    assert report.ready is True
    assert report.reason_codes == ()


def test_database_preflight_rejects_writable_reporting_object():
    adapter = SQLServerAdapter(
        dsn="Driver={ODBC Driver 18 for SQL Server};Server=localhost;Database=EduQuery;Encrypt=True;ApplicationIntent=ReadOnly;"
    )
    report = adapter._run_preflight(_FakeConnection(writable_object=True))
    assert report.ready is False
    assert "WRITABLE_REPORTING_OBJECT" in report.reason_codes
