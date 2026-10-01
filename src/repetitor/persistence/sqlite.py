from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from repetitor.domain import AttemptEvidence, KnowledgeState, ReviewItem


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS attempts (
    id TEXT PRIMARY KEY,
    student_id TEXT NOT NULL,
    problem_id TEXT NOT NULL,
    skill_id TEXT NOT NULL,
    occurred_at TEXT NOT NULL,
    correct INTEGER NOT NULL CHECK(correct IN (0, 1)),
    purpose TEXT NOT NULL,
    hint_level INTEGER,
    answer_revealing_hint INTEGER NOT NULL DEFAULT 0 CHECK(answer_revealing_hint IN (0, 1)),
    transfer INTEGER NOT NULL DEFAULT 0 CHECK(transfer IN (0, 1)),
    misconception TEXT,
    prerequisite_failure INTEGER NOT NULL DEFAULT 0 CHECK(prerequisite_failure IN (0, 1))
);

CREATE TABLE IF NOT EXISTS knowledge_states (
    student_id TEXT NOT NULL,
    skill_id TEXT NOT NULL,
    mastery REAL NOT NULL,
    confidence REAL NOT NULL,
    independence REAL NOT NULL,
    transfer REAL NOT NULL,
    retention REAL NOT NULL,
    evidence_count INTEGER NOT NULL,
    updated_at TEXT,
    PRIMARY KEY(student_id, skill_id)
);

