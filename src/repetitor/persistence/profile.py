from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class StudentProfile:
    id: str
    subject: str
    grade: int
    goal: str


class SQLiteProfileRepository:
    def __init__(self, path: str | Path) -> None:
        self.path = str(path)

    def initialize(self) -> None:
        with sqlite3.connect(self.path) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id TEXT PRIMARY KEY,
                    subject TEXT NOT NULL,
                    grade INTEGER NOT NULL,
                    goal TEXT NOT NULL
                )
            """)

    def save(self, profile: StudentProfile) -> None:
        with sqlite3.connect(self.path) as connection:
            connection.execute(
                """INSERT INTO students (id, subject, grade, goal)
                   VALUES (?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                     subject=excluded.subject,
                     grade=excluded.grade,
                     goal=excluded.goal""",
                (profile.id, profile.subject, profile.grade, profile.goal),
            )

    def get(self, student_id: str) -> StudentProfile | None:
        with sqlite3.connect(self.path) as connection:
            row = connection.execute(
                "SELECT id, subject, grade, goal FROM students WHERE id=?",
                (student_id,),
            ).fetchone()
        return StudentProfile(*row) if row else None
