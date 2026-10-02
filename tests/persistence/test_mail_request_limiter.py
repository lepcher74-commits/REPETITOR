from datetime import datetime, timedelta, timezone

import pytest

from repetitor.persistence.mail_request_limiter import AbuseLimitExceeded, MailRequestLimiter


NOW = datetime(2026, 10, 2, tzinfo=timezone.utc)


def test_account_limit_persists_across_restarts(tmp_path):
    path = tmp_path / "limits.sqlite"
    for _ in range(3):
        MailRequestLimiter(path).check_and_record(parent_id="p", client_ip="1.2.3.4", now=NOW)
    with pytest.raises(AbuseLimitExceeded):
        MailRequestLimiter(path).check_and_record(parent_id="p", client_ip="1.2.3.4", now=NOW)
    MailRequestLimiter(path).check_and_record(parent_id="p", client_ip="1.2.3.4", now=NOW + timedelta(hours=1))


def test_ip_limit_is_shared_across_accounts_and_failed_request_is_atomic(tmp_path):
    store = MailRequestLimiter(tmp_path / "limits.sqlite")
    for i in range(10):
        store.check_and_record(parent_id=f"p{i}", client_ip="1.2.3.4", now=NOW)
    with pytest.raises(AbuseLimitExceeded):
        store.check_and_record(parent_id="new", client_ip="1.2.3.4", now=NOW)
    # Rejected request must not consume the account quota.
    store.check_and_record(parent_id="new", client_ip="5.6.7.8", now=NOW)


def test_invalid_identity_or_time_rejected(tmp_path):
    store = MailRequestLimiter(tmp_path / "limits.sqlite")
    with pytest.raises(ValueError):
        store.check_and_record(parent_id=" ", client_ip="1.2.3.4", now=NOW)
    with pytest.raises(ValueError):
        store.check_and_record(parent_id="p", client_ip="1.2.3.4", now=NOW.replace(tzinfo=None))
