# Accessibility pilot audit record

Date opened: 2026-10-01
Stage: 8 / E8.5
Status: MANUAL TESTING REQUIRED

This record distinguishes automated evidence from checks that require a real interactive desktop session. It is not a WCAG conformance statement.

| Check | Windows | macOS | Evidence/status |
|---|---|---|---|
| Primary controls have accessible names | PASS automated | PASS automated | `tests/integration/test_accessibility.py` |
| Answer inputs accept keyboard focus | PASS automated | PASS automated | `tests/integration/test_accessibility.py` |
| Full keyboard-only flow | NOT TESTED | NOT TESTED | Requires interactive pilot build |
| Narrator/VoiceOver spoken name and state | NOT TESTED | NOT TESTED | Requires target assistive technology |
| Focus order through onboarding/diagnostic/remediation/progress | NOT TESTED | NOT TESTED | Requires interactive observation |
| Feedback discoverable without color/position alone | NOT TESTED | NOT TESTED | Requires interactive AT/visual review |
| 200% text scaling | NOT TESTED | NOT TESTED | Requires interactive target OS |
| Visible focus indication | NOT TESTED | NOT TESTED | Requires interactive target OS |

## Pilot gate

A pilot operator must fill the NOT TESTED cells for the actual intended pilot OS/AT combinations and record:
- OS version;
- assistive technology and version;
- pilot artifact identifier/commit;
- PASS/FAIL;
- reproduction steps for failures;
- resolution or explicit pilot blocker decision.

Automated CI passing does not convert any manual NOT TESTED item to PASS.


## Partial Windows observations received 2026-10-02

See `docs/WINDOWS_MANUAL_AUDIT_2026-10-02.md` for exact build SHA and Controller-reported observations. Main-screen keyboard navigation, visible focus and 200% scaling were reported PASS. **Full keyboard-only learning flow and Narrator remain NOT TESTED**; Windows OS version and exact scaling configuration remain unknown. Do not upgrade the broader matrix rows above to PASS on the strength of these partial observations. macOS manual audit is still NOT TESTED.
