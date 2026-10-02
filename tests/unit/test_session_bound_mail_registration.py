from datetime import datetime, timezone

import pytest

from repetitor.application.bound_mail_registration import BoundMailRegistration
from repetitor.application.mail_registration import MailRegistration
from repetitor.application.session_bound_mail_registration import SessionBoundMailRegistration
from repetitor.persistence.email_challenge_store import EmailChallengeStore
from repetitor.persistence.mail_request_limiter import MailRequestLimiter
from repetitor.persistence.parent_session_store import ParentSessionStore


NOW = datetime(2026, 10, 2, tzinfo=timezone.utc)


class Directory:
    def registered_mailbox(self, parent_id):
        return {"p": "p@example.test"}.get(parent_id)


class Sender:
    def __init__(self):
        self.sent = []

    def send_challenge(self, *, recipient, token):
        self.sent.append((recipient, token))


def test_session_is_required_for_mail_request_and_verification(tmp_path):
    sessions = ParentSessionStore(tmp_path / "sessions.sqlite")
    sender = Sender()
    mail = BoundMailRegistration(
        MailRegistration(
            limiter=MailRequestLimiter(tmp_path / "limits.sqlite"),
            challenges=EmailChallengeStore(tmp_path / "challenges.sqlite"),
            sender=sender,
        ),
        Directory(),
    )
    flow = SessionBoundMailRegistration(sessions=sessions, mail=mail)
    with pytest.raises(PermissionError):
        flow.request_challenge(session_token="invalid", server_client_ip="192.0.2.1", now=NOW)
    assert sender.sent == []
    token = sessions.create(parent_id="p", now=NOW)
    flow.request_challenge(session_token=token, server_client_ip="192.0.2.1", now=NOW)
    challenge = sender.sent[0][1]
    sessions.revoke(token=token)
    assert not flow.verify_challenge(session_token=token, challenge_token=challenge, now=NOW)
    new_token = sessions.create(parent_id="p", now=NOW)
    assert flow.verify_challenge(session_token=new_token, challenge_token=challenge, now=NOW)
