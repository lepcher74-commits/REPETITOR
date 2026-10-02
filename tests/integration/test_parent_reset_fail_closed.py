"""Additional fail-closed tests for local password recovery."""
from datetime import datetime, timezone

from repetitor.application.atomic_parent_password_reset import AtomicParentPasswordReset
from repetitor.persistence.parent_credentials import ParentCredentials
from repetitor.persistence.parent_session_store import ParentSessionStore
from repetitor.persistence.password_recovery_store import PasswordRecoveryStore


NOW = datetime(2026, 10, 2, tzinfo=timezone.utc)


def test_missing_credentials_do_not_consume_recovery_token(tmp_path):
    path = tmp_path / "parent.sqlite"
    credentials = ParentCredentials(path)
    recovery = PasswordRecoveryStore(path)
    sessions = ParentSessionStore(path)
    reset = AtomicParentPasswordReset(credentials, recovery, sessions)
    token = recovery.issue(parent_id="parent", now=NOW)
    assert not reset.reset(
        parent_id="parent", token=token,
        new_password="replacement private password", now=NOW,
    )
    credentials.register(parent_id="parent", password="previous private password")
    assert reset.reset(
        parent_id="parent", token=token,
        new_password="replacement private password", now=NOW,
    )
    assert credentials.verify(parent_id="parent", password="replacement private password")


def test_recovery_token_cannot_reset_other_parent(tmp_path):
    path = tmp_path / "parent.sqlite"
    credentials = ParentCredentials(path)
    recovery = PasswordRecoveryStore(path)
    sessions = ParentSessionStore(path)
    reset = AtomicParentPasswordReset(credentials, recovery, sessions)
    credentials.register(parent_id="first", password="first private password")
    credentials.register(parent_id="second", password="second private password")
    other_session = sessions.create(parent_id="second", now=NOW)
    token = recovery.issue(parent_id="first", now=NOW)
    assert not reset.reset(
        parent_id="second", token=token,
        new_password="replacement private password", now=NOW,
    )
    assert credentials.verify(parent_id="second", password="second private password")
    assert sessions.authenticate(token=other_session, now=NOW) is not None
    assert reset.reset(
        parent_id="first", token=token,
        new_password="replacement private password", now=NOW,
    )
