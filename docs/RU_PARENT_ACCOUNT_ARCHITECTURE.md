# Stage 8 — Approved Russian parent-account and data architecture

Status: DESIGN APPROVED by Controller 2026-10-02; IMPLEMENTATION AND LEGAL REVIEW PENDING.
Scope change: add optional Russian-hosted parent registration, consent workflow and sync architecture; retain fully offline child learning. This document is a design, not a claim of legal compliance.

## Roles and access
- Parent/legal representative is the account owner. A child receives a pseudonymous local profile and cannot independently activate cloud services.
- Verified email proves mailbox access only. It does **not** establish age, identity, parenthood or legal authority.
- A parent's declaration is recorded but cannot alone be treated as verified representative status. Until a legally reviewed verification method and appropriate consent are completed, cloud processing of child data stays disabled.
- Age band and school grade are preferred over date of birth. Never infer age from email.
- Support grades 1–11 in identity design; Stage 8 pilot curriculum remains the approved grade-6 mathematics fraction module.

## Consent and evidence
- Present separate, comprehensible notices and choices for account administration, optional learning-data synchronization, and any future external AI transfer. Optional purposes default OFF; no bundled consent.
- Capture notice/consent version, purpose, actor, timestamp, explicit action, verification status and withdrawal event in an append-only audit record without unnecessary child content.
- Do not enable child-data sync on an unchecked box or email verification alone.
- Legal review must establish the lawful basis, representative verification method, required consent form and evidence, localization and operator obligations under applicable Russian law before any live collection.
- No passport scans, biometrics or facial recognition in the pilot by default.

## Data flow and storage
- Local-first: existing SQLite learning state remains functional without registration, internet or server.
- Optional service: Russian-hosted application API + PostgreSQL in a Russian data center; encrypted transport and backups in a separate Russian facility subject to vendor due diligence.
- Keep identity/consent records separate from pseudonymous learning records. Minimize server fields; do not upload free-form child dialogue, raw answers or diagnostics by default.
- No production external AI provider or external transfer is enabled in this candidate.
- No cloud credentials or secrets in repository. Server/provider selection requires documented contract, security review and verified hosting geography.

## Proposed operational policy [ASSUMPTION; operator/legal approval pending]
- Authenticated parent may request export, withdraw optional consent or request deletion. Immediately block further optional sync on withdrawal; preserve only records required under an independently documented legal basis.
- Target working-data deletion within 30 calendar days after verified request; backups age out within 90 days. These are project targets, NOT statutory universal periods. Publish the exact policy and exceptions after legal/operator approval.
- Enforce least privilege, MFA for operators, audit access, encrypted backups and tested restore. Incident owner/contact and notification duties must be set before pilot.
- Fail closed if authorization, consent evidence, connectivity or server status is uncertain. Local offline lessons continue.

## Implementation gates (no live children before all pass)
1. Legal/operator decision: Russian legal entity or person acting as operator, jurisdiction and counsel-approved consent/representative verification.
2. Server/provider contract and threat/privacy review; Russian hosting and backups verified.
3. Implement parent onboarding, separate consent ledger, withdrawal/deletion/export and secure optional sync behind default-off feature flag.
4. Automated negative tests: child cannot enable sync; email alone cannot verify representative; revoked consent blocks uploads; offline app works; retention/deletion and recovery paths tested.
5. Manual Windows Narrator/macOS VoiceOver full-flow accessibility checks and full pilot content age review.
6. Re-run final same-SHA CI and Pilot Build. Stage 8 closure still requires Controller approval.

No claim of 152-FZ compliance, consent validity, production security or accessibility conformance is made by this design.
