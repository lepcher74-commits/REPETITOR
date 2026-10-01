# Stage 5 — MVP acceptance record

## Scope
One complete desktop vertical slice for grade 6 mathematics: unlike-denominator fraction addition, with local SQLite state, formal verification, adaptive diagnostic routing, prerequisite remediation, review scheduling, transfer evidence, progress display, and optional/failure-safe AI boundary.

## Acceptance criteria status
- AC-01: onboarding exposes subject, grade, goal and starts diagnostics in <=3 selections/actions.
- AC-02: diagnostic router has answer-dependent branches; covered by router tests.
- AC-03: prerequisite failure -> declarative remediation -> verified evidence -> persisted prerequisite state -> declared return problem; integration-tested.
- AC-04: correct entry diagnostic skips prerequisite/guided basics and routes to independent evidence; acceptance-tested.
- AC-05: unrecognized errors remain unconfirmed; misconception is only a hypothesis until probes/evidence.
- AC-06: least-help-first hints and revealing-help independence penalty/guard are tested.
- AC-07: supported MVP answers use the formal Verification Engine; expected answers self-check.
- AC-08: review is scheduled in SQLite, selected when due before rescheduling current evidence, mapped declaratively to a review problem, and review evidence updates retention.
- AC-09: knowledge state persists in SQLite and is verified after repository reopen.
- AC-10: core module/content/verification/state path uses local files and SQLite; GUI smoke runs offscreen without network.
- AC-11: AI provider failure is isolated; formal learning and persistence continue, integration-tested.
- AC-12: student learning data is local SQLite by default.
- AC-13: module manifest owns subject/grade/goals/skill graph/routes; generic UI is guarded against fraction-specific IDs.
- AC-14: critical learning, routing, persistence, verification, GUI smoke, AI failure, remediation, review and content acceptance logic have automated tests.

## Content acceptance
Automated reference-slice tests cover CA-01…CA-20 with these MVP boundaries:
- CA-03 proves acyclic consistency for the current one-module graph, not a future repository-wide multi-module DAG.
- CA-20 is a static obvious-PII marker check; it is not a semantic privacy proof.
- CA-13 verifies hint ordering/uniqueness; pedagogical quality still requires human review.

## Explicit assumptions
[ДОПУЩЕНИЕ] Mastery coefficients, thresholds (0.45 prerequisite, 0.70 mastery, 0.60 transfer), and review intervals are transparent MVP heuristics requiring later calibration.
[ДОПУЩЕНИЕ] Repeating the last remediation independent item after insufficient evidence is acceptable only for MVP; Stage 6 should test memorization risk and replace it with variants if needed.

## Known risks
1. Reference content is intentionally one coherent slice, not the full grade 6 curriculum.
2. Review and remediation item pools are small; repeated exposure can inflate apparent mastery.
3. Accessibility is basic (large readable UI and keyboard submit), not a complete accessibility audit.
4. AI is intentionally non-authoritative and optional; no production API provider is required for offline MVP.
5. Installer/distribution packaging belongs to Stage 7.

## Run
```bash
python -m pip install -e ".[dev]"
pytest -q
python -m repetitor
```

## Gate
Stage 5 is complete only when the latest main-branch CI run is green after this acceptance record and all Stage 5 tests are included.
