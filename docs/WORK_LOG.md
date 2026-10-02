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
