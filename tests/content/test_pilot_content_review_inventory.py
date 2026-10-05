import re
from pathlib import Path

import yaml


ROOT = Path('.')
INVENTORY = ROOT / 'docs/PILOT_CONTENT_REVIEW_INVENTORY.md'
PROBLEM_FILES = (
    ROOT / 'content/mathematics/fractions/equivalent/problems.yaml',
    ROOT / 'content/mathematics/fractions/simplify/problems.yaml',
    ROOT / 'content/mathematics/fractions/add_unlike/problems.yaml',
    ROOT / 'content/mathematics/fractions/subtract_unlike/problems.yaml',
)
REMEDIATION = ROOT / 'content/mathematics/fractions/add_unlike/remediation.yaml'


def _problem_ids() -> set[str]:
    ids: set[str] = set()
    for path in PROBLEM_FILES:
        data = yaml.safe_load(path.read_text(encoding='utf-8'))
        ids.update(problem['id'] for problem in data['problems'])
    remediation = yaml.safe_load(REMEDIATION.read_text(encoding='utf-8'))
    for route in remediation['remediations']:
        ids.update(problem['id'] for problem in route['problems'])
    return ids


def _hint_count() -> int:
    total = 0
    for path in PROBLEM_FILES:
        data = yaml.safe_load(path.read_text(encoding='utf-8'))
        total += sum(len(problem.get('hints', ())) for problem in data['problems'])
    return total


def test_review_inventory_tracks_every_pilot_problem_id():
    text = INVENTORY.read_text(encoding='utf-8')
    inventoried = set(re.findall(r'`((?:frac\.)[^`]+)`', text))
    actual = _problem_ids()

    assert actual == inventoried, (
        'Pilot content changed without refreshing PILOT_CONTENT_REVIEW_INVENTORY.md: '
        f'missing={sorted(actual - inventoried)}, stale={sorted(inventoried - actual)}'
    )


def test_review_inventory_declared_counts_match_authored_content():
    text = INVENTORY.read_text(encoding='utf-8')
    actual_problems = len(_problem_ids())
    actual_hints = _hint_count()

    assert f'Problems: {actual_problems} total' in text
    assert f'Hints: {actual_hints} authored hints' in text
