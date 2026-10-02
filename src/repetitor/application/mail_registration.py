"""Offline-testable mailbox registration orchestration; no network implementation.

The caller must authenticate/resolve parent_id and derive client_ip at a trusted edge.
A verified mailbox is NOT proof of parent/guardian authority.
"""
from __future__ import annotations

from datetime import datetime
from typing import Protocol

from repetitor.persistence.email_challenge_store import EmailChallengeStore
from repetitor.persistence.mail_request_limiter import MailRequestLimiter


class MailSender(Protocol):
    def send_challenge(self, *, recipient: str, token: str) -> None: ...


class MailRegistration:
    def __init__(
        self, *, limiter: MailRequestLimiter, challenges: EmailChallengeStore,
        sender: MailSender,
    ):
        self.limiter = limiter
        self.challenges = challenges
        self.sender = sender

    def request_challenge(
        self, *, parent_id: str, recipient: str, client_ip: str, now: datetime,
    ) -> None:
        if not recipient.strip() or "@" not in recipient:
            raise ValueError("Recipient email required")
        # Both persisted protections run before any challenge is created or mail sent.
        # Production must bind recipient to the server-authenticated parent account.
        self.limiter.check_and_record(parent_id=parent_id, client_ip=client_ip, now=now)
        token = self.challenges.issue(parent_id, now)
        # Never return/log token from this boundary. Delivery failure propagates;
        # the unused challenge expires, and throttling still applies.
        self.sender.send_challenge(recipient=recipient, token=token)

    def verify_challenge(self, *, parent_id: str, token: str, now: datetime) -> bool:
        # This proves possession of a delivered token only; never marks guardian approval.
        return self.challenges.verify(parent_id, token, now)
