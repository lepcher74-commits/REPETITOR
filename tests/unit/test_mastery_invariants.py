from datetime import datetime, timezone

from repetitor.application.mastery import apply_evidence
from repetitor.domain import AttemptEvidence, KnowledgeState


NOW = datetime(2026, 10, 1, tzinfo=timezone.utc)


def ev(i, *, correct, purpose="independent", hint=None, revealing=False, transfer=False, prerequisite=False):
    return AttemptEvidence(
        id=f"e{i}", student_id="s", problem_id=f"p{i}", skill_id="skill",
        occurred_at=NOW, correct=correct, purpose=purpose, hint_level=hint,
        answer_revealing_hint=revealing, transfer=transfer,
        prerequisite_failure=prerequisite,
    )


def test_all_mastery_dimensions_remain_bounded_under_long_evidence_sequence():
    state = KnowledgeState("s", "skill")
    for i in range(200):
        state = apply_evidence(
            state,
            ev(
                i,
                correct=i % 3 != 0,
                purpose="review" if i % 5 == 0 else "transfer" if i % 7 == 0 else "independent",
                hint=4 if i % 11 == 0 else None,
                revealing=i % 11 == 0,
                transfer=i % 7 == 0,
            ),
        )
        for value in (state.mastery, state.confidence, state.independence, state.transfer, state.retention):
            assert 0.0 <= value <= 1.0


def test_wrong_review_never_increases_retention():
    initial = KnowledgeState("s", "skill", retention=0.6)
    updated = apply_evidence(initial, ev(1, correct=False, purpose="review"))
    assert updated.retention <= initial.retention


def test_revealing_hint_never_increases_independence():
    initial = KnowledgeState("s", "skill", independence=0.6)
    updated = apply_evidence(initial, ev(1, correct=True, hint=4, revealing=True))
    assert updated.independence <= initial.independence


def test_prerequisite_failure_never_changes_current_mastery():
    initial = KnowledgeState("s", "skill", mastery=0.6)
    updated = apply_evidence(initial, ev(1, correct=False, prerequisite=True))
    assert updated.mastery == initial.mastery
