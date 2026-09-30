# Decision Log

## Approved through Stage 3

### R1–R5 — pedagogical/product foundation
1. The student knowledge model is the center of the system.
2. AI is a pedagogue, not the sole verification mechanism.
3. Learning adaptively selects the next best step.
4. Mastery and olympiad mastery are distinct.
5. Primary metric is change in knowledge, not engagement for its own sake.

### R6–R13 — MVP specification
6. MVP contains one complete grade-6 mathematics module, not the whole curriculum.
7. Diagnostics are adaptive and continue during learning.
8. Knowledge, independence and transfer are assessed separately.
9. Offline core is a complete learning product; API augments it.
10. Tutor/subject is modular.
11. Formal verification outranks LLM output where applicable.
12. Error cause may be `unknown`.
13. MVP acceptance is based on AC-01…AC-14.

### R14–R27 — architecture
14. MVP stack: Python + PySide6/Qt + SQLite.
15. Layered architecture: Domain → Application → Infrastructure → UI.
16. SQLite stores local user data.
17. Evidence/attempt history is stored separately from computed knowledge state.
18. Knowledge graph is a DAG with prerequisites.
19. Knowledge state is multidimensional: mastery, confidence, independence, transfer, retention.
20. Next-Step Engine is the central algorithmic component.
21. Verification Engine is extensible and deterministic where possible.
22. LLM cannot directly modify knowledge state.
23. AI access only through replaceable AIProvider.
24. Send only minimally necessary learner context to AI APIs.
25. MVP tutor plugins are trusted packages only.
26. MVP implements MIDDLE UI; JUNIOR/SENIOR remain architectural modes.
27. Pedagogical core must be testable without GUI or Internet.

## Approved MVP acceptance criteria
AC-01 ≤3 actions to start diagnostic; AC-02 adaptive branching; AC-03 prerequisite fallback; AC-04 strong learners skip redundant basics; AC-05 substantive error feedback/unknown; AC-06 fading hints; AC-07 deterministic verification for supported math; AC-08 scheduled review; AC-09 persisted progress; AC-10 offline learning; AC-11 graceful AI failure; AC-12 local-by-default data; AC-13 modular tutor; AC-14 automated tests for critical logic.
