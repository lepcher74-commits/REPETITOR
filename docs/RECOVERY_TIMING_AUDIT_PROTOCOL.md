# Recovery response timing audit protocol

Status: manual security test plan, not completed evidence. No public HTTP endpoint exists.

## Goal

Measure whether an unauthenticated requester can statistically distinguish registered,
unknown, malformed, throttled and mail-delivery-failure requests by elapsed response time.
Identical response text alone is insufficient.

## Controlled environment

Use an isolated staging deployment with synthetic adult accounts, a stub delivery
provider and no child learning data. Record exact commit SHA, OS, deployment
topology, proxy configuration, storage backend, clock source and network conditions.
Run only against infrastructure owned or explicitly authorized by the operator.

## Method

1. Pre-register synthetic accounts and establish equal-length test addresses.
   Use distinct, preallocated client identities for throttled and unthrottled groups.
2. Warm up the service. Randomize interleaved requests across all five conditions
   to reduce drift. Keep payload sizes, transport settings and client location fixed.
3. Record at least 200 samples per condition across several independent sessions,
   including both cold and warm paths. Separate delivery-provider latency from
   the public response if delivery is asynchronous.
4. Record response status, body, duration distribution, p50/p95/p99 and confidence
   intervals; inspect overlapping distributions and repeatable classifiers rather
   than declaring safety from average equality.
5. Repeat under moderate concurrent load and after quota-window rollover. Evaluate
   potential mailbox existence signals through provider behavior, retries and errors.
6. Investigate measurable differences and rerun the full matrix after remediation.
   Never add fixed sleep as a substitute for architecture/security review.

## Gate and evidence

Security reviewer and Controller must approve a deployment-specific acceptance
criterion before the run. Store anonymized sample data, reproducible harness,
findings, mitigations and sign-off in the Stage 8 evidence matrix. Do not enable
public recovery or child-data transfer on the basis of unit-test success.
