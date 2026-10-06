# Stage 8 — Production Readiness & Pilot evidence matrix

Historical technical baseline: `87eceb5ca1e48bdd52943f65b594495d25af6998` (2026-10-01 evidence snapshot only; **not** the current/final pilot candidate)
Final pilot candidate: **NOT NOMINATED** — nominate only after manual/operational gates are complete.

Status vocabulary:
- **PASS** — objective repository/CI evidence exists.
- **BLOCKED** — required manual/operational evidence is not yet complete.
- **NOT TESTED** — no valid evidence exists yet.

| Criterion | Status | Evidence |
|---|---|---|
| PR-01 Windows pilot artifact builds reproducibly in CI | PASS | Pilot Build run 36862547237 on 87eceb5...; Windows frozen build/full-sequence smoke/provenance verification success |
| PR-02 macOS pilot artifact builds reproducibly in CI | PASS | Pilot Build run 36862547237 on 87eceb5...; macOS frozen build/full-sequence smoke/provenance verification success |
| PR-03 packaged app contains required trusted offline content | PASS | Pilot Build 36862547237 verifies embedded content; frozen smoke loads the full declared learning sequence and prerequisite DAG |
| PR-04 packaged startup smoke automated where runner constraints permit | PASS | Pilot Build 36862547237 executes frozen Windows/macOS binaries with `--smoke-test` and verifies exact build SHA |
| PR-05 local DB backup/restore documented/tested | PASS | `persistence/backup.py`, schema-aware persistence tests, `DATA_BACKUP_RECOVERY.md`; schema hardening `c82c5d7...`, CI 36856369288 success |
| PR-06 corrupt/conflicting restore fails safely | PASS | corrupt backup, healthy-unrelated-SQLite rejection and overwrite-conflict tests; schema hardening `c82c5d7...`, CI 36856369288 success |
| PR-07 critical runtime failures explicit user-facing paths | PASS | fail-closed startup boundary + integration test; minimal local startup diagnostics |
| PR-08 automated accessibility green; manual results/limits recorded | BLOCKED | automated checks green; `ACCESSIBILITY_PILOT_AUDIT_RECORD.md` explicitly leaves target OS/AT manual checks NOT TESTED |
| PR-09 privacy/data-flow inventory documented/checked | PASS | `PRIVACY_CHILD_SAFETY_REVIEW.md`; current default core has no required production network AI provider |
| PR-10 child-safety release checklist documented | PASS (documentation) / BLOCKED (pilot operation) | checklist exists; guardian/consent, retention/deletion and manual content/accessibility items remain operator gates |
| PR-11 pilot curriculum multiple connected grade-6 fraction skills through generic architecture | PASS | declarative sequence equivalent → simplify → add_unlike → subtract_unlike; real prerequisite DAG loaded from skill metadata; generic runtime progression; each sequence skill now has 3 unique declarative review problems; regression/contract tests included |
| PR-12 pilot protocol/measurement plan before real-user pilot | PASS | `PILOT_PROTOCOL.md`; measures, minimization, incidents, stop conditions and interpretation limits pre-defined |
| PR-13 all Stage 5–7 regressions green | PASS | CI run 36862547259 success on 87eceb5... after full-sequence packaged smoke, compile gate and sequence-router runtime fix |
| PR-14 final pilot candidate commit passes supported CI/release matrix | BLOCKED | baseline CI is green, but a final candidate cannot be declared until PR-08 and operational PR-10 blockers are resolved and the resulting final SHA is re-run |

## Current Stage 8 gate

Stage 8 is **not closed**.

Historical repository/automation evidence supports PR-01–07, PR-09 and PR-11–13 for the cited implementations/runs; these PASS rows do not nominate the current repository HEAD as the final pilot candidate. PR-13 is backed by CI 36862547259 on the same technical SHA 87eceb5... whose Windows/macOS Pilot Build 36862547237 also passed. PR-11 is a technical reachability result only and is not evidence of learning efficacy. The remaining release blockers are deliberately human/operational:
1. complete `PILOT_MANUAL_GATE_RECORD.md` for the intended Windows/macOS environment and assistive technology;
2. resolve pilot jurisdiction/operator/participant authorization and guardian/consent requirements in that record;
3. complete `PILOT_DATA_OPERATIONS_TEMPLATE.md` with actual retention/deletion procedure and support contact;
4. complete the age-appropriateness section of `PILOT_MANUAL_GATE_RECORD.md` for the complete pilot content;
5. after those records are committed, designate one final candidate SHA and require both CI and Pilot Build to pass again.

