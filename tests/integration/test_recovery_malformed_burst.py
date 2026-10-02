"""Boundary regressions: malformed bursts cannot affect another client."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from threading import Barrier

from repetitor.application.recovery_acknowledgement import RecoveryAcknowledgement
from repetitor.application.parent_recovery_request import ParentRecoveryRequest
from repetitor.persistence.mail_request_limiter import MailRequestLimiter
from repetitor.persistence.malformed_request_limiter import MalformedRequestLimiter
from repetitor.persistence.password_recovery_store import PasswordRecoveryStore


NOW = datetime(2026, 10, 2, tzinfo=timezone.utc)


class Directory:
    def find_parent(self, *, normalized_email):
        return None


class Sender:
    def send_challenge(self, *, recipient, token):
        raise AssertionError("No email should be sent")


def test_parallel_malformed_burst_has_uniform_response_and_client_isolation(tmp_path):
    service = RecoveryAcknowledgement(
        ParentRecoveryRequest(
            directory=Directory(),
            limiter=MailRequestLimiter(tmp_path / "normal.sqlite"),
            recovery=PasswordRecoveryStore(tmp_path / "recovery.sqlite"),
            sender=Sender(),
        ),
        malformed_limiter=MalformedRequestLimiter(tmp_path / "malformed.sqlite"),
    )
    barrier = Barrier(12)

    def submit(_):
        barrier.wait(timeout=10)
        return service.submit(email="invalid", server_client_ip="192.0.2.1", now=NOW)

    with ThreadPoolExecutor(max_workers=12) as pool:
        replies = list(pool.map(submit, range(12)))
    assert len(set(replies)) == 1
    other = service.submit(email="invalid", server_client_ip="192.0.2.2", now=NOW)
    assert other == replies[0]
    from repetitor.persistence.mail_request_limiter import AbuseLimitExceeded
    import pytest
    with pytest.raises(AbuseLimitExceeded):
        service.malformed_limiter.check_and_record(client_ip="192.0.2.1", now=NOW)
    service.malformed_limiter.check_and_record(client_ip="192.0.2.2", now=NOW)
