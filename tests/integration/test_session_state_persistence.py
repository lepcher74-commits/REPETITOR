from datetime import datetime, timezone

from repetitor.persistence import SQLiteLearningRepository


def test_session_state_survives_repository_reopen(tmp_path):
    db = tmp_path / "learning.sqlite3"
    first = SQLiteLearningRepository(db)
    first.initialize()
    now = datetime.now(timezone.utc)
    first.save_session_state(
        "student",
        "module",
        "problem-2",
        "remediation",
        "skill-prerequisite",
        now,
    )

    reopened = SQLiteLearningRepository(db)
    reopened.initialize()
    state = reopened.get_session_state("student")

    assert state is not None
    assert state["module_id"] == "module"
    assert state["problem_id"] == "problem-2"
    assert state["phase"] == "remediation"
    assert state["remediation_skill_id"] == "skill-prerequisite"
