# Pilot manual gate record

Prepared audit candidate/artifact set for manual execution: `983d04c564879f9ff8b6de110497901279073aeb`; CI `37304924020`; Pilot Build `37304924030`; Windows artifact `11343327951`; macOS artifact `11342674307`. This is preparation only; `Audit candidate SHA observed` remains unfilled until the checks are actually performed.

Audit candidate SHA observed: [FILL]
Final candidate SHA after any required fixes: [FILL AT FINAL CANDIDATE NOMINATION]
Date: [FILL WHEN FINAL MANUAL GATE IS EXECUTED]
Reviewer/operator: [ROLE OR IDENTIFIER]
Pilot jurisdiction: APPROVED — Russia; setting: самостоятельное домашнее обучение
Intended participant age range: APPROVED — школьные классы 5–11

Use PASS, FAIL, or NOT TESTED. A NOT TESTED or FAIL required row blocks pilot release. Historical observations belong in dated audit/evidence records; this file represents only the final nominated candidate.

## Accessibility

| Check | Windows result | macOS result | Notes / reproduction |
|---|---|---|---|
| Keyboard-only onboarding → diagnostic → answer → progress | NOT TESTED | NOT TESTED | |
| Narrator / VoiceOver announces actionable control names | NOT TESTED | NOT TESTED | |
| Focus order is understandable | NOT TESTED | NOT TESTED | |
| Feedback is discoverable without relying on color alone | NOT TESTED | NOT TESTED | |
| 200% text scaling remains operable/readable | NOT TESTED | NOT TESTED | |
| Visible keyboard focus is sufficient | NOT TESTED | NOT TESTED | |

Record OS version and AT/version used:
- Windows: [FILL]
- macOS: [FILL]

## Complete pilot-content age review

Reviewer reads every learner-visible prompt, hint, explanation and feedback in the pilot content/build.

| Check | Result | Notes |
|---|---|---|
| Language is understandable for intended grade/age | NOT TESTED | |
| No unsafe, humiliating, manipulative or age-inappropriate wording | NOT TESTED | |
| Hints do not falsely present unsupported claims as facts | NOT TESTED | |
| Mathematical authored answers were already formally checked; reviewer found no semantic ambiguity that makes a task unfair | NOT TESTED | |
| No engagement mechanic pressures the child to continue | NOT TESTED | |

## Authorization and privacy operations

| Requirement | Result | Recorded decision |
|---|---|---|
| Operator/controller role identified | PASS | Самостоятельное домашнее обучение; без отдельной организации-оператора |
| Applicable participant/guardian authorization process defined | PASS | B1: явное разрешение родителя/законного представителя до включения ребёнка; согласие фиксируется вне child-facing приложения |
| Support contact defined | PASS | Родитель(и)/законный представитель(и), давшие согласие |
| Local-data retention period defined | PASS | Активный пилот + 30 дней; досрочно удалить по withdrawal/request или при выходе из пилота |
| Withdrawal/deletion procedure defined | PASS | Запрос через родителя/законного представителя; удалить локальные данные и одобренные копии/диагностические материалы участника |
| No unreviewed production network AI provider enabled | NOT TESTED | Policy APPROVED: production child sync/public recovery/external AI-LLM with learner data/external learner-data telemetry are prohibited. Exact-build operational verification still required |

## Release decision

Manual gate: [BLOCKED / PASS]

A PASS here is an operational pilot decision for the stated environment only. It is not a legal-compliance, accessibility-conformance, educational-efficacy, signing or notarization certification.
