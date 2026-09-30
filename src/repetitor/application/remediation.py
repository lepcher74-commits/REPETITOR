from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RemediationStep:
    skill_id: str
    title_ru: str
    explanation_ru: str
    prompt_ru: str
    verifier: dict
    success_message_ru: str


REMEDIATIONS = {
    "math.g6.fractions.equivalent": RemediationStep(
        skill_id="math.g6.fractions.equivalent",
        title_ru="Эквивалентные дроби",
        explanation_ru=(
            "Дробь не меняет значение, если числитель и знаменатель умножить "
            "на одно и то же ненулевое число. Например, 1/3 = 2/6: мы умножили "
            "и верхнюю, и нижнюю часть на 2."
        ),
        prompt_ru="Заполни пропуск: 2/5 = ?/10",
        verifier={"type": "exact_integer", "expected": 4},
        success_message_ru="Верно: 2/5 = 4/10. Возвращаемся к следующему prerequisite.",
    ),
    "math.prereq.lcm": RemediationStep(
        skill_id="math.prereq.lcm",
        title_ru="Наименьшее общее кратное",
        explanation_ru=(
            "Общее кратное делится на оба числа. Для 4 и 6 кратные: "
            "4, 8, 12… и 6, 12… Первое общее — 12, значит НОК(4, 6) = 12."
        ),
        prompt_ru="Найди НОК(6, 8).",
        verifier={"type": "exact_integer", "expected": 24},
        success_message_ru="Верно: НОК(6, 8) = 24. Можно вернуться к сложению дробей.",
    ),
}