CREATE TABLE IF NOT EXISTS session_state (
    student_id TEXT PRIMARY KEY,
    module_id TEXT NOT NULL,
    problem_id TEXT,
    phase TEXT NOT NULL,
    remediation_skill_id TEXT,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS review_queue (
    student_id TEXT NOT NULL,
    skill_id TEXT NOT NULL,
    due_at TEXT NOT NULL,
    reason TEXT NOT NULL,
    PRIMARY KEY(student_id, skill_id)
);
"""


class SQLiteLearningRepository:
    def __init__(self, path: str | Path) -> None:
        self.path = str(path)

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(SCHEMA)

    def save_submission(
        self,
        evidence: AttemptEvidence,
        state: KnowledgeState,
        review: ReviewItem,
    ) -> None:
        """Persist one learning submission atomically."""
        with self.connect() as connection:
            connection.execute(
                """INSERT INTO attempts
                (id, student_id, problem_id, skill_id, occurred_at, correct, purpose,
                 hint_level, answer_revealing_hint, transfer, misconception, prerequisite_failure)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    evidence.id, evidence.student_id, evidence.problem_id, evidence.skill_id,
                    evidence.occurred_at.isoformat(), int(evidence.correct), evidence.purpose,
                    evidence.hint_level, int(evidence.answer_revealing_hint), int(evidence.transfer),
                    evidence.misconception, int(evidence.prerequisite_failure),
                ),
            )
            connection.execute(
                """INSERT INTO knowledge_states
                (student_id, skill_id, mastery, confidence, independence, transfer,
                 retention, evidence_count, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(student_id, skill_id) DO UPDATE SET
                    mastery=excluded.mastery, confidence=excluded.confidence,
                    independence=excluded.independence, transfer=excluded.transfer,
                    retention=excluded.retention, evidence_count=excluded.evidence_count,
                    updated_at=excluded.updated_at""",
                (
                    state.student_id, state.skill_id, state.mastery, state.confidence,
                    state.independence, state.transfer, state.retention, state.evidence_count,
                    state.updated_at.isoformat() if state.updated_at else None,
                ),
            )
            connection.execute(
                """INSERT INTO review_queue (student_id, skill_id, due_at, reason)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(student_id, skill_id) DO UPDATE SET
                    due_at=excluded.due_at, reason=excluded.reason""",
                (review.student_id, review.skill_id, review.due_at.isoformat(), review.reason),
            )

    def add_attempt(self, evidence: AttemptEvidence) -> None:
        with self.connect() as connection:
            connection.execute(
                """INSERT INTO attempts
                (id, student_id, problem_id, skill_id, occurred_at, correct, purpose,
                 hint_level, answer_revealing_hint, transfer, misconception, prerequisite_failure)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    evidence.id,
                    evidence.student_id,
                    evidence.problem_id,
                    evidence.skill_id,
                    evidence.occurred_at.isoformat(),
                    int(evidence.correct),
                    evidence.purpose,
                    evidence.hint_level,
                    int(evidence.answer_revealing_hint),
                    int(evidence.transfer),
                    evidence.misconception,
                    int(evidence.prerequisite_failure),
                ),
            )

    def save_state(self, state: KnowledgeState) -> None:
        with self.connect() as connection:
            connection.execute(
                """INSERT INTO knowledge_states
                (student_id, skill_id, mastery, confidence, independence, transfer,
                 retention, evidence_count, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(student_id, skill_id) DO UPDATE SET
                    mastery=excluded.mastery,
                    confidence=excluded.confidence,
                    independence=excluded.independence,
                    transfer=excluded.transfer,
                    retention=excluded.retention,
                    evidence_count=excluded.evidence_count,
                    updated_at=excluded.updated_at""",
                (
                    state.student_id, state.skill_id, state.mastery, state.confidence,
                    state.independence, state.transfer, state.retention,
                    state.evidence_count,
                    state.updated_at.isoformat() if state.updated_at else None,
                ),
            )

    def get_state(self, student_id: str, skill_id: str) -> KnowledgeState | None:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM knowledge_states WHERE student_id=? AND skill_id=?",
                (student_id, skill_id),
            ).fetchone()
        if row is None:
            return None
        return KnowledgeState(
            student_id=row["student_id"],
            skill_id=row["skill_id"],
            mastery=row["mastery"],
            confidence=row["confidence"],
            independence=row["independence"],
            transfer=row["transfer"],
            retention=row["retention"],
            evidence_count=row["evidence_count"],
            updated_at=datetime.fromisoformat(row["updated_at"]) if row["updated_at"] else None,
        )



    def save_session_state(
        self,
        student_id: str,
        module_id: str,
        problem_id: str | None,
        phase: str,
        remediation_skill_id: str | None,
        updated_at: datetime,
    ) -> None:
        with self.connect() as connection:
            connection.execute(
                """INSERT INTO session_state
                (student_id, module_id, problem_id, phase, remediation_skill_id, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(student_id) DO UPDATE SET
                    module_id=excluded.module_id, problem_id=excluded.problem_id,
                    phase=excluded.phase, remediation_skill_id=excluded.remediation_skill_id,
                    updated_at=excluded.updated_at""",
                (student_id, module_id, problem_id, phase, remediation_skill_id, updated_at.isoformat()),
            )

    def get_session_state(self, student_id: str) -> dict[str, str | None] | None:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM session_state WHERE student_id=?", (student_id,)
            ).fetchone()
        return dict(row) if row is not None else None

    def attempted_problem_ids(self, student_id: str, skill_id: str | None = None) -> set[str]:
        query = "SELECT DISTINCT problem_id FROM attempts WHERE student_id=?"
        params: tuple[str, ...] = (student_id,)
        if skill_id is not None:
            query += " AND skill_id=?"
            params = (student_id, skill_id)
        with self.connect() as connection:
            rows = connection.execute(query, params).fetchall()
        return {str(row["problem_id"]) for row in rows}

    def save_review(self, item: ReviewItem) -> None:
        with self.connect() as connection:
            connection.execute(
                """INSERT INTO review_queue (student_id, skill_id, due_at, reason)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(student_id, skill_id) DO UPDATE SET
                    due_at=excluded.due_at, reason=excluded.reason""",
                (item.student_id, item.skill_id, item.due_at.isoformat(), item.reason),
            )

    def due_reviews(self, student_id: str, now: datetime) -> list[ReviewItem]:
        with self.connect() as connection:
            rows = connection.execute(
                """SELECT * FROM review_queue
                   WHERE student_id=? AND due_at<=?
                   ORDER BY due_at""",
                (student_id, now.isoformat()),
            ).fetchall()
        return [
            ReviewItem(
                student_id=row["student_id"],
                skill_id=row["skill_id"],
                due_at=datetime.fromisoformat(row["due_at"]),
                reason=row["reason"],
            )
            for row in rows
        ]
