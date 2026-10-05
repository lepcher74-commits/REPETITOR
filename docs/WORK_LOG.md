# REPETITOR — рабочий журнал выполнения

Статус: ACTIVE  
Назначение: единая точка сверки выполненных действий, доказательств, исправлений, открытых рисков и следующих шагов.

## Правило использования

Перед новым изменением сверяться с этим журналом и текущим состоянием репозитория/CI.

- Не повторять уже выполненную работу без новой причины.
- PASS означает наличие указанного доказательства, а не запрет на повторную проверку.
- Если новая проверка выявляет ошибку в ранее закрытом пункте, статус возвращается в BLOCKED/IN PROGRESS, фиксируется причина и исправление.
- Старый зелёный CI не переносится автоматически на новый HEAD.
- Старый красный CI не считается дефектом текущего HEAD, если причина уже исправлена; он сохраняется как история.
- Ручные gates нельзя объявлять PASS по автоматическим тестам.
- Не расширять Stage 8 за утверждённый scope без решения Controller.

## Stage 8 — Production Readiness & Pilot

### Выполнено и проверено

| Область | Статус | Доказательство / примечание |
|---|---|---|
| E8.1 bundle-safe content paths | PASS | runtime_paths + frozen path tests; Windows/macOS Pilot Build ранее зелёный |
| PR-04 packaged smoke | PASS | frozen executable запускает --smoke-test на Windows/macOS |
| E8.3 backup/restore | PASS, повторно усилено | online SQLite backup, safe restore, corrupt/conflict tests; добавлена проверка обязательной REPETITOR schema |
| E8.4 runtime resilience | PASS | fail-closed startup + privacy-preserving local diagnostics |
| PR-09 privacy inventory | PASS | docs/PRIVACY_CHILD_SAFETY_REVIEW.md |
| PR-11 connected curriculum reachability | PASS на проверенном runtime sequence | declarative sequence + gated advance + integration CI run 36856243285; позже prerequisites исправлены на реальный DAG и regression CI 36857758947 зелёный |
| PR-12 pilot protocol | PASS | docs/PILOT_PROTOCOL.md |
| Declarative prerequisite DAG | PASS | runtime больше не выводит prerequisites из позиции sequence; commit 2a40b0f..., regression commit 5907fb6... |
| Content root scope | PASS | runtime сканирует content/, а не корень repo; commit 2a40b0f... |

### Найденные ошибки и исправления

1. PR-11 первоначально был переоценён: новые skills существовали, но не были learner-reachable. Исправлено declarative learning_sequence и runtime progression.
2. Sequence test ошибочно запрещал legitimate prerequisite_probe в общем pool. Исправлен тест, production content не менялся ради теста.
3. Runtime временно трактовал все предыдущие sequence skills как prerequisites. Исправлено: DAG читается из skill.yaml.
4. Runtime использовал слишком широкий content root. Исправлено на content_dir.parents[2].
5. Backup принимал любую целую SQLite как REPETITOR backup. Исправлено обязательной проверкой REPETITOR tables и regression test.
6. Build provenance через environment variable не переживал freezing. Переведено на build_metadata.py.
7. Первый build_metadata workflow штамповал файл после pip install ., поэтому frozen app мог брать установленную unstamped копию. Исправление: commit a84292a... — stamping до install + PyInstaller --paths src.
8. Unit test build-info ошибочно предполагал installed package metadata в обычном CI. Исправлен test contract commit 3aa5321....
9. После stamping-before-install Pilot Build a84292a... всё ещё падал: PyInstaller не включал repetitor.build_metadata при script entrypoint. Попытка commit 4bf3799... с explicit --hidden-import НЕ закрыла проблему: Pilot Build 36858330679 красный. Provenance остаётся BLOCKED; следующая проверка должна анализировать PyInstaller module resolution, а не повторять прежние варианты.
10. E8.7 review gap: manifest подключал review pool только для add_unlike. Добавлены review.002/.003 для equivalent/simplify/subtract_unlike, подключены 4×3 pools и добавлен contract test commit 8051be7....
11. Provenance module-resolution approach заменён, а не повторён: commits c9f7cca.../e525fcb.../fb69fcb... читают SHA из bundled build-info.txt через application_root(). Generated Python module/hidden-import больше не являются частью решения. Pilot Build 36858892837 на e525fcb... SUCCESS Windows/macOS: frozen smoke + exact github.sha grep прошли.
12. После расширения review manifest старый CA acceptance test искал все review IDs только в add_unlike/problems.yaml и падал StopIteration (1 failed, 104 passed). Это test defect: multi-skill manifest должен разрешаться по full sequence pools. Исправлено commit ba57526... через load_sequence_problems(module, Path("content")).
13. PR-13 подтверждён свежим полным CI 36859274736 SUCCESS после bundled provenance, review pools и acceptance-test fix. Старый regression evidence больше не используется.
14. Packaged smoke ранее проверял только historical add_unlike slice. Исправлено commit 7c7e661...: smoke загружает всю learning_sequence и declared prerequisite DAG; commit cadf1dd... добавляет fail-closed regression при отсутствующем sequence content. Новый CI/Pilot Build ожидается; прежний artifact PASS не переносится автоматически на этот HEAD.
15. Повторная архитектурная проверка выявила production defect: DiagnosticRouter default применялся к sequence problems вне исходного diagnostic route и мог преждевременно отключить ввод. Исправлено commits 8140dca.../986c03a...: router exposes handles(problem_id), а sequence-only tasks остаются под Next-Step Engine. Regression test 09161c4.... Из-за production code change PR-13 и PR-14 требуют нового CI; прежний green regression не переносится.
16. CI/Pilot Build после full-sequence smoke/runtime fix упали до исполнения логики из-за механической patch-ошибки: в __main__.py import содержал literal `\\n`, SyntaxError на всех OS. Исправлено 41a033b.... Чтобы этот класс ошибок ловился раньше, CI теперь выполняет `python -m compileall -q src tests` перед pytest (a351316...).

### Текущая работа

**Build provenance / E8.1 / PR-01, PR-02, PR-14**

Provenance mechanism previously PASS — Pilot Build 36858892837. После runtime fix 986c03a... текущий HEAD требует нового CI/Pilot Build; PR-13 временно IN PROGRESS. PR-08/PR-10 остаются ручными/операционными, PR-14 финальным gate.

Нужно:
1. Дождаться CI contract test review pools на 8051be7... или новее.
2. Для provenance исследовать PyInstaller module resolution по свежему failure; не повторять env/stamp-order/hidden-import гипотезы без новых данных.
3. Добиться frozen `--build-info` с точным `github.sha` на Windows/macOS.
4. Только после этого обновить evidence matrix и технический baseline.

### Ручные / внешние gates, которые нельзя закрыть кодом

- PR-08: keyboard-only полный flow; Narrator/VoiceOver; focus order; feedback not color-only; 200% scaling; visible focus.
- PR-10 operational gate: возрастная/контентная ручная проверка, guardian/consent procedure, support/incident contact.
- Pilot data operations: jurisdiction/operator/age range, retention period, deletion/withdrawal process, support contact.
- PR-14 final candidate требует финальный supported CI/release matrix после всех изменений и ручных release gates.

### Следующий шаг

Проверить Actions после commit a84292a...; при красном результате читать конкретный job log и исправлять первопричину. При зелёном — обновить STAGE_8_EVIDENCE_MATRIX.md и определить, остались ли технические blockers до передачи на ручные gates.

## Decision log

### РЕШЕНИЯ
- Рабочий журнал является постоянной точкой сверки.
- Повторная проверка разрешена и обязательна при новых изменениях, противоречиях, рисках или подозрении на ошибку.
- Не считать старые доказательства автоматически действительными для нового HEAD.

### ОТКРЫТЫЕ ВОПРОСЫ
- Финальный результат freeze-safe provenance после a84292a....
- Ручные accessibility/privacy/pilot-operation gates.

### СЛЕДУЮЩИЙ ШАГ
Проверить CI + Pilot Build для актуальной реализации provenance.


## 2026-10-01 — same-SHA technical candidate verified
- Production/runtime SHA `87eceb5ca1e48bdd52943f65b594495d25af6998`.
- CI run `36862547259`: SUCCESS.
- Pilot Build run `36862547237`: SUCCESS on Windows/macOS, including frozen full-sequence smoke and build provenance.
- PR-13 restored to PASS on current technical candidate.
- PR-14 remains BLOCKED by policy of this stage until manual PR-08 and operational PR-10/data-operations records are completed; after those record commits, final candidate must run CI + Pilot Build again.
- Do not reopen syntax/import/route-ownership work unless new evidence fails.
- Next: manual PR-08 accessibility audit + PR-10 operational/child-safety/data-operations inputs.


