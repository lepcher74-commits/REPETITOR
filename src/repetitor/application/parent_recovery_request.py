"""Offline recovery request orchestration; no public HTTP endpoint.

The directory and client IP must be server-controlled. Unknown addresses receive
the same public response and consume the same request limits as known ones.
"""
from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Protocol

from repetitor.application.mail_registration import MailSender
from repetitor.persistence.mail_request_limiter import MailRequestLimiter
from repetitor.persistence.password_recovery_store import PasswordRecoveryStore


class RecoveryDirectory(Protocol):
    def find_parent(self, *, normalized_email: str) -> str | None: ...


class ParentRecoveryRequest:
    def __init__(
        self, *, directory: RecoveryDirectory, limiter: MailRequestLimiter,
        recovery: PasswordRecoveryStore, sender: MailSender,
    ):
        self.directory = directory
        self.limiter = limiter
        self.recovery = recovery
        self.sender = sender

    def request(self, *, email: str, server_client_ip: str, now: datetime) -> None:
        normalized = email.strip().casefold()
        if not normalized or "@" not in normalized or len(normalized) > 254:
            raise ValueError("Valid email required")
        # The limiter key is independent of whether the account exists.
        address_key = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        self.limiter.check_and_record(
            parent_id=address_key, client_ip=server_client_ip, now=now,
        )
        parent_id = self.directory.find_parent(normalized_email=normalized)
        if parent_id is None:
            return
        token = self.recovery.issue(parent_id=parent_id, now=now)
        # MailSender is injected; production must use a dedicated recovery
        # template, generic HTTP response and avoid logging this token.
        self.sender.send_challenge(recipient=normalized, token=token)
