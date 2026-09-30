from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QStackedWidget, QVBoxLayout, QWidget,
)

from repetitor.application.diagnostic import DiagnosticRouter
from repetitor.application.remediation import load_remediations
from repetitor.application.session import LearningSessionService
from repetitor.content import load_problems
from repetitor.domain import KnowledgeState
from repetitor.persistence import (
    SQLiteLearningRepository, SQLiteProfileRepository, StudentProfile,
)


STUDENT_ID = "local-student"
SKILL = "math.g6.fractions.add_unlike"
PREREQS = ("math.g6.fractions.equivalent", "math.g6.fractions.common_denominator")


class RepetitorWindow(QMainWindow):
    def __init__(self, data_dir: Path, content_dir: Path) -> None:
        super().__init__()
        self.setWindowTitle("REPETITOR")
        self.resize(920, 640)

        data_dir.mkdir(parents=True, exist_ok=True)
        db = data_dir / "repetitor.sqlite3"
        self.learning = SQLiteLearningRepository(db)
        self.learning.initialize()
        self.profiles = SQLiteProfileRepository(db)
        self.profiles.initialize()

        self.problems = load_problems(content_dir / "problems.yaml")
        self.remediations = load_remediations(content_dir / "remediation.yaml")
        self.problem_by_id = {p.id: p for p in self.problems}
        self.problem = self.problem_by_id[self.router.start_problem_id]
        self.router = DiagnosticRouter.from_yaml(content_dir / "diagnostic_route.yaml")
        self.session = LearningSessionService(self.learning, {SKILL: PREREQS})
        self.hint_level: int | None = None
        self.remediation_skill: str | None = None
        self.return_problem_id: str | None = None
        self.remediation_index = 0

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.onboarding = self._build_onboarding()
        self.diagnostic = self._build_diagnostic()
        self.progress = self._build_progress()
        self.remediation = self._build_remediation()
        for page in (self.onboarding, self.diagnostic, self.remediation, self.progress):
            self.stack.addWidget(page)

        if self.profiles.get(STUDENT_ID):
            self.stack.setCurrentWidget(self.diagnostic)

    def _page(self, title: str, subtitle: str) -> tuple[QWidget, QVBoxLayout]:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(72, 52, 72, 52)
        layout.setSpacing(18)
        heading = QLabel(title)
        heading.setObjectName("heading")
        sub = QLabel(subtitle)
        sub.setWordWrap(True)
        sub.setObjectName("subtitle")
        layout.addWidget(heading)
        layout.addWidget(sub)
        return page, layout

    def _build_onboarding(self) -> QWidget:
        page, layout = self._page(
            "Начнём учиться",
            "Три решения — и сразу короткая диагностика. Настройки можно уточнить позже.",
        )
        self.subject = QComboBox(); self.subject.addItem("Математика", "mathematics")
        self.grade = QComboBox(); self.grade.addItem("6 класс", 6)
        self.goal = QComboBox()
        self.goal.addItem("Догнать программу", "catch_up")
        self.goal.addItem("Углубить знания", "deepen")
        self.goal.addItem("Олимпиадный путь", "olympiad")
        for label, widget in (
            ("Предмет", self.subject), ("Класс", self.grade), ("Цель", self.goal)
        ):
            layout.addWidget(QLabel(label)); layout.addWidget(widget)
        start = QPushButton("Начать диагностику")
        start.clicked.connect(self._start_diagnostic)
        layout.addWidget(start)
        layout.addStretch()
        return page

    def _build_diagnostic(self) -> QWidget:
        page, layout = self._page(
            "Короткая диагностика",
            "Это не контрольная. Задача нужна, чтобы понять, с какого места лучше начать.",
        )
        card = QFrame(); card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        self.problem_label = QLabel(self.problem.prompt_ru)
        self.problem_label.setObjectName("problem")
        self.answer = QLineEdit()
        self.answer.setPlaceholderText("Например: 5/6")
        self.answer.returnPressed.connect(self._submit)
        self.feedback = QLabel("")
        self.feedback.setWordWrap(True)
        self.feedback.setObjectName("feedback")
        submit = QPushButton("Проверить")
        submit.clicked.connect(self._submit)
        hint = QPushButton("Нужна подсказка")
        hint.setObjectName("secondary")
        hint.clicked.connect(self._hint)
        row = QHBoxLayout(); row.addWidget(submit); row.addWidget(hint)
        card_layout.addWidget(self.problem_label)
        card_layout.addWidget(self.answer)
        card_layout.addLayout(row)
        card_layout.addWidget(self.feedback)
        layout.addWidget(card)
        progress = QPushButton("Мой прогресс")
        progress.setObjectName("secondary")
        progress.clicked.connect(self._show_progress)
        layout.addWidget(progress)
        layout.addStretch()
        return page

    def _build_remediation(self) -> QWidget:
        page, layout = self._page(
            "Восстановим фундамент",
            "Коротко разберём навык, который мешает двигаться дальше.",
        )
        self.remediation_title = QLabel()
        self.remediation_title.setObjectName("problem")
        self.remediation_explanation = QLabel()
        self.remediation_explanation.setWordWrap(True)
        self.remediation_prompt = QLabel()
        self.remediation_prompt.setWordWrap(True)
        self.remediation_answer = QLineEdit()
        self.remediation_answer.returnPressed.connect(self._submit_remediation)
        self.remediation_feedback = QLabel()
        self.remediation_feedback.setWordWrap(True)
        check = QPushButton("Проверить и вернуться")
        check.clicked.connect(self._submit_remediation)
        for widget in (
            self.remediation_title, self.remediation_explanation,
            self.remediation_prompt, self.remediation_answer,
            self.remediation_feedback, check,
        ):
            layout.addWidget(widget)
        layout.addStretch()
        return page

    def _start_remediation(self, skill_id: str, return_problem_id: str) -> None:
        step = self.remediations.get(skill_id)
        if step is None:
            self.feedback.setText(
                self.feedback.text() + "\n\nДля этого prerequisite контент remediation ещё не создан."
            )
            return
        self.remediation_skill = skill_id
        self.return_problem_id = step.return_problem_id
        self.remediation_index = 0
        self.remediation_title.setText(step.title_ru)
        self.remediation_explanation.setText(step.explanation_ru)
        self.remediation_prompt.setText(step.problems[0].prompt_ru)
        self.remediation_answer.clear()
        self.remediation_feedback.clear()
        self.stack.setCurrentWidget(self.remediation)
        self.remediation_answer.setFocus()

    def _submit_remediation(self) -> None:
        if not self.remediation_skill:
            return
        step = self.remediations[self.remediation_skill]
        raw = self.remediation_answer.text().strip()
        outcome = self.session.submit(
            student_id=STUDENT_ID,
            problem=step.problems[self.remediation_index],
            answer=raw,
            occurred_at=datetime.now(timezone.utc),
        )
        result = outcome.verification
        if not result.correct:
            self.remediation_feedback.setText(
                "Пока не получилось. Перечитай объяснение и попробуй ещё раз."
            )
            return

        state = self.learning.get_state(STUDENT_ID, step.skill_id)
        self.remediation_index += 1
        if self.remediation_index < len(step.problems):
            self.remediation_answer.clear()
            self.remediation_prompt.setText(step.problems[self.remediation_index].prompt_ru)
            self.remediation_feedback.setText(
                "Верно. Это одно evidence; нужна ещё проверка, прежде чем возвращаться."
            )
            return

        if state is None or state.mastery < step.exit_mastery:
            self.remediation_index = max(1, len(step.problems) - 1)
            self.remediation_answer.clear()
            self.remediation_prompt.setText(step.problems[self.remediation_index].prompt_ru)
            self.remediation_feedback.setText(
                "Ответы улучшаются, но evidence пока недостаточно. Повторим независимую проверку."
            )
            return

        if self.return_problem_id:
            self.problem = self.problem_by_id[self.return_problem_id]
            self.problem_label.setText(self.problem.prompt_ru)
        self.answer.clear()
        self.answer.setEnabled(True)
        self.hint_level = None
        self.stack.setCurrentWidget(self.diagnostic)
        self.feedback.setText(
            "Prerequisite восстановлен по нескольким проверяемым evidence. Продолжаем основной маршрут."
        )

    def _build_progress(self) -> QWidget:
        page, layout = self._page(
            "Мой прогресс",
            "Показываем знания, самостоятельность и перенос — не время в приложении.",
        )
        self.progress_text = QLabel()
        self.progress_text.setWordWrap(True)
        self.progress_text.setObjectName("progress")
        layout.addWidget(self.progress_text)
        back = QPushButton("Продолжить учиться")
        back.clicked.connect(lambda: self.stack.setCurrentWidget(self.diagnostic))
        layout.addWidget(back)
        layout.addStretch()
        return page

    def _start_diagnostic(self) -> None:
        self.profiles.save(StudentProfile(
            STUDENT_ID,
            self.subject.currentData(),
            self.grade.currentData(),
            self.goal.currentData(),
        ))
        self.stack.setCurrentWidget(self.diagnostic)
        self.answer.setFocus()

    def _hint(self) -> None:
        hints = self.problem.hints
        if not hints:
            self.feedback.setText("Для этой диагностической задачи подсказка не раскрывается сразу.")
            return
        current = 0 if self.hint_level is None else self.hint_level
        next_hint = next((h for h in hints if h.level > current), None)
        if next_hint:
            self.hint_level = next_hint.level
            self.feedback.setText("Подсказка: " + next_hint.text_ru)

    def _submit(self) -> None:
        raw = self.answer.text().strip()
        if not raw:
            self.feedback.setText("Сначала введи ответ.")
            return
        outcome = self.session.submit(
            student_id=STUDENT_ID,
            problem=self.problem,
            answer=raw,
            occurred_at=datetime.now(timezone.utc),
            hint_level=self.hint_level,
            answer_revealing_hint=False,
        )
        if outcome.verification.correct:
            self.feedback.setText("Верно. Я учту, что ты решил эту задачу самостоятельно.")
        elif outcome.verification.mathematically_equivalent:
            self.feedback.setText("По значению верно, но проверь требуемую форму ответа.")
        elif outcome.misconception_hypothesis:
            self.feedback.setText(
                "Ответ не совпал. Я заметил возможную закономерность, но одной ошибки "
                "недостаточно для вывода — проверим её отдельной задачей."
            )
        else:
            self.feedback.setText("Пока не совпало. Проверим, на каком шаге возникла трудность.")
        decision = self.router.decide(
            problem=self.problem,
            correct=outcome.verification.correct,
            misconception_hypothesis=outcome.misconception_hypothesis,
        )
        self._refresh_progress()
        if decision.next_problem_id:
            self.problem = self.problem_by_id[decision.next_problem_id]
            self.problem_label.setText(self.problem.prompt_ru)
            self.answer.clear()
            self.hint_level = None
            self.feedback.setText(self.feedback.text() + "\n\n" + decision.message_ru)
        elif decision.phase == "remediation":
            self.answer.setEnabled(False)
            self.feedback.setText(self.feedback.text() + "\n\n" + decision.message_ru)
            if self.problem.id == "frac.add.probe.equivalent":
                self._start_remediation(
                    "math.g6.fractions.equivalent",
                    "frac.add.probe.lcm",
                )
            elif self.problem.id == "frac.add.probe.lcm":
                self._start_remediation(
                    "math.prereq.lcm",
                    "frac.add.guided.001",
                )
        else:
            self.answer.setEnabled(False)
            self.feedback.setText(self.feedback.text() + "\n\n" + decision.message_ru)

    def _refresh_progress(self) -> None:
        state = self.learning.get_state(STUDENT_ID, SKILL)
        if state is None:
            self.progress_text.setText("Пока недостаточно данных.")
            return
        self.progress_text.setText(
            f"Навык: сложение дробей с разными знаменателями\n\n"
            f"Освоение: {state.mastery:.0%}\n"
            f"Самостоятельность: {state.independence:.0%}\n"
            f"Перенос: {state.transfer:.0%}\n"
            f"Свидетельств: {state.evidence_count}"
        )

    def _show_progress(self) -> None:
        self._refresh_progress()
        self.stack.setCurrentWidget(self.progress)


def run(data_dir: Path, content_dir: Path) -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget { font-size: 17px; }
        QMainWindow { background: #f6f7f9; }
        QLabel#heading { font-size: 32px; font-weight: 700; }
        QLabel#subtitle { font-size: 17px; }
        QLabel#problem { font-size: 28px; font-weight: 600; padding: 20px 0; }
        QFrame#card { background: white; border-radius: 14px; padding: 20px; }
        QLineEdit, QComboBox { min-height: 42px; padding: 4px 10px; }
        QPushButton { min-height: 44px; padding: 4px 18px; font-weight: 600; }
        QPushButton#secondary { font-weight: 400; }
        QLabel#feedback, QLabel#progress { padding: 12px 0; }
    """)
    window = RepetitorWindow(data_dir, content_dir)
    window.show()
    return app.exec()
