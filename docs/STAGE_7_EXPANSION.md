# Stage 7 — Expansion

Status: **IN PROGRESS — authorized by Controller**.

## Approved baseline
- Stages 0–6 complete.
- Offline-first desktop architecture: Python + PySide6/Qt + SQLite.
- Formal verification is authoritative for supported tasks; LLM is optional and cannot modify KnowledgeState.
- Next-Step Engine owns routing.
- Local data is the default.
- Stage 6 final CI baseline: 67 passing tests.

## Expansion order

Stage 7 expands only from proven MVP constraints. It does not add breadth merely to increase feature count.

### E1 — Scale-safe content graph
Upgrade content validation from the current reference-slice checks to repository/module-wide graph validation. Cross-module references must resolve and prerequisite cycles must fail validation.

### E2 — Fresh evidence pools
Remove the Stage 6 safe-stop limitation by providing distinct declarative remediation/review variants and selecting fresh evidence where available. Repeating an identical problem must not be the mechanism for crossing mastery thresholds.

### E3 — Session continuity
Persist enough local session state to resume the learner's current activity after restart without changing KnowledgeState semantics.

### E4 — Desktop platform CI
Add supported CI coverage for Linux, Windows and macOS where dependencies permit. Platform-specific failures must be visible rather than inferred from Linux offscreen success.

### E5 — Accessibility hardening
Add keyboard/focus/label checks that can be automated and document the remaining manual assistive-technology audit.

### E6 — Curriculum breadth
Only after E1–E5 are stable, extend the grade-6 fractions graph/content beyond the single unlike-denominator slice. New skills must satisfy the existing content contract and CA acceptance checks.

## Non-goals
- No new school subject before the current tutor-module architecture is proven by more than one mathematics skill.
- No LLM authority over scoring/mastery.
- No cloud requirement for core learning.
- No addictive engagement mechanics.
- No claim of empirically calibrated mastery thresholds without evidence.

## Exit criteria
- repository-wide content graph validation is automated;
- repeated practice can use fresh declarative variants;
- restart continuity is tested;
- desktop CI coverage is expanded and limitations documented;
- accessibility baseline is improved and residual manual checks are explicit;
- at least one additional connected mathematics skill is implemented through the same module/content interfaces;
- all prior Stage 5/6 acceptance tests remain green.

Transition beyond Stage 7 requires the Controller gate defined by Constitution v1.0.


## Implementation status

- E1 — repository-wide prerequisite graph validation: implemented and regression-tested.
- E2 — fresh review/remediation evidence pools: implemented; attempted problem history prevents identical authored evidence from being the sole mastery mechanism.
- E3 — session continuity: implemented separately from KnowledgeState; restart and stale-position fallback are tested.
- E4 — desktop CI: Linux, Windows, and macOS matrix implemented. Final Stage 7 head must be green before closure.
- E5 — accessibility baseline: automated accessible-name/focus checks implemented; manual Narrator/VoiceOver/WCAG audit remains a release limitation, documented in ACCESSIBILITY_AUDIT.md.
- E6 — curriculum breadth: equivalent fractions is a second declarative grade-6 mathematics skill with diagnostic, guided, independent, transfer, review, formal verification, and generic LearningSessionService coverage.

## Residual risks at final gate

1. [ДОПУЩЕНИЕ] Mastery coefficients, thresholds, and review intervals remain heuristic and are not empirically calibrated.
2. Manual screen-reader and formal WCAG audit has not been executed.
3. CI proves automated runtime/tests on hosted Linux, Windows, and macOS runners; it is not a substitute for packaged installer testing on representative user machines.
4. Content breadth is still deliberately narrow: grade-6 fractions, not a complete grade-6 curriculum.
5. Production AI provider remains optional; offline formal learning core is authoritative.
6. Fresh evidence pools are finite. When exhausted, the application fails safely rather than recycling identical evidence to inflate mastery.

## Final gate rule

Stage 7 is technically complete only after the final three-platform CI head succeeds. Constitutional closure still requires explicit Controller approval.
