"""Local append-only consent event store. Not proof of representative identity."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from uuid import uuid4

from repetitor.application.parent_consent import ConsentPurpose


class ConsentLedger:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute("""CREATE TABLE IF NOT EXISTS consent_events (
                event_id TEXT PRIMARY KEY,
                parent_id TEXT NOT NULL,
                purpose TEXT NOT NULL,
                event_type TEXT NOT NULL CHECK(event_type IN ('grant','withdraw')),
                notice_version TEXT NOT NULL,
                occurred_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
            )""")

    def append(self, parent_id: str, purpose: ConsentPurpose, event_type: str, notice_version: str) -> str:
        if not parent_id.strip() or not notice_version.strip() or event_type not in {"grant", "withdraw"}:
            raise ValueError("Invalid consent event")
        event_id = str(uuid4())
        with sqlite3.connect(self.path) as db:
            db.execute(
                "INSERT INTO consent_events(event_id,parent_id,purpose,event_type,notice_version) VALUES(?,?,?,?,?)",
                (event_id, parent_id, purpose.value, event_type, notice_version),
            )
        return event_id

    def active(self, parent_id: str, purpose: ConsentPurpose) -> bool:
        with sqlite3.connect(self.path) as db:
            row = db.execute(
                """SELECT event_type FROM consent_events WHERE parent_id=? AND purpose=?
                   ORDER BY occurred_at DESC, rowid DESC LIMIT 1""",
                (parent_id, purpose.value),
            ).fetchone()
        return row is not None and row[0] == "grant"
