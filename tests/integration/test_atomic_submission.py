from datetime import datetime, timedelta, timezone

import pytest

from repetitor.domain import AttemptEvidence, KnowledgeState, ReviewItem
from repetitor.persistence import SQLiteLearningRepository


NOW = datetime(2026, 10, 1, tzinfo=timezone.utc)


def attempt(attempt_id):
    return AttemptEvidence(
        id=attempt_id, student_id="s", problem_id="p", skill_id="skill",
        occurred_at=NOW, correct=True, purpose="independent",
    )


def test_submission_rolls_back_state_and_review_when_attempt_insert_fails(tmp_path):
    repo = SQLiteLearningRepository(tmp_path / "learning.sqlite3")
    repo.initialize()
    original_state = KnowledgeState("s", "skill", mastery=0.2, evidence_count=1)
    original_review = ReviewItem("s", "skill", NOW + timedelta(days=2), "original")
    repo.save_submission(attempt("same"), original_state, original_review)

    changed_state = KnowledgeState("s", "skill", mastery=0.9, evidence_count=99)
    changed_review = ReviewItem("s", "skill", NOW + timedelta(days=30), "changed")
    with pytest.raises(Exception):
        repo.save_submission(attempt("same"), changed_state, changed_review)

    state = repo.get_state("s", "skill")
    assert state is not None
    assert state.mastery == 0.2
    assert state.evidence_count == 1
    due = repo.due_reviews("s", NOW + timedelta(days=3))
    assert len(due) == 1
    assert due[0].reason == "original"
