# Stage 8 accessibility observation worksheet

Status: PREPARED / NOT TESTED.

Audit candidate: `983d04c564879f9ff8b6de110497901279073aeb`
CI: `37304924020`
Pilot Build: `37304924030`
Windows artifact: `11343327951`
macOS artifact: `11342674307`

This worksheet records human PR-08 observations only. Automated accessibility tests are supporting evidence and must not be copied into the human-result cells below.

## Environment record

| Field | Windows | macOS |
|---|---|---|
| Reviewer/operator | [FILL] | [FILL] |
| Date | [FILL] | [FILL] |
| OS version/build | [FILL] | [FILL] |
| Display/text scale | [FILL] | [FILL] |
| Keyboard layout | [FILL] | [FILL] |
| Assistive technology | Narrator | VoiceOver |
| AT version | [FILL] | [FILL] |
| Artifact archive digest verified | NOT TESTED | NOT TESTED |
| Packaged app launched from verified artifact | NOT TESTED | NOT TESTED |

## Keyboard-only flow

Perform the full path without mouse/pointer assistance.

| Step | Windows result | macOS result | Notes / reproduction |
|---|---|---|---|
| Onboarding controls reachable in sensible order | NOT TESTED | NOT TESTED | |
| Start diagnostic using keyboard | NOT TESTED | NOT TESTED | |
| Answer field receives focus | NOT TESTED | NOT TESTED | |
| Submit answer using keyboard | NOT TESTED | NOT TESTED | |
| Request hint using keyboard | NOT TESTED | NOT TESTED | |
| Continue after hint/feedback | NOT TESTED | NOT TESTED | |
| Enter remediation path | NOT TESTED | NOT TESTED | |
| Complete remediation controls by keyboard | NOT TESTED | NOT TESTED | |
| Return to main learning flow | NOT TESTED | NOT TESTED | |
| Open progress screen | NOT TESTED | NOT TESTED | |
| Return from progress screen | NOT TESTED | NOT TESTED | |

## Focus and visual operability

| Check | Windows result | macOS result | Notes / reproduction |
|---|---|---|---|
| Visible focus indicator is consistently perceivable | NOT TESTED | NOT TESTED | |
| Focus order matches visual/logical order | NOT TESTED | NOT TESTED | |
| No keyboard trap | NOT TESTED | NOT TESTED | |
| 200% scaling: onboarding readable/operable | NOT TESTED | NOT TESTED | |
| 200% scaling: diagnostic readable/operable | NOT TESTED | NOT TESTED | |
| 200% scaling: remediation readable/operable | NOT TESTED | NOT TESTED | |
| 200% scaling: progress readable/operable | NOT TESTED | NOT TESTED | |
| Feedback does not rely on color alone | NOT TESTED | NOT TESTED | |

## Screen-reader observations

| Check | Windows Narrator | macOS VoiceOver | Notes / exact spoken behavior |
|---|---|---|---|
| Subject control has understandable name/state | NOT TESTED | NOT TESTED | |
| Grade control has understandable name/state | NOT TESTED | NOT TESTED | |
| Goal control has understandable name/state | NOT TESTED | NOT TESTED | |
| Start button announced meaningfully | NOT TESTED | NOT TESTED | |
| Current problem text discoverable | NOT TESTED | NOT TESTED | |
| Answer input announced with meaningful name | NOT TESTED | NOT TESTED | |
| Submit button announced meaningfully | NOT TESTED | NOT TESTED | |
| Hint button announced meaningfully | NOT TESTED | NOT TESTED | |
| Hint/answer feedback change is discoverable | NOT TESTED | NOT TESTED | |
| Remediation title/explanation/prompt discoverable | NOT TESTED | NOT TESTED | |
| Remediation answer input/button announced meaningfully | NOT TESTED | NOT TESTED | |
| Progress content discoverable | NOT TESTED | NOT TESTED | |
| No critical state is conveyed only visually | NOT TESTED | NOT TESTED | |

## Defect record

For each FAIL, record a sanitized defect reference and:
- exact platform/version;
- exact step;
- expected behavior;
- observed behavior;
- whether the issue blocks the pilot;
- whether affected checks must be repeated after a fix.

Do not include learner personal data.

## Completion

Windows PR-08 result: **NOT TESTED**

macOS PR-08 result: **NOT TESTED**

Overall PR-08 accessibility result: **BLOCKED**

A PASS may be reconciled into the Stage 8 manual gate only after every required row for the intended pilot environment is executed on the exact verified artifact. Any relevant runtime/UI fix invalidates affected observations and requires a replacement audit candidate.
