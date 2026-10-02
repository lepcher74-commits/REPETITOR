"""Internal password-to-session boundary; deploy only behind request throttling."""
from __future__ import annotations

from datetime import datetime

from repetitor.persistence.parent_credentials import ParentCredentials
from repetitor.persistence.parent_session_store import ParentSessionStore


class ParentLogin:
    def __init__(self, credentials: ParentCredentials, sessions: ParentSessionStore):
        self.credentials = credentials
        self.sessions = sessions

    def login(self, *, parent_id: str, password: str, now: datetime) -> str | None:
        if not self.credentials.verify(parent_id=parent_id, password=password):
            return None
        return self.sessions.create(parent_id=parent_id, now=now)
