from pathlib import Path

from repetitor.application.remediation import load_remediations
from repetitor.verification import verify_answer


PATH = Path("content/mathematics/fractions/add_unlike/remediation.yaml")


def test_remediation_is_content_not_python_constant():
    remediations = load_remediations(PATH)
    assert set(remediations) == {
        "math.g6.fractions.equivalent",
        "math.prereq.lcm",
    }


def test_equivalent_fraction_remediation_has_verifiable_exit():
    step = load_remediations(PATH)["math.g6.fractions.equivalent"]
    assert verify_answer(step.problem.verifier, "4").correct
    assert not verify_answer(step.problem.verifier, "5").correct


def test_lcm_remediation_has_verifiable_exit():
    step = load_remediations(PATH)["math.prereq.lcm"]
    assert verify_answer(step.problem.verifier, "24").correct
