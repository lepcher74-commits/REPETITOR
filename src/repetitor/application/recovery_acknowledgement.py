"""Transport-independent recovery response with no account-existence signal.

The future HTTP adapter must return the same status and body for every request.
This does not eliminate timing differences or replace operational error logging.
"""
from __future__ import annotations

from datetime import datetime

from repetitor.application.parent_recovery_request import ParentRecoveryRequest
from repetitor.persistence.mail_request_limiter import AbuseLimitExceeded


RECOVERY_ACKNOWLEDGEMENT = (
    "If this address is registered, recovery instructions may arrive."
)


class RecoveryAcknowledgement:
    def __init__(self, requests: ParentRecoveryRequest):
        self.requests = requests

    def submit(self, *, email: str, server_client_ip: str, now: datetime) -> str:
        try:
            self.requests.request(
                email=email, server_client_ip=server_client_ip, now=now,
            )
        except (AbuseLimitExceeded, OSError):
            # Operational monitoring must record failures without token or email.
            # The response does not expose existence or delivery status.
            pass
        return RECOVERY_ACKNOWLEDGEMENT
