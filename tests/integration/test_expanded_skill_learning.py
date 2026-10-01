from datetime import datetime, timezone
from pathlib import Path

from repetitor.application.session import LearningSessionService
from repetitor.content import load_problems
from repetitor.content.loader import load_skill
from repetitor.persistence import SQLiteLearningRepository


BASE = Path("content/mathematics/fractions/equivalent")


def test_second_skill_updates_knowledge_through_generic_learning_service(tmp_path):
    skill = load_skill(BASE / "skill.yaml")
    problem = next(
        p for p in load_problems(BASE / "problems.yaml")
        if p.id == "frac.eq.independent.001"
    )
    repo = SQLiteLearningRepository(tmp_path / "learning.sqlite3")
    repo.initialize()
    service = LearningSessionService(repo, {skill.id: skill.prerequisites})

    outcome = service.submit(
        student_id="student",
        problem=problem,
        answer=str(problem.verifier["expected"]),
        occurred_at=datetime.now(timezone.utc),
    )

    state = repo.get_state("student", skill.id)
    assert outcome.verification.correct
    assert state is not None
    assert state.evidence_count == 1
    assert state.mastery > 0
