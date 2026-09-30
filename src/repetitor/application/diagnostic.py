from __future__ import annotations

from dataclasses import dataclass

from repetitor.domain import Problem


@dataclass(frozen=True, slots=True)
class DiagnosticDecision:
    next_problem_id: str | None
    phase: str
    message_ru: str


class FractionDiagnosticRouter:
    """Deterministic reference router for the Stage-5 fractions slice.

    It does not change KnowledgeState itself. Submitted problems still flow
    through LearningSessionService; this router only chooses the next probe.
    """

    def decide(
        self,
        *,
        problem: Problem,
        correct: bool,
        misconception_hypothesis: str | None,
    ) -> DiagnosticDecision:
        pid = problem.id

        if pid == "frac.add.diag.001":
            if correct:
                return DiagnosticDecision(
                    "frac.add.independent.001", "independent",
                    "Базовая задача решена. Проверим самостоятельность на другом примере.",
                )
            if misconception_hypothesis == "add_denominators":
                return DiagnosticDecision(
                    "frac.add.probe.add_denominators", "misconception_probe",
                    "Проверим одну возможную причину ошибки.",
                )
            return DiagnosticDecision(
                "frac.add.probe.equivalent", "prerequisite_probe",
                "Проверим навык, который нужен для сложения дробей.",
            )

        if pid == "frac.add.probe.add_denominators":
            if correct:
                return DiagnosticDecision(
                    "frac.add.probe.equivalent", "prerequisite_probe",
                    "Хорошо. Теперь проверим эквивалентные дроби.",
                )
            return DiagnosticDecision(
                "frac.add.probe.equivalent", "prerequisite_probe",
                "Эта идея требует разбора. Сначала проверим фундаментальный навык.",
            )

        if pid == "frac.add.probe.equivalent":
            if correct:
                return DiagnosticDecision(
                    "frac.add.probe.lcm", "prerequisite_probe",
                    "Эквивалентные дроби понятны. Проверим общий кратный.",
                )
            return DiagnosticDecision(
                None, "remediation",
                "Нашли более ранний пробел: сначала восстановим эквивалентные дроби.",
            )

        if pid == "frac.add.probe.lcm":
            if correct:
                return DiagnosticDecision(
                    "frac.add.guided.001", "guided",
                    "Пререквизиты готовы. Разберём сложение с поддержкой.",
                )
            return DiagnosticDecision(
                None, "remediation",
                "Сначала восстановим поиск общего кратного, затем вернёмся к дробям.",
            )

        if pid == "frac.add.guided.001":
            return DiagnosticDecision(
                "frac.add.independent.001", "independent",
                "Теперь попробуй похожую задачу самостоятельно.",
            )

        if pid == "frac.add.independent.001":
            if correct:
                return DiagnosticDecision(
                    "frac.add.independent.002", "independent",
                    "Ещё одна самостоятельная задача для устойчивого evidence.",
                )
            return DiagnosticDecision(
                "frac.add.guided.001", "guided",
                "Вернём немного поддержки и затем попробуем снова.",
            )

        if pid == "frac.add.independent.002":
            if correct:
                return DiagnosticDecision(
                    "frac.add.transfer.001", "transfer",
                    "Вычисления получаются. Проверим применение в новой ситуации.",
                )
            return DiagnosticDecision(
                "frac.add.guided.001", "guided",
                "Нужна дополнительная практика с поддержкой.",
            )

        if pid == "frac.add.transfer.001":
            if correct:
                return DiagnosticDecision(
                    "frac.add.transfer.002", "reverse_transfer",
                    "Перенос получился. Теперь обратная задача.",
                )
            return DiagnosticDecision(
                "frac.add.independent.002", "independent",
                "Вернёмся на один шаг и укрепим выбор способа.",
            )

        if pid == "frac.add.transfer.002":
            return DiagnosticDecision(
                None, "complete" if correct else "transfer",
                "Диагностический маршрут завершён." if correct
                else "Обратные задачи пока требуют отдельной тренировки.",
            )

        return DiagnosticDecision(None, "complete", "Маршрут для этой задачи завершён.")