No efficacy, WCAG conformance, legal compliance, code-signing or notarization claim is made.


## 2026-10-02 technical verification update (not a final pilot gate)

- On commit `714e96ed19ce4c0d44d23bdc5646b28d6880ad96`, CI run **36978627964** and Windows/macOS Pilot Build run **36978627923** both completed **SUCCESS**. This verifies the manual-gate preflight implementation on a matching technical SHA, but does **not** supersede the Stage 8 final pilot candidate or imply that manual records are approved.
- Preflight tests CI **36978645777** SUCCESS on `5a7c31c...`; handoff document CI **36978761574** SUCCESS on `3dab042...`; handoff journal CI **36978781165** SUCCESS on `bae638d...`.
- **PR-08 remains BLOCKED:** interactive Windows/macOS accessibility checks are still NOT TESTED.
- **PR-10 pilot operation remains BLOCKED:** actual operator, guardian authorization, support, retention/deletion and content-review sign-offs remain unfilled.
- **PR-14 remains BLOCKED:** final candidate SHA must be nominated only after those manual records are complete and both workflows pass on that exact final SHA.


## 2026-10-02 accessibility fix verification and deferred manual gate

- Windows 11 operator confirmed that the first accessibility announcement implementation (SHA `3175c422ea2a8230ac64ae1a6724098744017d53`) did **not** cause Narrator to speak correct/incorrect feedback. That manual FAIL remains valid for that artifact.
- A second implementation adds an accessibility Alert event alongside Announcement (SHA `80edc27fb81e2257599f260f1bce311a48ea3b75`). CI **36990447333** and Windows/macOS Pilot Build **36990447259** both succeeded on that **same implementation SHA**, including packaged smoke and bundled-content verification. The resulting Windows artifact ID is `11219631559`, macOS artifact ID `11219586996`. Regression-test commit `1a6a63eb...` independently passed CI **36990464483**; its test additions are not part of the implementation artifact.
- Controller deferred further Windows Narrator retest. **PR-08 remains BLOCKED**: successful CI and packaging do not prove actual spoken feedback. Other incomplete manual accessibility checks, including macOS VoiceOver, remain open.
- PR-10 operator decision packet: `STAGE_8_PR10_OPERATOR_DECISION_PACKET.md`. This is preparatory documentation, not evidence of operator identity, guardian authorization, legal review, content sign-off, actual retention/deletion drill or incident rehearsal. **PR-10 operational remains BLOCKED**.
- The older working baseline in the table above is historical, not the current code. **PR-14 remains BLOCKED**; only after all manual gates are resolved can a final SHA receive same-SHA CI and Pilot Build verification and Controller approval.


## 2026-10-05 conservative preflight hardening

- `PILOT_CONTENT_REVIEW_INVENTORY.md` is now a required input to the read-only Stage 8 manual-marker preflight (implementation `86ee03f...`, unit update `a188c18...`). This prevents an unreviewed/missing learner-content record from being silently omitted from the textual completeness check.
- The implementation-only CI run **37263037839** failed because the pre-existing tests still expected three manual records; Ubuntu evidence shows 3 failed / 181 passed, specifically the intended new fourth-record behavior. This was a test expectation lag, not evidence that the gate logic should be reverted.
- Updated tests then passed CI **37263055579** on `a188c18...`; journal follow-up CI **37263071548** also passed. Pilot Build **37263037789** on the implementation SHA succeeded. None of these automated results grants PR-08/PR-10 approval.
- Current manual records still contain unresolved markers by design. PR-08, operational/content PR-10 and final PR-14 remain BLOCKED.


## 2026-10-05 candidate-neutral gate records

