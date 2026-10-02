from datetime import datetime, timezone

from repetitor.application.parent_consent import (
    ConsentPurpose, ConsentRecord, ParentAuthorization, may_transfer_child_data,
)


def test_email_and_consent_alone_cannot_authorize_child_upload():
    consent = ConsentRecord(ConsentPurpose.CLOUD_LEARNING_SYNC, "v1", datetime.now(timezone.utc))
    assert not may_transfer_child_data(ParentAuthorization(mailbox_verified=True), consent, ConsentPurpose.CLOUD_LEARNING_SYNC, feature_enabled=True)


def test_default_off_and_separate_purposes():
    auth = ParentAuthorization(True, True, True)
    consent = ConsentRecord(ConsentPurpose.CLOUD_LEARNING_SYNC, "v1", datetime.now(timezone.utc))
    assert not may_transfer_child_data(auth, consent, ConsentPurpose.CLOUD_LEARNING_SYNC)
    assert not may_transfer_child_data(auth, consent, ConsentPurpose.EXTERNAL_AI, feature_enabled=True)
    assert may_transfer_child_data(auth, consent, ConsentPurpose.CLOUD_LEARNING_SYNC, feature_enabled=True)


def test_withdrawal_immediately_revokes_authorization():
    auth = ParentAuthorization(True, True, True)
    consent = ConsentRecord(ConsentPurpose.CLOUD_LEARNING_SYNC, "v1", datetime.now(timezone.utc))
    assert not may_transfer_child_data(auth, consent.withdraw(), ConsentPurpose.CLOUD_LEARNING_SYNC, feature_enabled=True)


def test_missing_notice_or_legal_approval_fails_closed():
    now = datetime.now(timezone.utc)
    consent = ConsentRecord(ConsentPurpose.CLOUD_LEARNING_SYNC, "", now)
    assert not may_transfer_child_data(ParentAuthorization(True, True, True), consent, ConsentPurpose.CLOUD_LEARNING_SYNC, feature_enabled=True)
    valid = ConsentRecord(ConsentPurpose.CLOUD_LEARNING_SYNC, "v1", now)
    assert not may_transfer_child_data(ParentAuthorization(True, True, False), valid, ConsentPurpose.CLOUD_LEARNING_SYNC, feature_enabled=True)
