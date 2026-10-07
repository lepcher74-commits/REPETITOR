from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/stage8_content_review_cli.py"
WORKSHEET = ROOT / "docs/STAGE_8_HUMAN_CONTENT_REVIEW_WORKSHEET.md"


def _load_module():
    spec = importlib.util.spec_from_file_location("stage8_content_review_cli", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_content_review_cli_parses_all_bound_rows() -> None:
    module = _load_module()
    candidate_sha, rows = module.parse_worksheet(WORKSHEET)
    assert candidate_sha == "983d04c564879f9ff8b6de110497901279073aeb"
    assert len(rows) == 135
    assert rows[0]["row"] == 1
    assert rows[-1]["row"] == 135


def test_content_review_cli_starts_fail_closed() -> None:
    module = _load_module()
    candidate_sha, rows = module.parse_worksheet(WORKSHEET)
    state = module.new_state(candidate_sha, rows)

    assert all(item["result"] == "NOT TESTED" for item in state["rows"])
    errors = module.validate_state(
        state,
        candidate_sha,
        rows,
        require_complete=True,
    )
    assert any("still NOT TESTED" in error for error in errors)
    assert any("reviewer is required" in error for error in errors)
    assert any("review_date is required" in error for error in errors)


def test_content_review_cli_requires_notes_for_fail() -> None:
    module = _load_module()
    candidate_sha, rows = module.parse_worksheet(WORKSHEET)
    state = module.new_state(candidate_sha, rows)
    state["reviewer"] = "Controller"
    state["review_date"] = "2026-10-07"
    for item in state["rows"]:
        item["result"] = "PASS"
    state["rows"][0]["result"] = "FAIL"

    errors = module.validate_state(
        state,
        candidate_sha,
        rows,
        require_complete=True,
    )
    assert errors == ["row 1: FAIL requires notes / issue reference"]


def test_content_review_cli_rejects_text_drift() -> None:
    module = _load_module()
    candidate_sha, rows = module.parse_worksheet(WORKSHEET)
    state = module.new_state(candidate_sha, rows)
    state["rows"][10]["text"] = "changed"

    errors = module.validate_state(
        state,
        candidate_sha,
        rows,
        require_complete=False,
    )
    assert "row 11: text differs from worksheet" in errors
