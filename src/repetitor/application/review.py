from __future__ import annotations

from datetime import datetime, timedelta

from repetitor.domain import AttemptEvidence, KnowledgeState, ReviewItem


def schedule_review(
    state: KnowledgeState,
    evidence: AttemptEvidence,
    now: datetime | None = None,
) -> ReviewItem:
    """Schedule the next skill review using an explainable MVP heuristic.

    [ASSUMPTION] Intervals require later calibration.
    """
    base = now or evidence.occurred_at

    if not evidence.correct or evidence.misconception:
        delay = timedelta(days=1)
        reason = "recent_error"
    elif evidence.answer_revealing_hint or (evidence.hint_level or 0) >= 2:
        delay = timedelta(days=2)
        reason = "hint_dependence"
    elif state.retention >= 0.70 and state.independence >= 0.70:
        delay = timedelta(days=14)
        reason = "stable_retrieval"
    elif state.mastery >= 0.70:
        delay = timedelta(days=7)
        reason = "mastery"
    else:
        delay = timedelta(days=3)
        reason = "learning"

    return ReviewItem(
        student_id=state.student_id,
        skill_id=state.skill_id,
        due_at=base + delay,
        reason=reason,
    )
