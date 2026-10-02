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

The operator must enter its actual identity/role, applicable jurisdiction,
intended pilot participants, verified legal guardian authorization process,
support and incident contacts, retention period, withdrawal/deletion workflow,
and complete age-appropriateness review of every learner-visible pilot item.
Use PILOT_MANUAL_GATE_RECORD.md and PILOT_DATA_OPERATIONS_TEMPLATE.md.
Record who approved each decision and when. A mailbox challenge is not
guardian verification; do not enable cloud sync or public recovery.

## 4. Submit evidence and freeze

Attach sanitized observation logs and exact artifact/SHA references; exclude
children's personal data and recovery tokens. A reviewer must resolve failures
and mark any unsupported OS/AT combination out of pilot scope explicitly.
Then nominate the final candidate SHA and verify both CI and Windows/macOS
Pilot Build on that exact SHA. Record run IDs in STAGE_8_EVIDENCE_MATRIX.md.
Present remaining risks for explicit Controller approval. Never mark
NOT TESTED rows PASS based on automation or on this checklist.
