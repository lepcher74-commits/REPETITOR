from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
from pathlib import Path

from repetitor.persistence import SQLiteLearningRepository, SQLiteProfileRepository

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/stage8_synthetic_operator_rehearsal.py"
CANDIDATE = "983d04c564879f9ff8b6de110497901279073aeb"


def make_db(path: Path) -> None:
    SQLiteLearningRepository(path).initialize()
    SQLiteProfileRepository(path).initialize()
    with sqlite3.connect(path) as connection:
        connection.execute("CREATE TABLE rehearsal_probe (value TEXT NOT NULL)")
        connection.execute("INSERT INTO rehearsal_probe VALUES ('synthetic')")


def test_stage8_rehearsal_helper_backup_restore_and_delete(tmp_path: Path) -> None:
    data_dir = tmp_path / "synthetic-data"
    data_dir.mkdir()
    make_db(data_dir / "repetitor.sqlite3")
    evidence = tmp_path / "evidence.json"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--data-dir",
            str(data_dir),
            "--expected-build-sha",
            CANDIDATE,
            "--observed-build-sha",
            CANDIDATE,
            "--evidence-json",
            str(evidence),
            "--delete-synthetic-data",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    record = json.loads(evidence.read_text(encoding="utf-8"))
    assert record["backup_restore_verified"] is True
    assert record["delete_verified"] is True
    assert record["expected_build_sha"] == CANDIDATE
    assert record["observed_build_sha"] == CANDIDATE
    assert record["synthetic_only"] is True
    assert not data_dir.exists()


def test_stage8_rehearsal_helper_fails_closed_on_build_sha_mismatch(tmp_path: Path) -> None:
    data_dir = tmp_path / "synthetic-data"
    data_dir.mkdir()
    make_db(data_dir / "repetitor.sqlite3")
    evidence = tmp_path / "evidence.json"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--data-dir",
            str(data_dir),
            "--expected-build-sha",
            CANDIDATE,
            "--observed-build-sha",
            "deadbeef",
            "--evidence-json",
            str(evidence),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 2
    assert "Build SHA mismatch" in result.stderr
    assert not evidence.exists()
    assert data_dir.exists()
