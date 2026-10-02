from datetime import datetime, timedelta, timezone

import pytest

from repetitor.application.email_challenge import issue_email_challenge


NOW = datetime(2026, 10, 2, tzinfo=timezone.utc)


def test_mailbox_challenge_is_one_time_and_stores_only_digest():
    challenge, token = issue_email_challenge("parent", NOW)
    assert token not in repr(challenge)
    assert not challenge.verify("wrong", NOW)
    assert challenge.verify(token, NOW)
    assert not challenge.verify(token, NOW)


def test_mailbox_challenge_expires_and_limits_guesses():
    expired, token = issue_email_challenge("parent", NOW)
    assert not expired.verify(token, NOW + timedelta(minutes=15))
    limited, token = issue_email_challenge("parent", NOW)
    for _ in range(5):
        assert not limited.verify("wrong", NOW)
    assert not limited.verify(token, NOW)


def test_mailbox_challenge_rejects_invalid_parameters():
    with pytest.raises(ValueError):
        issue_email_challenge(" ", NOW)
    with pytest.raises(ValueError):
        issue_email_challenge("parent", NOW.replace(tzinfo=None))
    with pytest.raises(ValueError):
        issue_email_challenge("parent", NOW, ttl_minutes=120)
