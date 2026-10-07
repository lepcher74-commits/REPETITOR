from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

DEFAULT_WORKSHEET = Path("docs/STAGE_8_HUMAN_CONTENT_REVIEW_WORKSHEET.md")
ROW_RESULTS = {"PASS", "FAIL", "NOT TESTED"}


def parse_worksheet(path: Path) -> tuple[str, list[dict[str, object]]]:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"exact audit candidate.*?([0-9a-f]{40})", text, re.S)
    if not match:
        raise ValueError("Could not find candidate SHA in worksheet")
    candidate_sha = match.group(1)

    rows: list[dict[str, object]] = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 7 or not cells[0].isdigit():
            continue
        rows.append(
            {
                "row": int(cells[0]),
                "source": cells[1].strip(chr(96)),
                "item": cells[2].strip(chr(96)),
                "field": cells[3],
                "text": cells[4],
            }
        )

    if not rows:
        raise ValueError("No review rows found")
    if [row["row"] for row in rows] != list(range(1, len(rows) + 1)):
        raise ValueError("Worksheet rows are not contiguous from 1")
    return candidate_sha, rows


def new_state(candidate_sha: str, rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "schema_version": 1,
        "candidate_sha": candidate_sha,
        "reviewer": "",
        "review_date": "",
        "intended_context": "school grades 5-11, Russia, independent home learning",
        "rows": [{**row, "result": "NOT TESTED", "notes": ""} for row in rows],
    }


def save_state(path: Path, state: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_or_create_state(
    state_path: Path, candidate_sha: str, rows: list[dict[str, object]]
) -> dict[str, object]:
    if state_path.exists():
        return json.loads(state_path.read_text(encoding="utf-8"))
    state = new_state(candidate_sha, rows)
    save_state(state_path, state)
    return state


def validate_state(
    state: dict[str, object],
    candidate_sha: str,
    worksheet_rows: list[dict[str, object]],
    *,
    require_complete: bool,
) -> list[str]:
    errors: list[str] = []
    if state.get("candidate_sha") != candidate_sha:
        errors.append("candidate SHA does not match worksheet")

    state_rows = state.get("rows")
    if not isinstance(state_rows, list):
        return errors + ["rows must be a list"]
    if len(state_rows) != len(worksheet_rows):
        errors.append(f"expected {len(worksheet_rows)} rows, found {len(state_rows)}")

    by_row = {
        item.get("row"): item
        for item in state_rows
        if isinstance(item, dict) and isinstance(item.get("row"), int)
    }
    for expected in worksheet_rows:
        number = expected["row"]
        item = by_row.get(number)
        if item is None:
            errors.append(f"row {number}: missing")
            continue
        for key in ("source", "item", "field", "text"):
            if item.get(key) != expected[key]:
                errors.append(f"row {number}: {key} differs from worksheet")
        result = item.get("result")
        if result not in ROW_RESULTS:
            errors.append(f"row {number}: invalid result {result!r}")
        if require_complete and result == "NOT TESTED":
            errors.append(f"row {number}: still NOT TESTED")
        if result == "FAIL" and not str(item.get("notes", "")).strip():
            errors.append(f"row {number}: FAIL requires notes / issue reference")

    if require_complete:
        for field in ("reviewer", "review_date", "intended_context"):
            if not str(state.get(field, "")).strip():
                errors.append(f"{field} is required for completed review")
    return errors


def review_interactively(
    state_path: Path,
    worksheet_path: Path,
    *,
    start_row: int | None = None,
) -> int:
    candidate_sha, rows = parse_worksheet(worksheet_path)
    state = load_or_create_state(state_path, candidate_sha, rows)
    errors = validate_state(state, candidate_sha, rows, require_complete=False)
    if errors:
        raise ValueError("\n".join(errors))

    state_rows = state["rows"]
    assert isinstance(state_rows, list)

    if not str(state.get("reviewer", "")).strip():
        state["reviewer"] = input("Reviewer / role: ").strip()
    if not str(state.get("review_date", "")).strip():
        state["review_date"] = input("Review date (YYYY-MM-DD): ").strip()
    save_state(state_path, state)

    for item in state_rows:
        assert isinstance(item, dict)
        number = int(item["row"])
        if start_row is not None and number < start_row:
            continue
        if item.get("result") in {"PASS", "FAIL"}:
            continue

        print("\n" + "=" * 72)
        print(f"Row {number}/{len(state_rows)}")
        print(f"Source: {item['source']}")
        print(f"Item:   {item['item']}")
        print(f"Field:  {item['field']}")
        print(f"Text:   {item['text']}")
        print("Criteria: age/grade clarity; semantic clarity; non-humiliating/non-manipulative;")
        print("          no unsupported claims; no pressure-to-continue; behavior consistency.")

        while True:
            answer = input("[p]ass / [f]ail / [s]kip / [q]uit: ").strip().lower()
            if answer in {"p", "pass"}:
                item["result"] = "PASS"
                item["notes"] = input("Optional notes: ").strip()
                break
            if answer in {"f", "fail"}:
                notes = input("Required issue / notes: ").strip()
                if not notes:
                    print("FAIL requires notes.")
                    continue
                item["result"] = "FAIL"
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

    errors = validate_state(state, candidate_sha, rows, require_complete=True)
    if errors:
        print("\nReview is still BLOCKED:")
        for error in errors:
            print(f"- {error}")
        return 2

    print(f"\nAll {len(rows)} rows reviewed. Validation PASS.")
    print(f"Evidence file: {state_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail-closed interactive Stage 8 human content review helper."
    )
    parser.add_argument("--worksheet", type=Path, default=DEFAULT_WORKSHEET)
    sub = parser.add_subparsers(dest="command", required=True)

    init_parser = sub.add_parser("init", help="Create a NOT TESTED review evidence file")
    init_parser.add_argument("state", type=Path)

    review_parser = sub.add_parser("review", help="Interactively review/resume rows")
    review_parser.add_argument("state", type=Path)
    review_parser.add_argument("--start-row", type=int)

    validate_parser = sub.add_parser("validate", help="Validate review evidence")
    validate_parser.add_argument("state", type=Path)
    validate_parser.add_argument("--require-complete", action="store_true")

    args = parser.parse_args()
    candidate_sha, rows = parse_worksheet(args.worksheet)

    if args.command == "init":
        if args.state.exists():
            raise SystemExit(f"Refusing to overwrite existing evidence file: {args.state}")
        save_state(args.state, new_state(candidate_sha, rows))
        print(f"Created {args.state} with {len(rows)} NOT TESTED rows.")
        return 0

    if args.command == "review":
        return review_interactively(args.state, args.worksheet, start_row=args.start_row)

    state = json.loads(args.state.read_text(encoding="utf-8"))
    errors = validate_state(
        state,
        candidate_sha,
        rows,
        require_complete=args.require_complete,
    )
    if errors:
        print("BLOCKED")
        for error in errors:
            print(f"- {error}")
        return 2

    print(f"PASS: evidence matches candidate {candidate_sha}; rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
