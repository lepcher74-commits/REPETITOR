from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from repetitor.domain import Problem


@dataclass(frozen=True, slots=True)
class Remediation:
    skill_id: str
    title_ru: str
    explanation_ru: str
    return_problem_id: str
    exit_mastery: float
    problems: tuple[Problem, ...]


class RemediationLoadError(ValueError):
    pass


def _problem(data: dict[str, Any]) -> Problem:
    return Problem(
        id=str(data["id"]),
        primary_skill=str(data["primary_skill"]),
        purpose=str(data["purpose"]),
        prompt_ru=str(data["prompt_ru"]),
        verifier=dict(data["verifier"]),
    )


def load_remediations(path: Path) -> dict[str, Remediation]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise RemediationLoadError(f"Cannot load {path}: {exc}") from exc
    raw = data.get("remediations") if isinstance(data, dict) else None
    if not isinstance(raw, list):
        raise RemediationLoadError(f"{path}: 'remediations' must be a list")

    result = {}
    for item in raw:
        problems = tuple(_problem(p) for p in item.get("problems", []))
        if not problems:
            raise RemediationLoadError(f"{item.get('skill_id')}: problems required")
        skill_id = str(item["skill_id"])
        if any(p.primary_skill != skill_id for p in problems):
            raise RemediationLoadError(f"{skill_id}: every problem must target remediation skill")
        exit_mastery = float(item.get("exit_mastery", 0.45))
        if not 0.0 <= exit_mastery <= 1.0:
            raise RemediationLoadError(f"{skill_id}: invalid exit_mastery")
        result[skill_id] = Remediation(
            skill_id=skill_id,
            title_ru=str(item["title_ru"]),
            explanation_ru=str(item["explanation_ru"]),
            return_problem_id=str(item["return_problem_id"]),
            exit_mastery=exit_mastery,
            problems=problems,
        )
    return result
