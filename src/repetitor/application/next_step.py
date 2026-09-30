from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from repetitor.domain import KnowledgeState, ReviewItem


@dataclass(frozen=True, slots=True)
class NextActivity:
    kind: str
    skill_id: str
    reason: str


def select_next_activity(
    *,
    current_skill_id: str,
    states: dict[str, KnowledgeState],
    prerequisites: dict[str, tuple[str, ...]],
    due_reviews: Iterable[ReviewItem],
    now: datetime,
) -> NextActivity:
    """Apply the approved priority order using explicit deterministic rules."""
    for prerequisite_id in prerequisites.get(current_skill_id, ()):
        state = states.get(prerequisite_id)
        if state is None or state.mastery < 0.45:
            return NextActivity("prerequisite", prerequisite_id, "critical_prerequisite_gap")

    due = sorted(
        (item for item in due_reviews if item.due_at <= now),
        key=lambda item: item.due_at,
    )
    if due:
        return NextActivity("review", due[0].skill_id, "review_due")

    current = states.get(current_skill_id)
    if current is None or current.mastery < 0.70:
        return NextActivity("learn", current_skill_id, "unfinished_current_skill")

    if current.transfer < 0.60:
        return NextActivity("transfer", current_skill_id, "transfer_not_demonstrated")

    return NextActivity("enrichment", current_skill_id, "ready_for_non_routine_work")
