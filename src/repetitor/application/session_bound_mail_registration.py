"""Resolve a parent session before calling the account-bound mail adapter."""
from __future__ import annotations

from datetime import datetime

from repetitor.application.bound_mail_registration import BoundMailRegistration
from repetitor.persistence.parent_session_store import ParentSessionStore


class SessionBoundMailRegistration:
    def __init__(self, *, sessions: ParentSessionStore, mail: BoundMailRegistration):
        self.sessions = sessions
        self.mail = mail

    def request_challenge(
        self, *, session_token: str, server_client_ip: str, now: datetime,
    ) -> None:
        actor = self.sessions.authenticate(token=session_token, now=now)
        if actor is None:
            raise PermissionError("Valid parent session required")
        self.mail.request_challenge(
            actor=actor, server_client_ip=server_client_ip, now=now,
        )

    def verify_challenge(
        self, *, session_token: str, challenge_token: str, now: datetime,
    ) -> bool:
        actor = self.sessions.authenticate(token=session_token, now=now)
        if actor is None:
            return False
        return self.mail.verify_challenge(
            actor=actor, token=challenge_token, now=now,
        )
