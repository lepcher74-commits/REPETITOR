from pathlib import Path

from repetitor.content import load_problems, load_skill
from repetitor.verification import verify_answer


ROOT = Path("content/mathematics/fractions/subtract_unlike")


def test_subtraction_skill_uses_connected_generic_architecture():
    skill = load_skill(ROOT / "skill.yaml")
    problems = load_problems(ROOT / "problems.yaml")

    assert {
        "math.g6.fractions.equivalent",
        "math.prereq.lcm",
        "math.g6.fractions.simplify",
    } <= set(skill.prerequisites)
    assert {"diagnostic", "guided", "independent", "transfer", "review"} <= {
        problem.purpose for problem in problems
    }
    assert all(problem.primary_skill == skill.id for problem in problems)

    for problem in problems:
        result = verify_answer(problem.verifier, str(problem.verifier["expected"]))
        assert result.correct, problem.id
