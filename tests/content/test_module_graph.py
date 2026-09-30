from pathlib import Path

from repetitor.application.remediation import load_remediations
from repetitor.content import load_problems
from repetitor.content.module import load_module_manifest


BASE = Path("content/mathematics/fractions/add_unlike")


def test_manifest_prerequisites_have_probe_and_remediation_evidence():
    module = load_module_manifest(BASE / "module.yaml")
    problems = load_problems(BASE / "problems.yaml")
    remediations = load_remediations(BASE / module.remediation_route)

    probed = {
        problem.primary_skill
        for problem in problems
        if problem.purpose == "prerequisite_probe"
    }

    for skill_id in module.prerequisites:
        assert skill_id in probed
        assert skill_id in remediations