## 2026-10-01 — manual gate prefill
- Prefilled only repository-verifiable operational facts for candidate 87eceb5...; no manual PASS invented.
- Data operations now records default `~/.repetitor`, SQLite/log files, tested backup requirement, NO external transfer for this candidate, and minimal incident-preservation procedure.
- Manual gate now records candidate/date and PASS only for the objectively verifiable no-production-network-AI item.
- Remaining human inputs: (1) jurisdiction + operator/controller role + participant age range/guardian authorization; (2) retention/deletion/support/incident owner; (3) actual Windows/macOS accessibility results and complete content age review.


## 2026-10-01 — backup documentation debt closed
- `DATA_BACKUP_RECOVERY.md` now documents both SQLite integrity and required REPETITOR schema validation; healthy unrelated SQLite is explicitly rejected (c40f433...).
- Stage 8 evidence PR-05/PR-06 now points to schema hardening `c82c5d7...` and CI `36856369288` (00d8745...).
- No runtime code changed; technical candidate evidence 87eceb5... remains the last runtime same-SHA CI/Pilot Build proof.
- Remaining blockers are manual/operational only: PR-08 accessibility, PR-10 authorization/content review/data operations, then final PR-14 rerun.


## 2026-10-02 — approved scope change: Russian parent accounts
- Controller approved optional Russian-hosted parent registration/consent/sync design; local offline learning remains mandatory.
- Design and fail-closed gates recorded in `docs/RU_PARENT_ACCOUNT_ARCHITECTURE.md` (794fa36...). Email verification is explicitly not age/parenthood verification.
- This is approval of architecture, not evidence of implemented server, lawful consent or operational pilot authorization.
- Next: implement in small testable slices; operator identity, representative-verification method, provider contract and manual accessibility remain external gates.


## 2026-10-02 — parent consent implementation slice 1
- Added pure fail-closed policy `application/parent_consent.py`: distinct sync/AI purposes, notice version, representative/legal approval, default-off feature flag and withdrawal.
- Added four negative/positive unit tests. This is NOT an identity-verification service, stored consent ledger, server, or production authorization; those remain pending.
- Await CI on test commit a5d0d31...; preserve manual and legal gates.


## 2026-10-02 — parent consent slice 2: local event ledger
- CI 36961891265 SUCCESS on previous parent-consent policy journal SHA 02022ae...; earlier test SHA a5d0d31... also green (36961879830).
- Added `persistence/consent_ledger.py` and three persistence tests: default-off, per-purpose/parent isolation, persisted withdrawal, event history.
- SQLite history is application append-only, NOT tamper-evident and NOT identity or legally valid consent proof. No child data sync connected to ledger; cloud remains OFF.
- Await fresh CI for test commit 38bb821...; no manual gates marked complete.


## 2026-10-02 — parent onboarding slice 3
- Consent-ledger tests CI 36963172217 SUCCESS at 38bb821...; journal SHA 1057c14... CI still in progress when checked.
- Added immutable onboarding state `application/parent_onboarding.py` with explicit email, representative and legal-review stages. Email challenge validation itself is not implemented, and there is deliberately no public setter that claims verified guardianship.
- Added three unit tests for email-only denial, separate legal gate, default-off sync and consent withdrawal (fe34ecc...). No actual server, identity provider or child-data transfer enabled.
- Next gate: fresh CI on this implementation, then review integration of persisted consent and onboarding without treating SQLite events as verified legal consent.


## 2026-10-02 — parent onboarding slice 4: combined local sync gate
- Previous onboarding test SHA fe34ecc... CI 36963292420 SUCCESS; journal SHA 6e16d7a... CI 36963303450 SUCCESS. Pilot Build 36963283937 SUCCESS on earlier d6e50f... only, not current final candidate.
- Added `application/sync_gate.py`: optional sync requires BOTH current persisted purpose-specific grant AND onboarding authorization/active consent/default-off feature flag. Added two tests for persisted revocation, missing grant, other parent/purpose, email-only denial (0fd4dd8...).
- This is a local policy gate only: no production network, identity verification, server enforcement or live child data collection. A future server must reauthorize every request. Await fresh CI.


## 2026-10-02 — mailbox challenge primitive
- Combined sync-gate implementation CI 36963537747 SUCCESS on 8e9bddc...; later test/journal CI and Pilot Build were still running at last check.
- Added single-use random mailbox challenge: SHA-256 token digest, constant-time comparison, 15-minute default expiry, five-attempt limit, no plaintext token persisted in challenge object (ebac34d...). Added three tests (7187942...).
- This is an in-memory primitive only. It does not send mail, persist attempts across restarts, authenticate an account, verify parent age/authority or activate any server; deployment requires server-side persistence, rate limiting and abuse protections.
- Await CI on test SHA 7187942... and final journal HEAD. Keep all cloud features OFF.


## 2026-10-02 — persistent mailbox challenge slice
- Prior mailbox challenge CI 36963652588 SUCCESS and journal CI 36963664549 SUCCESS; Pilot Build 36963642697 SUCCESS on implementation SHA ebac34d... only.
- Added SQLite-backed per-parent challenge store with token digests, 15-minute expiry, five persisted attempts and atomic read/consume using BEGIN IMMEDIATE (ad3b842...). Added restart/replay, expiry/guess-limit and parent isolation tests (61abe63...).
- Issuance still needs API-level throttling; repeated issuance currently replaces the previous token and MUST NOT be exposed directly to unauthenticated requests. No mail delivery, server deployment, identity/guardian proof or live sync enabled. Await CI on new test SHA.


## 2026-10-02 — mailbox issuance cooldown
- Added atomic 60-second per-parent issuance cooldown persisted in SQLite (ae35598...) and restart/old-token survival test (598fb0f...). Repeated issue inside cooldown fails without replacing the valid original token.
- Migration caveat: existing development SQLite databases created before `last_issued_at` require schema migration before deploying this store; no production deployment exists. API-wide IP/device abuse throttling and email delivery still pending. Await fresh CI and Pilot Build; manual gates unchanged.


## 2026-10-02 — legacy mailbox challenge migration
- Cooldown implementation CI 36964216757 SUCCESS and Pilot Build 36964216782 SUCCESS at ae35598...; cooldown test CI 36964225734 SUCCESS; journal CI 36964236072 SUCCESS.
- Implemented startup migration for pre-cooldown SQLite challenge tables: add last_issued_at, conservatively mark legacy rows at migration time to prevent immediate resend (8fed93e...). Added legacy-row preservation test (38537bd...). No live production DB or email service exists.
- Await fresh CI. Remaining public API IP/device throttling and operator/legal/manual gates unchanged.


## 2026-10-02 — server-side mail abuse-limit primitive
- Legacy migration CI 36964994262 SUCCESS and journal CI 36965006479 SUCCESS; Pilot Build on 8fed93e... was still running at last check.
- Added persistent SQLite `MailRequestLimiter` with atomic per-account (3/hour) and server-derived per-IP (10/hour) windows; rejected requests do not consume the other quota (417c72e...). Three tests added (ae6d60f...).
- Limiter is not wired to a public endpoint. Future deployment MUST enforce limiter before issuing codes, validate trusted-proxy IP handling, handle email enumeration, distributed deployment/shared datastore and operational abuse monitoring. No email sent and no child data uploaded. Await CI.


## 2026-10-02 — composed mailbox registration boundary
- Prior limiter test CI 36965110777 SUCCESS and journal CI 36965120694 SUCCESS; implementation Pilot Build 36965100907 SUCCESS at 417c72e... (not latest HEAD).
- Added injectable `MailRegistration` orchestration: persisted account/IP limiter → persisted one-time challenge → injected sender; verification consumes token once (72fc9ae...). Three offline fake-sender tests for success/replay, cooldown/no duplicate delivery, and delivery failure (1a1167f...). Await fresh CI.
- Critical deployment gates: caller must authenticate parent ID, bind recipient to account, derive trusted client IP, avoid account enumeration, provision actual Russian-region mail/hosting and shared distributed rate limits. Fake sender only; no real mail or child-data transfer. Mailbox possession does not prove guardian status. Stage 8 remains open.


## 2026-10-02 — account-bound mailbox adapter
- Previous composed mail registration CI 36965301555 SUCCESS, journal CI 36965314373 SUCCESS; Pilot Build 36965289994 SUCCESS on implementation SHA 72fc9ae... only.
- Added `BoundMailRegistration` with authenticated-actor value and server-owned registered-mailbox directory; request cannot supply an arbitrary recipient, and verification is scoped to the actor (f8e56ef...). Added two offline tests (3da60ee...). Await CI.
- AuthenticatedParent is a trusted-boundary data carrier, NOT an authentication implementation; actual session validation, immutable account-mailbox binding during outstanding challenges, trusted proxy configuration and enumeration-safe HTTP responses remain prerequisites. No guardian proof or cloud transfer enabled.


