import sqlite3

import pytest

from repetitor.persistence.parent_credentials import ParentCredentials


def test_register_verify_and_restart_without_plaintext(tmp_path):
    path = tmp_path / "credentials.sqlite"
    credentials = ParentCredentials(path)
    credentials.register(parent_id="p", password="long private passphrase")
    with sqlite3.connect(path) as db:
        row = db.execute("SELECT salt,password_digest FROM parent_credentials").fetchone()
    assert b"long private passphrase" not in row
    assert ParentCredentials(path).verify(parent_id="p", password="long private passphrase")
    assert not ParentCredentials(path).verify(parent_id="p", password="wrong password")


def test_unknown_account_and_duplicate_registration(tmp_path):
    credentials = ParentCredentials(tmp_path / "credentials.sqlite")
    assert not credentials.verify(parent_id="missing", password="long private passphrase")
    credentials.register(parent_id="p", password="long private passphrase")
    with pytest.raises(sqlite3.IntegrityError):
        credentials.register(parent_id="p", password="another private passphrase")


def test_rejects_weak_or_oversized_password(tmp_path):
    credentials = ParentCredentials(tmp_path / "credentials.sqlite")
    with pytest.raises(ValueError):
        credentials.register(parent_id="p", password="short")
    with pytest.raises(ValueError):
        credentials.register(parent_id="p", password="x" * 1025)
