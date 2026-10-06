# Stage 8 audit artifact preservation and renewal

Status: PREPARED. This procedure preserves the verified audit candidate without silently moving manual review to a newer runtime/content revision.

## Pinned audit candidate

- SHA: `983d04c564879f9ff8b6de110497901279073aeb`
- Preservation branch: `stage8/audit-candidate-983d04c`
- Original CI: `37304924020` — SUCCESS on Windows/macOS/Ubuntu
- Original Pilot Build: `37304924030` — SUCCESS on Windows/macOS
- Original Windows artifact: `11343327951`
- Original macOS artifact: `11342674307`
- Original artifact expiry: 2026-10-19

The preservation branch points to the exact verified audit-candidate commit. It is not a new candidate and does not change the manual-review scope.

## If the original artifacts are still available

Use only the original artifacts and verify their archive SHA-256 values from `STAGE_8_MANUAL_AUDIT_PACKET.md`.

## If the original artifacts have expired before manual execution

Do **not** substitute a build from current `main`.

A replacement downloadable artifact is acceptable for continuing the same audit candidate only if all of the following are true:

1. The build is executed from exact commit `983d04c564879f9ff8b6de110497901279073aeb` (for example from preservation branch `stage8/audit-candidate-983d04c`).
2. The build workflow verifies the embedded/frozen build SHA equals that exact candidate.
3. Windows and macOS Pilot Build jobs both succeed, including bundled offline-content verification and packaged executable smoke.
4. New artifact IDs and archive SHA-256 digests are recorded in the manual audit packet/evidence matrix before human observation begins.
5. No source/content commit is inserted into the preserved candidate branch.

If any source/content change is required, STOP: the old candidate is superseded and the normal replacement-audit-candidate lifecycle applies (fresh fingerprints, CI, Pilot Build and affected manual checks).

## Evidence rule

A re-built artifact from the exact same Git commit is artifact renewal, not candidate nomination. A build from a different commit — even a docs-only current HEAD — must not be represented as the existing audit candidate unless the Stage 8 evidence explicitly establishes why the changed SHA is permissible for the specific gate.

## Manual-review continuity

If human observations were already performed on an original artifact and the artifact later expires, those observations remain evidence for the exact original candidate/artifact recorded at the time. Artifact expiry by itself does not erase completed observations.

If manual execution has not begun, prefer one consistent artifact pair for the full Windows/macOS audit rather than mixing original and renewed builds without recording that distinction.
