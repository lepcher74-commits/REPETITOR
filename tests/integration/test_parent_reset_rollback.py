import sqlite3
from datetime import datetime, timezone

import pytest

from repetitor.application.atomic_parent_password_reset import AtomicParentPasswordReset
from repetitor.persistence.parent_credentials import ParentCredentials
from repetitor.persistence.parent_session_store import ParentSessionStore
from repetitor.persistence.password_recovery_store import PasswordRecoveryStore


def test_reset_rolls_back_if_session_revoke_fails(tmp_path):
    path = tmp_path / "parent.sqlite"
    credentials = ParentCredentials(path)
    recovery = PasswordRecoveryStore(path)
    sessions = ParentSessionStore(path)
    now = datetime(2026, 10, 2, tzinfo=timezone.utc)
    credentials.register(parent_id="parent", password="previous private password")
    old_session = sessions.create(parent_id="parent", now=now)
    token = recovery.issue(parent_id="parent", now=now)
    with sqlite3.connect(path) as db:
        db.execute(
            "CREATE TRIGGER block_revoke BEFORE UPDATE ON parent_sessions "
            "BEGIN SELECT RAISE(ABORT, 'test failure'); END"
        )
    reset = AtomicParentPasswordReset(credentials, recovery, sessions)
    with pytest.raises(sqlite3.IntegrityError):
        reset.reset(
            parent_id="parent", token=token,
            new_password="replacement private password", now=now,
        )
    assert credentials.verify(parent_id="parent", password="previous private password")
    assert sessions.authenticate(token=old_session, now=now) is not None
    with sqlite3.connect(path) as db:
        db.execute("DROP TRIGGER block_revoke")
    assert reset.reset(
        parent_id="parent", token=token,
        new_password="replacement private password", now=now,
    )
    assert sessions.authenticate(token=old_session, now=now) is None
