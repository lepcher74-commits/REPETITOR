from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True, slots=True)
class Choice:
    id: str
    title_ru: str


@dataclass(frozen=True, slots=True)
class ModuleManifest:
    id: str
    subject: Choice
    grade: int
    primary_skill: Choice
    prerequisites: tuple[str, ...]
    goals: tuple[Choice, ...]
    diagnostic_route: str
    remediation_route: str
    review_problem_by_skill: dict[str, str]


def load_module_manifest(path: Path) -> ModuleManifest:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    return ModuleManifest(
        id=str(raw["id"]),
        subject=Choice(str(raw["subject"]["id"]), str(raw["subject"]["title_ru"])),
        grade=int(raw["grade"]),
        primary_skill=Choice(str(raw["primary_skill"]["id"]), str(raw["primary_skill"]["title_ru"])),
        prerequisites=tuple(str(x) for x in raw.get("prerequisites", ())),
        goals=tuple(Choice(str(x["id"]), str(x["title_ru"])) for x in raw["goals"]),
        diagnostic_route=str(raw["routes"]["diagnostic"]),
        remediation_route=str(raw["routes"]["remediation"]),
        review_problem_by_skill={str(k): str(v) for k, v in raw.get("review_problem_by_skill", {}).items()},
    )
