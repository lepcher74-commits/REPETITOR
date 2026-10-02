"""Trusted account-bound mailbox registration adapter (no HTTP or mail provider).

Only an authenticated server boundary may construct AuthenticatedParent. Never
accept client-supplied parent_id, recipient or forwarded IP as trusted values.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from repetitor.application.mail_registration import MailRegistration


@dataclass(frozen=True)
class AuthenticatedParent:
    parent_id: str


class ParentMailboxDirectory(Protocol):
    def registered_mailbox(self, parent_id: str) -> str | None: ...


class BoundMailRegistration:
    def __init__(self, registration: MailRegistration, directory: ParentMailboxDirectory):
        self.registration = registration
        self.directory = directory

    def request_challenge(
        self, *, actor: AuthenticatedParent, server_client_ip: str, now: datetime,
    ) -> None:
        if not actor.parent_id.strip():
            raise ValueError("Authenticated parent required")
        # A server-owned directory prevents callers redirecting a challenge.
        recipient = self.directory.registered_mailbox(actor.parent_id)
        if recipient is None:
            raise ValueError("No registered mailbox for authenticated parent")
        self.registration.request_challenge(
            parent_id=actor.parent_id, recipient=recipient,
            client_ip=server_client_ip, now=now,
        )

    def verify_challenge(
        self, *, actor: AuthenticatedParent, token: str, now: datetime,
    ) -> bool:
        if not actor.parent_id.strip():
            raise ValueError("Authenticated parent required")
        if self.directory.registered_mailbox(actor.parent_id) is None:
            return False
        return self.registration.verify_challenge(
            parent_id=actor.parent_id, token=token, now=now,
        )
