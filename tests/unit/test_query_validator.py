from services.api.query.validator import validate_and_sanitize_sql


def test_select_is_allowed():
    res = validate_and_sanitize_sql("SELECT * FROM v_student_attendance WHERE campus_id = 'DAANISH-01'")
    assert res.is_valid is True
    assert res.reason_code is None
    assert "LIMIT 1000" in res.sanitized_sql.upper()


def test_insert_is_rejected():
    res = validate_and_sanitize_sql("INSERT INTO v_student_attendance VALUES ('1', '2', '3', '4', '5', '6')")
    assert res.is_valid is False
    assert res.reason_code == "NON_SELECT_SQL"


def test_drop_is_rejected():
    res = validate_and_sanitize_sql("DROP TABLE v_student_attendance")
    assert res.is_valid is False
    assert res.reason_code == "NON_SELECT_SQL"


def test_exec_is_rejected():
    res = validate_and_sanitize_sql("EXEC xp_cmdshell('dir')")
    assert res.is_valid is False
    assert res.reason_code in ("NON_SELECT_SQL", "SQL_PARSE_ERROR")


def test_unknown_table_is_rejected():
    res = validate_and_sanitize_sql("SELECT * FROM sys.tables")
    assert res.is_valid is False
    assert res.reason_code == "UNAPPROVED_OBJECT"
    assert "sys.tables" in res.safe_message


def test_sql_injection_multiple_statements_rejected():
    res = validate_and_sanitize_sql("SELECT * FROM v_student_attendance; DROP TABLE v_student_attendance")
    assert res.is_valid is False
    assert res.reason_code in ("MULTIPLE_STATEMENTS_DISALLOWED", "SQL_PARSE_ERROR")


def test_row_limit_is_injected():
    res = validate_and_sanitize_sql("SELECT student_id, status FROM v_student_attendance")
    assert res.is_valid is True
    assert "LIMIT 1000" in res.sanitized_sql.upper()


def test_excessive_limit_is_capped():
    res = validate_and_sanitize_sql("SELECT student_id FROM v_student_attendance LIMIT 5000")
    assert res.is_valid is True
    assert "LIMIT 1000" in res.sanitized_sql.upper()
