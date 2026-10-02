# Stage 8 PR-10 — operator decision packet (draft, not authorization)

Status: PREPARED / AWAITING OPERATOR. Jurisdiction planning assumption: Russian pilot, to be confirmed by actual operator and counsel. This packet is a decision aid, not evidence of legal compliance or consent.

## 1. Required named decisions

Record each decision in `PILOT_MANUAL_GATE_RECORD.md` and `PILOT_DATA_OPERATIONS_TEMPLATE.md` with decision maker, date and evidence reference. Do not put children's names, addresses, tokens or account credentials into GitHub.

| Decision | Operator must supply | Gate condition |
|---|---|---|
| Pilot owner | Actual organization/person, controller/operator responsibilities and escalation owner | Identified and accepted |
| Population | Actual participant age range, grade and intended platforms/locations | Bounded and recorded |
| Guardian authority | Documented process establishing that an authorizing adult has the requisite authority for each participating child, plus withdrawal path | Reviewed and approved; email verification alone insufficient |
| Pilot support | Reachable support channel, coverage hours and incident owner | Tested before admission |
| Local data | Data inventory, storage device ownership, access controls, retention trigger/period and secure disposal workflow | Documented and rehearsed with synthetic data |
| Incident response | Reporting route, device-loss response, access restriction, evidence handling, notification decision owner | Tabletop walkthrough documented |
| Content review | Reviewer of every learner-visible grade-6 pilot prompt, hint, explanation, feedback and progression message, with issue disposition | Completed on exact candidate content |
| Network scope | Offline-only default, explicit inventory of any intended outbound telemetry/AI/sync/recovery | No unreviewed endpoint or child transfer |

## 2. Proposed safe pilot admission workflow (requires approval)

1. Operator selects a narrowly bounded offline-only pilot cohort and supported devices. Do not recruit or collect real child data until all required gates are approved.
2. Operator gives the parent/authorized guardian a plain-language information notice describing purpose, local data, who has access, retention and deletion, incident contact, and withdrawal route. A legal reviewer checks applicable requirements for the actual operator and population.
3. Operator verifies guardian authority through its approved procedure and records only the minimum evidence needed outside the code repository. Email possession is **not** proof of guardian authority.
4. Operator records the authorization and any separate optional permissions using an approved, auditable process; do not silently treat general pilot participation as permission for network AI or cloud synchronization.
5. Operator installs only the pinned approved artifact on approved devices; checks backup/restore and support route with synthetic records first.
6. Before first learner session, operator verifies child-facing material review, required accessibility support for each included participant, and ability to stop participation and delete local data.

## 3. Local data and withdrawal drill — synthetic only

- Inventory actual local storage, backup locations and authorized access. The application's default offline data location and tested SQLite backup are technical facts, not an operator retention policy.
- On a synthetic device, practice stopping use, preserving only any records lawfully needed for a documented incident, deleting primary data and all operator-managed backups under the approved retention/deletion schedule, and recording completion without storing children's identifiers in GitHub.
- Record exceptional legal retention or incident hold decisions with a responsible reviewer; never promise instantaneous deletion from inaccessible third-party backups.
- A successful automated backup test does not establish that an operator performed this drill.

## 4. Incident tabletop — synthetic only

Scenario: a pilot laptop is lost or accessed by an unauthorized person. Operator documents the first contact, containment, assessment of affected local files/backups, who determines notification obligations, contact route for guardians, and recovery decision. Record dates, roles and lessons learned without personal data.

## 5. Acceptance evidence and blockers

For each requirement, provide a sanitized reference to the approved procedure, reviewer, date, scope and test result. Use `NOT TESTED` or `BLOCKED` until human evidence exists. Do not enter invented organization names, support contacts, retention periods, legal conclusions or guardian approvals.

Independent remaining blockers: PR-08 Narrator re-test is **deferred by Controller**, not passed; macOS accessibility observations and full end-to-end coverage remain unverified. PR-14 final same-SHA technical verification and Controller approval follow only after required manual/operational gates.
