from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from repetitor.application.mastery import apply_evidence
from repetitor.application.next_step import NextActivity, select_next_activity
from repetitor.application.review import schedule_review
from repetitor.domain import AttemptEvidence, KnowledgeState, Problem, VerificationResult
from repetitor.persistence import SQLiteLearningRepository
from repetitor.verification import verify_answer


@dataclass(frozen=True, slots=True)
class SubmissionOutcome:
    verification: VerificationResult
    misconception_hypothesis: str | None
    knowledge_state: KnowledgeState
    next_activity: NextActivity


class LearningSessionService:
    def __init__(
        self,
        repository: SQLiteLearningRepository,
        prerequisites: dict[str, tuple[str, ...]],
    ) -> None:
        self.repository = repository
        self.prerequisites = prerequisites

    def submit(
        self,
        *,
        student_id: str,
        problem: Problem,
        answer: str,
        occurred_at: datetime,
        hint_level: int | None = None,
        answer_revealing_hint: bool = False,
    ) -> SubmissionOutcome:
        verification = verify_answer(problem.verifier, answer)

        # A recognized response creates a hypothesis only. Confirmation belongs
        # to a separate probe/evidence process.
        misconception = None
        if not verification.correct:
            misconception = problem.misconception_probes.get(str(answer).strip())

        prerequisite_failure = problem.purpose == "prerequisite_probe" and not verification.correct
        evidence = AttemptEvidence(
            id=str(uuid4()),
            student_id=student_id,
            problem_id=problem.id,
            skill_id=problem.primary_skill,
            occurred_at=occurred_at,
            correct=verification.correct,
            purpose=problem.purpose,
            hint_level=hint_level,
            answer_revealing_hint=answer_revealing_hint,
            transfer=problem.transfer,
            misconception=misconception,
            prerequisite_failure=prerequisite_failure,
        )
        self.repository.add_attempt(evidence)

        previous = self.repository.get_state(student_id, problem.primary_skill)
        if previous is None:
            previous = KnowledgeState(student_id=student_id, skill_id=problem.primary_skill)

        updated = apply_evidence(previous, evidence)
        self.repository.save_state(updated)
        due = self.repository.due_reviews(student_id, occurred_at)

        states: dict[str, KnowledgeState] = {problem.primary_skill: updated}
        for prerequisite_id in self.prerequisites.get(problem.primary_skill, ()):
            state = self.repository.get_state(student_id, prerequisite_id)
            if state is not None:
                states[prerequisite_id] = state

        next_activity = select_next_activity(
            current_skill_id=problem.primary_skill,
            states=states,
            prerequisites=self.prerequisites,
            due_reviews=due,
            now=occurred_at,
        )
        self.repository.save_review(schedule_review(updated, evidence))
        return SubmissionOutcome(
            verification=verification,
            misconception_hypothesis=misconception,
            knowledge_state=updated,
            next_activity=next_activity,
        )
