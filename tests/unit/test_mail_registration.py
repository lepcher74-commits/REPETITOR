from datetime import datetime, timedelta, timezone

import pytest

from repetitor.application.mail_registration import MailRegistration
from repetitor.persistence.email_challenge_store import EmailChallengeStore
from repetitor.persistence.mail_request_limiter import AbuseLimitExceeded, MailRequestLimiter


NOW = datetime(2026, 10, 2, tzinfo=timezone.utc)


class FakeSender:
    def __init__(self, fail=False):
        self.messages = []
        self.fail = fail

    def send_challenge(self, *, recipient, token):
        if self.fail:
            raise RuntimeError("Delivery failed")
        self.messages.append((recipient, token))


def build(tmp_path, sender):
    return MailRegistration(
        limiter=MailRequestLimiter(tmp_path / "limits.sqlite"),
        challenges=EmailChallengeStore(tmp_path / "codes.sqlite"),
        sender=sender,
    )


def test_request_deliver_verify_once_without_exposing_token_as_result(tmp_path):
    sender = FakeSender()
    service = build(tmp_path, sender)
    assert service.request_challenge(
        parent_id="p", recipient="parent@example.test", client_ip="192.0.2.1", now=NOW
    ) is None
    assert sender.messages[0][0] == "parent@example.test"
    token = sender.messages[0][1]
    assert service.verify_challenge(parent_id="p", token=token, now=NOW)
    assert not service.verify_challenge(parent_id="p", token=token, now=NOW)


def test_cooldown_denies_repeat_without_sending(tmp_path):
    sender = FakeSender()
    service = build(tmp_path, sender)
    args = dict(parent_id="p", recipient="parent@example.test", client_ip="192.0.2.1")
    service.request_challenge(**args, now=NOW)
    with pytest.raises(ValueError, match="rate limited"):
        service.request_challenge(**args, now=NOW + timedelta(seconds=30))
    assert len(sender.messages) == 1


def test_delivery_failure_propagates_without_exposing_token(tmp_path):
    sender = FakeSender(fail=True)
    service = build(tmp_path, sender)
    with pytest.raises(RuntimeError, match="Delivery failed"):
        service.request_challenge(
            parent_id="p", recipient="parent@example.test", client_ip="192.0.2.1", now=NOW
        )
    assert sender.messages == []
