from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


@dataclass(frozen=True, slots=True)
class AttemptEvidence:
    id: str
    student_id: str
    problem_id: str
    skill_id: str
    occurred_at: datetime
    correct: bool
    purpose: str
    hint_level: int | None = None
    answer_revealing_hint: bool = False
    transfer: bool = False
    misconception: str | None = None
    prerequisite_failure: bool = False


@dataclass(frozen=True, slots=True)
class KnowledgeState:
    student_id: str
    skill_id: str
    mastery: float = 0.0
    confidence: float = 0.0
    independence: float = 0.0
    transfer: float = 0.0
    retention: float = 0.0
    evidence_count: int = 0
    updated_at: datetime | None = None

    def bounded(self) -> "KnowledgeState":
        return replace(
            self,
            mastery=_clamp(self.mastery),
            confidence=_clamp(self.confidence),
            independence=_clamp(self.independence),
            transfer=_clamp(self.transfer),
            retention=_clamp(self.retention),
        )


@dataclass(frozen=True, slots=True)
class ReviewItem:
    student_id: str
    skill_id: str
    due_at: datetime
    reason: str
