"""One-time mailbox challenge primitives; no outbound email or identity claims."""
from __future__ import annotations

import hashlib
import hmac
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass
class EmailChallenge:
    parent_id: str
    token_digest: str
    expires_at: datetime
    attempts_remaining: int = 5
    consumed: bool = False

    def verify(self, token: str, now: datetime) -> bool:
        if now.tzinfo is None:
            raise ValueError("Timezone-aware verification time required")
        if self.consumed or self.attempts_remaining <= 0 or now >= self.expires_at:
            return False
        self.attempts_remaining -= 1
        valid = hmac.compare_digest(
            hashlib.sha256(token.encode("utf-8")).hexdigest(), self.token_digest
        )
        if valid:
            self.consumed = True
        return valid


def issue_email_challenge(
    parent_id: str, now: datetime, *, ttl_minutes: int = 15
) -> tuple[EmailChallenge, str]:
    if not parent_id.strip() or now.tzinfo is None or not 1 <= ttl_minutes <= 60:
        raise ValueError("Invalid challenge parameters")
    token = secrets.token_urlsafe(32)
    challenge = EmailChallenge(
        parent_id=parent_id,
        token_digest=hashlib.sha256(token.encode("utf-8")).hexdigest(),
        expires_at=now + timedelta(minutes=ttl_minutes),
    )
    return challenge, token
