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
    review_problems_by_skill: dict[str, tuple[str, ...]]
    learning_sequence: tuple[str, ...]


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
        review_problems_by_skill={
            str(k): tuple(str(problem_id) for problem_id in v)
            for k, v in raw.get("review_problems_by_skill", {}).items()
        },
        learning_sequence=tuple(str(x) for x in raw.get("learning_sequence", ())),
    )


def discover_skill_directories(content_root: Path) -> dict[str, Path]:
    """Map stable skill IDs to their content directories without subject-specific code."""
    from repetitor.content.loader import load_skill

    directories: dict[str, Path] = {}
    for skill_path in content_root.rglob("skill.yaml"):
        skill = load_skill(skill_path)
        directories[skill.id] = skill_path.parent
    return directories


def load_sequence_problems(module: ModuleManifest, content_root: Path):
    """Load problem pools for every skill declared learner-reachable by the module."""
    from repetitor.content.loader import load_problems

    directories = discover_skill_directories(content_root)
    pools = {}
    for skill_id in module.learning_sequence:
        if skill_id not in directories:
            raise ValueError(f"Learning sequence references unknown skill: {skill_id}")
        pools[skill_id] = load_problems(directories[skill_id] / "problems.yaml")
    return pools


def next_sequence_skill(module: ModuleManifest, current_skill_id: str) -> str | None:
    """Return the next declared learner skill, if the current one is in the sequence."""
    try:
        index = module.learning_sequence.index(current_skill_id)
    except ValueError:
        return None
    next_index = index + 1
    return module.learning_sequence[next_index] if next_index < len(module.learning_sequence) else None


def load_sequence_prerequisites(module: ModuleManifest, content_root: Path) -> dict[str, tuple[str, ...]]:
    """Load each learner-reachable skill's declared prerequisite DAG edges."""
    from repetitor.content.loader import load_skill

    directories = discover_skill_directories(content_root)
    prerequisites: dict[str, tuple[str, ...]] = {}
    for skill_id in module.learning_sequence:
        if skill_id not in directories:
            raise ValueError(f"Learning sequence references unknown skill: {skill_id}")
        skill = load_skill(directories[skill_id] / "skill.yaml")
        prerequisites[skill_id] = tuple(skill.prerequisites)
    return prerequisites
