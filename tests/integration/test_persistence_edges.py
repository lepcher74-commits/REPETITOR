from datetime import datetime, timezone

import pytest

from repetitor.domain import AttemptEvidence, KnowledgeState
from repetitor.persistence import SQLiteLearningRepository


NOW = datetime(2026, 10, 1, tzinfo=timezone.utc)


def evidence(attempt_id):
    return AttemptEvidence(
        id=attempt_id, student_id="s", problem_id="p", skill_id="skill",
        occurred_at=NOW, correct=True, purpose="independent",
    )


def test_duplicate_attempt_id_is_rejected_without_corrupting_state(tmp_path):
    db = tmp_path / "learning.sqlite3"
    repo = SQLiteLearningRepository(db)
    repo.initialize()
    repo.add_attempt(evidence("same"))
    with pytest.raises(Exception):
        repo.add_attempt(evidence("same"))

    repo.save_state(KnowledgeState("s", "skill", mastery=0.4, evidence_count=1))
    reopened = SQLiteLearningRepository(db)
    reopened.initialize()
    state = reopened.get_state("s", "skill")
    assert state is not None
    assert state.mastery == 0.4
    assert state.evidence_count == 1


def test_state_upsert_survives_repository_reopen(tmp_path):
    db = tmp_path / "learning.sqlite3"
    repo = SQLiteLearningRepository(db)
    repo.initialize()
    repo.save_state(KnowledgeState("s", "skill", mastery=0.2, evidence_count=1))
    repo.save_state(KnowledgeState("s", "skill", mastery=0.7, evidence_count=4))

    reopened = SQLiteLearningRepository(db)
    reopened.initialize()
    state = reopened.get_state("s", "skill")
    assert state is not None
    assert state.mastery == 0.7
    assert state.evidence_count == 4
