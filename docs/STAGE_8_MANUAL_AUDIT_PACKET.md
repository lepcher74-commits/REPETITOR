# Stage 8 manual audit packet — final-candidate execution template

**Prepared:** 2026-10-02; refreshed 2026-10-05. **Status:** final candidate NOT NOMINATED; NO final manual result recorded.

## Artifact to inspect

Do **not** use the historical 2026-10-02 baseline as final-gate evidence. It predates later accessibility and gate-hardening changes and its workflow artifacts may expire.

For manual execution, first pin an exact **audit candidate SHA** and obtain a successful Windows/macOS Pilot Build for that SHA. After all required observations/decisions and any resulting fixes are complete, nominate the separate **final candidate SHA** for PR-14 same-SHA verification. For the audit candidate record:
- audit candidate SHA: `983d04c564879f9ff8b6de110497901279073aeb`;
- Pilot Build run ID: `37304924030`;
- Windows artifact ID: `11343327951`;
- macOS artifact ID: `11342674307`;
- CI run ID on the same audit SHA: `37304924020`.
- Windows artifact archive digest (GitHub Actions SHA-256): `2c40cb9cda7cc7cb6f87c218dffea1f7d7e6046261d54567616a4c767c80a416`.
- macOS artifact archive digest (GitHub Actions SHA-256): `1d5c9490e53c4b75948360f0170e311a6d371d8bf86a53854a0d593399367a28`.

Previous audit candidate `e017aaaff1f5d30c188775a552240a829d9685fc` and its artifacts are historical only. The replacement artifact set above is the one prepared for manual audit.

## Verify the downloaded archive before execution

Do this on the machine where the manual check will run, before extraction. A filename match is not sufficient.

- Windows PowerShell: `Get-FileHash .\repetitor-windows-983d04c.zip -Algorithm SHA256` must equal `2c40cb9cda7cc7cb6f87c218dffea1f7d7e6046261d54567616a4c767c80a416`.
- macOS Terminal: `shasum -a 256 repetitor-macos-983d04c.zip` must equal `1d5c9490e53c4b75948360f0170e311a6d371d8bf86a53854a0d593399367a28`.
- If the digest does not match, STOP. Do not run the archive and do not record accessibility/content observations against this candidate.
- After extraction, run only the packaged application from this archive for PR-08 observations; do not substitute a source-tree launch.

If any code or learner-visible content changes after these observations, repeat affected manual checks on the replacement audit candidate. Do not relabel an older audited SHA as the final candidate.

Historical reference only: baseline `714e96ed19ce4c0d44d23bdc5646b28d6880ad96`, CI run `36978627964`, Pilot Build run `36978627923`. These runs are not valid substitutes for final-candidate verification.

Use `docs/STAGE_8_AUDIT_EXECUTION_CHECKLIST.md` as the operator-facing step sequence for this candidate.
Use `docs/STAGE_8_ACCESSIBILITY_OBSERVATION_WORKSHEET.md` to record PR-08 Windows/macOS observations row by row.
Use `docs/STAGE_8_OPERATOR_DATA_DECISION_WORKSHEET.md` for PR-10 operator/authorization/data-lifecycle decisions and rehearsal evidence.

## Operator observation sequence

1. Extract/run the unsigned artifact on the intended Windows machine. Record OS version, display scale, artifact name/SHA, reviewer, date, keyboard layout, and Narrator version. Record any platform warnings; do not bypass organizational security policy.
2. Complete onboarding → diagnostic → answer → remediation → progress using only keyboard. Observe visible focus and 200% scaling. Repeat with Narrator; record spoken names/states and how feedback is discovered.
3. Repeat the same flow on the intended macOS machine using keyboard and VoiceOver. Record OS/VoiceOver versions and observations.
4. For each row in `docs/PILOT_MANUAL_GATE_RECORD.md` and `docs/ACCESSIBILITY_PILOT_AUDIT_RECORD.md`, enter PASS, FAIL, or NOT TESTED separately for Windows/macOS. For FAIL, capture reproducible steps and issue link; for NOT TESTED, state the limitation. Do not include child personal data.
5. Independently review all learner-visible pilot content for age suitability and mathematical clarity using `docs/STAGE_8_HUMAN_CONTENT_REVIEW_WORKSHEET.md` (135 extracted learner-visible rows bound to the exact audit candidate); record reviewer and observed issues. Fill real operator, guardian authorization, support, incident, retention and deletion decisions in the two operational records. Do not enable child sync/public recovery to perform this audit.

## Return package

Provide completed versions of the three manual records, plus sanitized defect references and exact build run/SHA. I can implement fixes and rerun technical verification. The Controller alone approves the pilot-readiness gate after all evidence is reconciled.
