from pathlib import Path

from repetitor.content.validator import validate_content_graph


def test_repository_skill_graph_has_known_prerequisites_and_no_cycles():
    issues = validate_content_graph(Path("content"))
    assert issues == []
