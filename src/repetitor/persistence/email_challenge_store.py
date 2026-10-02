"""SQLite-backed one-time mailbox challenges; caller must apply account/IP rate limits."""
from __future__ import annotations

import hashlib
import hmac
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from repetitor.application.email_challenge import issue_email_challenge


class EmailChallengeStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute("""CREATE TABLE IF NOT EXISTS email_challenges (
                parent_id TEXT PRIMARY KEY, digest TEXT NOT NULL,
                expires_at TEXT NOT NULL, attempts INTEGER NOT NULL,
                consumed INTEGER NOT NULL DEFAULT 0
            )""")

    def issue(self, parent_id: str, now: datetime) -> str:
        challenge, token = issue_email_challenge(parent_id, now)
        with sqlite3.connect(self.path) as db:
            db.execute(
                """INSERT INTO email_challenges(parent_id,digest,expires_at,attempts,consumed)
                   VALUES(?,?,?,?,0) ON CONFLICT(parent_id) DO UPDATE SET
                   digest=excluded.digest,expires_at=excluded.expires_at,
                   attempts=excluded.attempts,consumed=0""",
                (parent_id, challenge.token_digest, challenge.expires_at.isoformat(), 5),
            )
        return token

    def verify(self, parent_id: str, token: str, now: datetime) -> bool:
        if now.tzinfo is None:
            raise ValueError("Timezone-aware verification time required")
        # BEGIN IMMEDIATE serializes read/consume to prevent concurrent replay.
        with sqlite3.connect(self.path, timeout=5) as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT digest,expires_at,attempts,consumed FROM email_challenges WHERE parent_id=?",
                (parent_id,),
            ).fetchone()
            if row is None or row[3] or row[2] <= 0 or now >= datetime.fromisoformat(row[1]):
                return False
            valid = hmac.compare_digest(
                hashlib.sha256(token.encode("utf-8")).hexdigest(), row[0]
            )
            db.execute(
                "UPDATE email_challenges SET attempts=attempts-1, consumed=? WHERE parent_id=?",
                (int(valid), parent_id),
            )
            return valid
