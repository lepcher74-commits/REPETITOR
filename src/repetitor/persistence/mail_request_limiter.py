"""Persistent shared abuse limits for a future authenticated mail API.

This is a reusable server-side primitive, not a public HTTP endpoint.
Never use untrusted forwarded IP headers without a configured trusted proxy.
"""
from __future__ import annotations

import hashlib
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path


class AbuseLimitExceeded(RuntimeError):
    pass


class MailRequestLimiter:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute("""CREATE TABLE IF NOT EXISTS mail_request_limits (
                scope TEXT NOT NULL, key_digest TEXT NOT NULL,
                window_start TEXT NOT NULL, requests INTEGER NOT NULL,
                PRIMARY KEY(scope,key_digest)
            )""")

    def check_and_record(self, *, parent_id: str, client_ip: str, now: datetime) -> None:
        if not parent_id.strip() or not client_ip.strip() or now.tzinfo is None:
            raise ValueError("Verified parent identifier, server-derived IP and aware time required")
        # Fixed windows; per-account AND per-IP must both have capacity.
        limits = (("account", parent_id, 3), ("ip", client_ip, 10))
        with sqlite3.connect(self.path, timeout=5) as db:
            db.execute("BEGIN IMMEDIATE")
            updates = []
            for scope, value, maximum in limits:
                digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
                row = db.execute(
                    "SELECT window_start,requests FROM mail_request_limits WHERE scope=? AND key_digest=?",
                    (scope, digest),
                ).fetchone()
                if row and now < datetime.fromisoformat(row[0]):
                    raise AbuseLimitExceeded("Clock moved backwards; retry later")
                count = row[1] if row and now - datetime.fromisoformat(row[0]) < timedelta(hours=1) else 0
                if count >= maximum:
                    raise AbuseLimitExceeded("Mail request limit exceeded")
                start = row[0] if count else now.isoformat()
                updates.append((scope, digest, start, count + 1))
            for scope, digest, start, count in updates:
                db.execute(
                    """INSERT INTO mail_request_limits(scope,key_digest,window_start,requests)
                       VALUES(?,?,?,?) ON CONFLICT(scope,key_digest) DO UPDATE SET
                       window_start=excluded.window_start,requests=excluded.requests""",
                    (scope, digest, start, count),
                )
