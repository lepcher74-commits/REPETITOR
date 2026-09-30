from datetime import datetime, timedelta, timezone

from repetitor.application.next_step import select_next_activity
from repetitor.domain import KnowledgeState, ReviewItem


NOW = datetime(2026, 9, 30, 12, 0, tzinfo=timezone.utc)


def test_prerequisite_gap_has_priority_over_due_review():
    states = {
        "prereq": KnowledgeState("s", "prereq", mastery=0.2),
        "current": KnowledgeState("s", "current", mastery=0.3),
    }
    reviews = [ReviewItem("s", "other", NOW - timedelta(days=1), "due")]
    result = select_next_activity(
        current_skill_id="current",
        states=states,
        prerequisites={"current": ("prereq",)},
        due_reviews=reviews,
        now=NOW,
    )
    assert result.kind == "prerequisite"
    assert result.skill_id == "prereq"


def test_due_review_precedes_current_skill_when_prereqs_ready():
    states = {
        "prereq": KnowledgeState("s", "prereq", mastery=0.8),
        "current": KnowledgeState("s", "current", mastery=0.3),
    }
    reviews = [ReviewItem("s", "old", NOW - timedelta(hours=1), "due")]
    result = select_next_activity(
        current_skill_id="current",
        states=states,
        prerequisites={"current": ("prereq",)},
        due_reviews=reviews,
        now=NOW,
    )
    assert result.kind == "review"
