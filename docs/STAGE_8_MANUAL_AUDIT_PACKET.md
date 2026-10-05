# Stage 8 manual audit packet — final-candidate execution template

**Prepared:** 2026-10-02; refreshed 2026-10-05. **Status:** final candidate NOT NOMINATED; NO final manual result recorded.

## Artifact to inspect

Do **not** use the historical 2026-10-02 baseline as final-gate evidence. It predates later accessibility and gate-hardening changes and its workflow artifacts may expire.

For final execution, first nominate an exact candidate SHA after the prerequisite manual/operational decisions are ready, then obtain a successful Windows/macOS Pilot Build for that exact SHA. Record:
- candidate SHA: [FILL];
- Pilot Build run ID: [FILL];
- Windows artifact ID: [FILL];
- macOS artifact ID: [FILL];
- CI run ID on the same SHA: [FILL].

Historical reference only: baseline `714e96ed19ce4c0d44d23bdc5646b28d6880ad96`, CI run `36978627964`, Pilot Build run `36978627923`. These runs are not valid substitutes for final-candidate verification.

## Operator observation sequence

1. Extract/run the unsigned artifact on the intended Windows machine. Record OS version, display scale, artifact name/SHA, reviewer, date, keyboard layout, and Narrator version. Record any platform warnings; do not bypass organizational security policy.
2. Complete onboarding → diagnostic → answer → remediation → progress using only keyboard. Observe visible focus and 200% scaling. Repeat with Narrator; record spoken names/states and how feedback is discovered.
3. Repeat the same flow on the intended macOS machine using keyboard and VoiceOver. Record OS/VoiceOver versions and observations.
4. For each row in `docs/PILOT_MANUAL_GATE_RECORD.md` and `docs/ACCESSIBILITY_PILOT_AUDIT_RECORD.md`, enter PASS, FAIL, or NOT TESTED separately for Windows/macOS. For FAIL, capture reproducible steps and issue link; for NOT TESTED, state the limitation. Do not include child personal data.
5. Independently review all learner-visible pilot content for age suitability and mathematical clarity; record reviewer and observed issues. Fill real operator, guardian authorization, support, incident, retention and deletion decisions in the two operational records. Do not enable child sync/public recovery to perform this audit.

## Return package

Provide completed versions of the three manual records, plus sanitized defect references and exact build run/SHA. I can implement fixes and rerun technical verification. The Controller alone approves the pilot-readiness gate after all evidence is reconciled.
