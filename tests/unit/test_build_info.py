from repetitor.__main__ import build_info


def test_build_info_contains_package_version_and_injected_sha(monkeypatch):
    monkeypatch.setenv("REPETITOR_BUILD_SHA", "pilot-sha-123")
    info = build_info()
    assert info.startswith("REPETITOR 0.1.0 build ")
    assert info.endswith("pilot-sha-123")


def test_build_info_has_explicit_development_fallback(monkeypatch):
    monkeypatch.delenv("REPETITOR_BUILD_SHA", raising=False)
    assert build_info().endswith("build development")
