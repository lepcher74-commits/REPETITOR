from repetitor.ai import NoAIProvider, SafeAIProvider


class BrokenProvider:
    def explain(self, **kwargs):
        raise ConnectionError("network down")

    def ask_socratic(self, **kwargs):
        raise TimeoutError("timeout")


def test_no_ai_is_safe_offline_default():
    ai = SafeAIProvider(NoAIProvider())
    result = ai.explain(skill_id="skill", context="context")
    assert not result.available
    assert result.error_code == "ai_unavailable"


def test_provider_failure_is_contained():
    ai = SafeAIProvider(BrokenProvider())
    result = ai.ask_socratic(skill_id="skill", context="context")
    assert not result.available
    assert result.error_code == "ai_failure"
    assert "Прогресс сохранён" in result.text
