from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs/STAGE_8_AUDIT_CANDIDATE_MANIFEST.json"

DOCS_WITH_CANDIDATE = (
    ROOT / "docs/STAGE_8_MANUAL_AUDIT_PACKET.md",
    ROOT / "docs/PILOT_MANUAL_GATE_RECORD.md",
    ROOT / "docs/PILOT_DATA_OPERATIONS_TEMPLATE.md",
    ROOT / "docs/ACCESSIBILITY_PILOT_AUDIT_RECORD.md",
    ROOT / "docs/PILOT_CONTENT_REVIEW_INVENTORY.md",
    ROOT / "docs/STAGE_8_ACCESSIBILITY_OBSERVATION_WORKSHEET.md",
    ROOT / "docs/STAGE_8_HUMAN_CONTENT_REVIEW_WORKSHEET.md",
    ROOT / "docs/STAGE_8_OPERATOR_DATA_DECISION_WORKSHEET.md",
)

def _manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))

def test_stage8_manifest_tracks_manual_and_final_gate_issues() -> None:
    data = _manifest()
    assert data["tracking_issues"] == {
        "pr_08_accessibility": 2,
        "pr_10_content_operations": 3,
        "pr_14_final_candidate": 4,
    }


def test_stage8_audit_candidate_manifest_is_not_final_candidate() -> None:
    data = _manifest()
    assert data["status"] == "audit_candidate"
    assert data["final_candidate_nominated"] is False
    assert data["manual_gates"]["pr_08_accessibility"].startswith("blocked")
    assert data["manual_gates"]["pr_10_content_operations"].startswith("blocked")
    assert data["manual_gates"]["pr_14_final_candidate"] == "blocked_not_nominated"

def test_stage8_manual_docs_bind_to_one_candidate_sha() -> None:
    data = _manifest()
    sha = data["candidate_sha"]
    for path in DOCS_WITH_CANDIDATE:
        text = path.read_text(encoding="utf-8")
        assert sha in text, f"{path.name} is not bound to audit candidate {sha}"

def test_stage8_packet_matches_manifest_artifacts_and_runs() -> None:
    data = _manifest()
    text = (ROOT / "docs/STAGE_8_MANUAL_AUDIT_PACKET.md").read_text(encoding="utf-8")
    expected = (
        str(data["ci"]["run_id"]),
        str(data["pilot_build"]["run_id"]),
        str(data["pilot_build"]["artifacts"]["windows"]["id"]),
        str(data["pilot_build"]["artifacts"]["macos"]["id"]),
        data["pilot_build"]["artifacts"]["windows"]["archive_sha256"],
        data["pilot_build"]["artifacts"]["macos"]["archive_sha256"],
    )
    for value in expected:
        assert value in text

def test_stage8_review_inventory_matches_manifest_fingerprints() -> None:
    data = _manifest()
    text = (ROOT / "docs/PILOT_CONTENT_REVIEW_INVENTORY.md").read_text(encoding="utf-8")
    assert data["review_bindings"]["learner_visible_yaml_sha256"] in text
    assert data["review_bindings"]["runtime_ui_source_sha256"] in text
