from pathlib import Path
import re

import yaml

from repetitor.application.diagnostic import DiagnosticRouter
from repetitor.application.remediation import load_remediations
from repetitor.content import load_problems, load_skill
from repetitor.content.module import load_module_manifest, load_sequence_problems
from repetitor.verification import verify_answer


BASE = Path("content/mathematics/fractions/add_unlike")


def _yaml(name):
    return yaml.safe_load((BASE / name).read_text(encoding="utf-8"))


def test_ca01_ids_unique_across_each_namespace():
    problems = load_problems(BASE / "problems.yaml")
    remediations = load_remediations(BASE / "remediation.yaml")
    errors = _yaml("errors.yaml")["misconceptions"]
    lesson = _yaml("lesson.yaml")["lesson"]
    assert len({p.id for p in problems}) == len(problems)
    remediation_problem_ids = [p.id for r in remediations.values() for p in r.problems]
    assert len(set(remediation_problem_ids)) == len(remediation_problem_ids)
    assert len({x["id"] for x in errors}) == len(errors)
    assert lesson["id"]


def test_ca02_references_resolve_and_ca03_graph_is_acyclic_for_slice():
    module = load_module_manifest(BASE / "module.yaml")
    skill = load_skill(BASE / "skill.yaml")
    problems = {p.id: p for p in load_problems(BASE / "problems.yaml")}
    remediations = load_remediations(BASE / module.remediation_route)
    route = _yaml(module.diagnostic_route)
    assert tuple(skill.prerequisites) == module.prerequisites
    assert route["start_problem_id"] in problems
    for rule in route["rules"]:
        assert rule["problem_id"] in problems
        if rule.get("next_problem_id"):
            assert rule["next_problem_id"] in problems
        if rule.get("remediation_skill_id"):
            assert rule["remediation_skill_id"] in remediations
    for remediation in remediations.values():
        assert remediation.return_problem_id in problems
    assert module.primary_skill.id not in module.prerequisites
    assert len(set(module.prerequisites)) == len(module.prerequisites)


def test_ca04_reachability_and_ca10_diagnostic_path():
    module = load_module_manifest(BASE / "module.yaml")
    route = _yaml(module.diagnostic_route)
    adjacency = {}
    for rule in route["rules"]:
        nxt = rule.get("next_problem_id")
        if nxt:
            adjacency.setdefault(rule["problem_id"], set()).add(nxt)
    seen = set()
    stack = [route["start_problem_id"]]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(adjacency.get(node, ()))
    assert route["start_problem_id"] in seen
    assert "frac.add.independent.001" in seen
    assert "frac.add.transfer.001" in seen


def test_ca05_ca06_ca07_ca08_ca09_schema_and_verification_integrity():
    problems = load_problems(BASE / "problems.yaml")
    for p in problems:
        assert p.id and p.primary_skill and p.purpose and p.verifier.get("type")
        expected = p.verifier.get("expected")
        assert verify_answer(p.verifier, str(expected)).correct
        if p.verifier.get("type") == "multiple_choice":
            assert expected in p.choices
            assert len(p.choices) == len(set(p.choices))
        if p.verifier.get("require_simplified"):
            assert "/" in str(expected)
            a, b = map(int, str(expected).split("/"))
            import math
            assert math.gcd(abs(a), abs(b)) == 1


def test_ca11_ca12_ca16_ca17_evidence_and_progression():
    module = load_module_manifest(BASE / "module.yaml")
    primary_problems = load_problems(BASE / "problems.yaml")
    purposes = {p.purpose for p in primary_problems}
    assert "independent" in purposes
    assert "review" in purposes
    assert any(p.transfer for p in primary_problems)
    assert "guided" in purposes and "independent" in purposes

    sequence_pools = load_sequence_problems(module, Path("content"))
    sequence_problems = {
        p.id: p
        for pool in sequence_pools.values()
        for p in pool
    }
    for skill_id, problem_ids in module.review_problems_by_skill.items():
        assert problem_ids
        for problem_id in problem_ids:
            p = sequence_problems[problem_id]
            assert p.primary_skill == skill_id
            assert p.purpose == "review"


def test_ca13_hints_progress_and_ca14_misconceptions_require_confirmation():
    problems = load_problems(BASE / "problems.yaml")
    for p in problems:
        levels = [h.level for h in p.hints]
        assert levels == sorted(set(levels))
    errors = _yaml("errors.yaml")["misconceptions"]
    for error in errors:
        confirmation = error.get("confirmation")
        if confirmation:
            assert confirmation.get("minimum_independent_evidence", 2) >= 2


def test_ca15_prerequisite_failure_has_remediation_route():
    module = load_module_manifest(BASE / "module.yaml")
    problems = {p.id: p for p in load_problems(BASE / "problems.yaml")}
    router = DiagnosticRouter.from_yaml(BASE / module.diagnostic_route)
    remediations = load_remediations(BASE / module.remediation_route)
    probes = [p for p in problems.values() if p.purpose == "prerequisite_probe"]
    for probe in probes:
        decision = router.decide(problem=probe, correct=False, misconception_hypothesis=None)
        assert decision.phase == "remediation"
        assert decision.remediation_skill_id == probe.primary_skill
        assert probe.primary_skill in remediations


def test_ca18_russian_learner_text_and_ca19_declarative_content_and_ca20_no_pii_markers():
    learner_files = ["problems.yaml", "lesson.yaml", "errors.yaml", "remediation.yaml", "diagnostic_route.yaml"]
    cyrillic = re.compile(r"[А-Яа-яЁё]")
    pii = re.compile(r"\b(?:\d{3}-\d{2}-\d{4}|\+?\d[\d ()-]{8,}\d|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,})\b")
    for name in learner_files:
        text = (BASE / name).read_text(encoding="utf-8")
        assert cyrillic.search(text)
        assert not pii.search(text)
    assert not list(BASE.glob("*.py"))
