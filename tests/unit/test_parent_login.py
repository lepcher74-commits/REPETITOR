from datetime import datetime, timezone

from repetitor.application.parent_login import ParentLogin
from repetitor.persistence.parent_credentials import ParentCredentials
from repetitor.persistence.parent_session_store import ParentSessionStore


def test_login_issues_session_only_after_password_verification(tmp_path):
    credentials = ParentCredentials(tmp_path / "credentials.sqlite")
    sessions = ParentSessionStore(tmp_path / "sessions.sqlite")
    login = ParentLogin(credentials, sessions)
    credentials.register(parent_id="p", password="long private passphrase")
    now = datetime(2026, 10, 2, tzinfo=timezone.utc)
    assert login.login(parent_id="p", password="incorrect", now=now) is None
    token = login.login(parent_id="p", password="long private passphrase", now=now)
    assert token is not None
    assert sessions.authenticate(token=token, now=now).parent_id == "p"
    sessions.revoke(token=token)
    assert sessions.authenticate(token=token, now=now) is None
