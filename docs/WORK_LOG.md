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

### Текущая работа

**Build provenance / E8.1 / PR-01, PR-02, PR-14**

Текущий исправляющий commit: `a84292addfef9715ef7b312f710ef7dbd7e9aade`.

Нужно:
1. Проверить CI для актуального HEAD.
2. Проверить Pilot Build Windows/macOS для a84292a... или более нового HEAD с тем же исправлением.
3. Убедиться, что frozen `--build-info` содержит точный `github.sha`.
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
