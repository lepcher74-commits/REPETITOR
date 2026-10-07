from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

CANDIDATE_SHA = "983d04c564879f9ff8b6de110497901279073aeb"
ARTIFACTS = {
    "windows": {
        "id": 11343327951,
        "sha256": "2c40cb9cda7cc7cb6f87c218dffea1f7d7e6046261d54567616a4c767c80a416",
    },
    "macos": {
        "id": 11342674307,
        "sha256": "1d5c9490e53c4b75948360f0170e311a6d371d8bf86a53854a0d593399367a28",
    },
}

STEPS = [
    ("A1", "Launch pinned build with separate synthetic data directory and create invented learner session."),
    ("A2", "Inventory database, startup log and operator-managed copies/access."),
    ("A3", "Perform documented SQLite backup after stopping/quiescing the app."),
    ("A4", "Restore synthetic backup into a fresh test directory and verify state."),
    ("A5", "Simulate withdrawal request through approved parent/legal-guardian route."),
    ("A6", "Apply approved deletion process to synthetic primary data and managed backups."),
    ("A7", "Confirm deleted synthetic profile cannot be reopened from approved local locations."),
    ("B1", "Lost-device tabletop: identify report receiver/timestamp and containment action."),
    ("B2", "Lost-device tabletop: inventory affected local files/backups without circulating learner data."),
    ("B3", "Lost-device tabletop: identify who determines applicable notifications/timelines."),
    ("B4", "Lost-device tabletop: identify approved guardian/support communication channel."),
    ("B5", "Lost-device tabletop: identify restoration/lessons-learned/pilot-stop decision owner."),
    ("NW-WIN", "Observe Windows packaged process network connections during normal synthetic learning flow."),
    ("NW-MAC", "Observe macOS packaged process network connections during normal synthetic learning flow."),
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_artifact(platform: str, path: Path) -> list[str]:
    errors: list[str] = []
    expected = ARTIFACTS[platform]
    actual = sha256_file(path)
    if actual != expected["sha256"]:
        errors.append(
            f"{platform}: archive SHA-256 mismatch: expected {expected['sha256']}, got {actual}"
        )
        return errors

    try:
        with zipfile.ZipFile(path) as archive:
            build_info_names = [
                name for name in archive.namelist() if name.endswith("build-info.txt")
            ]
            if not build_info_names:
                errors.append(f"{platform}: build-info.txt not found in archive")
                return errors
            contents = "\n".join(
                archive.read(name).decode("utf-8", errors="replace")
                for name in build_info_names
            )
    except zipfile.BadZipFile:
        errors.append(f"{platform}: artifact is not a valid ZIP archive")
        return errors

    if CANDIDATE_SHA not in contents:
        errors.append(f"{platform}: embedded build info does not contain {CANDIDATE_SHA}")
    return errors


def new_state() -> dict[str, object]:
    return {
        "schema_version": 1,
        "candidate_sha": CANDIDATE_SHA,
        "controller_scope": {
            "jurisdiction": "Russia",
            "setting": "independent_home_learning",
            "grades": "5-11",
            "max_participants": 10,
            "authorization": "B1 guardian before enrollment",
            "retention": "active pilot + 30 days; earlier deletion on withdrawal/request",
            "backups": "synthetic/test only unless separately approved",
        },
        "operator": "",
        "date": "",
        "test_machine_windows": "",
        "test_machine_macos": "",
        "artifact_verification": {
            "windows": {"path": "", "result": "NOT TESTED", "notes": ""},
            "macos": {"path": "", "result": "NOT TESTED", "notes": ""},
        },
        "steps": [
            {"id": step_id, "description": description, "result": "NOT TESTED", "notes": ""}
            for step_id, description in STEPS
        ],
    }


def save_state(path: Path, state: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_state(state: dict[str, object], *, require_complete: bool) -> list[str]:
    errors: list[str] = []
    if state.get("candidate_sha") != CANDIDATE_SHA:
        errors.append("candidate SHA mismatch")

    expected_scope = new_state()["controller_scope"]
    if state.get("controller_scope") != expected_scope:
        errors.append("Controller scope differs from approved Stage 8 values")

    artifacts = state.get("artifact_verification")
    if not isinstance(artifacts, dict):
        errors.append("artifact_verification must be an object")
    else:
        for platform in ("windows", "macos"):
            item = artifacts.get(platform)
            if not isinstance(item, dict):
                errors.append(f"{platform}: artifact verification missing")
                continue
            result = item.get("result")
            if result not in {"PASS", "FAIL", "NOT TESTED"}:
                errors.append(f"{platform}: invalid artifact result {result!r}")
            if result == "FAIL" and not str(item.get("notes", "")).strip():
                errors.append(f"{platform}: FAIL requires notes")
            if require_complete and result != "PASS":
                errors.append(f"{platform}: verified exact artifact PASS required")

    steps = state.get("steps")
    if not isinstance(steps, list):
        return errors + ["steps must be a list"]

    expected_ids = [step_id for step_id, _ in STEPS]
    actual_ids = [item.get("id") for item in steps if isinstance(item, dict)]
    if actual_ids != expected_ids:
        errors.append("operator drill step set/order differs from required A1-A7/B1-B5/network set")

    for item in steps:
        if not isinstance(item, dict):
            errors.append("invalid step entry")
            continue
        step_id = item.get("id")
        result = item.get("result")
        if result not in {"PASS", "FAIL", "NOT TESTED"}:
            errors.append(f"{step_id}: invalid result {result!r}")
        if result in {"PASS", "FAIL"} and not str(item.get("notes", "")).strip():
            errors.append(f"{step_id}: observed result requires sanitized evidence/notes")
        if require_complete and result != "PASS":
            errors.append(f"{step_id}: PASS required for completed drill")

    if require_complete:
        for field in ("operator", "date", "test_machine_windows", "test_machine_macos"):
            if not str(state.get(field, "")).strip():
                errors.append(f"{field} is required")
    return errors


def verify_and_record(state: dict[str, object], platform: str, path: Path) -> None:
    errors = verify_artifact(platform, path)
    artifacts = state["artifact_verification"]
    assert isinstance(artifacts, dict)
    item = artifacts[platform]
    assert isinstance(item, dict)
    item["path"] = str(path)
    if errors:
        item["result"] = "FAIL"
        item["notes"] = "; ".join(errors)
    else:
        item["result"] = "PASS"
        item["notes"] = (
            f"archive SHA-256 matches artifact {ARTIFACTS[platform]['id']}; "
            f"embedded build info contains {CANDIDATE_SHA}"
        )


def review_interactively(state_path: Path) -> int:
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
    else:
        state = new_state()

    if not str(state.get("operator", "")).strip():
        state["operator"] = input("Operator / reviewer role: ").strip()
    if not str(state.get("date", "")).strip():
        state["date"] = input("Date (YYYY-MM-DD): ").strip()

    steps = state["steps"]
    assert isinstance(steps, list)
    for item in steps:
        assert isinstance(item, dict)
        if item.get("result") in {"PASS", "FAIL"}:
            continue
        print("\n" + "=" * 72)
        print(f"{item['id']}: {item['description']}")
        while True:
            answer = input("[p]ass / [f]ail / [s]kip / [q]uit: ").strip().lower()
            if answer in {"p", "pass", "f", "fail"}:
                notes = input("Required sanitized observation / evidence reference: ").strip()
                if not notes:
                    print("Observation/evidence is required.")
                    continue
                item["result"] = "PASS" if answer in {"p", "pass"} else "FAIL"
                item["notes"] = notes
                break
            if answer in {"s", "skip"}:
                item["result"] = "NOT TESTED"
                break
            if answer in {"q", "quit"}:
                save_state(state_path, state)
                print(f"Progress saved to {state_path}")
                return 0
            print("Unknown choice.")
        save_state(state_path, state)

    errors = validate_state(state, require_complete=True)
    if errors:
        print("\nOperator drill remains BLOCKED:")
        for error in errors:
            print(f"- {error}")
        return 2

    print("\nOperator drill evidence validates PASS.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail-closed Stage 8 synthetic operator/network evidence helper."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    verify = sub.add_parser("verify-artifact")
    verify.add_argument("platform", choices=("windows", "macos"))
    verify.add_argument("archive", type=Path)

    init = sub.add_parser("init")
    init.add_argument("state", type=Path)

    record = sub.add_parser("record-artifact")
    record.add_argument("state", type=Path)
    record.add_argument("platform", choices=("windows", "macos"))
    record.add_argument("archive", type=Path)

    review = sub.add_parser("review")
    review.add_argument("state", type=Path)

    validate = sub.add_parser("validate")
    validate.add_argument("state", type=Path)
    validate.add_argument("--require-complete", action="store_true")

    args = parser.parse_args()

    if args.command == "verify-artifact":
        errors = verify_artifact(args.platform, args.archive)
        if errors:
            print("FAIL")
            for error in errors:
                print(f"- {error}")
            return 2
        print(
            f"PASS: {args.platform} archive digest and embedded build SHA match "
            f"candidate {CANDIDATE_SHA}"
        )
        return 0

    if args.command == "init":
        if args.state.exists():
            raise SystemExit(f"Refusing to overwrite existing evidence file: {args.state}")
        save_state(args.state, new_state())
        print(f"Created fail-closed evidence file: {args.state}")
        return 0

    if args.state.exists():
        state = json.loads(args.state.read_text(encoding="utf-8"))
    else:
        state = new_state()

    if args.command == "record-artifact":
        verify_and_record(state, args.platform, args.archive)
        save_state(args.state, state)
        item = state["artifact_verification"][args.platform]
        print(f"{args.platform}: {item['result']} — {item['notes']}")
        return 0 if item["result"] == "PASS" else 2

    if args.command == "review":
        save_state(args.state, state)
        return review_interactively(args.state)

    errors = validate_state(state, require_complete=args.require_complete)
    if errors:
        print("BLOCKED")
        for error in errors:
            print(f"- {error}")
        return 2
    print("PASS: operator evidence structure is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
