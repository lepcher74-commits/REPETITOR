import sqlite3

import pytest

from repetitor.persistence.backup import (
    BackupError,
    RestoreConflictError,
    create_backup,
    restore_backup,
)


def make_db(path, value="original"):
    with sqlite3.connect(path) as connection:
        connection.execute("CREATE TABLE sample (value TEXT NOT NULL)")
        connection.execute("INSERT INTO sample VALUES (?)", (value,))


def read_value(path):
    with sqlite3.connect(path) as connection:
        return connection.execute("SELECT value FROM sample").fetchone()[0]


def test_backup_and_restore_round_trip(tmp_path):
    source = tmp_path / "live.sqlite3"
    backup = tmp_path / "backup.sqlite3"
    restored = tmp_path / "restored.sqlite3"
    make_db(source)

    create_backup(source, backup)
    restore_backup(backup, restored)

    assert read_value(restored) == "original"


def test_restore_refuses_to_overwrite_existing_database(tmp_path):
    backup = tmp_path / "backup.sqlite3"
    destination = tmp_path / "live.sqlite3"
    make_db(backup, "old")
    make_db(destination, "new")

    with pytest.raises(RestoreConflictError):
        restore_backup(backup, destination)

    assert read_value(destination) == "new"


def test_corrupt_backup_is_rejected_without_touching_destination(tmp_path):
    backup = tmp_path / "broken.sqlite3"
    destination = tmp_path / "live.sqlite3"
    backup.write_bytes(b"not a sqlite database")
    make_db(destination, "safe")

    with pytest.raises(BackupError):
        restore_backup(backup, destination, allow_overwrite=True)

    assert read_value(destination) == "safe"


def test_backup_refuses_existing_destination(tmp_path):
    source = tmp_path / "live.sqlite3"
    backup = tmp_path / "backup.sqlite3"
    make_db(source)
    make_db(backup, "keep")

    with pytest.raises(RestoreConflictError):
        create_backup(source, backup)

    assert read_value(backup) == "keep"
