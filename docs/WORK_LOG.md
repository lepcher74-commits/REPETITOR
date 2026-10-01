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

### Текущая работа

**Build provenance / E8.1 / PR-01, PR-02, PR-14**

Provenance: PASS — Pilot Build 36858892837. PR-13 regressions: PASS — CI 36859274736. Автоматические технические критерии PR-01–07, PR-09, PR-11–13 имеют evidence; PR-08/PR-10 остаются ручными/операционными, PR-14 финальным gate.

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
