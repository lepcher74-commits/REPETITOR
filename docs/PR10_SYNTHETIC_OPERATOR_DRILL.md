# PR-10 synthetic operator drill and evidence worksheet

Status: NOT EXECUTED. Use only invented test records, never a real child's profile. This worksheet does not replace guardian verification, legal review, actual content sign-off or accessibility audit.

## Before starting

- Operator/reviewer: parent/legal guardian conducting independent home learning [APPROVED ROLE]; date: [FILL]; audit candidate SHA: `983d04c564879f9ff8b6de110497901279073aeb`; artifact ID: [FILL WINDOWS/MACOS USED].
- Approved test machine and OS: [FILL]; test data directory (not a real participant's directory): [FILL].
- Planned backup location and owner: synthetic/test only unless separately approved [POLICY APPROVED]; approved local retention period: active pilot + 30 days with earlier withdrawal/request deletion; support and incident role: parent(s)/legal guardian(s) who provided authorization.
- Keep all evidence sanitized. Do not commit names of children, parent emails, SQLite databases, logs containing personal data or recovery tokens.

## A. Local data, backup, restore and withdrawal rehearsal

| Step | Operator action | Expected observation | Actual observation / sanitized evidence | Result |
|---|---|---|---|---|
| A1 | Launch pinned offline build with a **separate synthetic** data directory; create an invented learner session. | Data remains within intended operator-managed local locations. | [FILL] | NOT TESTED |
| A2 | Locate database, startup log if any and any actual backups; list all copies and people/devices with access. | Inventory includes every operator-managed copy. | [FILL] | NOT TESTED |
| A3 | Stop or safely quiesce the app and perform documented SQLite backup from `DATA_BACKUP_RECOVERY.md`. | Backup is created without copying a live database ad hoc. | [FILL] | NOT TESTED |
| A4 | Restore synthetic backup in a fresh **test** directory using documented procedure. | Synthetic progress returns and database passes integrity/schema validation. | [FILL] | NOT TESTED |
| A5 | Simulate a withdrawal request through the proposed support route. | Request reaches assigned owner; authorization and completion are recorded in a separate approved system. | [FILL] | NOT TESTED |
| A6 | Apply the proposed deletion process to synthetic primary data and all operator-managed backups, subject to an explicitly documented lawful hold if applicable. | Inventory accounts for each copy; no claim about inaccessible external backups. | [FILL] | NOT TESTED |
| A7 | Try reopening the deleted synthetic profile from approved local locations. | No undeclared operator-managed copy recreates it. | [FILL] | NOT TESTED |

Stop and mark FAIL if any step risks a real participant's data. Do not use automated unit-test PASS as proof this operational drill happened.

## B. Lost-device incident tabletop (discussion only)

| Step | Operator decision to demonstrate | Evidence / reviewer | Result |
|---|---|---|---|
| B1 | Who receives and timestamps the report, and how is access to affected device/data restricted? | [FILL] | NOT TESTED |
| B2 | Who inventories affected local files, backups and possible exposure without circulating raw child data? | [FILL] | NOT TESTED |
| B3 | Who decides applicable notifications and timelines after legal/security review? | [FILL] | NOT TESTED |
| B4 | What approved channel reaches guardians and support if notification is required? | [FILL] | NOT TESTED |
| B5 | Who authorizes safe restoration, logs lessons learned and determines whether pilot must stop? | [FILL] | NOT TESTED |

## C. Admission and content gates

- Pilot owner/role: APPROVED — independent home learning, parent/legal guardian operator. Setting: APPROVED — home learning. Legal jurisdiction (country/region): [FILL].
- Participant scope: APPROVED — school grades 5–11. Numeric pilot-size maximum, actual location/jurisdiction and supported OS/assistive-technology combinations: [FILL / NOT TESTED].
- Guardian-authority model: APPROVED B1 — explicit parent/legal-guardian authorization before enrollment, recorded outside the child-facing app; withdrawal route through parent/legal guardian. Actual per-participant execution: NOT TESTED.
- Human content reviewer: APPROVED ROLE — Controller or reviewer explicitly appointed by Controller. Exact candidate/content binding is prepared; 135-row human review remains NOT TESTED.
- Data-transfer policy: APPROVED — no production child sync, public recovery, external AI/LLM with learner data, or external learner-data telemetry/analytics. Exact-build operational observation remains NOT TESTED.

## Evidence disposition

Operator signs only after real rehearsal and review: [NAME/ROLE], [DATE], [EVIDENCE REFS]. Until then all results above are **NOT TESTED**. Copy verified outcomes into `PILOT_MANUAL_GATE_RECORD.md` and `PILOT_DATA_OPERATIONS_TEMPLATE.md`; do not declare PR-10 PASS from this blank worksheet.

Independent blockers: Controller deferred the Windows Narrator retest; PR-08 remains BLOCKED. PR-14 final same-SHA verification and Controller approval remain pending.
