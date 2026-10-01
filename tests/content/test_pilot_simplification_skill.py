from pathlib import Path

from repetitor.content import load_problems, load_skill
from repetitor.verification import verify_answer


ROOT = Path("content/mathematics/fractions/simplify")


def test_simplification_skill_uses_generic_content_and_verification_interfaces():
    skill = load_skill(ROOT / "skill.yaml")
    problems = load_problems(ROOT / "problems.yaml")

    assert skill.id == "math.g6.fractions.simplify"
    assert "math.g6.fractions.equivalent" in skill.prerequisites
    assert {"diagnostic", "guided", "independent", "transfer", "review"} <= {
        problem.purpose for problem in problems
    }
    assert all(problem.primary_skill == skill.id for problem in problems)

    for problem in problems:
        expected = str(problem.verifier["expected"])
        result = verify_answer(problem.verifier, expected)
        assert result.correct, problem.id
