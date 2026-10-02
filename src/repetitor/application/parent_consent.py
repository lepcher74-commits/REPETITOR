"""Fail-closed parent authorization policy; no identity-verification service is implied."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class ConsentPurpose(str, Enum):
    CLOUD_LEARNING_SYNC = "cloud_learning_sync"
    EXTERNAL_AI = "external_ai"


@dataclass(frozen=True)
class ParentAuthorization:
    mailbox_verified: bool = False
    representative_verified: bool = False
    legal_review_approved: bool = False


@dataclass(frozen=True)
class ConsentRecord:
    purpose: ConsentPurpose
    notice_version: str
    granted_at: datetime
    withdrawn_at: datetime | None = None

    @property
    def active(self) -> bool:
        return (
            bool(self.notice_version.strip())
            and self.granted_at.tzinfo is not None
            and self.withdrawn_at is None
        )

    def withdraw(self, when: datetime | None = None) -> "ConsentRecord":
        from dataclasses import replace
        instant = when or datetime.now(timezone.utc)
        if instant.tzinfo is None or instant < self.granted_at:
            raise ValueError("Withdrawal must be timezone-aware and not predate consent")
        return replace(self, withdrawn_at=instant)


def may_transfer_child_data(
    authorization: ParentAuthorization,
    consent: ConsentRecord | None,
    purpose: ConsentPurpose,
    *,
    feature_enabled: bool = False,
) -> bool:
    """Default deny. Callers must separately enforce authentication and server policy."""
    return (
        feature_enabled
        and authorization.mailbox_verified
        and authorization.representative_verified
        and authorization.legal_review_approved
        and consent is not None
        and consent.purpose is purpose
        and consent.active
    )
