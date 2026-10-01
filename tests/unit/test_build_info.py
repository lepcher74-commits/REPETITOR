import repetitor.__main__ as app_main


def test_build_info_contains_version_and_injected_sha(monkeypatch):
    monkeypatch.setattr(app_main, "BUILD_SHA", "pilot-sha-123")
    info = app_main.build_info()
    assert info.startswith("REPETITOR ")
    assert " build pilot-sha-123" in info


def test_build_info_has_explicit_development_fallback():
    assert app_main.BUILD_SHA == "development"
    assert app_main.build_info().endswith("build development")
