# Pilot data operations record

Complete before real-user enrollment.

Prepared audit candidate for rehearsal: `983d04c564879f9ff8b6de110497901279073aeb` (CI `37304924020`; Pilot Build `37304924030`). The rehearsal/review field below remains unfilled until a human/operator actually executes it.

Audit candidate SHA rehearsed/reviewed: [FILL]\nFinal candidate SHA re-verified: [FILL AT FINAL CANDIDATE NOMINATION]
Pilot operator: [FILL]
Jurisdiction: [FILL]

## Local data
Storage location used by deployment: default `~/.repetitor` unless the operator explicitly launches with `--data-dir`; primary DB is `repetitor.sqlite3`, startup diagnostic log is `startup-errors.log`.
Backup owner/process: [OPERATOR TO ASSIGN]; use the tested SQLite backup path described in `DATA_BACKUP_RECOVERY.md`; do not copy/replace a live database ad hoc.
Retention period: [FILL]
Deletion trigger/process: [FILL]
Withdrawal request route: [FILL]
Support contact: [FILL]

## Data transfer
Default candidate: local/offline core.

Any external transfer enabled? [OPERATOR TO VERIFY ON EXACT CANDIDATE]. The current documented architecture is local/offline, but this record must not inherit that answer across candidate changes. Before enrollment, verify the exact candidate source/build and record YES/NO here.
If YES, pilot is blocked until the destination, exact fields, purpose, authorization, retention, deletion path, security/authentication and child-safety review are documented and approved.

## Incident handling
Person/role receiving incident reports: [OPERATOR TO ASSIGN]
How affected local data is preserved without unnecessary copying: stop the affected session; preserve the original `~/.repetitor` data directory (or configured `--data-dir`) in place where feasible; use the tested backup procedure when a recovery copy is required; do not paste learner data into issue text.
How participant/guardian communication is handled when required: [OPERATOR TO DEFINE FOR JURISDICTION/SETTING]

## Candidate verification checklist
- [ ] Audit candidate SHA/build used for rehearsal recorded above.\n- [ ] Exact final candidate SHA/build recorded and re-verified above.
- [ ] `--data-dir` behavior and actual deployment data directory verified.
- [ ] Primary SQLite database and startup-log locations verified on deployed build.
- [ ] Backup/restore rehearsal completed with synthetic data using `DATA_BACKUP_RECOVERY.md`.
- [ ] Network/external-transfer behavior verified on the exact candidate; destinations/fields documented if any.
- [ ] Retention, deletion/withdrawal, support and incident roles filled by the real operator.

Status: [BLOCKED / APPROVED FOR STATED PILOT]