- Final `PILOT_MANUAL_GATE_RECORD.md` and `PILOT_DATA_OPERATIONS_TEMPLATE.md` no longer inherit candidate-specific approvals from historical SHA `87eceb5...`; exact candidate SHA/date/network-transfer status must be recorded and verified at final nomination.
- The matrix's older PASS rows remain traceable technical evidence for their cited commits/runs, not a statement that current HEAD or a future final candidate has passed PR-14.
- Final pilot candidate remains **NOT NOMINATED**. PR-08, operational/content PR-10 and PR-14 remain BLOCKED.


## 2026-10-05 runtime UI review fingerprint gate

- Guard commit `ca5ac157ef2489dc8333e3e1cca1d4b8a1337a4a` intentionally failed CI run **37287549563** on Windows, macOS and Ubuntu because the inventory did not yet contain the runtime UI source fingerprint. Ubuntu showed **1 failed / 188 passed**; the sole failing assertion exposed SHA-256 `37be23a5802cf7902aeaa3a1ed2fd7d16bf4c4788a2e971183aa91fe9ad664a8` for `src/repetitor/ui/app.py`.
- `PILOT_CONTENT_REVIEW_INVENTORY.md` now pins that exact value from commit `19936c5848fc9ad820cbce41b801b1ffc87282aa`. This is drift-detection evidence only and does not perform human content/accessibility review.
- **Recovery CI is still UNVERIFIED in this evidence matrix.** Do not nominate an audit candidate until an exact CI run is captured for the fingerprint-pinned revision (or a descendant with unchanged guarded inputs) and is green. A documentation commit or matching hash alone is not a CI PASS.
- Consequently PR-08 remains BLOCKED/deferred, operational/content PR-10 remains BLOCKED, PR-14 remains BLOCKED, and the final candidate remains NOT NOMINATED.


## 2026-10-05 PR-triggered recovery verification

- This documentation-only descendant exists solely to obtain PR-triggered CI evidence after pinning the runtime UI review fingerprint. It does not change `src/repetitor/ui/app.py`, learner-visible YAML, manual gate status, or candidate nomination state.
- A green CI run on this branch is acceptable recovery evidence for the fingerprint guard because the guarded runtime/content inputs are unchanged from the pinned-fingerprint revision. It is **not** PR-14 final-candidate evidence and does not satisfy PR-08 or operational/content PR-10.


## 2026-10-05 runtime UI fingerprint recovery confirmed

- PR-triggered CI run **37300233581** on head `e2e0f49b109dd25b1fb2b594b100a1351ed6688b` completed **SUCCESS** on Windows, macOS and Ubuntu after normalizing the runtime UI source fingerprint across checkout line endings.
- The normalization changed only the test guard/documentation; `src/repetitor/ui/app.py` and learner-visible YAML remained unchanged, so the pinned runtime UI fingerprint `37be23a5802cf7902aeaa3a1ed2fd7d16bf4c4788a2e971183aa91fe9ad664a8` remains the canonical review binding.
- The runtime UI fingerprint **recovery CI gate is PASS**. This does not nominate a final candidate and does not complete manual PR-08 or operational/content PR-10.
- Per the closeout plan, an audit candidate still requires a successful Windows/macOS Pilot Build on the same candidate SHA before manual execution begins.


## 2026-10-05 audit candidate nominated after same-SHA verification

- **Audit candidate:** `e017aaaff1f5d30c188775a552240a829d9685fc`.
- Same-SHA CI run **37301914433** completed **SUCCESS** on Windows, macOS and Ubuntu.
- Same-SHA Pilot Build run **37301914518** completed **SUCCESS** on Windows and macOS, including bundled offline-content verification, packaged executable smoke, exact build-SHA verification, and artifact upload.
- Windows artifact: **11341429699** (`repetitor-windows`, unexpired at verification time). macOS artifact: **11341924295** (`repetitor-macos`, unexpired at verification time).
- This SHA is now the **audit candidate** for manual PR-08/PR-10 execution. It is **not** the PR-14 final candidate. Any relevant code or learner-visible content fix after manual findings invalidates affected observations and requires a replacement audit candidate.
- PR-08 remains BLOCKED/NOT TESTED for outstanding manual accessibility checks; operational/content PR-10 remains BLOCKED. Final candidate remains NOT NOMINATED; PR-14 remains BLOCKED.


