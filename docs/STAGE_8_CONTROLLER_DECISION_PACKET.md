# Stage 8 Controller decision packet

Status: REQUIRES CONTROLLER DECISION. No approval is implied by this document.

Audit candidate: `983d04c564879f9ff8b6de110497901279073aeb`

This packet collects only decisions that cannot be derived safely from source code, CI, artifacts or assistant review. Once the Controller approves/fills these items, the approved values can be written into the PR-10 operational records. Manual accessibility PR-08 still requires actual Windows/macOS observation and is not replaced by this packet.

## A. Pilot operator and setting

Please approve/fill:

- Pilot operator/controller legal or organizational role: [DECIDE]
- Jurisdiction / setting in which the pilot will run: [DECIDE]
- Intended participant age range: [DECIDE]
- Intended pilot size (maximum simultaneous/total participants): [DECIDE]
- Responsible support contact or role: [DECIDE]
- Incident-response owner or role: [DECIDE]

## B. Authorization model

Choose and approve one model appropriate to the intended setting:

### Option B1 — guardian authorization before enrollment
- No child is enrolled until a parent/guardian or other legally authorized adult gives explicit permission.
- Authorization is recorded by the operator outside the child-facing application.
- Withdrawal may be requested by the same authorized adult.
- On withdrawal, the learner is removed from the pilot and the local learner data is deleted according to the approved deletion procedure.

### Option B2 — institution-managed authorization
- Enrollment is allowed only when the participating school/organization confirms it has the required authority/consent for the intended participants.
- The operator records which institution authorized the pilot and the applicable process.
- Withdrawal and deletion requests are routed through the institution/operator.

### Option B3 — other
Describe the exact authorization basis/process: [DECIDE]

Selected authorization model: [DECIDE]

## C. Data retention and deletion

Recommended minimal-risk pilot defaults for Controller approval or replacement:

- Data location: local device only, using the verified offline build.
- Retention: keep learner data only for the active pilot plus **30 days** for issue resolution, then delete.
- Early deletion: delete sooner on withdrawal/request or when the participant leaves the pilot.
- Backups: synthetic/test backups only unless the Controller explicitly approves production learner-data backup.
- Deletion scope: local SQLite DB, any operator-created backup containing that learner, and any copied diagnostic material containing learner data.
- Issue trackers/screenshots/log excerpts must not contain learner personal data.

Approve these defaults: YES / NO
If NO, replacement retention/deletion policy: [DECIDE]

## D. External transfer / network policy

Recommended Stage 8 pilot restriction:

- No production child sync.
- No public recovery service.
- No external AI/LLM call with learner data.
- No learner-data upload to analytics/telemetry service.
- If any unexpected outbound connection or external learner-data destination is observed, STOP the pilot until separately reviewed.

Approve this restriction: YES / NO
If NO, describe each allowed external destination, fields, purpose, authorization and retention/deletion path: [DECIDE]

## E. Support and incident handling

Recommended minimal process:

1. Participant/guardian reports an issue to the approved support contact/role.
2. Support escalates privacy/safety incidents to the approved incident owner.
3. Only the minimum local evidence required to reproduce the issue is retained.
4. Learner personal data is removed/redacted from GitHub issues, screenshots and shared logs.
5. If applicable under the approved setting/jurisdiction, the operator handles participant/guardian notification and any required legal notification.

Approve this process: YES / NO
If NO, replacement process: [DECIDE]

## F. Controller authorization to write approved decisions into Stage 8 records

After the Controller supplies/approves A–E, the assistant may:
- update `STAGE_8_OPERATOR_DATA_DECISION_WORKSHEET.md`;
- update `PILOT_DATA_OPERATIONS_TEMPLATE.md`;
- update the operational portions of `PILOT_MANUAL_GATE_RECORD.md`;
- update issue #3 with the approved Controller decisions;
- keep operational PR-10 BLOCKED until actual synthetic backup/restore and exact-build external-transfer checks are performed.

Controller decision: [PENDING]

## What this does not approve

Even after A–F are approved:
- PR-08 remains blocked until Windows/Narrator and macOS/VoiceOver observations are actually performed;
- human content review remains separate unless the Controller explicitly designates a real reviewer and that reviewer completes the 135-row worksheet;
- final candidate is not automatically nominated;
- PR-14 remains blocked until all required manual evidence is reconciled.