## 2026-10-02 — authenticated session boundary primitive
- Previous account-bound adapter test CI 36965524418 SUCCESS, journal CI 36965533384 SUCCESS; implementation Pilot Build 36965514350 SUCCESS at f8e56ef... only.
- Added persisted opaque 256-bit parent sessions (SHA-256 digest only), configurable 1–24h expiry and revocation (9bf9093...), three tests (245e14a...). Added `SessionBoundMailRegistration` enforcing valid session for request and verification (690609b...), integration test for invalid/revoked session (cae2d09...). Await fresh CI.
- IMPORTANT: session creation is an internal primitive, not login: credential authentication, session rotation, CSRF/cookie security, account lifecycle and production server deployment remain missing. An authorized server must be the ONLY issuer. Guardian authority not inferred from session or email; cloud transfer remains off. Stage 8 remains open.


## 2026-10-02 — internal password-based parent login
- Previous session-bound mail test CI 36967914706 SUCCESS, journal CI 36967926717 SUCCESS; implementation Pilot Build 36967904356 SUCCESS on 690609b... only.
- Added salted scrypt credential storage and constant-time digest comparison (29549d2...), three persistence tests (2e3508c...). Added internal password-to-revocable-session login (ee43411...) and integration test (30438ac...). Await fresh CI.
- NOT production login: no public endpoint, server-side login rate limiting, breached-password policy, secure recovery, MFA decision, cookie/CSRF/TLS setup or deployment. Registration is not exposed. Guardian verification is separate and cloud transfer OFF. Stage 8 manual gates remain blocked.


## 2026-10-02 — failed parent login throttling
- Previous parent-login integration test CI 36968276309 SUCCESS, journal CI 36968286248 SUCCESS; implementation Pilot Build 36968268277 SUCCESS on ee43411... only.
- Added persisted account (5 failed attempts/15 min) and IP (20 failed attempts/15 min) limiter with atomic check-and-record for failed attempts (63765b6..., d32ddce...), two persistence tests (350c159...). Integrated optional limiter with internal `ParentLogin`, requiring trusted client IP when configured (f2b651f...), integration test (c64be94...). Await fresh CI.
- IMPORTANT: default legacy ParentLogin construction remains unthrottled for backwards compatibility; any future public endpoint MUST inject limiter, use trusted server-derived IP and handle generic errors. Success check vs concurrent failure remains a separate operation; production distributed deployment needs shared transactional datastore and review. No public endpoint or cloud sync. Stage 8 manual gates blocked.


## 2026-10-02 — password recovery token foundation
- Prior limited-login integration CI 36968727168 SUCCESS, journal CI 36968738294 SUCCESS; Pilot Build 36968715323 SUCCESS on f2b651f... only.
- Added persisted 256-bit one-time recovery tokens, SHA-256 digest storage, 15-minute UTC expiry, atomic consume and reissue invalidation (6e10795..., 045b37a...). Three persistence tests added (7594155...). Await CI.
- This is token storage ONLY, not a complete recovery flow: no recovery delivery, account enumeration controls, request throttling, password reset transaction or all-session revocation. A recovery token MUST NOT authorize password changes until those safeguards are implemented and tested. No public endpoint, no child-data transfer; Stage 8 remains open.


## 2026-10-02 — recovery transaction prerequisites
- Verified prior recovery-token tests CI 36969002584 SUCCESS, journal CI 36969012417 SUCCESS; Pilot Build 36968992224 SUCCESS on implementation 045b37a... only.
- Added atomic reset design and failure-case checklist in docs/PASSWORD_RESET_TRANSACTION_PLAN.md (4555ab8...). Added scoped all-session revocation method (c965ebc...) and regression test (afeb0db...). Await fresh CI.
- Full password reset is NOT implemented or enabled: must guarantee one transaction for token consumption, credential update and session invalidation, with rollback tests and deployment-specific datastore review. No public recovery endpoint or child-data transfer. Stage 8 remains open.


## 2026-10-02 — atomic local password reset
- Prior all-session revocation test CI SUCCESS at afeb0db..., journal CI SUCCESS at 26d494..., Pilot Build SUCCESS at c965ebc... (implementation SHA only).
- Added `AtomicParentPasswordReset` (a6fcb3b...) enforcing that recovery, credentials and session stores use ONE local SQLite file. A BEGIN IMMEDIATE transaction validates unused unexpired token, updates scrypt credential, consumes token and revokes all target-parent sessions; invalid token changes nothing. Three tests (563b28a...) cover successful reset, replay/expiry/wrong token and rejecting separate DBs. Await CI.
- NOT deployed or publicly exposed. Mailbox identity/delivery, reset request limits, enumeration-safe responses and production datastore review remain. Stage 8 manual gates remain blocked; cloud transfer off.


## 2026-10-02 — recovery request orchestration
- Previous atomic-reset tests CI SUCCESS at 563b28a..., journal CI SUCCESS at dea6939..., Pilot Build SUCCESS at a6fcb3b... (implementation SHA).
- Added offline `ParentRecoveryRequest` (d1078ac...) using server-owned normalized-email directory, persisted email/IP rate limiter, single-use recovery token and injected sender. Unknown emails consume quota and return the same result as known ones; two tests added (cfbb2a8...). Await fresh CI.
- No public HTTP endpoint, live sender or recovery mail template. Observable mail delivery/timing and explicit rate-limit handling require production enumeration-risk review; directory must be authoritative, IP trusted and logging token-free. No child-data transfer; Stage 8 open.


## 2026-10-02 — integrated offline recovery tests
- Prior recovery request tests CI SUCCESS at cfbb2a8..., journal CI SUCCESS at e341c4c..., Pilot Build SUCCESS at d1078ac... (implementation SHA).
- Added two full-path offline integration tests (a811cbe...) covering server directory -> request limiter -> token delivery stub -> atomic password replacement -> old session revocation, other-parent session isolation, token replay, unknown email and expiry. Await fresh CI; integration tests are not production security review.
- Remaining: generic HTTP response and timing, sender template, failure recovery and concurrency stress, operator/guardian checks, Russian-hosted deployment review, real accessibility manual gates. Stage 8 remains open and cloud sync disabled.


## 2026-10-02 — password reset contention and rollback
- Previous integrated recovery tests CI SUCCESS at a811cbe..., journal CI SUCCESS at e6b1e2b....
- Added concurrency regression (980364f...) requiring exactly one of two simultaneous resets to consume a token. Added injected SQLite trigger failure regression (1d0344d...) requiring password and token rollback when session revocation fails, followed by successful retry. Await fresh CI.
- Still offline only; real sender, HTTP anti-enumeration, deployment security and manual Stage 8 gates remain pending. No cloud transfer.


## 2026-10-02 — consent notice-version hardening
- Previous concurrency and rollback tests CI SUCCESS at 980364f... and 1d0344d..., journal CI SUCCESS at 5cdc43f....
- Fixed optional sync gate: latest persisted consent event must be an active grant for the EXACT supplied notice version; stale grants or a later withdrawal deny transfer (7a4c356..., e6b6ca9...). Regression test added (d20e302...). Await fresh CI.
- This is local fail-closed policy only, not guardian identity or production legal approval. Cloud transfer remains disabled, Stage 8 manual gates open.


## 2026-10-02 — reset fail-closed regression tests
- Added two recovery regressions (c46a7ee...): missing credential must not consume recovery token; another parent's recovery token must not change password or revoke sessions. Await fresh CI.
- Prior consent version CI/Pilot Build were still running at last check; no success claimed. No public reset endpoint or cloud transfer. Stage 8 remains open.


## 2026-10-02 — delivery-failure regression
- Previous reset fail-closed tests CI SUCCESS at c46a7ee..., journal CI SUCCESS at 5359602...; consent sync gate CI and Pilot Build SUCCESS at e6b6ca9... (earlier malformed intermediate e5ea5f6... CI failed, corrected next commit).
- Added failure-injection test (413dc3d...) proving that unavailable email transport raises an error and repeated failed deliveries still consume persisted request quotas. Await CI.
- Recovery delivery failure handling and generic external response remain unimplemented; test documents current internal behavior only. No public endpoint, no live sender, no child-data transfer; Stage 8 remains open.


## 2026-10-02 — generic recovery acknowledgement
- Prior delivery-failure test CI SUCCESS at 413dc3d..., journal CI SUCCESS at bf54c36....
- Added transport-independent `RecoveryAcknowledgement` (533f80c...) returning identical acknowledgement for registered, unknown, throttled and mail-transport-failure outcomes; two regression tests (7bcb6b7...). Await fresh CI.
- This is not an HTTP adapter or complete anti-enumeration: timing, invalid-input behavior, unexpected exception handling, trusted IP, safe telemetry and real sender must be reviewed before deployment. No public endpoint or cloud transfer. Stage 8 remains open.


