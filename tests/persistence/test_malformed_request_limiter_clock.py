"""Clock boundary and persistence tests for malformed request throttling."""
from datetime import datetime, timedelta, timezone

import pytest

from repetitor.persistence.mail_request_limiter import AbuseLimitExceeded
from repetitor.persistence.malformed_request_limiter import MalformedRequestLimiter


NOW = datetime(2026, 10, 2, tzinfo=timezone.utc)


def test_quota_survives_restart_and_resets_at_window_boundary(tmp_path):
    path = tmp_path / "limits.sqlite"
    for _ in range(10):
        MalformedRequestLimiter(path).check_and_record(client_ip="192.0.2.1", now=NOW)
    restarted = MalformedRequestLimiter(path)
    with pytest.raises(AbuseLimitExceeded):
        restarted.check_and_record(client_ip="192.0.2.1", now=NOW + timedelta(minutes=59))
    restarted.check_and_record(client_ip="192.0.2.1", now=NOW + timedelta(hours=1))
    restarted.check_and_record(client_ip="192.0.2.2", now=NOW)


def test_backwards_clock_does_not_reset_quota(tmp_path):
    limiter = MalformedRequestLimiter(tmp_path / "limits.sqlite")
    limiter.check_and_record(client_ip="192.0.2.1", now=NOW)
    with pytest.raises(AbuseLimitExceeded):
        limiter.check_and_record(client_ip="192.0.2.1", now=NOW - timedelta(seconds=1))
