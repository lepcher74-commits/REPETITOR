"""Offline integration tests for the entire parent recovery path."""
from datetime import datetime, timedelta, timezone

from repetitor.application.atomic_parent_password_reset import AtomicParentPasswordReset
from repetitor.application.parent_recovery_request import ParentRecoveryRequest
from repetitor.persistence.mail_request_limiter import MailRequestLimiter
from repetitor.persistence.parent_credentials import ParentCredentials
from repetitor.persistence.parent_session_store import ParentSessionStore
from repetitor.persistence.password_recovery_store import PasswordRecoveryStore


NOW = datetime(2026, 10, 2, tzinfo=timezone.utc)


class Directory:
    def find_parent(self, *, normalized_email):
        return "parent" if normalized_email == "parent@example.test" else None


class Sender:
    def __init__(self):
        self.deliveries = []

    def send_challenge(self, *, recipient, token):
        self.deliveries.append((recipient, token))


def test_full_recovery_flow_and_session_isolation(tmp_path):
    shared = tmp_path / "parent.sqlite"
    credentials = ParentCredentials(shared)
    recovery = PasswordRecoveryStore(shared)
    sessions = ParentSessionStore(shared)
    credentials.register(parent_id="parent", password="previous private password")
    credentials.register(parent_id="other", password="another private password")
    previous = sessions.create(parent_id="parent", now=NOW)
    other = sessions.create(parent_id="other", now=NOW)
    sender = Sender()
    requests = ParentRecoveryRequest(
        directory=Directory(), limiter=MailRequestLimiter(tmp_path / "limits.sqlite"),
        recovery=recovery, sender=sender,
    )
    reset = AtomicParentPasswordReset(credentials, recovery, sessions)
    assert requests.request(
        email="parent@example.test", server_client_ip="192.0.2.1", now=NOW,
    ) is None
    assert sender.deliveries[0][0] == "parent@example.test"
    token = sender.deliveries[0][1]
    assert reset.reset(
        parent_id="parent", token=token,
        new_password="replacement private password", now=NOW,
    )
    assert credentials.verify(parent_id="parent", password="replacement private password")
    assert not credentials.verify(parent_id="parent", password="previous private password")
    assert sessions.authenticate(token=previous, now=NOW) is None
    assert sessions.authenticate(token=other, now=NOW) is not None
    assert not reset.reset(
        parent_id="parent", token=token, new_password="third private password", now=NOW,
    )


def test_unknown_email_and_expired_delivery_do_not_change_credentials(tmp_path):
    shared = tmp_path / "parent.sqlite"
    credentials = ParentCredentials(shared)
    recovery = PasswordRecoveryStore(shared)
    sessions = ParentSessionStore(shared)
    credentials.register(parent_id="parent", password="previous private password")
    session = sessions.create(parent_id="parent", now=NOW)
    sender = Sender()
    requests = ParentRecoveryRequest(
        directory=Directory(), limiter=MailRequestLimiter(tmp_path / "limits.sqlite"),
        recovery=recovery, sender=sender,
    )
    reset = AtomicParentPasswordReset(credentials, recovery, sessions)
    assert requests.request(
        email="unknown@example.test", server_client_ip="192.0.2.1", now=NOW,
    ) is None
    assert not sender.deliveries
    requests.request(email="parent@example.test", server_client_ip="192.0.2.1", now=NOW)
    token = sender.deliveries[0][1]
    assert not reset.reset(
        parent_id="parent", token=token, new_password="replacement private password",
        now=NOW + timedelta(minutes=15),
    )
    assert credentials.verify(parent_id="parent", password="previous private password")
    assert sessions.authenticate(token=session, now=NOW) is not None