## 2026-10-02 — malformed recovery request boundary
- Previous generic acknowledgement CI SUCCESS at 7bcb6b7..., journal CI SUCCESS at d74e32a..., Pilot Build SUCCESS at 533f80c... (implementation SHA).
- Updated recovery acknowledgement (9296c71...) to return the same generic response for malformed email, while refusing missing trusted IP or naive time as programmer/deployment errors. Added two tests (b653412...). Await fresh CI.
- Invalid email is not quota charged; future HTTP edge must add abuse control for malformed traffic. Response equality does not prove timing indistinguishability. No live HTTP/mail or child cloud transfer; Stage 8 open.


## 2026-10-02 — malformed recovery traffic limits
- Prior malformed boundary tests CI SUCCESS at b653412..., journal CI SUCCESS at 787fd02..., Pilot Build SUCCESS at 9296c71... (implementation SHA).
- Added optional injected persistent limiter for malformed recovery requests (c054c45...), with generic response preserved even after quota exceeded; regression test (19c7907...). Await fresh CI.
- Existing fixed malformed key yields a global three-request-per-hour quota per limiter database, so a deployment MUST isolate/replace this policy before public traffic; optional injection is not production-ready. Timing and transport security review pending. Stage 8 remains open, no public endpoint or child sync.


## 2026-10-02 — isolated malformed request quotas
- Prior malformed limiter CI SUCCESS at 19c7907..., journal CI SUCCESS at 81870b0..., Pilot Build SUCCESS at c054c45... (implementation SHA).
- Replaced optional global malformed-email quota with separate persistent per-client digest limiter, 10/hour per trusted client IP (31856ec..., 9b9ecbf...). Updated regression and added cross-client isolation test (c65f6cb...). Await fresh CI.
- Shared NAT users may still affect one another; distributed deployment needs shared authoritative datastore and trusted-proxy IP policy. Timing and production transport review outstanding. No public endpoint or child sync; Stage 8 open.


## 2026-10-02 — concurrent malformed quota test
- Added 12-worker barrier concurrency test (45c0507...) for persisted per-client quota: exactly ten requests accepted and two rejected, with another IP unaffected. Await CI.
- Previous isolated-limiter CI and Pilot Build were in progress when checked; do not infer success. No public endpoint or child sync; Stage 8 remains open.


## 2026-10-02 — recovery boundary specification and clock tests
- Isolated limiter CI SUCCESS at c65f6cb... and journal CI SUCCESS at 665b020...; intermediate implementation 9b9ecbf... CI FAILED, corrected by later test update; Pilot Build SUCCESS at 9b9ecbf... (implementation SHA). Concurrent regression CI still in progress when checked.
- Added persisted malformed quota restart/window/backwards-clock regressions (93b37e5...), and future public recovery trust-boundary and required evidence contract (be309b8...). Await fresh CI.
- No live public endpoint, delivery or cloud child-data transfer. Stage 8 remains open; manual/legal/security gates unapproved.


## 2026-10-02 — concurrent recovery acknowledgement integration
- Concurrent limiter CI SUCCESS at 45c0507..., clock tests CI SUCCESS at 93b37e5..., public-boundary document CI SUCCESS at be309b8....
- Added 12-worker malformed burst integration test (9d45148...) exercising the complete acknowledgement and persisted per-client limiter, identical responses after quota and unaffected second IP. Await fresh CI.
- Tests verify response equality, not response-time anonymity; shared-IP fairness, distributed deployment, trusted proxy and security review remain pending. No public recovery endpoint, no child sync; Stage 8 open.


## 2026-10-02 — recovery timing audit plan
- Previous recovery boundary concurrency integration CI queued at 9d45148... and journal CI in progress at 7c499da... at check; preceding journal CI SUCCESS at f4f5944....
- Added controlled timing-security audit protocol (9ae63b2...) requiring synthetic accounts, randomized interleaved conditions, distribution measurements, repeatability, security-review sign-off and deployment-specific evidence. This is a plan, NOT a performed timing audit. Await CI.
- No public endpoint, no live mail sender, no cloud child transfer. Stage 8 manual and legal gates remain open.


## 2026-10-02 — offline timing-audit measurement helpers
- Recovery malformed-burst integration CI SUCCESS at 9d45148..., timing audit protocol CI SUCCESS at 9ae63b2..., journal CI SUCCESS at 8201dc0....
- Added offline seeded interleaved timing collector and nearest-rank p95/p99 summaries (a58ef78...) with deterministic tests (45061bd...). Await fresh CI.
- Measurement helpers are NOT timing-security evidence: no staging run, confidence intervals, independent security review or approved acceptance threshold. Do not log real account identifiers or use live endpoints. Stage 8 remains open; public recovery and child sync disabled.


## 2026-10-02 — exploratory timing uncertainty intervals
- Previous timing collector CI and Pilot Build were in progress at check; no success claim for those runs.
- Added seeded percentile bootstrap median interval helper (a8f8d6e...) and deterministic/invalid-input tests (e45936d...). Await fresh CI.
- Bootstrap intervals assume suitable samples and do not establish account non-enumerability. Deployment-specific timing audit, threat review and approved acceptance criteria remain pending. Stage 8 open; no public recovery or child sync.


## 2026-10-02 — timing scenario difference analysis
- Earlier collector CI SUCCESS at a58ef78... and Pilot Build SUCCESS at a58ef78...; median interval implementation CI SUCCESS at a8f8d6e..., its Pilot Build in progress when checked. Latest interval tests CI pending.
- Added exploratory independent-sample bootstrap interval for differences of scenario medians (35d2f5e...) and synthetic/invalid-input regressions (bca95ec...). Await fresh CI.
- Confidence intervals overlapping zero are NOT proof of timing equivalence. Actual controlled staging measurement and independent review still required. Stage 8 open; public recovery and child sync disabled.


## 2026-10-02 — Stage 8 closeout critical path
- Timing median/difference CI SUCCESS at e45936d... and 35d2f5e... respectively; latest difference tests CI and Pilot Build on 35d2f5e... in progress when checked.
- Added STAGE_8_CLOSEOUT_PLAN.md (becae9f...) to stop optional feature expansion, prioritize manual PR-08/PR-10, and require final same-SHA PR-14 verification and Controller approval. No manual gate marked passed.
- Conditional estimate: 3–5 working days assistant-owned technical closeout; 1–2 weeks full gate only with prompt operator/manual/legal review. Stage 8 remains open; it is the final currently approved numbered stage.


## 2026-10-02 — Stage 8 manual-gate preflight
- Latest timing comparison CI SUCCESS at bca95ec... and journal CI SUCCESS at 3282c02...; Pilot Build SUCCESS at 35d2f5e... (implementation SHA). Latest closeout journal CI was still in progress when checked.
- Added conservative read-only manual-record preflight (714e96e...) and tests (5a7c31c...) for missing files and unresolved markers. It deliberately cannot certify manual observations or Controller approval; explanatory NOT TESTED text can produce conservative false positives requiring human review. Await CI.
- PR-08 manual Windows/macOS AT, PR-10 operator/legal/guardian/data-operations evidence and final same-SHA PR-14 remain blocked. Stage 8 not closed.


## 2026-10-02 — manual pilot evidence handoff
- Previous closeout plan CI SUCCESS at becae9f... and journal CI SUCCESS at b6eb407.... Manual preflight CI and Pilot Build still in progress when checked; no success claim for these.
- Added STAGE_8_OPERATOR_HANDOFF.md (3dab042...) with exact candidate artifact/SHA capture, Windows/macOS assistive-technology observation steps, operator/guardian/data-operations review and final same-SHA verification procedure. No manual test was performed and no legal or Controller approval is implied.
- PR-08/PR-10 operational evidence and PR-14 final same-SHA verification remain outstanding; Stage 8 open.


## 2026-10-02 — evidence reconciliation, no new scope
- Confirmed same-SHA CI SUCCESS run 36978627964 and Pilot Build SUCCESS run 36978627923 on 714e96e...; preflight tests CI SUCCESS 36978645777; operator handoff CI SUCCESS 36978761574 and journal CI SUCCESS 36978781165.
- Updated STAGE_8_EVIDENCE_MATRIX.md (adab5ae...) with exact technical run IDs while preserving blocked PR-08 manual accessibility, operational PR-10 and final PR-14. No new optional features added. Stage 8 remains open pending real observations/operator decisions and final Controller approval.


