from datetime import datetime, timezone

import pytest

from repetitor.application.parent_login import ParentLogin
from repetitor.persistence.login_attempt_limiter import LoginAttemptLimiter, LoginRateLimited
from repetitor.persistence.parent_credentials import ParentCredentials
from repetitor.persistence.parent_session_store import ParentSessionStore


def test_limited_login_blocks_after_five_bad_passwords(tmp_path):
    credentials = ParentCredentials(tmp_path / "credentials.sqlite")
    sessions = ParentSessionStore(tmp_path / "sessions.sqlite")
    limiter = LoginAttemptLimiter(tmp_path / "attempts.sqlite")
    credentials.register(parent_id="p", password="long private passphrase")
    login = ParentLogin(credentials, sessions, limiter)
    now = datetime(2026, 10, 2, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        login.login(parent_id="p", password="bad", now=now)
    for _ in range(5):
        assert login.login(
            parent_id="p", password="bad", now=now, server_client_ip="192.0.2.1"
        ) is None
    with pytest.raises(LoginRateLimited):
        login.login(
            parent_id="p", password="long private passphrase",
            now=now, server_client_ip="192.0.2.1",
        )
