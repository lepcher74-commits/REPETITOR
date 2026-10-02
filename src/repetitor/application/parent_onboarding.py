"""Parent onboarding state: email verification is not representative verification.

This module does not implement identity proofing or activate cloud services.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum

from repetitor.application.parent_consent import (
    ConsentPurpose, ConsentRecord, ParentAuthorization, may_transfer_child_data,
)


class OnboardingStep(str, Enum):
    EMAIL_PENDING = "email_pending"
    REPRESENTATIVE_REVIEW = "representative_review"
    LEGAL_REVIEW = "legal_review"
    READY_FOR_OPTIONAL_CONSENT = "ready_for_optional_consent"


@dataclass(frozen=True)
class ParentOnboarding:
    parent_id: str
    email_verified: bool = False
    representative_verified: bool = False
    legal_review_approved: bool = False

    def __post_init__(self) -> None:
        if not self.parent_id.strip():
            raise ValueError("Parent identifier is required")

    @property
    def step(self) -> OnboardingStep:
        if not self.email_verified:
            return OnboardingStep.EMAIL_PENDING
        if not self.representative_verified:
            return OnboardingStep.REPRESENTATIVE_REVIEW
        if not self.legal_review_approved:
            return OnboardingStep.LEGAL_REVIEW
        return OnboardingStep.READY_FOR_OPTIONAL_CONSENT

    def mark_email_verified(self) -> "ParentOnboarding":
        """Only call after independently validating a one-time email challenge."""
        return replace(self, email_verified=True)

    def may_sync(
        self,
        consent: ConsentRecord | None,
        *,
        feature_enabled: bool = False,
    ) -> bool:
        return may_transfer_child_data(
            ParentAuthorization(
                mailbox_verified=self.email_verified,
                representative_verified=self.representative_verified,
                legal_review_approved=self.legal_review_approved,
            ),
            consent,
            ConsentPurpose.CLOUD_LEARNING_SYNC,
            feature_enabled=feature_enabled,
        )
