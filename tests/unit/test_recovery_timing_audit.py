"""Deterministic tests of audit collection, not timing-security claims."""
import pytest

from repetitor.application.recovery_timing_audit import (
    bootstrap_median_interval,
    collect_interleaved,
    summarize_durations,
)


def test_interleaved_collection_counts_and_deterministic_schedule():
    order = []

    def scenario(label):
        def run():
            order.append(label)
        return run

    ticks = iter(range(1000))
    results = collect_interleaved(
        {"known": scenario("known"), "unknown": scenario("unknown")},
        repetitions=10, seed=19, clock_ns=lambda: next(ticks),
    )
    assert {name: len(values) for name, values in results.items()} == {
        "known": 10, "unknown": 10,
    }
    assert all(value == 1 for values in results.values() for value in values)
    first_order = order.copy()
    order.clear()
    ticks = iter(range(1000))
    collect_interleaved(
        {"known": scenario("known"), "unknown": scenario("unknown")},
        repetitions=10, seed=19, clock_ns=lambda: next(ticks),
    )
    assert order == first_order


def test_nearest_rank_percentiles_and_input_validation():
    result = summarize_durations(list(range(1, 101)))
    assert (result.samples, result.median_ns, result.p95_ns, result.p99_ns) == (
        100, 50.5, 95, 99,
    )
    with pytest.raises(ValueError):
        summarize_durations([])
    with pytest.raises(ValueError):
        summarize_durations([-1])
    with pytest.raises(ValueError):
        collect_interleaved({"known": lambda: None}, repetitions=0)


def test_bootstrap_median_interval_is_reproducible_and_bounded():
    values = list(range(1, 201))
    first = bootstrap_median_interval(values, resamples=500, seed=42)
    second = bootstrap_median_interval(values, resamples=500, seed=42)
    assert first == second
    assert 1 <= first[0] <= first[1] <= 200
    assert bootstrap_median_interval([7] * 200, resamples=100) == (7, 7)


def test_bootstrap_rejects_invalid_inputs():
    for values, samples, confidence in [
        ([], 100, 0.95), ([-1], 100, 0.95),
        ([1, 2], 99, 0.95), ([1, 2], 100, 1),
    ]:
        with pytest.raises(ValueError):
            bootstrap_median_interval(values, resamples=samples, confidence=confidence)
