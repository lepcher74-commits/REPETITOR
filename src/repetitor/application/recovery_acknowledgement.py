"""Transport-independent recovery response with no account-existence signal.

The future HTTP adapter must return the same status and body for every request.
This does not eliminate timing differences or replace operational error logging.
"""
from __future__ import annotations

from datetime import datetime

from repetitor.application.parent_recovery_request import ParentRecoveryRequest
from repetitor.persistence.mail_request_limiter import AbuseLimitExceeded
from repetitor.persistence.malformed_request_limiter import MalformedRequestLimiter


RECOVERY_ACKNOWLEDGEMENT = (
    "If this address is registered, recovery instructions may arrive."
)


class RecoveryAcknowledgement:
    def __init__(self, requests: ParentRecoveryRequest, *, malformed_limiter: MalformedRequestLimiter | None = None):
        self.requests = requests
        self.malformed_limiter = malformed_limiter

    def submit(self, *, email: str, server_client_ip: str, now: datetime) -> str:
        if not server_client_ip.strip() or now.tzinfo is None:
            raise ValueError("Trusted client IP and aware time required")
        normalized = email.strip().casefold()
        if not normalized or "@" not in normalized or len(normalized) > 254:
            if self.malformed_limiter is not None:
                try:
                    self.malformed_limiter.check_and_record(client_ip=server_client_ip, now=now)
                except AbuseLimitExceeded:
                    pass
            return RECOVERY_ACKNOWLEDGEMENT
        try:
            self.requests.request(
                email=email, server_client_ip=server_client_ip, now=now,
            )
        except (AbuseLimitExceeded, OSError, ValueError):
            # Operational monitoring must record failures without token or email.
            # The response does not expose existence or delivery status.
            pass
        return RECOVERY_ACKNOWLEDGEMENT
