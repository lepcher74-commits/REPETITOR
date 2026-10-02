# Parent recovery: future public adapter security contract

Status: specification only. No public endpoint, live mail transport or cloud child-data transfer is approved.

## Trust boundaries

- The public request accepts an email address only. Resolve account ownership exclusively through the authoritative server-side directory. Do not accept parent_id from the requester.
- Determine the client IP at a configured trusted edge; never trust arbitrary forwarded headers. Use a shared authoritative quota store for multi-instance deployments.
- Use one generic HTTP status and response body for registered, unknown, malformed, throttled and expected mail-delivery-failure outcomes. The current transport-independent acknowledgement does not enforce HTTP behavior or timing equivalence.
- Validate and throttle malformed traffic by trusted client IP. Review the shared-IP/NAT fairness impact and the risk of distributed abuse before deployment.
- Do not log raw recovery tokens, passwords, full email addresses or child learning data. Establish approved, non-identifying operational error metrics before enabling delivery.
- Only the intended account may redeem its 15-minute, one-time recovery token. Password update, token consumption and revocation of its existing sessions must remain in one transaction against one authoritative database.
- Do not retry failed mail deliveries with the raw token unless a separately reviewed secure delivery queue is designed. Reissuing a token invalidates previous unconsumed tokens.
- Evaluate response-time distributions for registered, unknown, malformed, throttled and failed-delivery requests under realistic load. Equal response text alone does not prevent enumeration.
- A verified email address is not proof of parental or guardian authority. Legal representative verification, operator identity, lawful notices, hosting and data handling require separate approval.

## Required deployment evidence

Document: independent security review, abuse simulations across shared and distributed IPs, trusted-proxy configuration, error telemetry review, concurrency and expiry tests, sender configuration and secret handling, backup/recovery drills, and approval by the Controller. Record results in Stage 8 evidence matrix. Until then keep all optional network features disabled.
