import sqlite3

import pytest

from repetitor.application.parent_consent import ConsentPurpose
from repetitor.persistence.consent_ledger import ConsentLedger


def test_consent_ledger_is_default_off_and_persists_withdrawal(tmp_path):
    path = tmp_path / "consents.sqlite"
    ledger = ConsentLedger(path)
    purpose = ConsentPurpose.CLOUD_LEARNING_SYNC
    assert not ledger.active("parent1", purpose)
    ledger.append("parent1", purpose, "grant", "notice-v1")
    assert ledger.active("parent1", purpose)
    assert not ledger.active("parent1", ConsentPurpose.EXTERNAL_AI)
    ledger.append("parent1", purpose, "withdraw", "notice-v1")
    assert not ConsentLedger(path).active("parent1", purpose)


def test_consent_ledger_separates_parents_and_rejects_bad_events(tmp_path):
    ledger = ConsentLedger(tmp_path / "consents.sqlite")
    ledger.append("parent1", ConsentPurpose.EXTERNAL_AI, "grant", "v1")
    assert not ledger.active("parent2", ConsentPurpose.EXTERNAL_AI)
    with pytest.raises(ValueError):
        ledger.append("parent1", ConsentPurpose.EXTERNAL_AI, "approved", "v1")
    with pytest.raises(ValueError):
        ledger.append(" ", ConsentPurpose.EXTERNAL_AI, "grant", "v1")


def test_consent_ledger_preserves_event_history(tmp_path):
    path = tmp_path / "consents.sqlite"
    ledger = ConsentLedger(path)
    ledger.append("p", ConsentPurpose.CLOUD_LEARNING_SYNC, "grant", "v1")
    ledger.append("p", ConsentPurpose.CLOUD_LEARNING_SYNC, "withdraw", "v1")
    with sqlite3.connect(path) as db:
        assert db.execute("SELECT COUNT(*) FROM consent_events").fetchone()[0] == 2
