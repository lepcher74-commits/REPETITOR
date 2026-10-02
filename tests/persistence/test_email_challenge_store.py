from datetime import datetime, timedelta, timezone

from repetitor.persistence.email_challenge_store import EmailChallengeStore


NOW = datetime(2026, 10, 2, tzinfo=timezone.utc)


def test_persistent_challenge_survives_restart_and_blocks_replay(tmp_path):
    path = tmp_path / "mail.sqlite"
    token = EmailChallengeStore(path).issue("p", NOW)
    restarted = EmailChallengeStore(path)
    assert not restarted.verify("p", "wrong", NOW)
    assert restarted.verify("p", token, NOW)
    assert not EmailChallengeStore(path).verify("p", token, NOW)


def test_persistent_challenge_expiration_and_guess_limit(tmp_path):
    store = EmailChallengeStore(tmp_path / "mail.sqlite")
    token = store.issue("p", NOW)
    assert not store.verify("p", token, NOW + timedelta(minutes=15))
    for _ in range(5):
        assert not store.verify("p", "wrong", NOW)
    assert not store.verify("p", token, NOW)


def test_persistent_challenges_are_parent_scoped(tmp_path):
    store = EmailChallengeStore(tmp_path / "mail.sqlite")
    token = store.issue("p", NOW)
    assert not store.verify("other", token, NOW)
    assert store.verify("p", token, NOW)


def test_issuance_cooldown_survives_restart_and_does_not_replace_token(tmp_path):
    import pytest
    path = tmp_path / "mail.sqlite"
    first = EmailChallengeStore(path).issue("p", NOW)
    with pytest.raises(ValueError, match="rate limited"):
        EmailChallengeStore(path).issue("p", NOW + timedelta(seconds=30))
    assert EmailChallengeStore(path).verify("p", first, NOW + timedelta(seconds=31))
    second = EmailChallengeStore(path).issue("p", NOW + timedelta(seconds=61))
    assert EmailChallengeStore(path).verify("p", second, NOW + timedelta(seconds=62))
