# Pilot data operations record

Complete before real-user enrollment.

Prepared audit candidate for rehearsal: `983d04c564879f9ff8b6de110497901279073aeb` (CI `37304924020`; Pilot Build `37304924030`). The rehearsal/review field below remains unfilled until a human/operator actually executes it.

Audit candidate SHA rehearsed/reviewed: [FILL]
Final candidate SHA re-verified: [FILL AT FINAL CANDIDATE NOMINATION]
Pilot operator: APPROVED — самостоятельное домашнее обучение; без отдельной организации-оператора
Jurisdiction: APPROVED — Russia; setting APPROVED — самостоятельное домашнее обучение

## Local data
Storage location used by deployment: default `~/.repetitor` unless the operator explicitly launches with `--data-dir`; primary DB is `repetitor.sqlite3`, startup diagnostic log is `startup-errors.log`.
Backup owner/process: APPROVED POLICY — only synthetic/test backup unless production learner-data backup is separately approved; use the tested SQLite backup path described in `DATA_BACKUP_RECOVERY.md`; do not copy/replace a live database ad hoc.
Retention period: APPROVED — active pilot + 30 days; delete earlier on withdrawal/request or participant leaving the pilot
Deletion trigger/process: APPROVED — retention expiry, withdrawal/request, or participant leaving; delete local learner DB and any approved copies/diagnostic material containing that learner
Withdrawal request route: APPROVED — parent/legal guardian
Support contact: APPROVED ROLE — parent(s)/legal guardian(s) who provide authorization before learning

## Data transfer
Default candidate: local/offline core.

Any external transfer enabled? APPROVED POLICY = NO production child sync, public recovery, external AI/LLM with learner data, or external learner-data telemetry/analytics. Exact-candidate operational observation remains NOT TESTED and must be recorded before enrollment.
If YES, pilot is blocked until the destination, exact fields, purpose, authorization, retention, deletion path, security/authentication and child-safety review are documented and approved.

## Incident handling
Person/role receiving incident reports: APPROVED — parent(s)/legal guardian(s) who provide authorization before learning
How affected local data is preserved without unnecessary copying: stop the affected session; preserve the original `~/.repetitor` data directory (or configured `--data-dir`) in place where feasible; use the tested backup procedure when a recovery copy is required; do not paste learner data into issue text.
How participant/guardian communication is handled when required: APPROVED ROLE — through the parent/legal guardian; jurisdiction: Russia; applicable notification obligations remain operator responsibility

## Candidate verification checklist
- [ ] Audit candidate SHA/build used for rehearsal recorded above.
- [ ] Exact final candidate SHA/build recorded and re-verified above.
- [ ] `--data-dir` behavior and actual deployment data directory verified.
- [ ] Primary SQLite database and startup-log locations verified on deployed build.
- [ ] Backup/restore rehearsal completed with synthetic data using `DATA_BACKUP_RECOVERY.md`.
- [ ] Network/external-transfer behavior verified on the exact candidate using `STAGE_8_EXACT_BUILD_NETWORK_OBSERVATION.md`; destinations/fields documented if any.
- [ ] Retention, deletion/withdrawal, support and incident roles filled by the real operator.

Status: [BLOCKED / APPROVED FOR STATED PILOT]
