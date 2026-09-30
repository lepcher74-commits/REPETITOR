from pathlib import Path

from repetitor.application.diagnostic import FractionDiagnosticRouter
from repetitor.content import load_problems


PROBLEMS = {
    p.id: p
    for p in load_problems(Path("content/mathematics/fractions/add_unlike/problems.yaml"))
}
ROUTER = FractionDiagnosticRouter()


def test_characteristic_wrong_answer_routes_to_misconception_probe():
    result = ROUTER.decide(
        problem=PROBLEMS["frac.add.diag.001"],
        correct=False,
        misconception_hypothesis="add_denominators",
    )
    assert result.next_problem_id == "frac.add.probe.add_denominators"


def test_unknown_error_routes_to_prerequisite_probe():
    result = ROUTER.decide(
        problem=PROBLEMS["frac.add.diag.001"],
        correct=False,
        misconception_hypothesis=None,
    )
    assert result.next_problem_id == "frac.add.probe.equivalent"


def test_failed_equivalent_fraction_probe_stops_for_remediation():
    result = ROUTER.decide(
        problem=PROBLEMS["frac.add.probe.equivalent"],
        correct=False,
        misconception_hypothesis=None,
    )
    assert result.phase == "remediation"
    assert result.next_problem_id is None


def test_successful_standard_work_routes_to_transfer():
    result = ROUTER.decide(
        problem=PROBLEMS["frac.add.independent.002"],
        correct=True,
        misconception_hypothesis=None,
    )
    assert result.next_problem_id == "frac.add.transfer.001"
