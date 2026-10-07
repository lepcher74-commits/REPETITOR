# Stage 8 exact-build network observation protocol

Status: PREPARED / NOT EXECUTED.

Audit candidate: `983d04c564879f9ff8b6de110497901279073aeb`
Windows artifact: `11343327951`
macOS artifact: `11342674307`

Purpose: verify the packaged application does not create unexpected outbound connections during the approved offline learning flow. This is an operational observation, not a source-code inference.

## Why observation is required

The packaged Python/PySide runtime contains generic networking-capable libraries (for example Python socket/SSL components and QtNetwork) as transitive runtime dependencies. Their presence does not prove network use, but it means absence of an explicit application HTTP client dependency is not sufficient evidence by itself.

## Safety / privacy

- Use only the verified audit artifact and a synthetic learner profile.
- Do not enter real child personal data.
- Do not enable sync, public recovery, external AI, telemetry or analytics.
- If any unexpected endpoint appears, record hostname/IP/process/port only; do not capture learner payloads.

## Windows observation

1. Verify the Windows archive digest and embedded build SHA per `STAGE_8_MANUAL_AUDIT_PACKET.md`.
2. Launch the packaged REPETITOR application with a synthetic data directory.
3. Record the REPETITOR process ID.
4. In PowerShell, capture baseline connections:
   `Get-NetTCPConnection -OwningProcess <PID> -ErrorAction SilentlyContinue`
5. Perform the normal offline flow: onboarding → diagnostic → answer → hint → remediation → progress.
6. Repeat the PowerShell command during/after the flow.
7. Record whether any connection in `Established`, `SynSent`, `CloseWait` or other active state belongs to the REPETITOR PID.
8. If available, cross-check with Resource Monitor / Network or another local process-level network monitor.

Windows result: NOT TESTED

Evidence / observed endpoints: [FILL]

## macOS observation

1. Verify the macOS archive digest and embedded build SHA.
2. Launch the packaged REPETITOR application with synthetic data.
3. Record the REPETITOR process ID.
4. In Terminal, capture process network sockets:
   `lsof -nP -a -p <PID> -i`
5. Perform the normal offline flow: onboarding → diagnostic → answer → hint → remediation → progress.
6. Repeat the command during/after the flow.
7. If desired, cross-check interactively with:
   `nettop -p <PID>`
8. Record any destination/port associated with the application process.

macOS result: NOT TESTED

Evidence / observed endpoints: [FILL]

## Pass / fail rule

PASS for the approved offline policy requires:
- verified exact audit artifact;
- normal learner flow executed;
- no unexpected outbound application connection observed on the intended platform(s);
- any OS/runtime background traffic clearly distinguished from the REPETITOR process.

FAIL / BLOCKED if:
- REPETITOR opens an unexplained outbound connection;
- the process identity cannot be established;
- a different build is tested;
- observation is incomplete.

A static source/package scan is supporting evidence only and cannot replace this observation.
