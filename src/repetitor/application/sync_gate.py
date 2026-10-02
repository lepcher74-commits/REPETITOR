"""Combine persisted consent with onboarding gates without enabling any network client."""
from __future__ import annotations

from repetitor.application.parent_consent import ConsentPurpose, ConsentRecord
from repetitor.application.parent_onboarding import ParentOnboarding
from repetitor.persistence.consent_ledger import ConsentLedger


def may_start_optional_sync(
    parent: ParentOnboarding,
    ledger: ConsentLedger,
    consent: ConsentRecord | None,
    *,
    feature_enabled: bool = False,
) -> bool:
    """Deny unless both the current ledger and independent onboarding agree.

    A local ledger entry is not proof of legal consent or parent identity.
    The future server must independently authorize each request.
    """
    return (
        consent is not None
        and ledger.active(parent.parent_id, ConsentPurpose.CLOUD_LEARNING_SYNC)
        and parent.may_sync(consent, feature_enabled=feature_enabled)
    )
