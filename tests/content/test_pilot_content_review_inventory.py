import hashlib
import json
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
RUNTIME_UI = ROOT / 'src/repetitor/ui/app.py'


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


def _learner_visible_fingerprint() -> str:
    visible = []
    for path in PROBLEM_FILES:
        data = yaml.safe_load(path.read_text(encoding='utf-8'))
        for problem in data['problems']:
            visible.append({'id': problem['id'], 'prompt_ru': problem['prompt_ru'], 'choices': problem.get('choices', []), 'hints': [hint['text_ru'] for hint in problem.get('hints', [])]})
    remediation = yaml.safe_load(REMEDIATION.read_text(encoding='utf-8'))
    for route in remediation['remediations']:
        visible.append({'skill_id': route['skill_id'], 'title_ru': route['title_ru'], 'explanation_ru': route['explanation_ru'], 'problems': [{'id': problem['id'], 'prompt_ru': problem['prompt_ru']} for problem in route['problems']]})
    canonical = json.dumps(visible, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical.encode('utf-8')).hexdigest()


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


def test_review_inventory_fingerprint_matches_learner_visible_yaml():
    text = INVENTORY.read_text(encoding='utf-8')
    fingerprint = _learner_visible_fingerprint()
    assert f'Learner-visible YAML fingerprint (SHA-256): `{fingerprint}`' in text, (
        'Learner-visible pilot wording changed without refreshing the human-review inventory. '
        'Update the fingerprint and repeat affected semantic review; a matching hash is not approval.'
    )


def test_review_inventory_runtime_ui_source_fingerprint_matches():
    text = INVENTORY.read_text(encoding='utf-8')
    fingerprint = hashlib.sha256(RUNTIME_UI.read_bytes()).hexdigest()
    assert f'Runtime UI source fingerprint (SHA-256): `{fingerprint}`' in text, (
        'Runtime UI source changed without refreshing the learner-visible review inventory. '
        'Reassess affected UI wording/behavior and update the fingerprint; matching is not approval.'
    )
