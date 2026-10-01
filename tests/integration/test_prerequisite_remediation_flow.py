from datetime import datetime, timedelta, timezone
from pathlib import Path

from repetitor.application.diagnostic import DiagnosticRouter
from repetitor.application.remediation import load_remediations
from repetitor.application.session import LearningSessionService
from repetitor.content import load_problems
from repetitor.content.module import load_module_manifest
from repetitor.persistence import SQLiteLearningRepository


BASE = Path("content/mathematics/fractions/add_unlike")
NOW = datetime(2026, 9, 30, 12, 0, tzinfo=timezone.utc)


def test_failed_prerequisite_probe_remediates_persists_and_returns(tmp_path):
    module = load_module_manifest(BASE / "module.yaml")
    problems = {p.id: p for p in load_problems(BASE / "problems.yaml")}
    router = DiagnosticRouter.from_yaml(BASE / module.diagnostic_route)
    remediations = load_remediations(BASE / module.remediation_route)

    db = tmp_path / "learning.sqlite3"
    repo = SQLiteLearningRepository(db)
    repo.initialize()
    service = LearningSessionService(
        repo, {module.primary_skill.id: module.prerequisites}
    )

    probe = problems["frac.add.probe.equivalent"]
    failed = service.submit(
        student_id="student",
        problem=probe,
        answer="3",
        occurred_at=NOW,
    )
    assert not failed.verification.correct

    decision = router.decide(
        problem=probe,
        correct=False,
        misconception_hypothesis=failed.misconception_hypothesis,
    )
    assert decision.phase == "remediation"
    assert decision.remediation_skill_id == probe.primary_skill

    step = remediations[decision.remediation_skill_id]
    assert step.skill_id == probe.primary_skill

    for index, problem in enumerate(step.problems):
        expected = str(problem.verifier["expected"])
        outcome = service.submit(
            student_id="student",
            problem=problem,
            answer=expected,
            occurred_at=NOW + timedelta(minutes=index + 1),
        )
        assert outcome.verification.correct

    reopened = SQLiteLearningRepository(db)
    reopened.initialize()
    state = reopened.get_state("student", step.skill_id)
    assert state is not None
    assert state.evidence_count >= len(step.problems) + 1
    assert state.mastery >= step.exit_mastery

    assert step.return_problem_id in problems
    assert step.return_problem_id == "frac.add.probe.lcm"
