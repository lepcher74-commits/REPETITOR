# Stage 8 audit execution checklist

Status: PREPARED. This checklist coordinates human PR-08 / PR-10 execution for the verified audit candidate. It does not contain PASS results.

## Fixed audit candidate

- SHA: `983d04c564879f9ff8b6de110497901279073aeb`
- CI: `37304924020` — SUCCESS on Windows/macOS/Ubuntu
- Pilot Build: `37304924030` — SUCCESS on Windows/macOS
- Windows artifact: `11343327951`, archive SHA-256 `2c40cb9cda7cc7cb6f87c218dffea1f7d7e6046261d54567616a4c767c80a416`
- macOS artifact: `11342674307`, archive SHA-256 `1d5c9490e53c4b75948360f0170e311a6d371d8bf86a53854a0d593399367a28`

STOP if the candidate SHA, artifact ID, or downloaded archive digest does not match.

## Before opening the application

1. Verify the downloaded ZIP digest using the commands in `STAGE_8_MANUAL_AUDIT_PACKET.md`.
2. Record the machine OS version, display scaling, keyboard layout, assistive-technology name/version, reviewer/operator identifier and date.
3. Use a clean/synthetic pilot profile. Do not enter real child personal data.
4. Run the packaged application from the verified archive. Do not substitute a source-tree launch.

## PR-08 — Windows

Perform the complete learner path using keyboard only:
- onboarding;
- diagnostic;
- answer submission;
- hint use;
- remediation path;
- return to learning;
- progress screen.

Record separately:
- focus order;
- visible focus;
- whether every actionable control is reachable;
- whether feedback can be discovered without color;
- behavior at 200% text/display scaling.

Repeat the relevant path with Narrator and record spoken control names/states and whether changed feedback is announced/discoverable.

## PR-08 — macOS

Repeat the same complete path with keyboard navigation and VoiceOver. Record the same observations separately from Windows.

Do not copy a Windows result into the macOS column or vice versa.

## PR-10 — learner-visible content

Review the exact bounded inventory in `PILOT_CONTENT_REVIEW_INVENTORY.md` on candidate `983d04c...`.

Required judgments:
- understandable for the intended grade/age;
- mathematically unambiguous;
- no humiliating, manipulative or unsafe wording;
- no unsupported factual claims in hints/feedback;
- no pressure to continue;
- runtime messages accurately describe hint use and learning status.

A fingerprint match is only drift evidence. It is not a human content PASS.

## PR-10 — operations/data

Fill real decisions in `PILOT_DATA_OPERATIONS_TEMPLATE.md` and `PILOT_MANUAL_GATE_RECORD.md`:
- operator/controller role;
- jurisdiction;
- intended participant age range;
- guardian/participant authorization procedure;
- retention period;
- deletion/withdrawal route;
- support contact;
- incident owner/communication route;
- exact-candidate external-transfer verification;
- synthetic backup/restore rehearsal.

## Failure handling

For every FAIL:
1. record exact platform/version;
2. record reproducible steps;
3. record the expected and observed behavior;
4. create/link a sanitized defect reference;
5. leave the release gate BLOCKED.

Do not include learner personal data in issue text, screenshots or logs.

## Completion condition

Only after all required rows are PASS on the exact audit candidate and all operator fields are complete may the Controller consider the manual gate ready for reconciliation.

Any learner-visible/runtime fix after observation invalidates affected observations and requires a replacement audit candidate plus fresh same-SHA technical verification.

Final candidate nomination and PR-14 occur only after manual PR-08/PR-10 evidence has been reconciled.
