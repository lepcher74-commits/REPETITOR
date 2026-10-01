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