## 2026-10-05 audit-candidate manual preflight remains fail-closed

- After binding the prepared audit candidate `e017aaaff1f5d30c188775a552240a829d9685fc` to the manual records, the conservative Stage 8 textual preflight still finds **12 unresolved markers** across the four required records.
- Current unresolved categories include NOT TESTED, [FILL], reviewer/operator placeholders, [BLOCKED], MANUAL TESTING REQUIRED and NOT HUMAN-REVIEWED. This is expected: technical candidate preparation must not clear human/operational gates.
- Therefore the existence of same-SHA CI/Pilot Build evidence does not make the pilot ready. PR-08 and operational/content PR-10 remain BLOCKED; final candidate remains NOT NOMINATED and PR-14 remains BLOCKED.


## 2026-10-05 audit candidate invalidated by learner-visible wording fix

- Assistant pre-review of the bounded learner-visible scope found technical English terms in Russian child-facing feedback (`prerequisite`, `evidence`) and the ambiguous phrase «повышать оценку».
- Commit `b246ee2b793f8f0a9ff7d2947e9e7154515fd357` replaces only those learner-visible UI phrases with plain Russian wording; mathematical/content routing semantics are unchanged.
- Because `src/repetitor/ui/app.py` changed, audit candidate `e017aaaff1f5d30c188775a552240a829d9685fc` is **SUPERSEDED for affected UI/content review**. Its historical CI/Pilot Build evidence remains valid for that SHA but cannot be used as the current manual-review artifact.
- The runtime UI fingerprint guard must fail closed until the new canonical fingerprint is pinned, followed by fresh CI + Windows/macOS Pilot Build before nominating a replacement audit candidate.
- No human content review or accessibility result has been performed or inferred. Final candidate remains NOT NOMINATED; PR-08/PR-10/PR-14 remain BLOCKED.


## 2026-10-05 child-facing wording remediation and fingerprint refresh

- Learner-visible wording fix `b246ee2b793f8f0a9ff7d2947e9e7154515fd357` intentionally invalidated the runtime UI fingerprint binding.
- CI run **37303689834** failed closed on Ubuntu with two explained failures: the missing refreshed UI fingerprint and a unit test still asserting the old learner-facing phrase. The new canonical normalized UI SHA-256 exposed by CI is `47d78e92438dcb327ff9687ee5bb8287b153efb2912026e651460bb0a13edeaa`.
- The inventory fingerprint was refreshed in `12d054f...`; the architecture wording contract was updated in `8a8f56a...` without weakening its anti-repeat/mastery-farming assertion.
- Previous audit candidate `e017aa...` remains historical/superseded for affected UI review. Replacement audit candidate is not nominated until fresh same-SHA CI + Windows/macOS Pilot Build succeeds.


## 2026-10-05 assistant pre-review hardening before replacement audit candidate

- A preparatory assistant review of the bounded learner-visible scope found clarity/accuracy issues before human PR-10 review: technical English (`prerequisite`, `evidence`), ambiguous progress terminology, misleading remediation button text, an over-strong "independent" success message after hint use, and learner-visible diagnostic-route messages not covered by the existing YAML drift fingerprint.
- Learner-facing wording was simplified in commits `b246ee2...`, `5d16e07...`, `e474caf...`; hint-use feedback behavior was corrected in `4cc4d58...` / `1ff92b2...` and regression coverage tightened in `3c9c95d...` / `99da161...`.
- Diagnostic route wording was cleaned in `2337c64...`. The review guard was expanded in `fd8f7bf...` so every learner-visible `message_ru` from `diagnostic_route.yaml` participates in the bounded YAML fingerprint instead of silently escaping review drift detection.
- CI run **37304672691** failed closed as intended after the guard expansion. macOS reported exactly **2 failed / 187 passed**, both fingerprint assertions. CI-derived canonical fingerprints are:
  - learner-visible bounded YAML: `852ccdcaa0c2a243a06335dccaa5cd9a33f93953ab85013c60527f7a370c6258`;
  - runtime UI source: `39ffd7cc0e2a0fae1be9613e3722e17d90f0846bfa6b49fe86faba70ec42b438`.
