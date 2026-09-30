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
    problem: Problem


class RemediationLoadError(ValueError):
    pass


def load_remediations(path: Path) -> dict[str, Remediation]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise RemediationLoadError(f"Cannot load {path}: {exc}") from exc

    raw = data.get("remediations") if isinstance(data, dict) else None
    if not isinstance(raw, list):
        raise RemediationLoadError(f"{path}: 'remediations' must be a list")

    result: dict[str, Remediation] = {}
    for item in raw:
        problem_data: dict[str, Any] = item["problem"]
        problem = Problem(
            id=str(problem_data["id"]),
            primary_skill=str(problem_data["primary_skill"]),
            purpose=str(problem_data["purpose"]),
            prompt_ru=str(problem_data["prompt_ru"]),
            verifier=dict(problem_data["verifier"]),
        )
        skill_id = str(item["skill_id"])
        if problem.primary_skill != skill_id:
            raise RemediationLoadError(
                f"{problem.id}: primary_skill must equal remediation skill_id"
            )
        result[skill_id] = Remediation(
            skill_id=skill_id,
            title_ru=str(item["title_ru"]),
            explanation_ru=str(item["explanation_ru"]),
            return_problem_id=str(item["return_problem_id"]),
            problem=problem,
        )
    return result
