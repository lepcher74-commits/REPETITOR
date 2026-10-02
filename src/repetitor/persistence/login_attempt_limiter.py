"""Persistent, atomic password-login attempt limits for an authenticated server edge."""
from __future__ import annotations

import hashlib
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path


class LoginRateLimited(RuntimeError):
    pass


class LoginAttemptLimiter:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute("""CREATE TABLE IF NOT EXISTS login_attempts (
                scope TEXT NOT NULL, key_digest TEXT NOT NULL,
                window_start TEXT NOT NULL, failures INTEGER NOT NULL,
                PRIMARY KEY(scope,key_digest)
            )""")

    @staticmethod
    def _keys(parent_id: str, client_ip: str):
        return (
            ("account", hashlib.sha256(parent_id.encode("utf-8")).hexdigest(), 5),
            ("ip", hashlib.sha256(client_ip.encode("utf-8")).hexdigest(), 20),
        )

    def check(self, *, parent_id: str, client_ip: str, now: datetime) -> None:
        if not parent_id.strip() or not client_ip.strip() or now.tzinfo is None:
            raise ValueError("Server-resolved identity, IP and aware time required")
        with sqlite3.connect(self.path, timeout=5) as db:
            db.execute("BEGIN IMMEDIATE")
            for scope, digest, limit in self._keys(parent_id, client_ip):
                row = db.execute(
                    "SELECT window_start,failures FROM login_attempts WHERE scope=? AND key_digest=?",
                    (scope, digest),
                ).fetchone()
                if row:
                    start = datetime.fromisoformat(row[0])
                    if now < start or (now - start < timedelta(minutes=15) and row[1] >= limit):
                        raise LoginRateLimited("Login temporarily unavailable")

    def record_failure(self, *, parent_id: str, client_ip: str, now: datetime) -> None:
        if not parent_id.strip() or not client_ip.strip() or now.tzinfo is None:
            raise ValueError("Server-resolved identity, IP and aware time required")
        with sqlite3.connect(self.path, timeout=5) as db:
            db.execute("BEGIN IMMEDIATE")
            # Validate both scopes before changing either one.
            for scope, digest, limit in self._keys(parent_id, client_ip):
                row = db.execute(
                    "SELECT window_start,failures FROM login_attempts WHERE scope=? AND key_digest=?",
                    (scope, digest),
                ).fetchone()
                if row:
                    start = datetime.fromisoformat(row[0])
                    if now < start or (now - start < timedelta(minutes=15) and row[1] >= limit):
                        raise LoginRateLimited("Login temporarily unavailable")
            for scope, digest, _ in self._keys(parent_id, client_ip):
                row = db.execute(
                    "SELECT window_start,failures FROM login_attempts WHERE scope=? AND key_digest=?",
                    (scope, digest),
                ).fetchone()
                if row and now - datetime.fromisoformat(row[0]) < timedelta(minutes=15):
                    start, failures = row[0], row[1] + 1
                else:
                    start, failures = now.isoformat(), 1
                db.execute(
                    """INSERT INTO login_attempts(scope,key_digest,window_start,failures)
                       VALUES(?,?,?,?) ON CONFLICT(scope,key_digest) DO UPDATE SET
                       window_start=excluded.window_start,failures=excluded.failures""",
                    (scope, digest, start, failures),
                )
