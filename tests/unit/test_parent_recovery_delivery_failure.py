from datetime import datetime, timezone

import pytest

from repetitor.application.parent_recovery_request import ParentRecoveryRequest
from repetitor.persistence.mail_request_limiter import MailRequestLimiter
from repetitor.persistence.password_recovery_store import PasswordRecoveryStore


class Directory:
    def find_parent(self, *, normalized_email):
        return "parent" if normalized_email == "parent@example.test" else None


class FailingSender:
    def send_challenge(self, *, recipient, token):
        raise OSError("mail transport unavailable")


def test_delivery_failure_propagates_and_request_remains_limited(tmp_path):
    now = datetime(2026, 10, 2, tzinfo=timezone.utc)
    limiter = MailRequestLimiter(tmp_path / "limits.sqlite")
    recovery = PasswordRecoveryStore(tmp_path / "recovery.sqlite")
    service = ParentRecoveryRequest(
        directory=Directory(), limiter=limiter, recovery=recovery,
        sender=FailingSender(),
    )
    with pytest.raises(OSError):
        service.request(
            email="parent@example.test", server_client_ip="192.0.2.1", now=now,
        )
    for _ in range(2):
        with pytest.raises(OSError):
            service.request(
                email="parent@example.test", server_client_ip="192.0.2.1", now=now,
            )
    from repetitor.persistence.mail_request_limiter import AbuseLimitExceeded
    with pytest.raises(AbuseLimitExceeded):
        service.request(
            email="parent@example.test", server_client_ip="192.0.2.1", now=now,
        )
