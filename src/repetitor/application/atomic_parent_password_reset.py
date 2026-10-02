"""Local atomic parent password reset; all stores MUST share one SQLite file."""
from __future__ import annotations

import hashlib
import secrets
import sqlite3
from datetime import datetime, timezone

from repetitor.persistence.parent_credentials import ParentCredentials
from repetitor.persistence.parent_session_store import ParentSessionStore
from repetitor.persistence.password_recovery_store import PasswordRecoveryStore


class AtomicParentPasswordReset:
    def __init__(
        self, credentials: ParentCredentials,
        recovery: PasswordRecoveryStore,
        sessions: ParentSessionStore,
    ):
        paths = {credentials.path.resolve(), recovery.path.resolve(), sessions.path.resolve()}
        if len(paths) != 1:
            raise ValueError("Atomic reset requires all stores in one SQLite database")
        self.path = credentials.path

    def reset(
        self, *, parent_id: str, token: str, new_password: str, now: datetime,
    ) -> bool:
        if now.tzinfo is None:
            raise ValueError("Timezone-aware time required")
        if not parent_id.strip() or not token:
            return False
        if not 12 <= len(new_password) <= 1024:
            raise ValueError("Password length must be between 12 and 1024")
        salt = secrets.token_bytes(16)
        password_digest = ParentCredentials._derive(new_password, salt)
        token_digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        with sqlite3.connect(self.path, timeout=10) as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT expires_at,consumed FROM password_recovery WHERE parent_id=? AND token_digest=?",
                (parent_id, token_digest),
            ).fetchone()
            if row is None or row[1] or datetime.fromisoformat(row[0]) <= now.astimezone(timezone.utc):
                return False
            updated = db.execute(
                "UPDATE parent_credentials SET salt=?,password_digest=? WHERE parent_id=?",
                (salt, password_digest, parent_id),
            ).rowcount
            if updated != 1:
                return False
            db.execute(
                "UPDATE password_recovery SET consumed=1 WHERE parent_id=? AND token_digest=?",
                (parent_id, token_digest),
            )
            db.execute(
                "UPDATE parent_sessions SET revoked=1 WHERE parent_id=?",
                (parent_id,),
            )
            db.commit()
            return True
