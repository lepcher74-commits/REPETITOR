from datetime import datetime, timezone
from pathlib import Path

from repetitor.application.session import LearningSessionService
from repetitor.content import load_problems
from repetitor.domain import KnowledgeState
from repetitor.persistence import SQLiteLearningRepository


NOW = datetime(2026, 9, 30, 12, 0, tzinfo=timezone.utc)
CONTENT = Path("content/mathematics/fractions/add_unlike/problems.yaml")
SKILL = "math.g6.fractions.add_unlike"
PREREQS = (
    "math.g6.fractions.equivalent",
    "math.g6.fractions.common_denominator",
)


def setup_service(tmp_path):
    repo = SQLiteLearningRepository(tmp_path / "learning.sqlite3")
    repo.initialize()
    # Reference test starts with prerequisites known; prerequisite-routing has
    # separate tests and will later be populated by diagnostics.
    for prerequisite in PREREQS:
        repo.save_state(KnowledgeState("student", prerequisite, mastery=0.8))
    return repo, LearningSessionService(repo, {SKILL: PREREQS})


def problem(problem_id):
    return next(p for p in load_problems(CONTENT) if p.id == problem_id)


def test_correct_answer_persists_learning_and_schedules_next_step(tmp_path):
    repo, service = setup_service(tmp_path)
    outcome = service.submit(
        student_id="student",
        problem=problem("frac.add.diag.001"),
        answer="5/6",
        occurred_at=NOW,
    )
    assert outcome.verification.correct
    assert outcome.knowledge_state.mastery > 0
    assert repo.get_state("student", SKILL) is not None
    assert outcome.next_activity.kind == "learn"


def test_known_wrong_pattern_is_only_a_hypothesis(tmp_path):
    _, service = setup_service(tmp_path)
    outcome = service.submit(
        student_id="student",
        problem=problem("frac.add.diag.001"),
        answer="2/5",
        occurred_at=NOW,
    )
    assert not outcome.verification.correct
    assert outcome.misconception_hypothesis == "add_denominators"
    # No field or API marks it confirmed from this single response.


def test_transfer_updates_transfer_dimension(tmp_path):
    _, service = setup_service(tmp_path)
    outcome = service.submit(
        student_id="student",
        problem=problem("frac.add.transfer.001"),
        answer="7/18",
        occurred_at=NOW,
    )
    assert outcome.verification.correct
    assert outcome.knowledge_state.transfer > 0