## 2026-10-02 — executable manual evidence status report
- Evidence matrix and journal CI were in progress at last check. Added runnable read-only `python scripts/stage8_manual_status.py` (65bf25c...) to list unresolved Stage 8 manual record markers with nonzero exit status; it never approves release. Fixture-based tests retained so genuine future human approvals will not cause CI to fail (temporary repository-state assertion 143d7b6... reverted by 0d3fa2f...). Await CI.
- PR-08, operational PR-10 and final PR-14 remain outstanding; Stage 8 open.


## 2026-10-02 — pinned manual audit packet
- Verified manual-status script CI SUCCESS 36979217952 (65bf25c...), follow-up journal CI SUCCESS 36979238508 (e5f3cae...). No claim of final pilot gate.
- Added STAGE_8_MANUAL_AUDIT_PACKET.md (a13dc22...) with exact successful same-SHA technical baseline 714e96e... (CI 36978627964, Windows/macOS Pilot Build 36978627923), artifact expiry caveat, executable OS/AT audit instructions and required return evidence.
- No manual audit, legal review or Controller approval performed; PR-08, operational PR-10 and PR-14 remain BLOCKED.


## 2026-10-02 — verified audit artifact availability
- Audit packet CI SUCCESS 36979446640 (a13dc22...), subsequent journal CI SUCCESS 36979465847 (1973c1a...).
- Inspected actual Pilot Build run 36978627923 artifacts: Windows ID 11214672395 (~51 MB) and macOS ID 11214143484 (~101 MB), both present/unexpired at check. Recorded IDs in STAGE_8_MANUAL_AUDIT_PACKET.md (316e1ec...). These are pinned technical-baseline artifacts, not a final pilot approval.
- No human accessibility observations or operator/legal signoffs received. Stage 8 remains open; PR-08, operational PR-10, final PR-14 blocked.


## 2026-10-02 — Controller Windows manual observations (partial)
- Controller reported Windows launch PASS, main-screen keyboard navigation PASS, visible keyboard focus PASS and 200% scaling PASS for baseline 714e96e.... Full fractions learning flow and Narrator NOT TESTED; Windows version and scaling configuration unspecified. No defects reported in tested scenarios.
- Saved exact scope/limitations in WINDOWS_MANUAL_AUDIT_2026-10-02.md (2970ffc...) and linked ACCESSIBILITY_PILOT_AUDIT_RECORD.md (ae29164...). No claim of full PR-08 pass or macOS manual coverage.
- Operational PR-10, full PR-08 and final PR-14 remain BLOCKED; Stage 8 open.


## 2026-10-02 — Windows 11 progress display confirmation
- Controller confirmed Windows 11 and that progress displays in the tested application. Updated partial Windows audit (3c9a0cf...) without inferring a complete fractions exercise or end-to-end keyboard flow.
- Narrator, exact Windows build and remaining manual checks still outstanding. PR-08/operational PR-10/final PR-14 remain blocked; Stage 8 open.


## 2026-10-02 — Windows Narrator partial result
- Controller reports Narrator speech present on Windows 11; recorded in WINDOWS_MANUAL_AUDIT_2026-10-02.md (a0b8137...). Detailed button/input/answer-feedback spoken coverage and Narrator version not separately confirmed. No inferred full PR-08 PASS; operational PR-10 and final PR-14 blocked.


## 2026-10-02 — confirmed accessibility defect from Windows manual audit
- Controller clarified Narrator does not announce correct/incorrect answer feedback on Windows 11 baseline 714e96e.... Recorded explicit FAIL in WINDOWS_MANUAL_AUDIT_2026-10-02.md (36fbd8d...). General Narrator speech presence does not negate this defect.
- Required: implement an accessible feedback announcement, CI/Pilot Build on new exact SHA, and Controller retest using new Windows artifact. PR-08 BLOCKED; no final pilot release approval.


## 2026-10-02 — implement Narrator feedback announcement fix
- Confirmed manual Windows 11 defect: Narrator speaks interface but not answer correctness feedback (record 36fbd8d...).
- Added Qt accessibility announcement events and accessible descriptions for diagnostic answer feedback, hints and remediation feedback in src/repetitor/ui/app.py (3175c42...). Added integration regression checks in tests/integration/test_accessibility.py (0b6f4c7...).
- CI and Pilot Build triggered; results and real Narrator retest pending. Do not mark defect resolved or PR-08 PASS based solely on code/tests.


## 2026-10-02 — diagnose and correct accessibility regression test setup
- App-only commit 3175c42... CI SUCCESS run 36987973288 and unsigned Pilot Build SUCCESS 36987973267, but subsequent test commit 0b6f4c7... CI FAILURE 36987994403 (183 passed, 1 failed on Ubuntu; same failed assertion across platforms). Failure was test_empty_answer_announces_feedback_without_stealing_focus asserting hasFocus() in an offscreen, never-shown Qt window; event emission and accessibleDescription assertions passed.
- Updated test to show the window, process events, explicitly focus the answer input and assert the precondition before submitting (4994f32...). New CI run 36988653579 pending at time of log. Do not claim retest success yet. App's Narrator announcement remains unverified on real Windows 11.


## 2026-10-02 — fixed build ready for Windows Narrator retest
- Corrected test commit 4994f32... CI SUCCESS run 36988653579; journal commit bc9a571... CI SUCCESS run 36988703470.
- Accessibility implementation commit 3175c42... CI SUCCESS 36987973288 and Windows/macOS Pilot Build SUCCESS 36987973267; both jobs passed bundled-content verification, packaged-executable smoke and upload. Artifacts verified present/unexpired: Windows ID 11218133365, macOS ID 11218073752.
- Windows operator retest requested against artifact from build run 36987973267, exact code SHA 3175c42.... Later commits only changed tests/docs; do not represent this as a final exact-SHA release gate. Narrator behavior on real Windows still awaiting operator evidence.


## 2026-10-02 — second Narrator remediation: Alert fallback
- Controller retest on Windows 11 confirmed the first Announcement-only implementation did not produce spoken answer feedback; manual FAIL remains on baseline 3175c42....
- Qt documentation describes Announcement as an accessibility notification and updateAccessibility as the mechanism for notifying assistive technologies; added a second QAccessible.Alert event as a Windows screen-reader compatibility fallback (80edc27...). Added regression expectation for both events (1a6a63e...).
- New CI/Pilot Build pending. Must retest a new Windows artifact; no resolution claim until Narrator actually speaks the result.


## 2026-10-02 — Alert fallback build verified and handed off
- Implementation SHA 80edc27fb81e2257599f260f1bce311a48ea3b75: CI SUCCESS run 36990447333 and Windows/macOS Pilot Build SUCCESS run 36990447259. Both build jobs passed bundled offline content verification, packaged executable smoke and artifact upload.
- Test SHA 1a6a63eb035e4a05fe09eec37c0eb2fa1a8a28bf CI SUCCESS run 36990464483; previous journal cd87300... CI SUCCESS run 36990495136.
- Verified Windows artifact 11219631559 (~51MB) and macOS artifact 11219586996 (~101MB), both present/unexpired. Provided Windows build to Controller for actual Narrator correct/incorrect feedback retest. No real Windows speech result yet; PR-08 remains BLOCKED, operational PR-10 and final PR-14 remain BLOCKED. Later tests/docs are not included in implementation artifact SHA; final release gate still requires same-SHA verification.


## 2026-10-02 — Controller defers Narrator retest; PR-10 preparation
- Controller explicitly deferred the second Windows Narrator manual retest and requested continuation elsewhere. PR-08 remains BLOCKED/awaiting real manual verification; the prior failed observation remains historical and the Alert fallback is not certified by CI.
- Created STAGE_8_PR10_OPERATOR_DECISION_PACKET.md (104260b...) with actual operator decisions needed, guardian authority distinction, synthetic local deletion and incident tabletop procedures, exact evidence expectations and scope limits. Preparation only; no operator identity, legal authorization, consent, retention period, support or content review fabricated. PR-10 remains BLOCKED; PR-14 remains BLOCKED.


## 2026-10-02 — Stage 8 evidence reconciliation and synthetic PR-10 drill
- Reconciled STAGE_8_EVIDENCE_MATRIX.md (256895a...) with first Narrator manual FAIL, successful same-implementation-SHA CI/Pilot Build for second Alert fallback, deferred manual retest and independent test CI. No manual PR-08 PASS inferred.
- Created PR10_SYNTHETIC_OPERATOR_DRILL.md (3f36c69...) as an executable human worksheet for synthetic backup/restore/withdrawal, lost-device tabletop, operator authorization and content-review evidence. This is NOT EXECUTED; all rows remain NOT TESTED. No real learner data is required or permitted for rehearsal.
- PR-08 BLOCKED/deferred; PR-10 operational BLOCKED pending named operator and human evidence; PR-14 BLOCKED. Stage 8 remains open. Documentation-only CI pending for these changes.


