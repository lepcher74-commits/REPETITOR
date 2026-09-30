from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from repetitor.domain import Problem


@dataclass(frozen=True, slots=True)
class DiagnosticDecision:
    next_problem_id: str | None
    phase: str
    message_ru: str
    remediation_skill_id: str | None = None


@dataclass(frozen=True, slots=True)
class DiagnosticRule:
    problem_id: str
    when: dict[str, Any]
    decision: DiagnosticDecision


class DiagnosticRouter:
    """Generic declarative router. Subject-specific IDs live in content only."""

    def __init__(
        self,
        rules: tuple[DiagnosticRule, ...],
        default: DiagnosticDecision,
        start_problem_id: str,
    ) -> None:
        self.rules = rules
        self.default = default
        self.start_problem_id = start_problem_id

    @classmethod
    def from_yaml(cls, path: Path) -> "DiagnosticRouter":
        data = yaml.safe_load(path.read_text(encoding="utf-8"))

        def decision(raw: dict[str, Any]) -> DiagnosticDecision:
            return DiagnosticDecision(
                next_problem_id=raw.get("next_problem_id"),
                phase=str(raw["phase"]),
                message_ru=str(raw["message_ru"]),
                remediation_skill_id=raw.get("remediation_skill_id"),
            )

        rules = tuple(
            DiagnosticRule(
                problem_id=str(raw["problem_id"]),
                when=dict(raw.get("when", {})),
                decision=decision(raw),
            )
            for raw in data["rules"]
        )
        return cls(rules, decision(data["default"]), str(data["start_problem_id"]))

    def decide(
        self,
        *,
        problem: Problem,
        correct: bool,
        misconception_hypothesis: str | None,
    ) -> DiagnosticDecision:
        facts = {"correct": correct, "misconception": misconception_hypothesis}
        for rule in self.rules:
            if rule.problem_id != problem.id:
                continue
            if all(facts.get(key) == value for key, value in rule.when.items()):
                return rule.decision
        return self.default