- Both values were pinned in `PILOT_CONTENT_REVIEW_INVENTORY.md` by `2a98f88...`. Matching fingerprints remain drift evidence only; they are not semantic/age/safety/accessibility approval.
- The prior audit candidate `e017aa...` is historical/superseded for affected UI/content/accessibility checks. Manual audit/data-operation records were changed back to **replacement not yet nominated** and do not contain fabricated observations.
- This assistant pre-review does **not** satisfy human PR-10 content review. PR-08 and PR-10 remain BLOCKED; final candidate is NOT NOMINATED; PR-14 remains BLOCKED.


## 2026-10-05 stabilized replacement audit candidate verified

- **Replacement audit candidate:** `983d04c564879f9ff8b6de110497901279073aeb`.
- Same-SHA CI run **37304924020** completed **SUCCESS** on Windows, macOS and Ubuntu after the expanded learner-visible fingerprint guards and hint-feedback regression fixes.
- Same-SHA Pilot Build run **37304924030** completed **SUCCESS** on Windows and macOS. Both jobs passed bundle build, embedded offline-content verification, packaged executable smoke, exact build-SHA verification and artifact upload.
- Windows artifact **11343327951** (`repetitor-windows`), GitHub Actions digest `sha256:2c40cb9cda7cc7cb6f87c218dffea1f7d7e6046261d54567616a4c767c80a416`.
- macOS artifact **11342674307** (`repetitor-macos`), GitHub Actions digest `sha256:1d5c9490e53c4b75948360f0170e311a6d371d8bf86a53854a0d593399367a28`.
- Manual audit packet and PR-08/PR-10 records were rebound to this replacement candidate without filling any human observation/review/rehearsal result. Previous `e017aa...` artifacts remain historical only.
- This is an **audit candidate**, not the final candidate. PR-08 and operational/content PR-10 remain BLOCKED; final candidate remains NOT NOMINATED; PR-14 remains BLOCKED.


## 2026-10-05 replacement-candidate preflight remains blocked

- After rebinding all four required manual records to replacement audit candidate `983d04c564879f9ff8b6de110497901279073aeb`, the conservative textual preflight still finds **12 unresolved markers**.
- Remaining marker classes are exclusively manual/operational: NOT TESTED, [FILL], reviewer/operator placeholders, [BLOCKED], MANUAL TESTING REQUIRED and NOT HUMAN-REVIEWED.
- This is the intended fail-closed state. Same-SHA CI/Pilot Build and prepared artifacts do not authorize a pilot, do not complete PR-08/PR-10, and do not permit final-candidate nomination.


## 2026-10-06 manual-execution support set complete

For verified audit candidate `983d04c564879f9ff8b6de110497901279073aeb`, the repository now contains three dedicated human-execution worksheets:

- `STAGE_8_ACCESSIBILITY_OBSERVATION_WORKSHEET.md` — Windows/macOS PR-08 keyboard, focus, scaling and Narrator/VoiceOver observations; all human cells NOT TESTED.
- `STAGE_8_HUMAN_CONTENT_REVIEW_WORKSHEET.md` — 135 extracted learner-visible rows bound to the exact candidate/fingerprints; all rows NOT TESTED.
- `STAGE_8_OPERATOR_DATA_DECISION_WORKSHEET.md` — operator/jurisdiction/authorization, retention/deletion/support, backup/restore rehearsal, exact-build external-transfer and incident decisions; all operator-controlled fields remain FILL/NOT TESTED/BLOCKED.

The manual audit packet also requires downloaded-artifact SHA-256 verification before execution and links all three worksheets. These materials reduce omission and wrong-artifact risk only; they do not constitute PR-08 or PR-10 evidence of execution.

Conservative preflight remains blocked on unresolved human/operational markers. Final candidate is still NOT NOMINATED and PR-14 remains BLOCKED.
