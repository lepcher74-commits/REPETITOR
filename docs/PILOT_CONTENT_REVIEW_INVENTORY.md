# Pilot learner-visible content review inventory

Status: PREPARED / NOT HUMAN-REVIEWED. Scope is the current grade-6 fractions pilot content. This inventory makes the PR-10 human review bounded and reproducible; it is not an age-appropriateness approval.

## Review method

Reviewer must inspect every item below in the exact candidate revision and record PASS/FAIL plus issue disposition. Check understandable Russian for intended age/grade, mathematical semantic clarity, non-humiliating/non-manipulative wording, absence of unsupported factual claims, and absence of pressure to continue. Formal verifier tests do not replace this semantic review.

## Equivalent fractions — 8 problems

Source: `content/mathematics/fractions/equivalent/problems.yaml`.

- `frac.eq.diag.001`
- `frac.eq.guided.001` — includes 3 hints
- `frac.eq.independent.001`
- `frac.eq.independent.002`
- `frac.eq.transfer.001`
- `frac.eq.review.001`
- `frac.eq.review.002`
- `frac.eq.review.003`

## Simplifying fractions — 8 problems

Source: `content/mathematics/fractions/simplify/problems.yaml`.

- `frac.simplify.diag.001`
- `frac.simplify.guided.001` — includes 3 hints
- `frac.simplify.independent.001`
- `frac.simplify.independent.002`
- `frac.simplify.transfer.001`
- `frac.simplify.review.001`
- `frac.simplify.review.002`
- `frac.simplify.review.003`

## Adding fractions with unlike denominators — 12 problems

Source: `content/mathematics/fractions/add_unlike/problems.yaml`.

- `frac.add.diag.001`
- `frac.add.probe.add_denominators` — multiple-choice learner text
- `frac.add.probe.equivalent`
- `frac.add.probe.lcm`
- `frac.add.guided.001` — includes 4 hints
- `frac.add.independent.001`
- `frac.add.independent.002`
- `frac.add.transfer.001`
- `frac.add.transfer.002`
- `frac.add.review.001`
- `frac.add.review.002`
- `frac.add.review.003`

## Subtracting fractions with unlike denominators — 8 problems

Source: `content/mathematics/fractions/subtract_unlike/problems.yaml`.

- `frac.sub.diag.001`
- `frac.sub.guided.001` — includes 3 hints
- `frac.sub.independent.001`
- `frac.sub.independent.002`
- `frac.sub.transfer.001`
- `frac.sub.review.001`
- `frac.sub.review.002`
- `frac.sub.review.003`

## Remediation — 6 problems + 2 explanations

Source: `content/mathematics/fractions/add_unlike/remediation.yaml`.

Equivalent-fractions remediation:
- title and explanation
- `frac.remediation.equivalent.guided`
- `frac.remediation.equivalent.independent.1`
- `frac.remediation.equivalent.independent.2`

LCM remediation:
- title and explanation
- `frac.remediation.lcm.guided`
- `frac.remediation.lcm.independent.1`
- `frac.remediation.lcm.independent.2`

## Runtime learner-visible messages

Also review the UI wording in `src/repetitor/ui/app.py`: onboarding/diagnostic/remediation/progress headings and subtitles; answer placeholders; empty-answer feedback; hints prefix; correct/equivalent/incorrect feedback; misconception uncertainty wording; review/enrichment transition messages; remediation success/failure/exhaustion messages; progress labels; startup failure dialog. Review exact final candidate source, because these messages can change independently of YAML content.

## Completion record

Candidate SHA reviewed: [FILL]

Reviewer / role: [FILL]

Review date: [FILL]

Problems: 42 total listed above (36 sequence/add-unlike problem entries + 6 remediation problems). Hints: 13 authored hints in problem pools, plus remediation explanations and runtime messages. Reviewer must verify these counts against the exact candidate; count mismatch is a STOP condition requiring inventory refresh.

| Area | Result | Issues / disposition |
|---|---|---|
| Equivalent fractions | NOT TESTED | |
| Simplifying fractions | NOT TESTED | |
| Addition unlike denominators | NOT TESTED | |
| Subtraction unlike denominators | NOT TESTED | |
| Remediation | NOT TESTED | |
| Runtime UI/feedback messages | NOT TESTED | |

Overall content review: **NOT TESTED**.

A PASS may be copied to `PILOT_MANUAL_GATE_RECORD.md` only after all rows are reviewed on the exact candidate and all blocking issues are resolved. Do not store learner personal data in this record.
