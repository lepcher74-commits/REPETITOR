from dataclasses import replace
from datetime import datetime, timezone

import pytest

from repetitor.application.parent_consent import ConsentPurpose, ConsentRecord
from repetitor.application.parent_onboarding import OnboardingStep, ParentOnboarding


def test_parent_onboarding_requires_identifier():
    with pytest.raises(ValueError):
        ParentOnboarding(" ")


def test_verified_email_does_not_verify_guardianship():
    parent = ParentOnboarding("p")
    assert parent.step is OnboardingStep.EMAIL_PENDING
    parent = parent.mark_email_verified()
    assert parent.step is OnboardingStep.REPRESENTATIVE_REVIEW
    consent = ConsentRecord(ConsentPurpose.CLOUD_LEARNING_SYNC, "v1", datetime.now(timezone.utc))
    assert not parent.may_sync(consent, feature_enabled=True)


def test_onboarding_requires_separate_legal_review_and_explicit_consent():
    parent = ParentOnboarding("p", email_verified=True, representative_verified=True)
    assert parent.step is OnboardingStep.LEGAL_REVIEW
    consent = ConsentRecord(ConsentPurpose.CLOUD_LEARNING_SYNC, "v1", datetime.now(timezone.utc))
    assert not parent.may_sync(consent, feature_enabled=True)
    parent = replace(parent, legal_review_approved=True)
    assert parent.step is OnboardingStep.READY_FOR_OPTIONAL_CONSENT
    assert not parent.may_sync(consent)
    assert parent.may_sync(consent, feature_enabled=True)
    assert not parent.may_sync(consent.withdraw(), feature_enabled=True)
