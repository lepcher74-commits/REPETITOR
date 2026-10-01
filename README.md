# REPETITOR

Offline-first desktop platform of AI tutors for school students (grades 1–11).

## Current status

Project process: Constitution v1.0. Stages 0–5 approved. Stage 6 (testing) is complete: final CI passed 67 tests. Stage 7 (expansion) is technically complete pending the Controller gate: E1–E6 are implemented, and the final three-platform CI baseline passes 82 tests on Windows, Ubuntu, and macOS.

### MVP
- Audience: grades 5–8; first content: mathematics, grade 6.
- Goal modes: catch up / deepen / olympiad path.
- Hybrid AI: core learning works offline; AI is optional through a provider adapter.
- Architecture target: Python + PySide6/Qt + SQLite.
- Core principle: student knowledge model and Next-Step Engine drive learning; LLM is not the source of truth.

See `docs/` for approved decisions and specifications.
