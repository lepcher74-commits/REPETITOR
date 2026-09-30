from datetime import datetime, timezone
from pathlib import Path

from repetitor.ai import SafeAIProvider
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


class BrokenProvider:
    def explain(self, **kwargs):
        raise ConnectionError("network unavailable")

    def ask_socratic(self, **kwargs):
        raise TimeoutError("provider timeout")


def test_ai_failure_does_not_break_verified_learning_or_persistence(tmp_path):
    db = tmp_path / "learning.sqlite3"
    repo = SQLiteLearningRepository(db)
    repo.initialize()
    for prerequisite in PREREQS:
        repo.save_state(KnowledgeState("student", prerequisite, mastery=0.8))

    ai = SafeAIProvider(BrokenProvider())
    ai_result = ai.explain(skill_id=SKILL, context="Explain unlike denominators")
    assert not ai_result.available
    assert ai_result.error_code == "ai_failure"

    service = LearningSessionService(repo, {SKILL: PREREQS})
    problem = next(
        p for p in load_problems(CONTENT)
        if p.id == "frac.add.diag.001"
    )
    outcome = service.submit(
        student_id="student",
        problem=problem,
        answer="5/6",
        occurred_at=NOW,
    )

    assert outcome.verification.correct
    assert outcome.knowledge_state.mastery > 0

    # Reopen storage to prove progress survived independently of AI failure.
    reopened = SQLiteLearningRepository(db)
    reopened.initialize()
    persisted = reopened.get_state("student", SKILL)
    assert persisted is not None
    assert persisted.mastery == outcome.knowledge_state.mastery
    assert persisted.evidence_count == outcome.knowledge_state.evidence_count
