from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path


class BackupError(RuntimeError):
    pass


class RestoreConflictError(BackupError):
    pass


def _require_healthy_database(path: Path) -> None:
    if not path.is_file():
        raise BackupError(f"Database does not exist: {path}")
    try:
        with closing(sqlite3.connect(path)) as connection:
            row = connection.execute("PRAGMA integrity_check").fetchone()
    except sqlite3.DatabaseError as exc:
        raise BackupError("Database is unreadable or corrupt") from exc
    if row is None or row[0] != "ok":
        raise BackupError("Database integrity check failed")


def create_backup(source: str | Path, destination: str | Path) -> Path:
    source_path = Path(source)
    destination_path = Path(destination)
    _require_healthy_database(source_path)
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    if destination_path.exists():
        raise RestoreConflictError(f"Backup destination already exists: {destination_path}")
    try:
        with closing(sqlite3.connect(source_path)) as source_db, closing(sqlite3.connect(destination_path)) as backup_db:
            source_db.backup(backup_db)
        _require_healthy_database(destination_path)
    except Exception:
        destination_path.unlink(missing_ok=True)
        raise
    return destination_path


def restore_backup(
    backup: str | Path,
    destination: str | Path,
    *,
    allow_overwrite: bool = False,
) -> Path:
    backup_path = Path(backup)
    destination_path = Path(destination)
    _require_healthy_database(backup_path)
    if destination_path.exists() and not allow_overwrite:
        raise RestoreConflictError(
            "Refusing to overwrite an existing learner database; preserve or rename it first"
        )
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = destination_path.with_name(destination_path.name + ".restore.tmp")
    temporary_path.unlink(missing_ok=True)
    try:
        with closing(sqlite3.connect(backup_path)) as backup_db, closing(sqlite3.connect(temporary_path)) as restored_db:
            backup_db.backup(restored_db)
        _require_healthy_database(temporary_path)
        temporary_path.replace(destination_path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise
    return destination_path