## 2026-10-05 — bounded learner-visible content review inventory
- Confirmed prior documentation CI SUCCESS: evidence matrix 256895a... run 36996117181, synthetic PR-10 drill 3f36c69... run 36996154707, journal 62552b2... run 36996184023.
- Added PILOT_CONTENT_REVIEW_INVENTORY.md (08226f6...) enumerating all current learner-visible problem/remediation content: 42 problem entries total, 10 authored problem-pool hints, 2 remediation explanations, plus runtime UI/feedback text that must be reviewed on the exact final candidate.
- This converts PR-10 content review from an open-ended task into a bounded checklist but does NOT perform or approve the human age/safety review. Count mismatch on a future candidate is a STOP/refresh condition. PR-08 remains deferred/BLOCKED; PR-10 operational remains BLOCKED; PR-14 remains BLOCKED. Stage 8 open.


## 2026-10-05 — content review wired into conservative Stage 8 preflight
- Content inventory commit 08226f6... CI SUCCESS run 37262143815; journal 26eaae9... CI SUCCESS run 37262155861.
- Found a completeness gap: stage8 manual preflight checked accessibility/manual/data-operation records but not the newly required PILOT_CONTENT_REVIEW_INVENTORY.md. Added it to MANUAL_RECORDS (86ee03f...) and updated unit expectations (a188c18...). This can only report unresolved/missing markers; an empty blocker list still cannot grant human or Controller approval.
- Fresh CI pending. Because production Python/test code changed, final PR-14 candidate is not implied; PR-08 deferred/BLOCKED, PR-10 operational/content review BLOCKED, PR-14 BLOCKED. Stage 8 open.


## 2026-10-05 — preflight CI failure triaged and evidence recorded
- Inspected failed implementation-only CI 37263037839: all OS jobs failed because tests still expected 3 manual records after production code added the fourth content-review record; Ubuntu log: 3 failed, 181 passed. This is fully explained by test expectation lag.
- Updated test commit a188c18... CI 37263055579 SUCCESS; journal f024d32... CI 37263071548 SUCCESS. Pilot Build 37263037789 on implementation 86ee03f... SUCCESS. Added this trace to STAGE_8_EVIDENCE_MATRIX.md (6a821e0...).
- No manual evidence status changed. PR-08 BLOCKED/deferred, PR-10 BLOCKED, PR-14 BLOCKED; Stage 8 open.


## 2026-10-05 — CI guard against pilot content-review inventory drift
- Confirmed evidence/journal CI SUCCESS: 6a821e0... run 37265437888 and 4172dbc... run 37265453757.
- Added tests/content/test_pilot_content_review_inventory.py (244c26d...) to compare every current pilot/remediation problem ID and authored problem-pool hint count against PILOT_CONTENT_REVIEW_INVENTORY.md. Future content additions/removals now require an explicit inventory refresh instead of silently escaping the bounded human-review scope.
- This is a completeness guard only; it cannot judge age appropriateness, wording safety, semantic fairness or approve PR-10. Fresh CI pending. PR-08 BLOCKED/deferred; PR-10 BLOCKED; PR-14 BLOCKED; Stage 8 open.


## 2026-10-05 — inventory drift guard caught authored-hint undercount
- CI 37265896881/37265914626 correctly failed the new content inventory guard on all OSes: actual authored problem-pool hints = 13, while PILOT_CONTENT_REVIEW_INVENTORY.md incorrectly stated 10. Ubuntu: 1 failed, 185 passed.
- Root cause was manual arithmetic in the inventory: equivalent 3 + simplify 3 + add_unlike 4 + subtract_unlike 3 = 13. Corrected the documentation to 13 (d16a9a6...) without weakening the guard. Problem-ID equality test had already passed, supporting the 42-problem inventory.
- Fresh CI pending. This correction does not perform the human content review; PR-10 remains BLOCKED. PR-08 deferred/BLOCKED and PR-14 BLOCKED; Stage 8 open.


## 2026-10-05 — PR-10 data-operations template made candidate-safe
- Corrected content inventory d16a9a6... CI 37274069332 SUCCESS; journal 7d58462... CI 37274086005 SUCCESS.
- Audited current runtime/backup code: CLI default data dir is `~/.repetitor` with explicit `--data-dir`; backup uses SQLite online backup API, integrity/schema checks and refuses silent overwrite. Existing DATA_BACKUP_RECOVERY.md matches those implementation contracts.
- Removed stale hard-coded candidate 87eceb5... from PILOT_DATA_OPERATIONS_TEMPLATE.md (68804c5...). Candidate SHA is now filled only at final nomination; external-transfer status must be re-verified on that exact candidate instead of inherited from an old build. Added explicit exact-candidate verification checklist for storage, backup rehearsal, network behavior and operator decisions.
- No operator decisions or manual evidence invented. PR-10 remains BLOCKED pending actual operator completion; PR-08 deferred/BLOCKED; PR-14 BLOCKED; Stage 8 open. Fresh CI pending.


## 2026-10-05 — final manual gate record made candidate-neutral
- Found PILOT_MANUAL_GATE_RECORD.md still pinned to historical candidate 87eceb5... and carrying a candidate-specific automated PASS for no production network AI provider.
- Updated the final manual-gate template (23daff6...) so candidate SHA/date are filled only when the final candidate is actually nominated/executed; network-provider row is reset to NOT TESTED and must be verified on that exact build. Historical observations remain in dated audit/evidence records rather than being inherited into a future release decision.
- This is deliberately more conservative and may keep the preflight blocked longer. No prior historical evidence was deleted. PR-08 BLOCKED/deferred; PR-10 BLOCKED; PR-14 BLOCKED; Stage 8 open. Fresh CI pending.


## 2026-10-05 — evidence matrix made explicit about historical vs final candidate
- Confirmed CI SUCCESS for candidate-safe data-operations docs: 68804c5... run 37274256869, 255e42a... run 37274272443; final manual-gate cleanup: 23daff6... run 37274369953, e04ce44... run 37274399399.
- STAGE_8_EVIDENCE_MATRIX.md still labeled 87eceb5... as a technical working baseline despite later text calling it historical. Updated the header and gate wording (25ecc95...) to state that it is a 2026-10-01 evidence snapshot only and that the final pilot candidate is NOT NOMINATED.
- Existing PASS rows remain historical technical evidence tied to their cited runs; they do not grant PR-14 to current HEAD or a future candidate. PR-08 BLOCKED/deferred; PR-10 BLOCKED; PR-14 BLOCKED; Stage 8 open. Fresh docs CI pending.


