from pathlib import Path


def test_generic_ui_contains_no_fraction_module_ids():
    source = Path("src/repetitor/ui/app.py").read_text(encoding="utf-8")
    assert "frac.add." not in source
    assert "math.g6.fractions." not in source


def test_gui_propagates_answer_revealing_hint_evidence():
    source = Path("src/repetitor/ui/app.py").read_text(encoding="utf-8")
    assert "hint.answer_revealing" in source
    assert "answer_revealing_hint=False" not in source
