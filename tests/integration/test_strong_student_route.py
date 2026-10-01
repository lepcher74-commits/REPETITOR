from pathlib import Path

from repetitor.application.diagnostic import DiagnosticRouter
from repetitor.content import load_problems
from repetitor.content.module import load_module_manifest


BASE = Path("content/mathematics/fractions/add_unlike")


def test_ac04_strong_student_skips_prerequisite_and_guided_practice():
    module = load_module_manifest(BASE / "module.yaml")
    problems = {p.id: p for p in load_problems(BASE / "problems.yaml")}
    router = DiagnosticRouter.from_yaml(BASE / module.diagnostic_route)

    diagnostic = problems[router.start_problem_id]
    first = router.decide(
        problem=diagnostic,
        correct=True,
        misconception_hypothesis=None,
    )

    assert first.phase == "independent"
    assert first.next_problem_id == "frac.add.independent.001"

    visited = {diagnostic.id, first.next_problem_id}
    assert "frac.add.probe.equivalent" not in visited
    assert "frac.add.probe.lcm" not in visited
    assert "frac.add.guided.001" not in visited
