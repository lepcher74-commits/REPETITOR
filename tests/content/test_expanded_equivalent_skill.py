from pathlib import Path

from repetitor.content import load_problems
from repetitor.content.loader import load_skill
from repetitor.verification import verify_answer


BASE = Path("content/mathematics/fractions/equivalent")


def test_equivalent_fraction_skill_uses_existing_content_interfaces():
    skill = load_skill(BASE / "skill.yaml")
    problems = load_problems(BASE / "problems.yaml")

    assert skill.id == "math.g6.fractions.equivalent"
    assert {p.purpose for p in problems} >= {
        "diagnostic", "guided", "independent", "transfer", "review"
    }
    assert all(p.primary_skill == skill.id for p in problems)


def test_equivalent_fraction_authored_answers_verify():
    for problem in load_problems(BASE / "problems.yaml"):
        expected = str(problem.verifier["expected"])
        result = verify_answer(problem.verifier, expected)
        assert result.correct, problem.id
