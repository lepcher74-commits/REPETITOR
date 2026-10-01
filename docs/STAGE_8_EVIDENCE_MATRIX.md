# Stage 8 — Production Readiness & Pilot evidence matrix

Candidate baseline: `d1eb80df0f75143ea78df7a3aba46f16fa3cedae`
Recorded: 2026-10-01

Status vocabulary:
- **PASS** — objective repository/CI evidence exists.
- **BLOCKED** — required manual/operational evidence is not yet complete.
- **NOT TESTED** — no valid evidence exists yet.

| Criterion | Status | Evidence |
|---|---|---|
| PR-01 Windows pilot artifact builds reproducibly in CI | PASS | Pilot Build run 36854193964; Windows job success |
| PR-02 macOS pilot artifact builds reproducibly in CI | PASS | Pilot Build run 36854193964; macOS job success |
| PR-03 packaged app contains required trusted offline content | PASS | Pilot Build verifies embedded manifest/problems; packaged smoke loads runtime content |
| PR-04 packaged startup smoke automated where runner constraints permit | PASS | Pilot Build run 36854193964 executes frozen Windows and macOS binaries with `--smoke-test` |
| PR-05 local DB backup/restore documented/tested | PASS | `persistence/backup.py`, persistence tests, `DATA_BACKUP_RECOVERY.md`; CI green after Windows handle fix |
| PR-06 corrupt/conflicting restore fails safely | PASS | corrupt backup and overwrite-conflict tests; Windows atomic-replace regression fixed and green |
| PR-07 critical runtime failures explicit user-facing paths | PASS | fail-closed startup boundary + integration test; minimal local startup diagnostics |
| PR-08 automated accessibility green; manual results/limits recorded | BLOCKED | automated checks green; `ACCESSIBILITY_PILOT_AUDIT_RECORD.md` explicitly leaves target OS/AT manual checks NOT TESTED |
| PR-09 privacy/data-flow inventory documented/checked | PASS | `PRIVACY_CHILD_SAFETY_REVIEW.md`; current default core has no required production network AI provider |
| PR-10 child-safety release checklist documented | PASS (documentation) / BLOCKED (pilot operation) | checklist exists; guardian/consent, retention/deletion and manual content/accessibility items remain operator gates |
| PR-11 pilot curriculum multiple connected grade-6 fraction skills through generic architecture | PASS | equivalent fractions, simplification, addition unlike denominators, subtraction unlike denominators; generic loaders/verifiers/tests |
| PR-12 pilot protocol/measurement plan before real-user pilot | PASS | `PILOT_PROTOCOL.md`; measures, minimization, incidents, stop conditions and interpretation limits pre-defined |
| PR-13 all Stage 5–7 regressions green | PASS | current CI run 36854206168 success after all Stage 8 changes |
| PR-14 final pilot candidate commit passes supported CI/release matrix | BLOCKED | baseline CI is green, but a final candidate cannot be declared until PR-08 and operational PR-10 blockers are resolved and the resulting final SHA is re-run |

## Current Stage 8 gate

Stage 8 is **not closed**.

Repository/automation evidence is strong enough for PR-01–07, PR-09, PR-11–13. The remaining release blockers are deliberately human/operational:
1. complete `PILOT_MANUAL_GATE_RECORD.md` for the intended Windows/macOS environment and assistive technology;
2. resolve pilot jurisdiction/operator/participant authorization and guardian/consent requirements in that record;
3. complete `PILOT_DATA_OPERATIONS_TEMPLATE.md` with actual retention/deletion procedure and support contact;
4. complete the age-appropriateness section of `PILOT_MANUAL_GATE_RECORD.md` for the complete pilot content;
5. after those records are committed, designate one final candidate SHA and require both CI and Pilot Build to pass again.

No efficacy, WCAG conformance, legal compliance, code-signing or notarization claim is made.
