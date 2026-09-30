from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class Hint:
    level: int
    kind: str
    text_ru: str

    @property
    def answer_revealing(self) -> bool:
        return self.kind in {"worked_step", "worked_example"}


@dataclass(frozen=True, slots=True)
class Skill:
    id: str
    subject: str
    grade_band: str
    module: str
    title_ru: str
    objectives: tuple[str, ...]
    prerequisites: tuple[str, ...]
    secondary_prerequisites: tuple[str, ...] = ()
    mastery_policy: str = ""
    misconceptions: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Problem:
    id: str
    primary_skill: str
    purpose: str
    prompt_ru: str
    verifier: dict[str, Any]
    secondary_skills: tuple[str, ...] = ()
    representation: str | None = None
    transfer: bool = False
    choices: tuple[str, ...] = ()
    hints: tuple[Hint, ...] = ()
    misconception_probes: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class VerificationResult:
    correct: bool
    mathematically_equivalent: bool
    instruction_satisfied: bool
    normalized_answer: str | None = None
    feedback_code: str | None = None
