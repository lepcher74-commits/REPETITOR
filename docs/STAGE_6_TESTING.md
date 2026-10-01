# Stage 6 — Testing

## Objective
Validate the Stage 5 MVP against AC-01…AC-14, exercise failure and boundary behavior, and correct defects that can distort learning evidence or corrupt local state. Stage 6 does not expand curriculum scope.

## Baseline
Stage 5 closed on commit 4ac63be319943f689f8b681bd8f79f13dbf5e445 with 47/47 tests passing.

## Defects found and corrected
1. **Revealing hint evidence lost in GUI.** The GUI always sent `answer_revealing_hint=False`, which could overstate independence after a worked step. Fixed by deriving the flag from the active Hint.
2. **Remediation mastery farming.** When the remediation chain ended below its exit threshold, the GUI repeated the same final independent item. Fixed: repeated identical evidence is no longer used to cross the threshold; the UI requests an additional content variant.
3. **Non-atomic learning persistence.** Attempt, knowledge state, and review queue were written in separate transactions. Fixed with `save_submission()`, which commits all three in one SQLite transaction.
4. **Review ordering regression risk.** Due reviews must be selected before the current evidence reschedules the skill. Preserved while moving persistence to the atomic transaction.
5. **Verifier edge contract.** Malformed rationals fail closed. The school-input contract accepts a leading negative numerator (for example `-1/2`) but treats `1/-2` as invalid input rather than silently normalizing it.

## Added Stage 6 tests
- long-sequence mastery boundedness (all dimensions remain in 0…1);
- wrong review cannot increase retention;
- revealing hint cannot increase independence;
- prerequisite failure cannot reduce current-skill mastery;
- malformed rational input and unsupported verifier behavior;
- duplicate attempt ID and database reopen behavior;
- atomic rollback for attempt/state/review;
- GUI empty input does not create evidence;
- GUI worked-step path does not create independent evidence.

## AC-01…AC-14 regression status
The Stage 5 acceptance tests remain mandatory in the same CI suite. Stage 6 adds adversarial and integration coverage; it does not replace the Stage 5 acceptance matrix.

## Residual risks
1. [ДОПУЩЕНИЕ] Mastery coefficients, thresholds and review intervals are MVP heuristics and are not empirically calibrated.
2. Remediation now fails safely when unique evidence is exhausted, but the content pool is still too small for robust repeated practice.
3. Current lesson position is not persisted across application restart. Knowledge/progress is persisted; restart resumes the module from its diagnostic entry. This does not violate AC-09 but is a UX limitation.
4. Accessibility has not undergone a formal WCAG/assistive-technology audit.
5. CI currently runs Python 3.12 on Ubuntu with Qt offscreen. Windows/macOS runtime behavior is not yet proven by CI.
6. Content acceptance CA-03 is reference-slice graph validation, not a repository-wide future multi-module DAG proof.
7. Static PII checks cannot prove semantic privacy.

## Exit gate
Stage 6 is complete only when the latest main-branch CI run is green with all Stage 5 and Stage 6 tests included. Transition to Stage 7 requires Controller approval.
