from __future__ import annotations

from dataclasses import replace

from repetitor.domain import AttemptEvidence, KnowledgeState


# [ASSUMPTION] Transparent MVP heuristic. Values are deliberately centralized
# so they can be tested/calibrated without changing authored content.
MASTERY_CORRECT = 0.16
MASTERY_WRONG = -0.10
INDEPENDENCE_CORRECT = 0.14
INDEPENDENCE_HINTED = -0.03
TRANSFER_CORRECT = 0.16
CONFIDENCE_EVIDENCE = 0.08
RETENTION_REVIEW_CORRECT = 0.14


def apply_evidence(state: KnowledgeState, evidence: AttemptEvidence) -> KnowledgeState:
    mastery = state.mastery
    confidence = state.confidence
    independence = state.independence
    transfer = state.transfer
    retention = state.retention

    # A prerequisite failure should route downward, not punish the current skill.
    if not evidence.prerequisite_failure:
        mastery += MASTERY_CORRECT if evidence.correct else MASTERY_WRONG

    confidence += CONFIDENCE_EVIDENCE

    if evidence.correct and evidence.hint_level is None:
        independence += INDEPENDENCE_CORRECT
    elif evidence.answer_revealing_hint:
        independence += INDEPENDENCE_HINTED

    if evidence.transfer and evidence.correct:
        transfer += TRANSFER_CORRECT

    if evidence.purpose == "review":
        retention += RETENTION_REVIEW_CORRECT if evidence.correct else -RETENTION_REVIEW_CORRECT

    return replace(
        state,
        mastery=mastery,
        confidence=confidence,
        independence=independence,
        transfer=transfer,
        retention=retention,
        evidence_count=state.evidence_count + 1,
        updated_at=evidence.occurred_at,
    ).bounded()
