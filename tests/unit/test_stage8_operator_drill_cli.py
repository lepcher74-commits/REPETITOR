from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/stage8_operator_drill_cli.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("stage8_operator_drill_cli", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_operator_drill_state_is_bound_and_fail_closed() -> None:
    module = _load_module()
    state = module.new_state()

    assert state["candidate_sha"] == "983d04c564879f9ff8b6de110497901279073aeb"
    assert state["controller_scope"]["jurisdiction"] == "Russia"
    assert state["controller_scope"]["max_participants"] == 10
    assert state["artifact_verification"]["windows"]["result"] == "NOT TESTED"
    assert state["artifact_verification"]["macos"]["result"] == "NOT TESTED"
    assert [item["id"] for item in state["steps"]] == [
        "A1", "A2", "A3", "A4", "A5", "A6", "A7",
        "B1", "B2", "B3", "B4", "B5", "NW-WIN", "NW-MAC",
    ]

    errors = module.validate_state(state, require_complete=True)
    assert any("windows: verified exact artifact PASS required" in error for error in errors)
    assert any("A1: PASS required" in error for error in errors)
    assert any("NW-MAC: PASS required" in error for error in errors)


def test_operator_drill_observed_results_require_notes() -> None:
    module = _load_module()
    state = module.new_state()
    state["steps"][0]["result"] = "PASS"

    errors = module.validate_state(state, require_complete=False)
    assert "A1: observed result requires sanitized evidence/notes" in errors


def test_operator_drill_rejects_scope_drift() -> None:
    module = _load_module()
    state = module.new_state()
    state["controller_scope"]["max_participants"] = 11

    errors = module.validate_state(state, require_complete=False)
    assert "Controller scope differs from approved Stage 8 values" in errors


def test_operator_drill_complete_structure_can_validate() -> None:
    module = _load_module()
    state = module.new_state()
    state["operator"] = "parent/legal guardian"
    state["date"] = "2026-10-07"
    state["test_machine_windows"] = "Windows test machine"
    state["test_machine_macos"] = "macOS test machine"

    for platform in ("windows", "macos"):
        state["artifact_verification"][platform]["result"] = "PASS"
        state["artifact_verification"][platform]["notes"] = "verified digest and embedded SHA"

    for item in state["steps"]:
        item["result"] = "PASS"
        item["notes"] = "sanitized evidence reference"

    assert module.validate_state(state, require_complete=True) == []
