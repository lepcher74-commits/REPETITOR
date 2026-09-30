from repetitor.verification import verify_answer


def test_rational_equivalence_accepts_equivalent_fraction():
    result = verify_answer(
        {"type": "rational_equivalence", "expected": "5/6"},
        "10/12",
    )
    assert result.correct
    assert result.mathematically_equivalent


def test_simplest_form_is_separate_instruction():
    result = verify_answer(
        {"type": "rational_equivalence", "expected": "5/6", "require_simplified": True},
        "10/12",
    )
    assert not result.correct
    assert result.mathematically_equivalent
    assert not result.instruction_satisfied
    assert result.feedback_code == "simplify_required"


def test_wrong_fraction_is_not_equivalent():
    result = verify_answer(
        {"type": "rational_equivalence", "expected": "5/6"},
        "2/5",
    )
    assert not result.correct
    assert not result.mathematically_equivalent
