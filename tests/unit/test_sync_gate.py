from datetime import datetime, timezone

from repetitor.application.parent_consent import ConsentPurpose, ConsentRecord
from repetitor.application.parent_onboarding import ParentOnboarding
from repetitor.application.sync_gate import may_start_optional_sync
from repetitor.persistence.consent_ledger import ConsentLedger


def test_sync_requires_both_persisted_event_and_verified_onboarding(tmp_path):
    ledger = ConsentLedger(tmp_path / "consent.sqlite")
    parent = ParentOnboarding("p", True, True, True)
    consent = ConsentRecord(ConsentPurpose.CLOUD_LEARNING_SYNC, "v1", datetime.now(timezone.utc))
    assert not may_start_optional_sync(parent, ledger, consent, feature_enabled=True)
    ledger.append("p", ConsentPurpose.CLOUD_LEARNING_SYNC, "grant", "v1")
    assert not may_start_optional_sync(parent, ledger, consent)
    assert may_start_optional_sync(parent, ledger, consent, feature_enabled=True)
    ledger.append("p", ConsentPurpose.CLOUD_LEARNING_SYNC, "withdraw", "v1")
    assert not may_start_optional_sync(parent, ledger, consent, feature_enabled=True)


def test_sync_rejects_other_parent_other_purpose_and_email_only(tmp_path):
    ledger = ConsentLedger(tmp_path / "consent.sqlite")
    ledger.append("other", ConsentPurpose.CLOUD_LEARNING_SYNC, "grant", "v1")
    ledger.append("p", ConsentPurpose.EXTERNAL_AI, "grant", "v1")
    consent = ConsentRecord(ConsentPurpose.CLOUD_LEARNING_SYNC, "v1", datetime.now(timezone.utc))
    assert not may_start_optional_sync(ParentOnboarding("p", True, True, True), ledger, consent, feature_enabled=True)
    ledger.append("p", ConsentPurpose.CLOUD_LEARNING_SYNC, "grant", "v1")
    assert not may_start_optional_sync(ParentOnboarding("p", True), ledger, consent, feature_enabled=True)


def test_sync_denies_mismatched_or_stale_notice_version(tmp_path):
    ledger = ConsentLedger(tmp_path / "consent.sqlite")
    parent = ParentOnboarding("p", True, True, True)
    consent = ConsentRecord(ConsentPurpose.CLOUD_LEARNING_SYNC, "v2", datetime.now(timezone.utc))
    ledger.append("p", ConsentPurpose.CLOUD_LEARNING_SYNC, "grant", "v1")
    assert not may_start_optional_sync(parent, ledger, consent, feature_enabled=True)
    ledger.append("p", ConsentPurpose.CLOUD_LEARNING_SYNC, "grant", "v2")
    assert may_start_optional_sync(parent, ledger, consent, feature_enabled=True)
    ledger.append("p", ConsentPurpose.CLOUD_LEARNING_SYNC, "withdraw", "v1")
    assert not may_start_optional_sync(parent, ledger, consent, feature_enabled=True)
