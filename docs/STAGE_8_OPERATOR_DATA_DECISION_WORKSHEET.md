# Stage 8 operator and data-operations decision worksheet

Status: PREPARED / BLOCKED UNTIL COMPLETED BY REAL OPERATOR.

Audit candidate: `983d04c564879f9ff8b6de110497901279073aeb`
CI: `37304924020`
Pilot Build: `37304924030`

This worksheet captures PR-10 operational decisions. It is not legal advice or a legal-compliance certification. Do not infer answers from repository architecture where an operator/jurisdiction decision is required.

## Pilot context

| Field | Decision |
|---|---|
| Pilot operator/controller legal or organizational role | APPROVED — самостоятельное домашнее обучение; без отдельной организации-оператора |
| Jurisdiction / setting | Setting APPROVED — самостоятельное домашнее обучение; legal jurisdiction [FILL] |
| Intended participant age range | APPROVED — школьные классы 5–11 |
| Intended pilot size | [FILL — численный максимум не указан Controller] |
| Responsible support contact | APPROVED — родитель(и)/законный представитель(и), дающие согласие до начала обучения |
| Incident-response owner | APPROVED — родитель(и)/законный представитель(и), дающие согласие до начала обучения |

## Authorization

| Decision | Result / procedure |
|---|---|
| Participant/guardian authorization required? | YES — APPROVED (B1) |
| Who is authorized to give it? | Родитель/законный представитель |
| How authorization is obtained before enrollment | Явное разрешение родителя/законного представителя до включения ребёнка |
| How authorization is recorded | Оператор/родитель фиксирует согласие вне child-facing приложения |
| How withdrawal is requested | Запрос родителя/законного представителя |
| What happens immediately after withdrawal | Участник прекращает участие; данные удаляются по утверждённой процедуре |

STOP enrollment until the applicable authorization process is explicitly defined for the intended jurisdiction/setting.

## Local data lifecycle

Known repository fact: default local data location is `~/.repetitor` unless launched with `--data-dir`; primary DB is `repetitor.sqlite3`; startup diagnostic log is `startup-errors.log`.

| Decision / rehearsal | Result |
|---|---|
| Actual deployment data directory verified | NOT TESTED |
| Backup owner assigned | APPROVED POLICY — только synthetic/test backup; production learner-data backup требует отдельного одобрения |
| Synthetic backup executed | NOT TESTED |
| Synthetic restore executed | NOT TESTED |
| Restored application state verified | NOT TESTED |
| Retention period | APPROVED — активный пилот + 30 дней |
| Deletion trigger | APPROVED — окончание retention, withdrawal/request или выход из пилота |
| Deletion procedure | APPROVED — удалить локальную SQLite DB и любые одобренные копии/диагностические материалы, содержащие данные участника |
| Withdrawal/deletion request route | APPROVED — через родителя/законного представителя |
| Support route | APPROVED — через родителя/законного представителя, давшего согласие |

## Exact-build external-transfer check

Repository design indicates a local/offline core, but that is not sufficient for this operational row.

| Check | Result |
|---|---|
| Exact candidate launched from verified artifact | NOT TESTED |
| Unexpected outbound connection observed during normal learning flow | NOT TESTED |
| External child/learner data transfer enabled | PROHIBITED BY APPROVED POLICY; exact-build observation still NOT TESTED |
| If YES: destination/provider | N/A under approved policy |
| If YES: exact fields transferred | N/A under approved policy |
| If YES: purpose and authorization | N/A under approved policy |
| If YES: retention/deletion path | N/A under approved policy |

If any unreviewed production network AI or child-data destination is enabled, STOP the pilot until separately reviewed and approved.

## Incident handling

| Field | Decision |
|---|---|
| How an incident is reported | APPROVED — участник/родитель сообщает родителю/законному представителю, ведущему домашнее обучение |
| Who receives it | APPROVED — родитель(и)/законный представитель(и), давшие согласие |
| How affected local data is preserved without unnecessary copying | APPROVED — остановить затронутую сессию; сохранять исходные локальные данные на месте где возможно; использовать tested backup только при необходимости |
| How participant/guardian communication is handled if required | APPROVED — через родителя/законного представителя; legal-jurisdiction-specific obligations remain [FILL] |
| How learner data is kept out of issue trackers/screenshots/log excerpts | APPROVED — не включать персональные данные ребёнка; редактировать/обезличивать перед передачей |

## Completion

Operator/data rehearsal performed by: [FILL]

Date: [FILL]

Audit candidate SHA rehearsed/reviewed: [FILL]

Overall operational PR-10 result: **BLOCKED**

Only a real operator may replace the placeholders/NOT TESTED values. Any material deployment/runtime change after rehearsal requires affected operational checks to be repeated before final-candidate nomination.
