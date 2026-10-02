"""One-use password recovery tokens; delivery and identity checks are external."""
from __future__ import annotations

import hashlib
import secrets
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path


class PasswordRecoveryStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute("""CREATE TABLE IF NOT EXISTS password_recovery (
                parent_id TEXT PRIMARY KEY, token_digest TEXT NOT NULL,
                expires_at TEXT NOT NULL, consumed INTEGER NOT NULL DEFAULT 0
            )""")

    def issue(self, *, parent_id: str, now: datetime) -> str:
        if not parent_id.strip() or now.tzinfo is None:
            raise ValueError("Valid parent and aware time required")
        token = secrets.token_urlsafe(32)
        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        with sqlite3.connect(self.path, timeout=5) as db:
            db.execute("BEGIN IMMEDIATE")
            db.execute(
                """INSERT INTO password_recovery(parent_id,token_digest,expires_at,consumed)
                   VALUES(?,?,?,0) ON CONFLICT(parent_id) DO UPDATE SET
                   token_digest=excluded.token_digest,expires_at=excluded.expires_at,
                   consumed=0""",
                (parent_id, digest, (now + timedelta(minutes=15)).isoformat()),
            )
        return token

    def consume(self, *, parent_id: str, token: str, now: datetime) -> bool:
        if now.tzinfo is None:
            raise ValueError("Aware time required")
        if not parent_id.strip() or not token:
            return False
        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        with sqlite3.connect(self.path, timeout=5) as db:
            db.execute("BEGIN IMMEDIATE")
            changed = db.execute(
                """UPDATE password_recovery SET consumed=1
                   WHERE parent_id=? AND token_digest=? AND consumed=0 AND expires_at>?""",
                (parent_id, digest, now.isoformat()),
            ).rowcount
            return changed == 1
