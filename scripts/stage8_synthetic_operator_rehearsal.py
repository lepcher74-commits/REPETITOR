#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_TABLES = frozenset({
    "attempts", "knowledge_states", "session_state", "review_queue", "students",
})


class DrillError(RuntimeError):
    pass


def db_health(path: Path) -> dict:
    if not path.is_file():
        raise DrillError(f"Database does not exist: {path}")
    try:
        with sqlite3.connect(path) as connection:
            integrity = connection.execute("PRAGMA integrity_check").fetchone()
            tables = {
                str(row[0])
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ).fetchall()
            }
    except sqlite3.DatabaseError as exc:
        raise DrillError(f"Unreadable SQLite database: {path}") from exc
    if integrity is None or integrity[0] != "ok":
        raise DrillError(f"Integrity check failed: {path}")
    missing = REQUIRED_TABLES - tables
    if missing:
        raise DrillError(
            "Not a REPETITOR learner database; missing: "
            + ", ".join(sorted(missing))
        )
    return {"integrity": "ok", "required_tables_present": True}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sqlite_backup(source: Path, destination: Path) -> None:
    if destination.exists():
        raise DrillError(f"Backup destination already exists: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(source) as source_db, sqlite3.connect(destination) as backup_db:
        source_db.backup(backup_db)
    db_health(destination)


def sqlite_restore(backup: Path, destination: Path) -> None:
    if destination.exists():
        raise DrillError(f"Restore destination already exists: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp = destination.with_name(destination.name + ".restore.tmp")
    temp.unlink(missing_ok=True)
    with sqlite3.connect(backup) as backup_db, sqlite3.connect(temp) as restored_db:
        backup_db.backup(restored_db)
    db_health(temp)
    temp.replace(destination)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Stage 8 synthetic operator rehearsal helper. Use only after the exact "
            "packaged REPETITOR build has created a synthetic data directory."
        )
    )
    parser.add_argument("--data-dir", required=True, type=Path)
    parser.add_argument("--expected-build-sha", required=True)
    parser.add_argument("--observed-build-sha", required=True)
    parser.add_argument("--evidence-json", required=True, type=Path)
    parser.add_argument(
        "--delete-synthetic-data",
        action="store_true",
        help="After successful backup/restore verification, delete synthetic source/backup/restore data.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.expected_build_sha != args.observed_build_sha:
        raise DrillError(
            f"Build SHA mismatch: expected {args.expected_build_sha}, observed {args.observed_build_sha}"
        )

    data_dir = args.data_dir.resolve()
    live_db = data_dir / "repetitor.sqlite3"
    backup_dir = data_dir.parent / (data_dir.name + "-stage8-backup")
    restore_dir = data_dir.parent / (data_dir.name + "-stage8-restore")
    backup_db = backup_dir / "repetitor.sqlite3"
    restored_db = restore_dir / "repetitor.sqlite3"

    source_health = db_health(live_db)
    source_hash = sha256(live_db)

    if backup_dir.exists() or restore_dir.exists():
        raise DrillError(
            "Backup/restore rehearsal directories already exist; remove or rename them first"
        )

    sqlite_backup(live_db, backup_db)
    backup_health = db_health(backup_db)
    backup_hash = sha256(backup_db)

    sqlite_restore(backup_db, restored_db)
    restored_health = db_health(restored_db)
    restored_hash = sha256(restored_db)

    result = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "expected_build_sha": args.expected_build_sha,
        "observed_build_sha": args.observed_build_sha,
        "synthetic_only": True,
        "source_database": str(live_db),
        "backup_database": str(backup_db),
        "restored_database": str(restored_db),
        "source_health": source_health,
        "backup_health": backup_health,
        "restored_health": restored_health,
        "source_sha256": source_hash,
        "backup_sha256": backup_hash,
        "restored_sha256": restored_hash,
        "backup_restore_verified": True,
        "delete_requested": bool(args.delete_synthetic_data),
        "delete_verified": False,
    }

    if args.delete_synthetic_data:
        shutil.rmtree(data_dir)
        shutil.rmtree(backup_dir)
        shutil.rmtree(restore_dir)
        result["delete_verified"] = not any(
            p.exists() for p in (data_dir, backup_dir, restore_dir)
        )

    args.evidence_json.parent.mkdir(parents=True, exist_ok=True)
    args.evidence_json.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except DrillError as exc:
        print(f"DRILL BLOCKED: {exc}", file=sys.stderr)
        raise SystemExit(2)
