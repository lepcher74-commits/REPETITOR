# Stage 8 — Production Readiness & Pilot

Status: APPROVED / ACTIVE
Approved by Controller: 2026-10-01

## Goal

Prepare REPETITOR for a limited, controlled pilot with real users. This stage does not claim readiness for mass production.

## Approved scope

### E8.1 — Reproducible desktop packaging
- Build an installable desktop artifact from a clean checkout.
- Windows and macOS are mandatory pilot targets; Linux remains CI/reference.
- Package must include trusted local content and start without a Python development environment.
- Version/build metadata must be visible and reproducible from the repository.

### E8.2 — Release pipeline and artifact verification
- CI builds pilot artifacts on supported targets.
- Build failures are visible and fail closed.
- Automated smoke check verifies packaged application structure/content before publishing artifacts.
- No claim of code signing/notarization until actually configured and verified.

### E8.3 — Local data safety and recovery
- Define backup/restore contract for the local SQLite learner database.
- Recovery must not silently overwrite a newer database.
- Corrupt/unreadable data must produce a clear failure path rather than fabricated progress.
- Automated persistence/recovery tests are required.

### E8.4 — Runtime resilience
- User-facing handling for recoverable startup/runtime failures.
- No learning-state mutation from optional AI failure.
- Unexpected failures must not be presented as successful learning actions.
- Add tests for critical failure boundaries where practical.

### E8.5 — Accessibility release audit
- Execute the manual checklist defined in docs/ACCESSIBILITY_AUDIT.md on available target systems.
- Record untested combinations explicitly.
- Automated accessibility tests remain mandatory.
- No WCAG conformance claim without sufficient evidence.

### E8.6 — Privacy and child-safety release review
- Document local data inventory and external data flows.
- Verify optional AI path sends only documented minimum context.
- Verify no advertising, behavioral engagement loops, or hidden cloud requirement.
- Record legal/compliance items as review requirements, not unsupported certification claims.

### E8.7 — Pilot content sufficiency
- Expand the grade-6 fractions pilot beyond the two-skill proof while preserving the content contract.
- Every new skill must pass repository graph validation and formal verification where applicable.
- Fresh evidence pools must remain finite and non-repeating by design.

### E8.8 — Controlled pilot protocol
- Define participant/session scope, consent/guardian workflow requirements, support/incident procedure, and exit criteria.
- Define learning-effect measures before pilot observation.
- Separate product telemetry from pedagogical evidence; collect only what is necessary and permitted.
- Do not claim efficacy from an uncontrolled or undersized pilot.

## Acceptance criteria

- PR-01 Windows pilot artifact builds reproducibly in CI.
- PR-02 macOS pilot artifact builds reproducibly in CI.
- PR-03 packaged app contains required trusted offline content.
- PR-04 packaged startup smoke check is automated where runner constraints permit.
- PR-05 local database backup/restore is documented and tested.
- PR-06 corrupt or conflicting restore fails safely.
- PR-07 critical runtime failures have explicit user-facing paths.
- PR-08 automated accessibility baseline remains green; manual audit results/limitations recorded.
- PR-09 privacy/data-flow inventory is documented and checked against implementation.
- PR-10 child-safety release checklist is documented.
- PR-11 pilot curriculum contains multiple connected grade-6 fraction skills through generic architecture.
- PR-12 pilot protocol and measurement plan exist before real-user pilot.
- PR-13 all Stage 5–7 regressions remain green.
- PR-14 final pilot candidate commit passes the supported CI/release matrix.

## Non-goals

- Mass-market production launch.
- Unsupported efficacy claims.
- Automatic collection of child data.
- Cloud dependency for the learning core.
- LLM authority over scoring or mastery.
- Code-signing/notarization claims before credentials and platform verification exist.
- New school subject before the mathematics pilot is operationally proven.

## Gate

Stage 8 closes only when the repository contains a verifiable pilot candidate satisfying PR-01–PR-14, residual risks are documented, and the Controller explicitly approves the pilot-readiness gate.
