from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class AIResult:
    available: bool
    text: str
    error_code: str | None = None


class AIProvider(Protocol):
    def explain(self, *, skill_id: str, context: str) -> str: ...
    def ask_socratic(self, *, skill_id: str, context: str) -> str: ...


class NoAIProvider:
    """Offline/default provider. Core learning remains fully available."""

    def explain(self, *, skill_id: str, context: str) -> str:
        raise RuntimeError("AI is disabled")

    def ask_socratic(self, *, skill_id: str, context: str) -> str:
        raise RuntimeError("AI is disabled")


class SafeAIProvider:
    """Failure boundary around any optional AI implementation."""

    def __init__(self, provider: AIProvider | None = None) -> None:
        self._provider = provider

    @property
    def available(self) -> bool:
        return self._provider is not None and not isinstance(self._provider, NoAIProvider)

    def explain(self, *, skill_id: str, context: str) -> AIResult:
        if not self.available:
            return AIResult(False, "AI-функции выключены. Основной урок работает офлайн.", "ai_unavailable")
        try:
            text = self._provider.explain(skill_id=skill_id, context=context)
        except Exception:
            return AIResult(False, "AI временно недоступен. Прогресс сохранён; продолжай офлайн.", "ai_failure")
        return AIResult(True, text)

    def ask_socratic(self, *, skill_id: str, context: str) -> AIResult:
        if not self.available:
            return AIResult(False, "AI-функции выключены. Основной урок работает офлайн.", "ai_unavailable")
        try:
            text = self._provider.ask_socratic(skill_id=skill_id, context=context)
        except Exception:
            return AIResult(False, "AI временно недоступен. Прогресс сохранён; продолжай офлайн.", "ai_failure")
        return AIResult(True, text)
