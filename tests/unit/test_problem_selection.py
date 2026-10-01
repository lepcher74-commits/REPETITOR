from repetitor.application.problem_selection import select_fresh_problem
from repetitor.domain import Problem


def problem(problem_id):
    return Problem(
        id=problem_id,
        primary_skill="skill",
        purpose="review",
        prompt_ru=problem_id,
        verifier={"type": "exact_integer", "expected": 1},
    )


def test_fresh_selector_skips_attempted_items():
    items = [problem("a"), problem("b"), problem("c")]
    assert select_fresh_problem(items, {"a", "b"}).id == "c"


def test_fresh_selector_returns_none_when_pool_exhausted():
    items = [problem("a"), problem("b")]
    assert select_fresh_problem(items, {"a", "b"}) is None
