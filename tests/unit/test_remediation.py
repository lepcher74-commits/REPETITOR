from repetitor.application.remediation import REMEDIATIONS
from repetitor.verification import verify_answer


def test_equivalent_fraction_remediation_has_verifiable_exit():
    step = REMEDIATIONS["math.g6.fractions.equivalent"]
    assert verify_answer(step.verifier, "4").correct
    assert not verify_answer(step.verifier, "5").correct


def test_lcm_remediation_has_verifiable_exit():
    step = REMEDIATIONS["math.prereq.lcm"]
    assert verify_answer(step.verifier, "24").correct
