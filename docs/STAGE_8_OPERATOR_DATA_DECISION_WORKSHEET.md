# Stage 8 operator and data-operations decision worksheet

Status: PREPARED / BLOCKED UNTIL COMPLETED BY REAL OPERATOR.

Audit candidate: `983d04c564879f9ff8b6de110497901279073aeb`
CI: `37304924020`
Pilot Build: `37304924030`

This worksheet captures PR-10 operational decisions. It is not legal advice or a legal-compliance certification. Do not infer answers from repository architecture where an operator/jurisdiction decision is required.

## Pilot context

| Field | Decision |
|---|---|
| Pilot operator/controller legal or organizational role | [FILL] |
| Jurisdiction / setting | [FILL] |
| Intended participant age range | [FILL] |
| Intended pilot size | [FILL] |
| Responsible support contact | [FILL] |
| Incident-response owner | [FILL] |

## Authorization

| Decision | Result / procedure |
|---|---|
| Participant/guardian authorization required? | [FILL] |
| Who is authorized to give it? | [FILL] |
| How authorization is obtained before enrollment | [FILL] |
| How authorization is recorded | [FILL] |
| How withdrawal is requested | [FILL] |
| What happens immediately after withdrawal | [FILL] |

STOP enrollment until the applicable authorization process is explicitly defined for the intended jurisdiction/setting.

## Local data lifecycle

Known repository fact: default local data location is `~/.repetitor` unless launched with `--data-dir`; primary DB is `repetitor.sqlite3`; startup diagnostic log is `startup-errors.log`.

| Decision / rehearsal | Result |
|---|---|
| Actual deployment data directory verified | NOT TESTED |
| Backup owner assigned | [FILL] |
| Synthetic backup executed | NOT TESTED |
| Synthetic restore executed | NOT TESTED |
| Restored application state verified | NOT TESTED |
| Retention period | [FILL] |
| Deletion trigger | [FILL] |
| Deletion procedure | [FILL] |
| Withdrawal/deletion request route | [FILL] |
| Support route | [FILL] |

## Exact-build external-transfer check

Repository design indicates a local/offline core, but that is not sufficient for this operational row.

| Check | Result |
|---|---|
| Exact candidate launched from verified artifact | NOT TESTED |
| Unexpected outbound connection observed during normal learning flow | NOT TESTED |
| External child/learner data transfer enabled | [FILL YES/NO] |
| If YES: destination/provider | [FILL / N/A] |
| If YES: exact fields transferred | [FILL / N/A] |
| If YES: purpose and authorization | [FILL / N/A] |
| If YES: retention/deletion path | [FILL / N/A] |

If any unreviewed production network AI or child-data destination is enabled, STOP the pilot until separately reviewed and approved.

## Incident handling

| Field | Decision |
|---|---|
| How an incident is reported | [FILL] |
| Who receives it | [FILL] |
| How affected local data is preserved without unnecessary copying | [FILL] |
| How participant/guardian communication is handled if required | [FILL] |
| How learner data is kept out of issue trackers/screenshots/log excerpts | [FILL] |

## Completion

Operator/data rehearsal performed by: [FILL]

Date: [FILL]

Audit candidate SHA rehearsed/reviewed: [FILL]

Overall operational PR-10 result: **BLOCKED**

Only a real operator may replace the placeholders/NOT TESTED values. Any material deployment/runtime change after rehearsal requires affected operational checks to be repeated before final-candidate nomination.
