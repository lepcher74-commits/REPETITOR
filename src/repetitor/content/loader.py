from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from repetitor.domain import Hint, Problem, Skill


class ContentLoadError(ValueError):
    pass


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ContentLoadError(f"Cannot load {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ContentLoadError(f"{path} must contain a YAML mapping")
    return data


def load_skill(path: Path) -> Skill:
    data = _read_yaml(path)
    required = ("id", "subject", "grade_band", "module", "title_ru", "objectives", "prerequisites")
    missing = [key for key in required if key not in data]
    if missing:
        raise ContentLoadError(f"{path}: missing skill fields: {', '.join(missing)}")
    return Skill(
        id=str(data["id"]),
        subject=str(data["subject"]),
        grade_band=str(data["grade_band"]),
        module=str(data["module"]),
        title_ru=str(data["title_ru"]),
        objectives=tuple(map(str, data["objectives"])),
        prerequisites=tuple(map(str, data["prerequisites"])),
        secondary_prerequisites=tuple(map(str, data.get("secondary_prerequisites", []))),
        mastery_policy=str(data.get("mastery_policy", "")),
        misconceptions=tuple(map(str, data.get("misconceptions", []))),
    )


def _problem_from_data(data: dict[str, Any], source: Path) -> Problem:
    required = ("id", "primary_skill", "purpose", "prompt_ru", "verifier")
    missing = [key for key in required if key not in data]
    if missing:
        raise ContentLoadError(f"{source}: problem missing fields: {', '.join(missing)}")
    hints = tuple(
        Hint(level=int(h["level"]), kind=str(h["kind"]), text_ru=str(h["text_ru"]))
        for h in data.get("hints", [])
    )
    return Problem(
        id=str(data["id"]),
        primary_skill=str(data["primary_skill"]),
        purpose=str(data["purpose"]),
        prompt_ru=str(data["prompt_ru"]),
        verifier=dict(data["verifier"]),
        secondary_skills=tuple(map(str, data.get("secondary_skills", []))),
        representation=data.get("representation"),
        transfer=bool(data.get("transfer", False)),
        choices=tuple(map(str, data.get("choices", []))),
        hints=hints,
        misconception_probes={str(k): str(v) for k, v in data.get("misconception_probes", {}).items()},
    )


def load_problems(path: Path) -> tuple[Problem, ...]:
    data = _read_yaml(path)
    raw = data.get("problems")
    if not isinstance(raw, list):
        raise ContentLoadError(f"{path}: 'problems' must be a list")
    return tuple(_problem_from_data(item, path) for item in raw)
