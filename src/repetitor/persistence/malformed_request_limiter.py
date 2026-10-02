"""Per-client malformed recovery request budget; no shared global counter."""
from __future__ import annotations

import hashlib
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

from repetitor.persistence.mail_request_limiter import AbuseLimitExceeded


class MalformedRequestLimiter:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS malformed_request_limits ("
                "client_digest TEXT PRIMARY KEY, window_start TEXT NOT NULL, requests INTEGER NOT NULL)"
            )

    def check_and_record(self, *, client_ip: str, now: datetime) -> None:
        if not client_ip.strip() or now.tzinfo is None:
            raise ValueError("Trusted client IP and aware time required")
        digest = hashlib.sha256(client_ip.encode("utf-8")).hexdigest()
        with sqlite3.connect(self.path, timeout=5) as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT window_start,requests FROM malformed_request_limits WHERE client_digest=?",
                (digest,),
            ).fetchone()
            if row and now < datetime.fromisoformat(row[0]):
                raise AbuseLimitExceeded("Clock moved backwards")
            count = row[1] if row and now - datetime.fromisoformat(row[0]) < timedelta(hours=1) else 0
            if count >= 10:
                raise AbuseLimitExceeded("Malformed request quota exceeded")
            start = row[0] if count else now.isoformat()
            db.execute(
                "INSERT INTO malformed_request_limits VALUES(?,?,?) "
                "ON CONFLICT(client_digest) DO UPDATE SET "
                "window_start=excluded.window_start,requests=excluded.requests",
                (digest, start, count + 1),
            )
