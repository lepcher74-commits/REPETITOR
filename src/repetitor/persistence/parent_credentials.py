"""Offline parent password verifier. No public registration/login endpoint.

Server must add per-account/IP login throttling, recovery and secure transport.
"""
from __future__ import annotations

import hashlib
import hmac
import secrets
import sqlite3
from pathlib import Path


class ParentCredentials:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute("""CREATE TABLE IF NOT EXISTS parent_credentials (
                parent_id TEXT PRIMARY KEY,
                salt BLOB NOT NULL,
                password_digest BLOB NOT NULL
            )""")

    @staticmethod
    def _derive(password: str, salt: bytes) -> bytes:
        return hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=32)

    def register(self, *, parent_id: str, password: str) -> None:
        if not parent_id.strip() or len(password) < 12 or len(password) > 1024:
            raise ValueError("Invalid parent ID or password length")
        salt = secrets.token_bytes(16)
        digest = self._derive(password, salt)
        with sqlite3.connect(self.path) as db:
            db.execute(
                "INSERT INTO parent_credentials(parent_id,salt,password_digest) VALUES(?,?,?)",
                (parent_id, salt, digest),
            )

    def verify(self, *, parent_id: str, password: str) -> bool:
        if not parent_id.strip() or len(password) > 1024:
            return False
        with sqlite3.connect(self.path) as db:
            row = db.execute(
                "SELECT salt,password_digest FROM parent_credentials WHERE parent_id=?",
                (parent_id,),
            ).fetchone()
        # Dummy KDF reduces timing differences for nonexistent accounts.
        if row is None:
            self._derive(password, b"\x00" * 16)
            return False
        return hmac.compare_digest(self._derive(password, row[0]), row[1])
