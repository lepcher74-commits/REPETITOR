from __future__ import annotations

from fractions import Fraction
from math import gcd
from typing import Any

from repetitor.domain import VerificationResult


class UnsupportedVerifierError(ValueError):
    pass


def _fraction(value: Any) -> Fraction:
    text = str(value).strip().replace(" ", "")
    try:
        return Fraction(text)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("invalid rational answer") from exc


def _is_simplified_fraction(text: str) -> bool:
    raw = text.strip().replace(" ", "")
    if "/" not in raw:
        return True
    try:
        numerator_s, denominator_s = raw.split("/", 1)
        numerator, denominator = int(numerator_s), int(denominator_s)
    except ValueError:
        return False
    return denominator > 0 and gcd(abs(numerator), denominator) == 1


def verify_answer(config: dict[str, Any], answer: Any) -> VerificationResult:
    verifier_type = config.get("type")
    expected = config.get("expected")

    if verifier_type == "exact_integer":
        try:
            actual = int(str(answer).strip())
            expected_int = int(expected)
        except (TypeError, ValueError):
            return VerificationResult(False, False, False, feedback_code="invalid_integer")
        correct = actual == expected_int
        return VerificationResult(correct, correct, correct, str(actual))

    if verifier_type == "multiple_choice":
        actual = str(answer).strip()
        expected_s = str(expected).strip()
        correct = actual == expected_s
        return VerificationResult(correct, correct, correct, actual)

    if verifier_type == "rational_equivalence":
        try:
            actual_fraction = _fraction(answer)
            expected_fraction = _fraction(expected)
        except ValueError:
            return VerificationResult(False, False, False, feedback_code="invalid_rational")
        equivalent = actual_fraction == expected_fraction
        simplified_required = bool(config.get("require_simplified", False))
        instruction_ok = (not simplified_required) or _is_simplified_fraction(str(answer))
        correct = equivalent and instruction_ok
        feedback = None
        if equivalent and not instruction_ok:
            feedback = "simplify_required"
        return VerificationResult(
            correct=correct,
            mathematically_equivalent=equivalent,
            instruction_satisfied=instruction_ok,
            normalized_answer=str(actual_fraction),
            feedback_code=feedback,
        )

    raise UnsupportedVerifierError(f"Unsupported verifier type: {verifier_type!r}")
