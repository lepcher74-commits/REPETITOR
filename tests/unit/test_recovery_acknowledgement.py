from datetime import datetime, timezone

from repetitor.application.parent_recovery_request import ParentRecoveryRequest
from repetitor.application.recovery_acknowledgement import RecoveryAcknowledgement
from repetitor.persistence.mail_request_limiter import MailRequestLimiter
from repetitor.persistence.password_recovery_store import PasswordRecoveryStore


NOW = datetime(2026, 10, 2, tzinfo=timezone.utc)


class Directory:
    def find_parent(self, *, normalized_email):
        return "parent" if normalized_email == "parent@example.test" else None


class Sender:
    def __init__(self, fail=False):
        self.fail = fail
        self.sent = []

    def send_challenge(self, *, recipient, token):
        if self.fail:
            raise OSError("transport unavailable")
        self.sent.append(recipient)


def make_service(tmp_path, sender):
    requests = ParentRecoveryRequest(
        directory=Directory(), limiter=MailRequestLimiter(tmp_path / "limits.sqlite"),
        recovery=PasswordRecoveryStore(tmp_path / "recovery.sqlite"), sender=sender,
    )
    return RecoveryAcknowledgement(requests)


def test_known_unknown_and_throttled_addresses_share_response(tmp_path):
    sender = Sender()
    service = make_service(tmp_path, sender)
    unknown = service.submit(
        email="unknown@example.test", server_client_ip="192.0.2.1", now=NOW,
    )
    known = service.submit(
        email="parent@example.test", server_client_ip="192.0.2.1", now=NOW,
    )
    for _ in range(2):
        assert service.submit(
            email="parent@example.test", server_client_ip="192.0.2.1", now=NOW,
        ) == known
    throttled = service.submit(
        email="parent@example.test", server_client_ip="192.0.2.1", now=NOW,
    )
    assert unknown == known == throttled
    assert len(sender.sent) == 3


def test_mail_transport_failure_does_not_change_response(tmp_path):
    service = make_service(tmp_path, Sender(fail=True))
    failed = service.submit(
        email="parent@example.test", server_client_ip="192.0.2.1", now=NOW,
    )
    unknown = service.submit(
        email="unknown@example.test", server_client_ip="192.0.2.1", now=NOW,
    )
    assert failed == unknown


def test_malformed_address_gets_same_acknowledgement(tmp_path):
    service = make_service(tmp_path, Sender())
    malformed = service.submit(
        email="not-an-address", server_client_ip="192.0.2.1", now=NOW,
    )
    unknown = service.submit(
        email="unknown@example.test", server_client_ip="192.0.2.1", now=NOW,
    )
    assert malformed == unknown


def test_untrusted_request_context_is_not_silently_accepted(tmp_path):
    import pytest
    service = make_service(tmp_path, Sender())
    with pytest.raises(ValueError):
        service.submit(email="parent@example.test", server_client_ip=" ", now=NOW)
    with pytest.raises(ValueError):
        service.submit(
            email="parent@example.test", server_client_ip="192.0.2.1",
            now=datetime(2026, 10, 2),
        )


def test_malformed_requests_are_persistently_throttled_when_configured(tmp_path):
    from repetitor.persistence.mail_request_limiter import AbuseLimitExceeded
    from repetitor.persistence.malformed_request_limiter import MalformedRequestLimiter
    limiter = MalformedRequestLimiter(tmp_path / "malformed.sqlite")
    requests = ParentRecoveryRequest(
        directory=Directory(), limiter=MailRequestLimiter(tmp_path / "normal.sqlite"),
        recovery=PasswordRecoveryStore(tmp_path / "recovery.sqlite"), sender=Sender(),
    )
    service = RecoveryAcknowledgement(requests, malformed_limiter=limiter)
    responses = [service.submit(
        email="invalid", server_client_ip="192.0.2.1", now=NOW,
    ) for _ in range(12)]
    assert len(set(responses)) == 1
    with __import__("pytest").raises(AbuseLimitExceeded):
        limiter.check_and_record(
            client_ip="192.0.2.1", now=NOW,
        )


def test_malformed_quota_does_not_block_other_client(tmp_path):
    from repetitor.persistence.malformed_request_limiter import MalformedRequestLimiter
    limiter = MalformedRequestLimiter(tmp_path / "malformed.sqlite")
    for _ in range(10):
        limiter.check_and_record(client_ip="192.0.2.1", now=NOW)
    limiter.check_and_record(client_ip="192.0.2.2", now=NOW)
