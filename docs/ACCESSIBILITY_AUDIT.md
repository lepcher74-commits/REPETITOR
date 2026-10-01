# Stage 7 E5 — Accessibility baseline

Automated checks are a baseline, not a WCAG conformance claim.

## Automated
- Primary onboarding controls expose explicit accessible names.
- Main learning answer and remediation answer expose explicit accessible names.
- Learning inputs accept keyboard focus.
- The same automated suite runs on Linux, Windows, and macOS CI.

## Manual assistive-technology audit before release
- Windows: keyboard-only path and Narrator.
- macOS: keyboard-only path and VoiceOver.
- Verify focus order from onboarding through diagnostic, hint, submit, remediation, and progress.
- Verify every actionable control has an understandable spoken name and state.
- Verify feedback changes are discoverable without relying only on visual position or colour.
- Verify 200% text scaling does not hide task text, answer controls, or navigation.
- Verify visible focus indication on every keyboard-reachable control.
- Record OS, assistive technology version, failure, reproduction steps, and resolution.

## Current limitation
No manual screen-reader/WCAG audit has yet been executed. Passing automated Qt tests must not be represented as accessibility certification.
