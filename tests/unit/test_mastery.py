from datetime import datetime, timezone

from repetitor.application.mastery import apply_evidence
from repetitor.domain import AttemptEvidence, KnowledgeState


NOW = datetime(2026, 9, 30, 12, 0, tzinfo=timezone.utc)


def evidence(**changes):
    values = dict(
        id="a1", student_id="s1", problem_id="p1", skill_id="skill",
        occurred_at=NOW, correct=True, purpose="independent",
    )
    values.update(changes)
    return AttemptEvidence(**values)


def test_independent_correct_updates_mastery_and_independence():
    state = apply_evidence(KnowledgeState("s1", "skill"), evidence())
    assert state.mastery > 0
    assert state.independence > 0
    assert state.evidence_count == 1


def test_answer_revealing_hint_does_not_create_independent_evidence():
    state = apply_evidence(
        KnowledgeState("s1", "skill", independence=0.5),
        evidence(hint_level=4, answer_revealing_hint=True),
    )
    assert state.independence < 0.5


def test_transfer_is_separate_dimension():
    state = apply_evidence(
        KnowledgeState("s1", "skill"),
        evidence(purpose="transfer", transfer=True),
    )
    assert state.transfer > 0
    assert state.mastery > 0


def test_prerequisite_failure_does_not_penalize_current_mastery():
    initial = KnowledgeState("s1", "skill", mastery=0.4)
    state = apply_evidence(initial, evidence(correct=False, prerequisite_failure=True))
    assert state.mastery == initial.mastery
