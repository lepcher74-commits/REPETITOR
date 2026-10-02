from datetime import datetime, timezone

import pytest

from repetitor.application.parent_recovery_request import ParentRecoveryRequest
from repetitor.persistence.mail_request_limiter import AbuseLimitExceeded, MailRequestLimiter
from repetitor.persistence.password_recovery_store import PasswordRecoveryStore


NOW = datetime(2026, 10, 2, tzinfo=timezone.utc)


class Directory:
    def find_parent(self, *, normalized_email):
        return "parent" if normalized_email == "parent@example.test" else None


class Sender:
    def __init__(self):
        self.sent = []

    def send_challenge(self, *, recipient, token):
        self.sent.append((recipient, token))


def test_known_address_receives_token_but_unknown_does_not(tmp_path):
    sender = Sender()
    recovery = PasswordRecoveryStore(tmp_path / "recovery.sqlite")
    service = ParentRecoveryRequest(
        directory=Directory(), limiter=MailRequestLimiter(tmp_path / "limits.sqlite"),
        recovery=recovery, sender=sender,
    )
    assert service.request(email="unknown@example.test", server_client_ip="192.0.2.1", now=NOW) is None
    assert sender.sent == []
    assert service.request(email=" PARENT@EXAMPLE.TEST ", server_client_ip="192.0.2.1", now=NOW) is None
    assert len(sender.sent) == 1
    recipient, token = sender.sent[0]
    assert recipient == "parent@example.test"
    assert recovery.consume(parent_id="parent", token=token, now=NOW)


def test_unknown_address_is_rate_limited_too(tmp_path):
    sender = Sender()
    service = ParentRecoveryRequest(
        directory=Directory(), limiter=MailRequestLimiter(tmp_path / "limits.sqlite"),
        recovery=PasswordRecoveryStore(tmp_path / "recovery.sqlite"), sender=sender,
    )
    for _ in range(3):
        service.request(email="unknown@example.test", server_client_ip="192.0.2.1", now=NOW)
    with pytest.raises(AbuseLimitExceeded):
        service.request(email="unknown@example.test", server_client_ip="192.0.2.1", now=NOW)
    assert not sender.sent
