from repetitor.persistence import SQLiteProfileRepository, StudentProfile


def test_profile_survives_reopen(tmp_path):
    db = tmp_path / "repetitor.sqlite3"
    repo = SQLiteProfileRepository(db)
    repo.initialize()
    repo.save(StudentProfile("student", "mathematics", 6, "olympiad"))

    reopened = SQLiteProfileRepository(db)
    assert reopened.get("student") == StudentProfile(
        "student", "mathematics", 6, "olympiad"
    )
