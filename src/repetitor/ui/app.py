from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAccessible, QAccessibleAnnouncementEvent, QAccessibleEvent
from PySide6.QtWidgets import (
    QApplication, QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMessageBox, QPushButton, QStackedWidget, QVBoxLayout, QWidget,
)

from repetitor.application.diagnostic import DiagnosticRouter
from repetitor.application.remediation import load_remediations
from repetitor.application.problem_selection import select_fresh_problem
from repetitor.application.session import LearningSessionService
from repetitor.content import load_problems
from repetitor.content.module import (
    load_module_manifest, load_sequence_prerequisites, load_sequence_problems,
    next_sequence_skill,
)
from repetitor.domain import KnowledgeState
from repetitor.diagnostics import record_startup_failure
from repetitor.persistence import (
    SQLiteLearningRepository, SQLiteProfileRepository, StudentProfile,
)


STUDENT_ID = "local-student"


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

        self.module = load_module_manifest(content_dir / "module.yaml")
        self.problems = load_problems(content_dir / "problems.yaml")
        content_root = content_dir.parents[2]
        self.sequence_pools = load_sequence_problems(self.module, content_root)
        self.remediations = load_remediations(content_dir / self.module.remediation_route)
        self.problem_by_id = {
            problem.id: problem
            for pool in self.sequence_pools.values()
            for problem in pool
        }
        self.problem_by_id.update({p.id: p for p in self.problems})
        self.router = DiagnosticRouter.from_yaml(content_dir / self.module.diagnostic_route)
        self.problem = self.problem_by_id[self.router.start_problem_id]
        sequence_prerequisites = load_sequence_prerequisites(self.module, content_root)
        self.session = LearningSessionService(self.learning, sequence_prerequisites)
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
            self._restore_session()

    def _save_session(self, *, phase: str, problem_id: str | None, remediation_skill_id: str | None = None) -> None:
        self.learning.save_session_state(
            STUDENT_ID,
            self.module.id,
            problem_id,
            phase,
            remediation_skill_id,
            datetime.now(timezone.utc),
        )

    def _restore_session(self) -> None:
        state = self.learning.get_session_state(STUDENT_ID)
        if not state or state["module_id"] != self.module.id:
            self.stack.setCurrentWidget(self.diagnostic)
            return
        problem_id = state["problem_id"]
        if state["phase"] == "remediation" and state["remediation_skill_id"] in self.remediations:
            self._start_remediation(str(state["remediation_skill_id"]))
            return
        if problem_id in self.problem_by_id:
            self.problem = self.problem_by_id[str(problem_id)]
            self.problem_label.setText(self.problem.prompt_ru)
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
        self.subject = QComboBox(); self.subject.setAccessibleName("Предмет"); self.subject.addItem(self.module.subject.title_ru, self.module.subject.id)
        self.grade = QComboBox(); self.grade.setAccessibleName("Класс"); self.grade.addItem(f"{self.module.grade} класс", self.module.grade)
        self.goal = QComboBox(); self.goal.setAccessibleName("Цель обучения")
        for goal in self.module.goals:
            self.goal.addItem(goal.title_ru, goal.id)
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
        self.answer.setAccessibleName("Ответ на текущую задачу")
        self.answer.setPlaceholderText("Например: 5/6")
        self.answer.returnPressed.connect(self._submit)
        self.feedback = QLabel("")
        self.feedback.setWordWrap(True)
        self.feedback.setObjectName("feedback")
        self.feedback.setAccessibleName("Результат проверки ответа")
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
        self.remediation_answer.setAccessibleName("Ответ на восстановительную задачу")
        self.remediation_answer.returnPressed.connect(self._submit_remediation)
        self.remediation_feedback = QLabel()
        self.remediation_feedback.setWordWrap(True)
        self.remediation_feedback.setAccessibleName("Результат восстановительной задачи")
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

    @staticmethod
    def _announce_feedback(label: QLabel) -> None:
        """Expose changed feedback to screen readers without stealing keyboard focus."""
        label.setAccessibleDescription(label.text())
        if label.text():
            # Announcement is the semantic API; Alert is a compatibility fallback
            # for screen readers that do not vocalize Announcement on Windows.
            QAccessible.updateAccessibility(QAccessibleAnnouncementEvent(label, label.text()))
            QAccessible.updateAccessibility(QAccessibleEvent(label, QAccessible.Alert))

    def _start_remediation(self, skill_id: str) -> None:
        step = self.remediations.get(skill_id)
        if step is None:
            self.feedback.setText(
                self.feedback.text() + "\n\nДля этого базового навыка восстановительные задания ещё не подготовлены."
            )
            return
        self.remediation_skill = skill_id
        self.return_problem_id = step.return_problem_id
        attempted = self.learning.attempted_problem_ids(STUDENT_ID, skill_id)
        fresh = select_fresh_problem(step.problems, attempted)
        if fresh is None:
            self.remediation_answer.setEnabled(False)
            self.remediation_feedback.setText(
                "Все подготовленные варианты этого навыка уже использованы. "
                "Не будем повтором повышать оценку; нужен новый вариант."
            )
            self._announce_feedback(self.remediation_feedback)
            self.stack.setCurrentWidget(self.remediation)
            return
        self.remediation_index = step.problems.index(fresh)
        self.remediation_answer.setEnabled(True)
        self.remediation_title.setText(step.title_ru)
        self.remediation_explanation.setText(step.explanation_ru)
        self.remediation_prompt.setText(fresh.prompt_ru)
        self.remediation_answer.clear()
        self.remediation_feedback.clear()
        self.stack.setCurrentWidget(self.remediation)
        self._save_session(
            phase="remediation",
            problem_id=fresh.id,
            remediation_skill_id=skill_id,
        )
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
            self._announce_feedback(self.remediation_feedback)
            return

        state = self.learning.get_state(STUDENT_ID, step.skill_id)
        attempted = self.learning.attempted_problem_ids(STUDENT_ID, step.skill_id)
        fresh = select_fresh_problem(step.problems, attempted)
        if fresh is not None:
            self.remediation_index = step.problems.index(fresh)
            self.remediation_answer.clear()
            self.remediation_prompt.setText(fresh.prompt_ru)
            self._save_session(
                phase="remediation",
                problem_id=fresh.id,
                remediation_skill_id=step.skill_id,
            )
            self.remediation_feedback.setText(
                "Верно. Это одна проверка; следующая будет на новом варианте."
            )
            self._announce_feedback(self.remediation_feedback)
            return

        if state is None or state.mastery < step.exit_mastery:
            self.remediation_answer.setEnabled(False)
            self.remediation_feedback.setText(
                "Проверок пока недостаточно для подтверждения навыка. "
                "Не будем повышать уровень освоения повторением той же задачи; "
                "нужен дополнительный вариант."
            )
            self._announce_feedback(self.remediation_feedback)
            return

        if self.return_problem_id:
            self.problem = self.problem_by_id[self.return_problem_id]
            self.problem_label.setText(self.problem.prompt_ru)
            self._save_session(phase="learning", problem_id=self.problem.id)
        self.answer.clear()
        self.answer.setEnabled(True)
        self.hint_level = None
        self.stack.setCurrentWidget(self.diagnostic)
        self.feedback.setText(
            "Базовый навык подтверждён несколькими проверками. Продолжаем основной маршрут."
        )
        self._announce_feedback(self.feedback)

    def _build_progress(self) -> QWidget:
        page, layout = self._page(
            "Мой прогресс",
            "Показываем знания, самостоятельность и умение применять навык в новых задачах — не время в приложении.",
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
        self._save_session(phase="learning", problem_id=self.problem.id)
        self.answer.setFocus()

    def _hint(self) -> None:
        hints = self.problem.hints
        if not hints:
            self.feedback.setText("Для этой диагностической задачи подсказка не раскрывается сразу.")
            self._announce_feedback(self.feedback)
            return
        current = 0 if self.hint_level is None else self.hint_level
        next_hint = next((h for h in hints if h.level > current), None)
        if next_hint:
            self.hint_level = next_hint.level
            self.feedback.setText("Подсказка: " + next_hint.text_ru)
            self._announce_feedback(self.feedback)

    def _submit(self) -> None:
        raw = self.answer.text().strip()
        if not raw:
            self.feedback.setText("Сначала введи ответ.")
            self._announce_feedback(self.feedback)
            return
        outcome = self.session.submit(
            student_id=STUDENT_ID,
            problem=self.problem,
            answer=raw,
            occurred_at=datetime.now(timezone.utc),
            hint_level=self.hint_level,
            answer_revealing_hint=any(
                hint.level == self.hint_level and hint.answer_revealing
                for hint in self.problem.hints
            ),
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
        decision = (
            self.router.decide(
                problem=self.problem,
                correct=outcome.verification.correct,
                misconception_hypothesis=outcome.misconception_hypothesis,
            )
            if self.router.handles(self.problem.id)
            else None
        )
        self._refresh_progress()
        review_problem_ids = self.module.review_problems_by_skill.get(
            outcome.next_activity.skill_id, ()
        )
        review_candidates = [
            self.problem_by_id[problem_id]
            for problem_id in review_problem_ids
            if problem_id in self.problem_by_id
        ]
        attempted = self.learning.attempted_problem_ids(
            STUDENT_ID, outcome.next_activity.skill_id
        )
        review_problem = select_fresh_problem(review_candidates, attempted)
        if outcome.next_activity.kind == "review" and review_problem:
            self.problem = review_problem
            self.problem_label.setText(self.problem.prompt_ru)
            self.answer.clear()
            self.hint_level = None
            self.feedback.setText(
                self.feedback.text() + "\n\nПора коротко повторить этот навык."
            )
        elif outcome.next_activity.kind == "enrichment":
            next_skill_id = next_sequence_skill(self.module, self.problem.primary_skill)
            next_pool = self.sequence_pools.get(next_skill_id, ()) if next_skill_id else ()
            entry = next((p for p in next_pool if p.purpose == "diagnostic"), None)
            if entry is not None:
                self.problem = entry
                self.problem_label.setText(self.problem.prompt_ru)
                self.answer.clear()
                self.hint_level = None
                self.feedback.setText(
                    self.feedback.text() + "\n\nТекущий навык устойчив. Переходим к следующему связанному навыку."
                )
                self._save_session(phase="learning", problem_id=self.problem.id)
            else:
                self.answer.setEnabled(False)
                self.feedback.setText(self.feedback.text() + "\n\n" + decision.message_ru)
        elif decision is not None and decision.next_problem_id:
            self.problem = self.problem_by_id[decision.next_problem_id]
            self.problem_label.setText(self.problem.prompt_ru)
            self.answer.clear()
            self.hint_level = None
            self.feedback.setText(self.feedback.text() + "\n\n" + decision.message_ru)
        elif decision is not None and decision.phase == "remediation":
            self.answer.setEnabled(False)
            self.feedback.setText(self.feedback.text() + "\n\n" + decision.message_ru)
            if decision.remediation_skill_id:
                self._start_remediation(decision.remediation_skill_id)
        elif decision is not None:
            self.answer.setEnabled(False)
            self.feedback.setText(self.feedback.text() + "\n\n" + decision.message_ru)
        else:
            self.answer.clear()
            self.hint_level = None
            self._save_session(phase="learning", problem_id=self.problem.id)
        if self.stack.currentWidget() is self.diagnostic:
            self._announce_feedback(self.feedback)

    def _refresh_progress(self) -> None:
        state = self.learning.get_state(STUDENT_ID, self.module.primary_skill.id)
        if state is None:
            self.progress_text.setText("Пока недостаточно данных.")
            return
        self.progress_text.setText(
            f"Навык: {self.module.primary_skill.title_ru}\n\n"
            f"Освоение: {state.mastery:.0%}\n"
            f"Самостоятельность: {state.independence:.0%}\n"
            f"Применение в новых задачах: {state.transfer:.0%}\n"
            f"Проверок: {state.evidence_count}"
        )

    def _show_progress(self) -> None:
        self._refresh_progress()
        self.stack.setCurrentWidget(self.progress)


def create_window(data_dir: Path, content_dir: Path) -> RepetitorWindow:
    return RepetitorWindow(data_dir, content_dir)


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
    try:
        window = create_window(data_dir, content_dir)
    except Exception as exc:
        record_startup_failure(data_dir, exc)
        QMessageBox.critical(
            None,
            "REPETITOR — ошибка запуска",
            "Не удалось безопасно открыть локальные данные или учебный контент. "
            "Приложение остановлено, чтобы не создавать ложный или пустой прогресс. "
            "Сохраните папку данных и обратитесь к сопровождающему пилота.",
        )
        return 2
    window.show()
    return app.exec()
