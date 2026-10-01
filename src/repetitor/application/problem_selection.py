from __future__ import annotations

from collections.abc import Iterable

from repetitor.domain import Problem


def select_fresh_problem(
    problems: Iterable[Problem],
    attempted_problem_ids: set[str],
) -> Problem | None:
    """Return the first authored problem not yet attempted by this learner."""
    return next((problem for problem in problems if problem.id not in attempted_problem_ids), None)
