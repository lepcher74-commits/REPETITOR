# Stage 8 closeout — critical path

Status: planning document; no release-gate approval implied.

## Critical path (in order)

1. **Stabilize an audit candidate.** Stop expanding optional recovery/security analytics within Stage 8. Inspect current CI/Pilot Build results, fix failures, and pin an **audit candidate SHA** for manual execution. This is not yet the PR-14 final candidate. Optional parent-account infrastructure remains disabled and is not a new Stage 8 release criterion.
2. **Manual accessibility PR-08 on the pinned audit candidate.** Controller/operator executes and records keyboard, Windows Narrator and macOS VoiceOver checks, target scaling, OS versions and failures in ACCESSIBILITY_PILOT_AUDIT_RECORD.md. Assistant can prepare checklists and fixes but cannot invent observed results. Any code/content fix invalidates affected observations and requires a new audit candidate/build.
3. **Child-safety/operational PR-10.** Identify actual Russian operator, support contact, authorized guardian/consent workflow, reviewed age-appropriate grade-6 pilot content, retention/deletion procedures, and any actual network/data flow. Record approvals or explicit exclusions in PILOT_MANUAL_GATE_RECORD.md and PILOT_DATA_OPERATIONS_TEMPLATE.md. Do not treat verified mailbox as guardian verification.
4. **Nominate final candidate and execute same-SHA PR-14.** Only after required manual records are complete and all resulting code/content fixes are incorporated, nominate the exact final candidate SHA. Run supported CI and Windows/macOS Pilot Build on that exact SHA; record run IDs and outcomes in STAGE_8_EVIDENCE_MATRIX.md. Documentation-only follow-up commits must not be misrepresented as the tested candidate SHA.
5. **Controller gate.** Present evidence, remaining risks and pilot restrictions. Stage 8 closes only on explicit Controller approval.

## Scheduling assumptions

Assistant-owned code/test/document preparation: estimate 3–5 working days if GitHub runners and connector remain available and no significant defects appear. Full closure: tentative 1–2 weeks **only if** target devices, operator decisions and legal/manual reviewers are available promptly. No unattended background work or guaranteed calendar deadline is implied.

## Scope boundary

Stage 8 is the last currently approved numbered stage. Real-user pilot operation, any production parent-account service, legal launch, additional grades/subjects and commercialization require separate post-gate decisions; they are not silently added as new mandatory Stage 8 criteria.


## Candidate terminology

- **Audit candidate:** pinned build used to collect manual PR-08/PR-10 evidence. It may be replaced after a defect/fix and does not satisfy PR-14 by itself.
- **Final candidate:** exact post-audit revision nominated only when required manual/operational gates are complete and no further code/content changes are pending; this SHA must receive the final same-SHA CI + Windows/macOS Pilot Build evidence.
