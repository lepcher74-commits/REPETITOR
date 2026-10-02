# Stage 8 closeout — critical path

Status: planning document; no release-gate approval implied.

## Critical path (in order)

1. **Stabilize candidate.** Stop expanding optional recovery/security analytics within Stage 8. Inspect all current CI/Pilot Build results, fix any failures, and freeze a proposed SHA. Optional parent-account infrastructure remains disabled and is not a new Stage 8 release criterion.
2. **Manual accessibility PR-08.** Controller/operator executes and records keyboard, Windows Narrator and macOS VoiceOver checks, target scaling, OS versions and failures in ACCESSIBILITY_PILOT_AUDIT_RECORD.md. Assistant can prepare checklists and fixes but cannot invent observed results.
3. **Child-safety/operational PR-10.** Identify actual Russian operator, support contact, authorized guardian/consent workflow, reviewed age-appropriate grade-6 pilot content, retention/deletion procedures, and any actual network/data flow. Record approvals or explicit exclusions in PILOT_MANUAL_GATE_RECORD.md and PILOT_DATA_OPERATIONS_TEMPLATE.md. Do not treat verified mailbox as guardian verification.
4. **Final same-SHA PR-14.** After required manual records and any fixes are committed, run supported CI and Windows/macOS Pilot Build on the exact final candidate SHA; record run IDs and outcomes in STAGE_8_EVIDENCE_MATRIX.md. Documentation-only follow-up commits must not be misrepresented as the tested candidate SHA.
5. **Controller gate.** Present evidence, remaining risks and pilot restrictions. Stage 8 closes only on explicit Controller approval.

## Scheduling assumptions

Assistant-owned code/test/document preparation: estimate 3–5 working days if GitHub runners and connector remain available and no significant defects appear. Full closure: tentative 1–2 weeks **only if** target devices, operator decisions and legal/manual reviewers are available promptly. No unattended background work or guaranteed calendar deadline is implied.

## Scope boundary

Stage 8 is the last currently approved numbered stage. Real-user pilot operation, any production parent-account service, legal launch, additional grades/subjects and commercialization require separate post-gate decisions; they are not silently added as new mandatory Stage 8 criteria.
