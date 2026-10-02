"""Concurrency regressions for the persisted malformed-request budget."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from threading import Barrier

from repetitor.persistence.mail_request_limiter import AbuseLimitExceeded
from repetitor.persistence.malformed_request_limiter import MalformedRequestLimiter


NOW = datetime(2026, 10, 2, tzinfo=timezone.utc)


def test_simultaneous_requests_cannot_exceed_budget(tmp_path):
    limiter = MalformedRequestLimiter(tmp_path / "limits.sqlite")
    barrier = Barrier(12)

    def attempt(_):
        barrier.wait(timeout=10)
        try:
            limiter.check_and_record(client_ip="192.0.2.1", now=NOW)
            return True
        except AbuseLimitExceeded:
            return False

    with ThreadPoolExecutor(max_workers=12) as pool:
        outcomes = list(pool.map(attempt, range(12)))
    assert outcomes.count(True) == 10
    assert outcomes.count(False) == 2
    limiter.check_and_record(client_ip="192.0.2.2", now=NOW)
