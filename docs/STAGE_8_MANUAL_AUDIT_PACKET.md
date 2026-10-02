# Stage 8 manual audit packet — reproducible technical baseline

**Prepared:** 2026-10-02. **Status:** ready for operator execution; NO manual result recorded.

## Artifact to inspect

- Baseline commit: `714e96ed19ce4c0d44d23bdc5646b28d6880ad96`.
- CI success: https://github.com/lepcher74-commits/REPETITOR/actions/runs/36978627964
- Windows/macOS Pilot Build success: https://github.com/lepcher74-commits/REPETITOR/actions/runs/36978627923
- Download both unsigned artifacts from that build run's Artifacts section. Artifacts expire after 14 days; if expired, rerun Pilot Build on an explicit pinned candidate ref and record the new run/SHA. Do not substitute a build of unrecorded provenance.
- This is a **technical baseline**, not a final candidate; subsequent changes require a new exact-SHA CI/Pilot Build pair before final approval.

## Operator observation sequence

1. Extract/run the unsigned artifact on the intended Windows machine. Record OS version, display scale, artifact name/SHA, reviewer, date, keyboard layout, and Narrator version. Record any platform warnings; do not bypass organizational security policy.
2. Complete onboarding → diagnostic → answer → remediation → progress using only keyboard. Observe visible focus and 200% scaling. Repeat with Narrator; record spoken names/states and how feedback is discovered.
3. Repeat the same flow on the intended macOS machine using keyboard and VoiceOver. Record OS/VoiceOver versions and observations.
4. For each row in `docs/PILOT_MANUAL_GATE_RECORD.md` and `docs/ACCESSIBILITY_PILOT_AUDIT_RECORD.md`, enter PASS, FAIL, or NOT TESTED separately for Windows/macOS. For FAIL, capture reproducible steps and issue link; for NOT TESTED, state the limitation. Do not include child personal data.
5. Independently review all learner-visible pilot content for age suitability and mathematical clarity; record reviewer and observed issues. Fill real operator, guardian authorization, support, incident, retention and deletion decisions in the two operational records. Do not enable child sync/public recovery to perform this audit.

## Return package

Provide completed versions of the three manual records, plus sanitized defect references and exact build run/SHA. I can implement fixes and rerun technical verification. The Controller alone approves the pilot-readiness gate after all evidence is reconciled.
