"""Offline timing-audit measurement helpers. Not a security certification."""
from __future__ import annotations

import random
import statistics
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class TimingSummary:
    samples: int
    median_ns: float
    p95_ns: int
    p99_ns: int


def summarize_durations(durations_ns: list[int]) -> TimingSummary:
    """Nearest-rank tails avoid interpolation hiding outliers."""
    if not durations_ns or any(x < 0 for x in durations_ns):
        raise ValueError("Nonempty nonnegative durations required")
    ordered = sorted(durations_ns)

    def rank(p: float) -> int:
        return ordered[max(0, int(__import__("math").ceil(p * len(ordered))) - 1)]

    return TimingSummary(
        samples=len(ordered),
        median_ns=statistics.median(ordered),
        p95_ns=rank(0.95),
        p99_ns=rank(0.99),
    )


def collect_interleaved(
    scenarios: Mapping[str, Callable[[], object]], *,
    repetitions: int,
    seed: int = 0,
    clock_ns: Callable[[], int] = time.perf_counter_ns,
) -> dict[str, list[int]]:
    """Run synthetic scenarios in reproducible randomized order.

    Labels must be non-identifying; do not provide real accounts or live endpoints.
    Caller owns staging isolation, quota resets, warmup and statistical review.
    """
    if not scenarios or repetitions < 1 or any(not label for label in scenarios):
        raise ValueError("Named scenarios and positive repetitions required")
    schedule = list(scenarios) * repetitions
    random.Random(seed).shuffle(schedule)
    results: dict[str, list[int]] = {label: [] for label in scenarios}
    for label in schedule:
        start = clock_ns()
        scenarios[label]()
        elapsed = clock_ns() - start
        if elapsed < 0:
            raise ValueError("Monotonic clock moved backwards")
        results[label].append(elapsed)
    return results


def bootstrap_median_interval(
    durations_ns: list[int], *, resamples: int = 2000, seed: int = 0,
    confidence: float = 0.95,
) -> tuple[float, float]:
    """Seeded percentile bootstrap interval; exploratory, not a security verdict.

    Independence of samples and environment stability must be reviewed separately.
    """
    if not durations_ns or any(x < 0 for x in durations_ns):
        raise ValueError("Nonempty nonnegative durations required")
    if resamples < 100 or not 0 < confidence < 1:
        raise ValueError("At least 100 resamples and confidence in (0, 1) required")
    rng = random.Random(seed)
    n = len(durations_ns)
    estimates = sorted(
        statistics.median(rng.choices(durations_ns, k=n))
        for _ in range(resamples)
    )
    lower = max(0, int(__import__("math").floor((1 - confidence) / 2 * resamples)))
    upper = min(resamples - 1, int(__import__("math").ceil((1 + confidence) / 2 * resamples)) - 1)
    return estimates[lower], estimates[upper]
