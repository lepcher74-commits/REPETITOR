from repetitor.diagnostics import record_startup_failure


def test_startup_diagnostic_records_type_not_exception_message(tmp_path):
    secret = "student-answer-123"
    path = record_startup_failure(tmp_path, RuntimeError(secret))

    text = path.read_text(encoding="utf-8")
    assert "startup_failure RuntimeError" in text
    assert secret not in text


def test_startup_diagnostic_is_local_to_data_directory(tmp_path):
    path = record_startup_failure(tmp_path, ValueError("ignored"))
    assert path.parent == tmp_path
    assert path.name == "startup-errors.log"
