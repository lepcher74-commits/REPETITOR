# PR-10 synthetic operator drill and evidence worksheet

Status: NOT EXECUTED. Use only invented test records, never a real child's profile. This worksheet does not replace guardian verification, legal review, actual content sign-off or accessibility audit.

## Before starting

- Operator/reviewer: [FILL]; date: [FILL]; candidate SHA and artifact ID: [FILL].
- Approved test machine and OS: [FILL]; test data directory (not a real participant's directory): [FILL].
- Planned backup location and owner: [FILL]; approved local retention period: [FILL]; support and incident contacts: [FILL].
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

- Pilot owner, role and jurisdiction: [FILL / NOT APPROVED].
- Participant age range, locations, OS/assistive technology support: [FILL / NOT APPROVED].
- Documented guardian-authority verification and withdrawal process (mailbox ownership alone is insufficient): [FILL / NOT APPROVED].
- Complete learner-visible content reviewer, exact content SHA, reviewed prompts/hints/explanations/feedback and disposition of issues: [FILL / NOT APPROVED].
- Data-transfer inventory: default offline only; any proposed network recovery, sync or AI integration requires separate explicit review. [CONFIRM / NOT APPROVED].

## Evidence disposition

Operator signs only after real rehearsal and review: [NAME/ROLE], [DATE], [EVIDENCE REFS]. Until then all results above are **NOT TESTED**. Copy verified outcomes into `PILOT_MANUAL_GATE_RECORD.md` and `PILOT_DATA_OPERATIONS_TEMPLATE.md`; do not declare PR-10 PASS from this blank worksheet.

Independent blockers: Controller deferred the Windows Narrator retest; PR-08 remains BLOCKED. PR-14 final same-SHA verification and Controller approval remain pending.
