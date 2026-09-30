# Architecture Baseline — approved Stage 3

## Stack
Python 3.12+, PySide6/Qt 6, SQLite, pytest, SymPy for supported symbolic checks, replaceable AIProvider.

## Layers
```text
UI (PySide6)
  ↓
Application Services
  ↓
Domain / Learning Engine
  ├─ Diagnostics
  ├─ Knowledge Model
  ├─ Mastery
  ├─ Next-Step Engine
  ├─ Review Scheduler
  └─ Error Analysis
  ↓
Repositories / Verification / Content
  ↓
SQLite + trusted tutor packages

AI Gateway is optional and isolated from authoritative verification.
```

## Key invariants
- Domain does not depend on Qt, SQLite or an AI vendor.
- UI does not own mastery formulas.
- LLM never directly writes knowledge state.
- Attempts/evidence are retained so knowledge state can be recomputed.
- Tutor packages expose content/knowledge graph through a stable contract.
- Core workflows continue without Internet or AI API.

## Planned top-level source layout (Stage 5)
```text
src/repetitor/
  domain/
  application/
  verification/
  ai/
  persistence/
  plugins/
  ui/
content/mathematics/
tests/{unit,integration,content}/
docs/
```
