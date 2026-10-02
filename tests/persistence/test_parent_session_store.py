from datetime import datetime, timedelta, timezone

import pytest

from repetitor.persistence.parent_session_store import ParentSessionStore


NOW = datetime(2026, 10, 2, tzinfo=timezone.utc)


def test_session_survives_restart_and_is_not_stored_in_plaintext(tmp_path):
    path = tmp_path / "sessions.sqlite"
    token = ParentSessionStore(path).create(parent_id="parent", now=NOW)
    import sqlite3
    with sqlite3.connect(path) as db:
        assert token not in repr(db.execute("SELECT * FROM parent_sessions").fetchall())
    assert ParentSessionStore(path).authenticate(token=token, now=NOW).parent_id == "parent"
    assert ParentSessionStore(path).authenticate(token="wrong", now=NOW) is None


def test_session_expiry_and_revocation(tmp_path):
    store = ParentSessionStore(tmp_path / "sessions.sqlite")
    expired = store.create(parent_id="p", now=NOW, ttl_hours=1)
    assert store.authenticate(token=expired, now=NOW + timedelta(hours=1)) is None
    active = store.create(parent_id="p", now=NOW)
    assert store.authenticate(token=active, now=NOW) is not None
    store.revoke(token=active)
    assert store.authenticate(token=active, now=NOW) is None


def test_invalid_session_creation_rejected(tmp_path):
    store = ParentSessionStore(tmp_path / "sessions.sqlite")
    with pytest.raises(ValueError):
        store.create(parent_id="", now=NOW)
    with pytest.raises(ValueError):
        store.create(parent_id="p", now=NOW.replace(tzinfo=None))
    with pytest.raises(ValueError):
        store.create(parent_id="p", now=NOW, ttl_hours=25)


def test_revoke_all_only_affects_target_parent(tmp_path):
    store = ParentSessionStore(tmp_path / "sessions.sqlite")
    first = store.create(parent_id="p", now=NOW)
    second = store.create(parent_id="p", now=NOW)
    other = store.create(parent_id="other", now=NOW)
    assert store.revoke_all(parent_id="p") == 2
    assert store.authenticate(token=first, now=NOW) is None
    assert store.authenticate(token=second, now=NOW) is None
    assert store.authenticate(token=other, now=NOW) is not None
    assert store.revoke_all(parent_id="p") == 0
