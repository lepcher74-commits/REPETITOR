from datetime import datetime, timedelta, timezone

import pytest

from repetitor.persistence.password_recovery_store import PasswordRecoveryStore


NOW = datetime(2026, 10, 2, tzinfo=timezone.utc)


def test_recovery_token_is_single_use_across_restarts(tmp_path):
    path = tmp_path / "recovery.sqlite"
    token = PasswordRecoveryStore(path).issue(parent_id="p", now=NOW)
    import sqlite3
    with sqlite3.connect(path) as db:
        assert token not in repr(db.execute("SELECT * FROM password_recovery").fetchall())
    restarted = PasswordRecoveryStore(path)
    assert not restarted.consume(parent_id="other", token=token, now=NOW)
    assert restarted.consume(parent_id="p", token=token, now=NOW)
    assert not restarted.consume(parent_id="p", token=token, now=NOW)


def test_recovery_token_expiry_and_reissue(tmp_path):
    store = PasswordRecoveryStore(tmp_path / "recovery.sqlite")
    old = store.issue(parent_id="p", now=NOW)
    assert not store.consume(parent_id="p", token=old, now=NOW + timedelta(minutes=15))
    new = store.issue(parent_id="p", now=NOW + timedelta(minutes=16))
    assert not store.consume(parent_id="p", token=old, now=NOW + timedelta(minutes=16))
    assert store.consume(parent_id="p", token=new, now=NOW + timedelta(minutes=16))


def test_recovery_token_requires_valid_identity_and_time(tmp_path):
    store = PasswordRecoveryStore(tmp_path / "recovery.sqlite")
    with pytest.raises(ValueError):
        store.issue(parent_id=" ", now=NOW)
    with pytest.raises(ValueError):
        store.issue(parent_id="p", now=NOW.replace(tzinfo=None))
