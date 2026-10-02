# Windows manual audit — partial operator observations

Date received: 2026-10-02
Observed build SHA: `714e96ed19ce4c0d44d23bdc5646b28d6880ad96`
Pilot Build run: `36978627923`
Platform: Windows; OS version **not supplied**
Reviewer identity: not supplied; observations reported by Controller
Status: **PARTIAL — not a PR-08 PASS**

| Observed check | Reported result | Scope limitation |
|---|---|---|
| Application launches without error | PASS reported | Exact Windows version not supplied |
| Can complete initial screens and solve fraction exercises | NOT TESTED | End-to-end learning flow remains unverified |
| Navigate main screens with Tab, Shift+Tab and Enter | PASS reported | Main screens only; not the complete onboarding → diagnostic → answer → remediation → progress flow |
| Visible keyboard focus while navigating | PASS reported | No individual-screen breakdown |
| Narrator announces controls and input fields | NOT TESTED | Assistive technology/version not supplied |
| Elements readable/operable at 200% text scaling | PASS reported | OS display/text scale configuration not recorded |

Free-text feedback: “Все работает штатно” (no specific defects reported in checked scenarios).

## Follow-up required

1. Record Windows version and whether 200% refers to Windows display scale or text-size setting.
2. Complete the actual fractions learning flow through progress, keyboard-only if possible.
3. Run Narrator (Win + Ctrl + Enter) and record spoken control names, states, answer feedback and focus order.
4. Check feedback is understandable without color alone and record any defects/reproduction steps.
5. Independently collect macOS results for any intended macOS pilot cohort. No macOS manual result is inferred from successful automated builds.

These are operator-reported observations, not independently instrumented evidence or a WCAG conformance claim. Keep PR-08 BLOCKED until required manual evidence and intended-platform scope are resolved.
