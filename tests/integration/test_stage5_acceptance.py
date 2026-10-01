from datetime import datetime, timezone
from pathlib import Path

from repetitor.application.mastery import apply_evidence
from repetitor.content import load_problems
from repetitor.content.module import load_module_manifest
from repetitor.domain import AttemptEvidence, KnowledgeState
from repetitor.verification import verify_answer


BASE = Path("content/mathematics/fractions/add_unlike")
NOW = datetime(2026, 10, 1, tzinfo=timezone.utc)


def test_ac06_hint_progression_ends_in_more_explicit_support():
    problems = {p.id: p for p in load_problems(BASE / "problems.yaml")}
    guided = problems["frac.add.guided.001"]
    assert [h.level for h in guided.hints] == [1, 2, 3, 4]
    assert guided.hints[0].kind == "socratic"
    assert guided.hints[-1].kind == "worked_step"


def test_ac06_revealing_help_is_not_rewarded_as_independence():
    state = KnowledgeState("student", "skill")
    evidence = AttemptEvidence(
        id="e1", student_id="student", problem_id="p", skill_id="skill",
        occurred_at=NOW, correct=True, purpose="guided", hint_level=4,
        answer_revealing_hint=True,
    )
    updated = apply_evidence(state, evidence)
    assert updated.independence <= state.independence


def test_ac07_supported_mvp_math_is_formally_verified():
    for problem in load_problems(BASE / "problems.yaml"):
        result = verify_answer(problem.verifier, str(problem.verifier["expected"]))
        assert result.correct


def test_ac10_ac12_module_requires_no_remote_resource_and_uses_local_content_paths():
    module = load_module_manifest(BASE / "module.yaml")
    assert module.diagnostic_route.endswith(".yaml")
    assert module.remediation_route.endswith(".yaml")
    for path in (module.diagnostic_route, module.remediation_route):
        assert "://" not in path
        assert (BASE / path).exists()
