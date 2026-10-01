import pytest

from repetitor.verification import UnsupportedVerifierError, verify_answer


@pytest.mark.parametrize("answer", ["", "abc", "1/0", "1/2/3", None])
def test_invalid_rational_inputs_fail_closed_without_crash(answer):
    result = verify_answer({"type": "rational_equivalence", "expected": "1/2"}, answer)
    assert not result.correct
    assert not result.mathematically_equivalent
    assert result.feedback_code == "invalid_rational"


@pytest.mark.parametrize(
    ("answer", "expected", "correct"),
    [("-1/2", "-2/4", True), (" 2 / 4 ", "1/2", True)],
)
def test_rational_equivalence_handles_sign_and_whitespace(answer, expected, correct):
    result = verify_answer({"type": "rational_equivalence", "expected": expected}, answer)
    assert result.correct is correct


def test_negative_denominator_text_fails_closed_as_invalid_school_input():
    result = verify_answer(
        {"type": "rational_equivalence", "expected": "-1/2", "require_simplified": True},
        "1/-2",
    )
    assert not result.mathematically_equivalent
    assert not result.correct
    assert result.feedback_code == "invalid_rational"


def test_unsupported_verifier_fails_explicitly():
    with pytest.raises(UnsupportedVerifierError):
        verify_answer({"type": "unknown", "expected": "x"}, "x")