## 2026-10-05 — fail-closed preflight for extended placeholders
- Confirmed evidence-matrix CI 37276311182 SUCCESS and journal CI 37276327285 SUCCESS.
- Found manual preflight checked literal [FILL] and [BLOCKED / but candidate-neutral templates use longer placeholders such as [FILL AT FINAL CANDIDATE NOMINATION]. This could miss a still-unfilled final SHA if other markers were cleared.
- Widened marker detection to [FILL, [BLOCKED and NOT HUMAN-REVIEWED (c502314...) and added a focused regression test for extended SHA/block/review markers (a93d4d4...). Textual preflight remains read-only and cannot approve manual evidence.
- CI pending. PR-08 BLOCKED/deferred, PR-10 BLOCKED, PR-14 BLOCKED; Stage 8 open.


## 2026-10-05 — PR-09 privacy baseline separated from final-candidate assertion
- Confirmed preflight hardening CI SUCCESS: c502314... run 37277739271 + Pilot Build 37277739407; regression-test a93d4d4... run 37277795327; journal 715b104... run 37277846396.
- PRIVACY_CHILD_SAFETY_REVIEW.md still said the 'current pilot candidate' had no required AI/cloud flow even though no final candidate is nominated. Updated it (acbc822...) to describe checked items as repository-implementation evidence and added an explicit exact-final-candidate outbound network/data-flow recheck before enrollment.
- No technical PASS was converted into operational approval. PR-09 historical/implementation evidence remains useful, while final candidate verification is explicitly pending. PR-08 BLOCKED/deferred; PR-10 BLOCKED; PR-14 BLOCKED; Stage 8 open. Fresh CI pending.


## 2026-10-05 — manual audit packet no longer points operators at stale artifacts
- Confirmed privacy-baseline CI SUCCESS: acbc822... run 37278043309; journal dee6b20... run 37278060358.
- Found STAGE_8_MANUAL_AUDIT_PACKET.md still presented 2026-10-02 artifacts as the artifact to inspect. Those artifacts predate later accessibility/gate changes and may expire, so they must not become final-gate evidence by convenience.
- Refreshed the packet (7c3ef0e...) into a final-candidate execution template: final audit requires an exact nominated SHA, same-SHA CI, Windows/macOS Pilot Build run and artifact IDs. The 714e96e... runs are retained only as historical reference and explicitly cannot substitute for final verification.
- No manual result was created. PR-08 BLOCKED/deferred; PR-10 BLOCKED; PR-14 BLOCKED; Stage 8 open. Fresh CI pending.


## 2026-10-05 — Stage 8 candidate lifecycle clarified
- Confirmed stale-artifact packet CI SUCCESS: 7c3ef0e... run 37278427014; journal 77a4e44... run 37278451190.
- Found a process ambiguity: CLOSEOUT_PLAN said freeze a proposed SHA before manual checks, while the refreshed audit packet used final-candidate language. Clarified a two-phase lifecycle: audit candidate -> manual PR-08/PR-10 evidence and fixes -> final candidate -> same-SHA PR-14.
- Updated STAGE_8_CLOSEOUT_PLAN.md (963dc5d...) with explicit audit/final candidate definitions and invalidation rule for code/content changes. Aligned STAGE_8_MANUAL_AUDIT_PACKET.md (2361274...) so manual evidence is collected on a pinned audit candidate and affected checks repeat after relevant changes.
- No candidate is currently nominated and no manual PASS is implied. PR-08 BLOCKED/deferred; PR-10 BLOCKED; PR-14 BLOCKED; Stage 8 open. Fresh CI pending.


## 2026-10-05 — manual records aligned to audit-candidate/final-candidate lifecycle
- Verified lifecycle clarification CI by exact SHA: 963dc5d... run 37279391932 SUCCESS; 2361274f... run 37279423004 SUCCESS; da5a017... run 37279461170 SUCCESS. A generic Actions listing had returned stale unrelated runs, so no run IDs were inferred from it.
- Audited Stage 8 manual records for candidate terminology. Several still asked reviewers to fill only a generic/final candidate SHA, which conflicted with the new two-phase process.
- Updated content review (d1dbef2...) to bind semantic review to an audit candidate and require repeat after learner-visible changes; data operations (3fdb08f...) now records audit rehearsal SHA plus final re-verification SHA; manual gate (65a4baf...) records audit observation SHA plus final post-fix SHA; synthetic drill (6b4c2c0...) explicitly uses an audit candidate.
- These are traceability changes only; no human review/rehearsal was performed. PR-08 BLOCKED/deferred; PR-10 BLOCKED; PR-14 BLOCKED; Stage 8 open. Fresh CI pending.


## 2026-10-05 — learner-visible YAML wording bound to review inventory
- Added deterministic learner-visible YAML fingerprint guard in b757308.... CI run 37287057864 failed as intended on Windows/macOS/Ubuntu; Ubuntu showed exactly 1 failed / 187 passed, with only the new missing-fingerprint assertion failing.
- CI-derived canonical fingerprint for the current bounded YAML learner-visible fields is `4d5bcb49392cd8e2119a0c1cc588aebb0fce62282704a33b0022aefef27ac9df`.
- Pinned that fingerprint in PILOT_CONTENT_REVIEW_INVENTORY.md (a980ecc...) and documented its exact scope and limitation: drift detection only, never semantic/age/safety approval. A changed fingerprint requires inventory refresh and affected human review before final nomination.
- Runtime UI wording remains a separately listed human-review scope and is not claimed to be covered by this YAML fingerprint. Fresh CI pending. PR-08 BLOCKED/deferred; PR-10 BLOCKED; PR-14 BLOCKED; Stage 8 open.


## 2026-10-05 — runtime UI drift guard added
- Confirmed YAML fingerprint inventory recovery CI SUCCESS: a980ecc... run 37287278707; journal fe7b832... run 37287302126.
- Added a second conservative review guard (ca5ac15...) that hashes the full `src/repetitor/ui/app.py` source and requires its fingerprint in PILOT_CONTENT_REVIEW_INVENTORY.md. This intentionally invalidates the review record on any runtime UI source change, including non-text changes, rather than risk silently missing learner-visible wording/behavior drift.
- The guard is expected to fail until the current source fingerprint is pinned in the inventory. Matching fingerprint remains drift evidence only, not semantic/accessibility approval. PR-08 BLOCKED/deferred; PR-10 BLOCKED; PR-14 BLOCKED; Stage 8 open.


## 2026-10-05 — runtime UI fingerprint pinned after expected fail-closed CI
- Runtime UI guard commit ca5ac15... produced the intended CI failure (run 37287549563): Ubuntu reported 1 failed / 188 passed, solely because the inventory lacked the current UI fingerprint; macOS showed the same test failure while Windows was still running when inspected.
- CI exposed current full-source `src/repetitor/ui/app.py` SHA-256 `37be23a5802cf7902aeaa3a1ed2fd7d16bf4c4788a2e971183aa91fe9ad664a8`.
- Pinned the UI fingerprint in PILOT_CONTENT_REVIEW_INVENTORY.md (19936c5...) next to the YAML fingerprint. Documented that full-source hashing is intentionally conservative and that matching hashes do not establish accessibility, age appropriateness, safety, clarity or human approval.
- Fresh CI pending. PR-08 BLOCKED/deferred; PR-10 BLOCKED; PR-14 BLOCKED; Stage 8 open.


## 2026-10-05 — runtime UI fingerprint fail-closed cycle fully reconciled
- Rechecked CI run 37287549563 for guard commit ca5ac157ef2489dc8333e3e1cca1d4b8a1337a4a: Windows, macOS and Ubuntu jobs all completed FAILURE at the runtime UI source fingerprint guard. Ubuntu reported exactly 1 failed / 188 passed; the failing assertion exposed SHA-256 `37be23a5802cf7902aeaa3a1ed2fd7d16bf4c4788a2e971183aa91fe9ad664a8` for `src/repetitor/ui/app.py`.
- Confirmed `PILOT_CONTENT_REVIEW_INVENTORY.md` on main contains that exact runtime UI source fingerprint, introduced by 19936c5848fc9ad820cbce41b801b1ffc87282aa, alongside the previously pinned learner-visible YAML fingerprint.
- This proves the intended fail-closed detection and repository-side remediation are traceable. It does NOT prove recovery CI green: no exact recovery workflow run was available through the current commit-run/status interface, so CI PASS is deliberately not inferred.
- Final candidate remains NOT NOMINATED. PR-08 BLOCKED/deferred; PR-10 BLOCKED; PR-14 BLOCKED; Stage 8 remains open. Next technical evidence gate is an exact CI run showing the fingerprint-pinned revision (or a descendant with unchanged guarded inputs) green.


## 2026-10-05 — evidence matrix blocks audit-candidate nomination until recovery CI
- Added explicit runtime UI fingerprint gate to STAGE_8_EVIDENCE_MATRIX.md (2c63b9b...). It records fail-closed CI 37287549563, the derived/pinned UI SHA-256, and marks recovery CI UNVERIFIED rather than inferring PASS from the matching inventory value.
- Audit candidate nomination is therefore blocked until an exact green CI run is captured for the fingerprint-pinned revision or an unchanged-input descendant. This does not alter any manual result.
- PR-08 BLOCKED/deferred; PR-10 BLOCKED; PR-14 BLOCKED; final candidate NOT NOMINATED; Stage 8 open.


## 2026-10-05 — Windows-only false drift in runtime UI fingerprint guard
- PR-triggered recovery CI run 37298623011 on documentation-only descendant 7aa21cd... completed FAILURE overall: Ubuntu and macOS passed, Windows failed exactly one test (188 passed / 1 failed).
- Windows computed runtime UI SHA-256 `972a4e61be88114a67947cd100c04666342981f3320a8bb5133dac2399f31970` while Linux-derived pinned value is `37be23a5802cf7902aeaa3a1ed2fd7d16bf4c4788a2e971183aa91fe9ad664a8`. The checkout log shows the PR merge ref on a Windows runner; the guard used raw `read_bytes()`, making the hash sensitive to checkout line-ending conversion (LF/CRLF).
- Fixed the test guard in 4b9ebd9... to read source as text with universal newline handling and hash canonical UTF-8 bytes. Runtime UI and learner-visible YAML were not changed; the pinned fingerprint remains the canonical LF/text value.
- Fresh PR CI is required before recovery PASS. PR-08 BLOCKED/deferred; PR-10 BLOCKED; PR-14 BLOCKED; audit/final candidate not nominated.


## 2026-10-05 — runtime UI fingerprint recovery CI green
- PR CI run 37300233581 on e2e0f49b109dd25b1fb2b594b100a1351ed6688b completed SUCCESS on Windows, macOS and Ubuntu after the cross-platform newline normalization fix.
- Recovery CI blocker is closed. Runtime/content guarded inputs did not change; pinned UI fingerprint remains 37be23a5802cf7902aeaa3a1ed2fd7d16bf4c4788a2e971183aa91fe9ad664a8.
- Audit candidate is still NOT NOMINATED because the closeout process also requires a same-SHA Windows/macOS Pilot Build before manual PR-08/PR-10 execution. Final candidate remains NOT NOMINATED; PR-08 BLOCKED/deferred; PR-10 BLOCKED; PR-14 BLOCKED; Stage 8 open.


## 2026-10-05 — audit candidate nominated after same-SHA CI + Pilot Build
- Direct Actions collection lookup confirmed push runs for `e017aaaff1f5d30c188775a552240a829d9685fc`: CI **37301914433** SUCCESS on Windows/macOS/Ubuntu and Pilot Build **37301914518** SUCCESS on Windows/macOS.
- Pilot Build jobs passed bundled offline-content verification, packaged executable smoke, exact build-SHA verification and upload. Artifacts: Windows **11341429699** (`repetitor-windows`), macOS **11341924295** (`repetitor-macos`), both unexpired when checked.
- `e017aaaff1f5d30c188775a552240a829d9685fc` is now nominated as the **audit candidate** for manual PR-08/PR-10 execution. It is NOT the final candidate and does not satisfy PR-14.
- STAGE_8_EVIDENCE_MATRIX.md updated in 189d2fe...; STAGE_8_MANUAL_AUDIT_PACKET.md bound to this audit candidate/run/artifact set in 273a574.... No manual observation was inferred or marked PASS.
- Next: execute/record manual accessibility and operational/content review against the pinned audit artifacts. Relevant code/content fixes require a replacement audit candidate. Final candidate remains NOT NOMINATED; PR-08 BLOCKED; PR-10 BLOCKED; PR-14 BLOCKED; Stage 8 open.


## 2026-10-05 — manual records bound to prepared audit candidate without fabricating execution
- Bound the prepared audit candidate `e017aaaff1f5d30c188775a552240a829d9685fc` and same-SHA evidence (CI 37301914433; Pilot Build 37301914518; Windows artifact 11341429699; macOS artifact 11341924295) into the content-review, data-operations, manual-gate and accessibility records.
- Commits: PILOT_CONTENT_REVIEW_INVENTORY.md 6436fbb...; PILOT_DATA_OPERATIONS_TEMPLATE.md 4bd1276...; PILOT_MANUAL_GATE_RECORD.md 50a7567...; ACCESSIBILITY_PILOT_AUDIT_RECORD.md dc28675....
- Fields that assert actual human action (reviewed/rehearsed/observed/results) remain unfilled or NOT TESTED. No manual PASS/FAIL was inferred from CI or artifact existence.
- The next blocking work is real manual PR-08 accessibility execution and PR-10 operator/content/data-operations review on the pinned audit artifacts. Final candidate remains NOT NOMINATED; PR-14 BLOCKED; Stage 8 open.


## 2026-10-05 — audit candidate preflight confirmed fail-closed
- Re-ran the Stage 8 marker logic conceptually against the four current manual records after audit-candidate binding. It still yields 12 unresolved marker categories/records, including NOT TESTED, [FILL], operator/reviewer placeholders, [BLOCKED], MANUAL TESTING REQUIRED and NOT HUMAN-REVIEWED.
- This confirms that the prepared audit candidate and green technical builds did not accidentally clear human gates. Evidence matrix updated in 219b7f6....
- No manual observation was performed. PR-08 BLOCKED; PR-10 BLOCKED; final candidate NOT NOMINATED; PR-14 BLOCKED; Stage 8 open.


## 2026-10-05 — audit-candidate source-level network check
- Reviewed audit candidate e017aaaff1f5d30c188775a552240a829d9685fc dependency manifest and common outbound-network API references. Runtime dependencies remain PySide6/PyYAML/sympy only; repository searches for common Python/Qt HTTP/socket/mail client APIs returned no matches, but GitHub reported incomplete_results=true.
- Recorded this as supporting negative source evidence in PRIVACY_CHILD_SAFETY_REVIEW.md (ff85525...). It is explicitly NOT an operational runtime/network PASS and does not clear the exact-build verification row.
- Manual preflight remains blocked; PR-08 BLOCKED, PR-10 BLOCKED, final candidate NOT NOMINATED, PR-14 BLOCKED; Stage 8 open.


## 2026-10-05 — assistant pre-review found child-facing wording defect
- Preparatory (non-human-gate) semantic review found learner-visible technical English in runtime feedback: prerequisite/evidence, plus ambiguous «повышать оценку». These are clarity defects for the intended Russian grade-6 audience.
- Fixed wording only in b246ee2b793f8f0a9ff7d2947e9e7154515fd357: «базовый навык», «одна проверка», «уровень освоения», «подтверждён несколькими проверками». No mathematical verifier/routing logic changed.
- This learner-visible source change supersedes audit candidate e017aa... for affected manual UI/content review. Historical technical evidence is retained, but a replacement audit candidate requires refreshed UI fingerprint + CI + Pilot Build.
- Evidence matrix invalidation recorded in 64c90dd.... Manual PR-08/PR-10 results remain unperformed; final candidate NOT NOMINATED; PR-14 BLOCKED; Stage 8 open.


## 2026-10-05 — child-facing wording fix fingerprint cycle
- CI 37303689834 on b246ee2... failed closed as intended after learner-visible UI wording changed. Ubuntu: 2 failed / 187 passed. Failures were (1) runtime UI fingerprint mismatch exposing new canonical SHA-256 `47d78e92438dcb327ff9687ee5bb8287b153efb2912026e651460bb0a13edeaa`; (2) stale unit wording assertion still expecting «повышать оценку».
- Refreshed PILOT_CONTENT_REVIEW_INVENTORY.md fingerprint in 12d054f... and updated the architecture wording contract to «повышать уровень освоения» in 8a8f56a.... No routing/verifier/mastery logic changed.
- Previous audit candidate e017aa... stays superseded for affected UI/content review. Replacement audit candidate requires fresh same-SHA CI + Pilot Build; no manual result is carried forward.


## 2026-10-05 — pre-review hardening stabilized before replacement audit candidate
- Assistant-only preparatory review (not a human PR-10 result) found and corrected learner-facing clarity/accuracy debt across runtime feedback/progress/remediation and diagnostic route messages. Key commits: b246ee2..., 5d16e07..., e474caf..., 4cc4d58..., 1ff92b2..., route wording 2337c64..., regression precision 99da161....
- Found a review-coverage defect: diagnostic_route.yaml message_ru values are learner-visible but were outside the bounded YAML fingerprint. Expanded the guard in fd8f7bf... to include all default/rule route messages.
- CI 37304672691 then failed closed exactly on two expected fingerprint assertions (macOS 2 failed / 187 passed), exposing YAML SHA-256 `852ccdcaa0c2a243a06335dccaa5cd9a33f93953ab85013c60527f7a370c6258` and UI SHA-256 `39ffd7cc0e2a0fae1be9613e3722e17d90f0846bfa6b49fe86faba70ec42b438`.
- Pinned both fingerprints in 2a98f88.... Retired stale e017aa... artifact references from the manual audit packet/records (95fed83..., f6029b4..., f44db71..., 27b5cef...). No human reviewed/rehearsed/observed field was filled.
- Replacement audit candidate is still NOT NOMINATED until a fresh exact same-SHA CI + Windows/macOS Pilot Build passes after this stabilized documentation state. Final candidate remains NOT NOMINATED; PR-08/PR-10/PR-14 BLOCKED; Stage 8 open.


## 2026-10-05 — stabilized replacement audit candidate ready for manual execution
- Verification SHA `983d04c564879f9ff8b6de110497901279073aeb` passed same-SHA CI **37304924020** on Windows/macOS/Ubuntu and Pilot Build **37304924030** on Windows/macOS.
- Pilot Build passed bundled-content verification, packaged executable smoke, exact build-SHA check and artifact upload on both platforms.
- Prepared artifacts: Windows **11343327951**, digest `2c40cb9cda7cc7cb6f87c218dffea1f7d7e6046261d54567616a4c767c80a416`; macOS **11342674307**, digest `1d5c9490e53c4b75948360f0170e311a6d371d8bf86a53854a0d593399367a28`.
- Replacement audit candidate is now `983d04c...`. Manual audit/content/data-operation templates were rebound to it (091ab8a..., 7a66356..., a37ed9f..., 83e3e9a..., b72c5d7...); artifact digests added in 5c288f6.... No human result was filled or inferred.
- Next blocker is actual manual PR-08 accessibility execution plus PR-10 human content/operator/data-operations review on these artifacts. Final candidate remains NOT NOMINATED; PR-14 BLOCKED; Stage 8 open.
