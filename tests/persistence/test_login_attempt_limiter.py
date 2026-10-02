from datetime import datetime, timedelta, timezone

import pytest

from repetitor.persistence.login_attempt_limiter import LoginAttemptLimiter, LoginRateLimited


NOW = datetime(2026, 10, 2, tzinfo=timezone.utc)


def test_account_limit_persists_and_resets(tmp_path):
    path = tmp_path / "login.sqlite"
    for _ in range(5):
        LoginAttemptLimiter(path).record_failure(parent_id="p", client_ip="192.0.2.1", now=NOW)
    with pytest.raises(LoginRateLimited):
        LoginAttemptLimiter(path).check(parent_id="p", client_ip="198.51.100.1", now=NOW)
    LoginAttemptLimiter(path).check(
        parent_id="p", client_ip="192.0.2.1", now=NOW + timedelta(minutes=15)
    )


def test_ip_limit_shared_across_accounts_and_rejection_atomic(tmp_path):
    limiter = LoginAttemptLimiter(tmp_path / "login.sqlite")
    for i in range(20):
        limiter.record_failure(parent_id=f"p{i}", client_ip="192.0.2.1", now=NOW)
    with pytest.raises(LoginRateLimited):
        limiter.record_failure(parent_id="new", client_ip="192.0.2.1", now=NOW)
    # IP rejection must not use account quota.
    for _ in range(5):
        limiter.record_failure(parent_id="new", client_ip="198.51.100.1", now=NOW)
    with pytest.raises(LoginRateLimited):
        limiter.check(parent_id="new", client_ip="198.51.100.1", now=NOW)
