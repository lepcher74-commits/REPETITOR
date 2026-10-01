from pathlib import Path

from repetitor.application.diagnostic import DiagnosticRouter
from repetitor.content import load_problems

BASE = Path("content/mathematics/fractions/add_unlike")
PROBLEMS = {p.id: p for p in load_problems(BASE / "problems.yaml")}
ROUTER = DiagnosticRouter.from_yaml(BASE / "diagnostic_route.yaml")


def test_router_is_loaded_from_content():
    assert ROUTER.start_problem_id == "frac.add.diag.001"


def test_characteristic_wrong_answer_routes_to_misconception_probe():
    result = ROUTER.decide(problem=PROBLEMS["frac.add.diag.001"], correct=False, misconception_hypothesis="add_denominators")
    assert result.next_problem_id == "frac.add.probe.add_denominators"


def test_unknown_error_routes_to_prerequisite_probe():
    result = ROUTER.decide(problem=PROBLEMS["frac.add.diag.001"], correct=False, misconception_hypothesis=None)
    assert result.next_problem_id == "frac.add.probe.equivalent"


def test_failed_equivalent_fraction_probe_stops_for_remediation():
    result = ROUTER.decide(problem=PROBLEMS["frac.add.probe.equivalent"], correct=False, misconception_hypothesis=None)
    assert result.phase == "remediation"
    assert result.next_problem_id is None


def test_successful_standard_work_routes_to_transfer():
    result = ROUTER.decide(problem=PROBLEMS["frac.add.independent.002"], correct=True, misconception_hypothesis=None)
    assert result.next_problem_id == "frac.add.transfer.001"


def test_remediation_decisions_declare_target_skill():
    router = DiagnosticRouter.from_yaml(BASE / "diagnostic_route.yaml")
    problems = {p.id: p for p in load_problems(BASE / "problems.yaml")}
    for problem_id in ("frac.add.probe.equivalent", "frac.add.probe.lcm"):
        problem = problems[problem_id]
        decision = router.decide(
            problem=problem,
            correct=False,
            misconception_hypothesis=None,
        )
        assert decision.phase == "remediation"
        assert decision.remediation_skill_id == problem.primary_skill


def test_router_reports_only_declared_problem_ownership():
    router = DiagnosticRouter.from_yaml(Path("content/mathematics/fractions/add_unlike/diagnostic_route.yaml"))
    assert router.handles(router.start_problem_id)
    assert not router.handles("frac.eq.diag.001")
