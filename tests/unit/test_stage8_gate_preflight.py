from pathlib import Path

from repetitor.application.stage8_gate_preflight import manual_gate_blockers


def test_missing_manual_records_are_blockers(tmp_path):
    blockers = manual_gate_blockers(tmp_path)
    assert len(blockers) == 4
    assert all("missing" in item for item in blockers)


def test_unresolved_manual_records_remain_blocked(tmp_path):
    for relative in (
        "docs/PILOT_MANUAL_GATE_RECORD.md",
        "docs/ACCESSIBILITY_PILOT_AUDIT_RECORD.md",
        "docs/PILOT_DATA_OPERATIONS_TEMPLATE.md",
        "docs/PILOT_CONTENT_REVIEW_INVENTORY.md",
    ):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("Result: NOT TESTED\nReviewer: [FILL]\n", encoding="utf-8")
    blockers = manual_gate_blockers(tmp_path)
    assert len(blockers) == 8


def test_complete_looking_text_does_not_certify_human_approval(tmp_path):
    for relative in (
        "docs/PILOT_MANUAL_GATE_RECORD.md",
        "docs/ACCESSIBILITY_PILOT_AUDIT_RECORD.md",
        "docs/PILOT_DATA_OPERATIONS_TEMPLATE.md",
        "docs/PILOT_CONTENT_REVIEW_INVENTORY.md",
    ):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("Reviewed observations recorded externally.\n", encoding="utf-8")
    assert manual_gate_blockers(tmp_path) == []
    # An empty blocker list is only a textual preflight, not a pilot-release gate.



def test_extended_candidate_and_review_markers_block_preflight(tmp_path):
    for relative in (
        'docs/PILOT_MANUAL_GATE_RECORD.md',
        'docs/ACCESSIBILITY_PILOT_AUDIT_RECORD.md',
        'docs/PILOT_DATA_OPERATIONS_TEMPLATE.md',
        'docs/PILOT_CONTENT_REVIEW_INVENTORY.md',
    ):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('Reviewed observations recorded externally.\n', encoding='utf-8')
    (tmp_path / 'docs/PILOT_MANUAL_GATE_RECORD.md').write_text(
        'Candidate SHA: [FILL AT FINAL CANDIDATE NOMINATION]\n'
        'Manual gate: [BLOCKED UNTIL REVIEW]\n', encoding='utf-8'
    )
    (tmp_path / 'docs/PILOT_CONTENT_REVIEW_INVENTORY.md').write_text(
        'Status: PREPARED / NOT HUMAN-REVIEWED\n', encoding='utf-8'
    )
    blockers = manual_gate_blockers(tmp_path)
    assert len(blockers) == 3
    assert any('unresolved [FILL' in item for item in blockers)
    assert any('unresolved [BLOCKED' in item for item in blockers)
    assert any('unresolved NOT HUMAN-REVIEWED' in item for item in blockers)
