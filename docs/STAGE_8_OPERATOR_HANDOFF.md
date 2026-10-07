# Stage 8 operator handoff — manual evidence collection

Status: ready-to-use instructions, NOT completed audit or pilot authorization.

## 1. Lock the artifact being inspected

Download the Windows and macOS artifacts from the same successful Pilot Build
workflow run. Record its exact Git commit SHA, run ID and artifact identifiers
before beginning. If the application or content changes, repeat affected checks
on the new candidate; do not reuse observations from an older build.

## 2. PR-08 interactive accessibility evidence

For each intended pilot platform, record OS build, display scale, keyboard
layout, assistive technology and version, reviewer and test date in
ACCESSIBILITY_PILOT_AUDIT_RECORD.md and PILOT_MANUAL_GATE_RECORD.md.
Run the actual learner flow: onboarding, diagnostic, answering, remediation
and progress. For every listed check, mark PASS, FAIL or NOT TESTED.
For a failure record reproduction steps, expected/observed behavior and
issue link. A screenshot alone cannot prove screen-reader announcements.

Required target observations: keyboard-only completion, spoken actionable
names/states (Windows Narrator or macOS VoiceOver), sensible focus order,
feedback not conveyed by color alone, readable/operable 200% text scaling,
and visible focus.

## 3. PR-10 operational and child-safety evidence

Controller-approved PR-10 policy is already recorded: independent home learning
with parent/legal-guardian operator role; school grades 5–11; B1 explicit
guardian authorization before enrollment; local retention for active pilot
plus 30 days with earlier withdrawal/request deletion; synthetic/test backups
only unless separately approved; and no production child sync, public recovery,
external AI/LLM with learner data, or external learner-data telemetry/analytics.
Support/incident role is the parent/legal guardian providing authorization.
Legal jurisdiction is approved as Russia and maximum pilot size is approved as
10 participants. The operator must still record actual contact/channel details,
exact-build network observation, synthetic backup/restore rehearsal and the
completed human content review. Use PILOT_MANUAL_GATE_RECORD.md, PILOT_DATA_OPERATIONS_TEMPLATE.md and
STAGE_8_CONTROLLER_DECISION_PACKET.md. Do not treat mailbox ownership alone as
guardian authority and do not enable prohibited network features.

## 4. Submit evidence and freeze

Attach sanitized observation logs and exact artifact/SHA references; exclude
children's personal data and recovery tokens. A reviewer must resolve failures
and mark any unsupported OS/AT combination out of pilot scope explicitly.
Then nominate the final candidate SHA and verify both CI and Windows/macOS
Pilot Build on that exact SHA. Record run IDs in STAGE_8_EVIDENCE_MATRIX.md.
Present remaining risks for explicit Controller approval. Never mark
NOT TESTED rows PASS based on automation or on this checklist.
