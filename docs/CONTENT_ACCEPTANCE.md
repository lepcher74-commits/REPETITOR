# Stage 4 Content Acceptance Criteria

Status: proposed for Controller approval.

A content package is acceptable only when all applicable checks pass.

## Structural

**CA-01 Unique IDs** — all skill/problem/misconception/lesson IDs are unique in their namespace.

**CA-02 References resolve** — every prerequisite, skill reference, problem reference, remediation target and lesson route points to an existing allowed object.

**CA-03 Acyclic prerequisites** — the skill prerequisite graph contains no directed cycle.

**CA-04 Reachability** — each non-entry taught skill is reachable from declared entry/prerequisite skills.

**CA-05 Schema** — every file satisfies the machine-readable schema for its object type.

## Verification

**CA-06 Verifier supported** — every problem uses a registered verifier type.

**CA-07 Self-check** — every expected answer passes the configured verifier and constraints.

**CA-08 Choice integrity** — multiple-choice expected answer exists among the choices and choices are non-duplicated.

**CA-09 Rational normalization** — when simplest form is required, the expected rational is normalized.

## Pedagogy

**CA-10 Diagnostic evidence** — each MVP taught skill has at least one diagnostic/probe path or an explicit reason it is not directly diagnosed.

**CA-11 Independent evidence** — each taught skill has at least one item that can produce independent mastery evidence without mandatory hints.

**CA-12 Review evidence** — each mastered skill can be revisited using a review-capable item/activity.

**CA-13 Hint progression** — hints are ordered from less revealing to more revealing; answer-revealing help is identifiable.

**CA-14 Misconception caution** — one response cannot directly confirm a misconception; confirmation requires additional evidence or remains unknown.

**CA-15 Prerequisite remediation** — detected prerequisite failure can route to the prerequisite rather than only repeating the current skill.

**CA-16 Transfer separation** — transfer tasks are explicitly marked and transfer evidence is separate from routine mastery.

**CA-17 Worked-to-independent path** — a taught skill has a path from explanation/worked support to independent attempt, unless the learner demonstrates mastery and skips support.

## Localization and safety

**CA-18 Russian learner text** — required learner-facing text exists in Russian for MVP.

**CA-19 No executable content** — bundled content contains declarative data/assets only; no arbitrary executable plugin code is required to interpret it.

**CA-20 No child PII in content** — authored content contains no real child personal data.

## Reference slice acceptance

The Stage 4 reference slice `content/mathematics/fractions/add_unlike/` is intended to satisfy CA-01…CA-20 after the Stage 5 validator is implemented.

Manual Stage 4 review establishes design completeness; Stage 5 automated tests establish executable compliance.
