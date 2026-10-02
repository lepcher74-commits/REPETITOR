"""Server-side parent sessions; never expose this store directly to clients.

Opaque tokens are returned only at creation and stored as SHA-256 digests.
Authentication of credentials and guardian authority are separate concerns.
"""
from __future__ import annotations

import hashlib
import hmac
import secrets
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

from repetitor.application.bound_mail_registration import AuthenticatedParent


class ParentSessionStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute("""CREATE TABLE IF NOT EXISTS parent_sessions (
                token_digest TEXT PRIMARY KEY,
                parent_id TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                revoked INTEGER NOT NULL DEFAULT 0
            )""")

    def create(self, *, parent_id: str, now: datetime, ttl_hours: int = 12) -> str:
        if not parent_id.strip() or now.tzinfo is None or not 1 <= ttl_hours <= 24:
            raise ValueError("Invalid session parameters")
        token = secrets.token_urlsafe(32)
        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        with sqlite3.connect(self.path) as db:
            db.execute(
                "INSERT INTO parent_sessions(token_digest,parent_id,expires_at) VALUES(?,?,?)",
                (digest, parent_id, (now + timedelta(hours=ttl_hours)).isoformat()),
            )
        return token

    def authenticate(self, *, token: str, now: datetime) -> AuthenticatedParent | None:
        if now.tzinfo is None:
            raise ValueError("Timezone-aware authentication time required")
        if not token:
            return None
        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        with sqlite3.connect(self.path) as db:
            row = db.execute(
                "SELECT parent_id,expires_at,revoked FROM parent_sessions WHERE token_digest=?",
                (digest,),
            ).fetchone()
        if row is None or row[2] or now >= datetime.fromisoformat(row[1]):
            return None
        return AuthenticatedParent(row[0])

    def revoke(self, *, token: str) -> None:
        if not token:
            return
        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        with sqlite3.connect(self.path) as db:
            db.execute("UPDATE parent_sessions SET revoked=1 WHERE token_digest=?", (digest,))
