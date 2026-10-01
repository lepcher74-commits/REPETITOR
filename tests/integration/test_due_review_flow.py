from datetime import datetime, timedelta, timezone
from pathlib import Path

from repetitor.application.session import LearningSessionService
from repetitor.content import load_problems
from repetitor.content.module import load_module_manifest
from repetitor.domain import KnowledgeState
from repetitor.persistence import SQLiteLearningRepository


BASE = Path("content/mathematics/fractions/add_unlike")
NOW = datetime(2026, 10, 1, 8, 0, tzinfo=timezone.utc)


def test_ac08_due_review_is_selected_completed_and_rescheduled(tmp_path):
    module = load_module_manifest(BASE / "module.yaml")
    problems = {p.id: p for p in load_problems(BASE / "problems.yaml")}
    repo = SQLiteLearningRepository(tmp_path / "learning.sqlite3")
    repo.initialize()

    for prerequisite in module.prerequisites:
        repo.save_state(KnowledgeState("student", prerequisite, mastery=0.8))

    service = LearningSessionService(
        repo, {module.primary_skill.id: module.prerequisites}
    )
    initial = problems["frac.add.independent.001"]
    first = service.submit(
        student_id="student",
        problem=initial,
        answer=str(initial.verifier["expected"]),
        occurred_at=NOW,
    )
    due_at = NOW + timedelta(days=3)

    trigger = service.submit(
        student_id="student",
        problem=initial,
        answer=str(initial.verifier["expected"]),
        occurred_at=due_at,
    )
    assert trigger.next_activity.kind == "review"
    assert trigger.next_activity.skill_id == module.primary_skill.id

    review_ids = module.review_problems_by_skill[trigger.next_activity.skill_id]
    review = problems[review_ids[0]]
    assert review.purpose == "review"

    before = repo.get_state("student", module.primary_skill.id)
    outcome = service.submit(
        student_id="student",
        problem=review,
        answer=str(review.verifier["expected"]),
        occurred_at=due_at + timedelta(minutes=1),
    )
    after = repo.get_state("student", module.primary_skill.id)

    assert outcome.verification.correct
    assert after is not None and before is not None
    assert after.retention > before.retention
    assert repo.due_reviews("student", due_at + timedelta(days=30))
