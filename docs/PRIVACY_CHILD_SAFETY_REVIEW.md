# Stage 8 privacy and child-safety release review

Status: technical privacy/child-safety baseline. Final pilot candidate is NOT NOMINATED. This document is not a legal certification.

## Current local data inventory

The default application stores data locally in `repetitor.sqlite3`:
- student profile: local stable ID, selected subject, grade, learning goal;
- attempts: problem/skill IDs, timestamp, correctness, purpose, hint metadata, transfer/misconception/prerequisite flags;
- computed knowledge state: mastery, confidence, independence, transfer, retention, evidence count;
- review queue and session-resume state.

Startup diagnostics are local in `startup-errors.log` and contain only UTC timestamp, event name and exception class. Exception messages are deliberately excluded.

The current profile schema does not require a child's name, email, phone number, address, account credential or advertising identifier.

## External data flows

- The default learning core is offline.
- `NoAIProvider` is the default no-network behavior.
- `SafeAIProvider` is an interface/failure boundary; this repository does not currently configure a production network AI provider.
- Therefore the currently reviewed repository architecture has no required AI/cloud data flow. This is not a final-candidate assertion; network/data-flow behavior must be re-verified on the exact nominated build before enrollment.
- Before any production AI provider is enabled, its exact destination, fields, retention, authentication, consent/guardian requirements and deletion path must be documented and reviewed. Only minimum pedagogical context may be sent.

## Child-safety release checklist

Required before controlled pilot. Checked technical items below describe the reviewed repository implementation; they must not be interpreted as approval of an un-nominated final candidate:
- [x] No advertising path in the application architecture currently implemented.
- [x] Learning core works without AI/cloud availability.
- [x] Formal verification, not an LLM, controls supported mathematical correctness.
- [x] Optional AI failure cannot mutate mastery through the AI boundary.
- [x] Local startup diagnostics exclude exception messages/learner answers by test.
- [x] Recovery refuses silent overwrite by default and rejects corrupt backups.
- [x] Progress UI is knowledge-oriented rather than time/engagement-oriented.
- [ ] Pilot operator confirms guardian/consent workflow appropriate to pilot jurisdiction and participant age.
- [ ] Pilot operator confirms data retention/deletion procedure and support contact.
- [ ] Manual content review confirms age-appropriate wording for the complete pilot content set.
- [ ] Manual accessibility audit is recorded for available Windows/macOS assistive technology combinations.
- [ ] Exact final candidate/build is re-checked for outbound network/data flows before enrollment.
- [ ] Any future network AI provider receives a separate privacy/safety review before activation.

## Release blockers

The following block a real-user pilot even if automated CI is green:
1. Missing guardian/consent workflow where required.
2. Unknown retention/deletion procedure.
3. Undocumented network destination receiving child/learner data.
4. Known critical data-loss defect.
5. Known unsafe or age-inappropriate required content.
6. Required manual accessibility checks not recorded for the intended pilot environment.

## Legal/compliance boundary

The project is designed toward data minimization and child safety, but this repository does not claim legal compliance or certification under GDPR/GDPR-K, COPPA, 152-FZ, accessibility law, or another jurisdictional regime. Applicable obligations depend on pilot jurisdiction, operator role, participant ages, data flows and deployment details and require current legal review before a real-user pilot.
