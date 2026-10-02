from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from threading import Barrier

from repetitor.application.atomic_parent_password_reset import AtomicParentPasswordReset
from repetitor.persistence.parent_credentials import ParentCredentials
from repetitor.persistence.parent_session_store import ParentSessionStore
from repetitor.persistence.password_recovery_store import PasswordRecoveryStore


def test_simultaneous_reset_consumes_token_once(tmp_path):
    path = tmp_path / "parent.sqlite"
    credentials = ParentCredentials(path)
    recovery = PasswordRecoveryStore(path)
    sessions = ParentSessionStore(path)
    credentials.register(parent_id="parent", password="previous private password")
    token = recovery.issue(parent_id="parent", now=datetime(2026, 10, 2, tzinfo=timezone.utc))
    reset = AtomicParentPasswordReset(credentials, recovery, sessions)
    barrier = Barrier(2)

    def attempt(password):
        barrier.wait()
        return reset.reset(
            parent_id="parent", token=token, new_password=password,
            now=datetime(2026, 10, 2, tzinfo=timezone.utc),
        )

    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(attempt, "replacement password alpha")
        second = pool.submit(attempt, "replacement password bravo")
        assert sorted([first.result(), second.result()]) == [False, True]
