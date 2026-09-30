from pathlib import Path
from repetitor.application.remediation import load_remediations
from repetitor.verification import verify_answer

PATH=Path("content/mathematics/fractions/add_unlike/remediation.yaml")

def test_each_remediation_has_guided_and_two_independent_checks():
    for r in load_remediations(PATH).values():
        assert [p.purpose for p in r.problems] == ["guided","independent","independent"]

def test_all_remediation_expected_answers_verify():
    for r in load_remediations(PATH).values():
        for p in r.problems:
            assert verify_answer(p.verifier,str(p.verifier["expected"])).correct

def test_exit_requires_accumulated_mastery():
    for r in load_remediations(PATH).values():
        assert r.exit_mastery == 0.45
