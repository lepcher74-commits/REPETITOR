from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from repetitor.content.loader import ContentLoadError, load_problems, load_skill
from repetitor.verification import UnsupportedVerifierError, verify_answer


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    message: str


def validate_reference_slice(directory: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    try:
        skill = load_skill(directory / "skill.yaml")
        problems = load_problems(directory / "problems.yaml")
    except ContentLoadError as exc:
        return [ValidationIssue("schema", str(exc))]

    ids: set[str] = set()
    for problem in problems:
        if problem.id in ids:
            issues.append(ValidationIssue("duplicate_id", f"Duplicate problem id: {problem.id}"))
        ids.add(problem.id)

        if problem.primary_skill != skill.id and problem.purpose not in {"prerequisite_probe"}:
            # Cross-skill prerequisite probes are allowed in this reference slice.
            issues.append(ValidationIssue(
                "unknown_primary_skill",
                f"{problem.id} references {problem.primary_skill}, not loaded skill {skill.id}",
            ))

        levels = [hint.level for hint in problem.hints]
        if levels != sorted(set(levels)):
            issues.append(ValidationIssue("hint_order", f"{problem.id}: hint levels must increase uniquely"))

        try:
            result = verify_answer(problem.verifier, problem.verifier.get("expected"))
        except UnsupportedVerifierError as exc:
            issues.append(ValidationIssue("unsupported_verifier", f"{problem.id}: {exc}"))
        else:
            if not result.correct:
                issues.append(ValidationIssue("self_check", f"{problem.id}: expected answer fails verifier"))

        if problem.verifier.get("type") == "multiple_choice":
            expected = str(problem.verifier.get("expected"))
            if len(problem.choices) != len(set(problem.choices)):
                issues.append(ValidationIssue("duplicate_choices", f"{problem.id}: duplicate choices"))
            if expected not in problem.choices:
                issues.append(ValidationIssue("missing_expected_choice", f"{problem.id}: expected choice absent"))

    purposes = {problem.purpose for problem in problems}
    for required in ("diagnostic", "independent", "review"):
        if required not in purposes:
            issues.append(ValidationIssue("coverage", f"Missing required purpose: {required}"))

    if not any(problem.transfer for problem in problems):
        issues.append(ValidationIssue("coverage", "Missing transfer evidence item"))

    return issues


def validate_content_graph(content_root: Path) -> list[ValidationIssue]:
    """Validate skill prerequisites across every skill.yaml under content_root."""
    issues: list[ValidationIssue] = []
    skills = {}
    for path in sorted(content_root.rglob("skill.yaml")):
        try:
            skill = load_skill(path)
        except ContentLoadError as exc:
            issues.append(ValidationIssue("schema", f"{path}: {exc}"))
            continue
        if skill.id in skills:
            issues.append(ValidationIssue("duplicate_skill_id", f"Duplicate skill id: {skill.id}"))
        else:
            skills[skill.id] = skill

    for skill in skills.values():
        for prerequisite in skill.prerequisites:
            if prerequisite not in skills:
                issues.append(ValidationIssue(
                    "unknown_prerequisite",
                    f"{skill.id} references unknown prerequisite {prerequisite}",
                ))

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(skill_id: str, path: tuple[str, ...]) -> None:
        if skill_id in visited:
            return
        if skill_id in visiting:
            start = path.index(skill_id) if skill_id in path else 0
            cycle = path[start:] + (skill_id,)
            issues.append(ValidationIssue("prerequisite_cycle", " -> ".join(cycle)))
            return
        visiting.add(skill_id)
        skill = skills[skill_id]
        for prerequisite in skill.prerequisites:
            if prerequisite in skills:
                visit(prerequisite, path + (skill_id,))
        visiting.remove(skill_id)
        visited.add(skill_id)

    for skill_id in sorted(skills):
        visit(skill_id, ())
    return issues
