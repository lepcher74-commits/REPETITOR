from datetime import datetime, timedelta, timezone

import pytest

from repetitor.application.atomic_parent_password_reset import AtomicParentPasswordReset
from repetitor.persistence.parent_credentials import ParentCredentials
from repetitor.persistence.parent_session_store import ParentSessionStore
from repetitor.persistence.password_recovery_store import PasswordRecoveryStore


NOW = datetime(2026, 10, 2, tzinfo=timezone.utc)


def setup(tmp_path):
    path = tmp_path / "parent.sqlite"
    credentials = ParentCredentials(path)
    recovery = PasswordRecoveryStore(path)
    sessions = ParentSessionStore(path)
    credentials.register(parent_id="p", password="previous private password")
    old_session = sessions.create(parent_id="p", now=NOW)
    other_session = sessions.create(parent_id="other", now=NOW)
    return AtomicParentPasswordReset(credentials, recovery, sessions), credentials, recovery, sessions, old_session, other_session


def test_reset_updates_password_consumes_token_and_revokes_only_parent_sessions(tmp_path):
    reset, credentials, recovery, sessions, old, other = setup(tmp_path)
    token = recovery.issue(parent_id="p", now=NOW)
    assert reset.reset(parent_id="p", token=token, new_password="replacement private password", now=NOW)
    assert credentials.verify(parent_id="p", password="replacement private password")
    assert not credentials.verify(parent_id="p", password="previous private password")
    assert sessions.authenticate(token=old, now=NOW) is None
    assert sessions.authenticate(token=other, now=NOW) is not None
    assert not reset.reset(parent_id="p", token=token, new_password="third private password", now=NOW)


def test_expired_or_wrong_token_changes_nothing(tmp_path):
    reset, credentials, recovery, sessions, old, _ = setup(tmp_path)
    token = recovery.issue(parent_id="p", now=NOW)
    assert not reset.reset(parent_id="p", token="wrong", new_password="replacement private password", now=NOW)
    assert not reset.reset(
        parent_id="p", token=token, new_password="replacement private password",
        now=NOW + timedelta(minutes=15),
    )
    assert credentials.verify(parent_id="p", password="previous private password")
    assert sessions.authenticate(token=old, now=NOW) is not None


def test_rejects_separate_databases(tmp_path):
    credentials = ParentCredentials(tmp_path / "credentials.sqlite")
    recovery = PasswordRecoveryStore(tmp_path / "recovery.sqlite")
    sessions = ParentSessionStore(tmp_path / "sessions.sqlite")
    with pytest.raises(ValueError):
        AtomicParentPasswordReset(credentials, recovery, sessions)
