from datetime import datetime, timezone

import pytest

from repetitor.application.bound_mail_registration import (
    AuthenticatedParent, BoundMailRegistration,
)
from repetitor.application.mail_registration import MailRegistration
from repetitor.persistence.email_challenge_store import EmailChallengeStore
from repetitor.persistence.mail_request_limiter import MailRequestLimiter


NOW = datetime(2026, 10, 2, tzinfo=timezone.utc)


class Directory:
    def registered_mailbox(self, parent_id):
        return {"p": "parent@example.test", "other": "other@example.test"}.get(parent_id)


class Sender:
    def __init__(self):
        self.sent = []

    def send_challenge(self, *, recipient, token):
        self.sent.append((recipient, token))


def service(tmp_path):
    sender = Sender()
    core = MailRegistration(
        limiter=MailRequestLimiter(tmp_path / "limits.sqlite"),
        challenges=EmailChallengeStore(tmp_path / "codes.sqlite"),
        sender=sender,
    )
    return BoundMailRegistration(core, Directory()), sender


def test_challenge_delivered_only_to_server_registered_mailbox(tmp_path):
    bound, sender = service(tmp_path)
    bound.request_challenge(
        actor=AuthenticatedParent("p"), server_client_ip="192.0.2.1", now=NOW
    )
    assert sender.sent[0][0] == "parent@example.test"
    token = sender.sent[0][1]
    assert not bound.verify_challenge(actor=AuthenticatedParent("other"), token=token, now=NOW)
    assert bound.verify_challenge(actor=AuthenticatedParent("p"), token=token, now=NOW)


def test_missing_or_blank_authenticated_parent_cannot_request(tmp_path):
    bound, sender = service(tmp_path)
    for parent_id in ("", "missing"):
        with pytest.raises(ValueError):
            bound.request_challenge(
                actor=AuthenticatedParent(parent_id),
                server_client_ip="192.0.2.1", now=NOW,
            )
    assert sender.sent == []
