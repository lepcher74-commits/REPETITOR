"""Internal password-to-session boundary; deploy only behind request throttling."""
from __future__ import annotations

from datetime import datetime

from repetitor.persistence.login_attempt_limiter import LoginAttemptLimiter
from repetitor.persistence.parent_credentials import ParentCredentials
from repetitor.persistence.parent_session_store import ParentSessionStore


class ParentLogin:
    def __init__(
        self, credentials: ParentCredentials, sessions: ParentSessionStore,
        limiter: LoginAttemptLimiter | None = None,
    ):
        self.credentials = credentials
        self.sessions = sessions
        self.limiter = limiter

    def login(
        self, *, parent_id: str, password: str, now: datetime,
        server_client_ip: str | None = None,
    ) -> str | None:
        if self.limiter is not None:
            if server_client_ip is None:
                raise ValueError("Trusted client IP required with login limiter")
            self.limiter.check(parent_id=parent_id, client_ip=server_client_ip, now=now)
        if not self.credentials.verify(parent_id=parent_id, password=password):
            if self.limiter is not None:
                self.limiter.record_failure(
                    parent_id=parent_id, client_ip=server_client_ip, now=now,
                )
            return None
        return self.sessions.create(parent_id=parent_id, now=now)
