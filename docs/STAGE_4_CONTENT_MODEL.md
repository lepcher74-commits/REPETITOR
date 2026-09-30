# Stage 4 — Content Model

Status: **IN PROGRESS — not yet approved by Controller**.

## Selected MVP module

**Grade 6 mathematics: Common fractions — from meaning to operations and transfer.**

[ASSUMPTION] The exact boundary is an MVP content decision. The architecture remains capable of hosting the complete grade-6 curriculum.

### Why this module
- prerequisite structure is explicit and testable;
- answers can often be deterministically verified;
- misconceptions are recognizable;
- supports CPA (concrete → pictorial → abstract);
- naturally supports worked examples and fading hints;
- enables transfer into ratios, proportions, percentages and word problems;
- supports a bridge into non-routine/olympiad-style reasoning.

## Content hierarchy

```text
Subject
  └─ Module
      └─ Topic
          └─ Skill
              ├─ prerequisite edges
              ├─ learning objectives
              ├─ explanations
              ├─ worked examples
              ├─ problems
              ├─ misconceptions
              └─ review rules
```

A **Skill** is the smallest pedagogically meaningful node whose evidence can update the learner knowledge state. A Problem may provide evidence for more than one skill, but one skill is marked primary.

## Proposed skill graph v0.1

```text
P0 whole-number arithmetic
├─ P1 multiplication/division facts
├─ P2 factors and multiples
│  ├─ P3 GCD
│  └─ P4 LCM
└─ P5 order/comparison of whole numbers

F1 fraction as part of a whole
├─ F2 numerator / denominator meaning
├─ F3 fraction on number line
└─ F4 fraction as division

F2 + P2 ──> F5 equivalent fractions
F5 + P3 ──> F6 simplify fractions
F3 + F5 ──> F7 compare fractions
F5 + P4 ──> F8 common denominator
F8 ──> F9 add/subtract unlike denominators
F2 ──> F10 add/subtract like denominators
F9 + F10 ──> F11 mixed operation problems
F4 ──> F12 multiply fraction by whole number
F2 ──> F13 multiply fractions
F4 + F13 ──> F14 reciprocal meaning
F14 ──> F15 divide fractions
F9 + F13 + F15 ──> F16 multi-step fraction expressions
F7 + F9 + F13 + F15 ──> F17 fraction word problems
F17 ──> F18 transfer/non-routine fraction problems
F18 ──> F19 olympiad bridge: invariants, reverse reasoning, construction/search
```

P-nodes are diagnostic prerequisites and need not all be taught inside this module; if missing, the Next-Step Engine routes to remediation content.

## Skill schema v0.1

Required fields:

```yaml
id: math.g6.fractions.add_unlike
subject: mathematics
grade_band: middle
module: fractions
title: Addition of fractions with unlike denominators
objectives:
  - find a valid common denominator
  - transform both fractions equivalently
  - add and simplify the result
prerequisites:
  - math.g6.fractions.equivalent
  - math.g6.fractions.common_denominator
mastery_policy: fraction_standard
misconceptions:
  - add_denominators
  - transform_only_one_fraction
  - invalid_equivalent_fraction
tags: [fractions, arithmetic]
```

## Problem schema v0.1

```yaml
id: frac.add.001
primary_skill: math.g6.fractions.add_unlike
secondary_skills:
  - math.g6.fractions.simplify
kind: exact_fraction
difficulty: 2
stage: independent
prompt:
  ru: "Вычисли: 1/2 + 1/3"
answer:
  verifier: rational_equivalence
  expected: "5/6"
solution:
  steps:
    - "Найти общий знаменатель 6."
    - "1/2 = 3/6; 1/3 = 2/6."
    - "3/6 + 2/6 = 5/6."
hints:
  - level: 1
    type: socratic
    text_ru: "Что должно быть одинаковым у дробей, чтобы складывать их части?"
  - level: 2
    type: focus
    text_ru: "Найди общий знаменатель для 2 и 3."
  - level: 3
    type: step
    text_ru: "Приведи обе дроби к знаменателю 6."
misconception_probes:
  "2/5": add_denominators
evidence:
  correct_no_hint:
    mastery: strong_positive
    independence: strong_positive
  correct_after_hint:
    mastery: positive
    independence: weak_positive
```

## Problem dimensions

Difficulty is not a single synonym for bigger numbers. Each item can vary across:
- conceptual depth;
- computation load;
- number complexity;
- number of steps;
- amount of scaffolding;
- representation (objects / diagram / number line / symbols / text);
- context familiarity;
- transfer distance.

The MVP UI may expose a simple 1–5 difficulty, while content internally retains these dimensions.

## Lesson activity stages

```text
RETRIEVAL
→ CHALLENGE/PROBE
→ EXPLANATION when needed
→ WORKED EXAMPLE
→ GUIDED PRACTICE
→ FADING
→ INDEPENDENT PRACTICE
→ TRANSFER
→ FEYNMAN/REFLECTION when AI is available
→ REVIEW SCHEDULING
```

Stages are conditional. A learner who demonstrates the skill can skip explanation and routine practice.

## Hint policy

Hints follow least-help-first:
1. metacognitive/Socratic cue;
2. point attention to relevant representation or fact;
3. name the next subgoal;
4. expose one worked step;
5. show a worked example, then require a new analogous problem.

The system must not award independent evidence to an answer obtained after answer-revealing help.

## Error taxonomy

```text
careless
calculation
misconception
prerequisite_gap
wrong_strategy
incomplete_reasoning
representation_error
unknown
```

Domain misconception IDs are separate, e.g.:
- add_denominators;
- compare_by_denominator_only;
- cancel_across_addition;
- invert_wrong_operand;
- reciprocal_without_division;
- treat_fraction_as_two_unrelated_whole_numbers.

Deterministic pattern matching is attempted before optional AI analysis. If evidence is insufficient, classification remains `unknown`.

## Verification

MVP verifier types:
- exact integer;
- rational equivalence;
- numeric tolerance where explicitly permitted;
- multiple choice;
- ordered/unordered finite set;
- symbolic equivalence for explicitly supported expressions.

Correct final value and pedagogically required form are separate checks. Example: `10/12` may be numerically equivalent to `5/6`, while a task requiring "answer in simplest form" additionally checks normalization.

## Evidence emitted by an attempt

An attempt records facts, not a magical final score:

```text
correct
verifier_result
difficulty dimensions
hints used and levels
attempt number
response duration (coarse; not used alone as ability)
representation
standard vs transfer
detected misconception
prerequisite evidence
```

The Mastery Engine converts this evidence into the multidimensional KnowledgeState. Formula weights remain [ASSUMPTION] until Stage 5 implementation/testing and later calibration.

## Diagnostic design

The diagnostic seeks a useful starting point, not an exam percentage.

For the fractions module it probes:
1. fraction meaning/representation;
2. equivalent fractions;
3. factors/multiples only when implicated;
4. comparison;
5. addition/subtraction;
6. multiplication/division if prior evidence supports moving upward;
7. one transfer item when standard mastery is demonstrated.

Branching principle:
- confident success → move upward or farther transfer;
- recognizable misconception → confirm with a discriminating probe;
- prerequisite-shaped failure → probe prerequisite;
- uncertain/no-answer → reduce complexity without punishment.

Stopping is confidence-based and bounded for child comfort. Exact thresholds/item counts are [ASSUMPTION] and require testing.

## Review model

Review is skill-based, not card-based. A review activity should preferably use a fresh problem and may change representation/context.

Signals that shorten review interval:
- recent error;
- low retention evidence;
- high hint dependence;
- repeated misconception.

Signals that lengthen it:
- repeated independent retrieval across sessions;
- successful delayed retrieval;
- successful transfer.

Exact intervals are [ASSUMPTION].

## Bridge to olympiad-style work

Olympiad progression is not "difficulty level 6".

```text
routine execution
→ concept explanation
→ mixed selection of method
→ transfer to unfamiliar context
→ multi-step reasoning
→ reverse problem
→ constraint/search problem
→ proof/justification
→ heuristic family
→ novel combination
```

For the fractions MVP, F19 is a bridge layer, not a claim that completing the module makes a learner olympiad-level.

## Content validation requirements

Before a content package can ship:
- every skill ID is unique;
- prerequisite graph is acyclic;
- every non-entry skill has reachable prerequisites;
- every problem references existing skills;
- verifier config is valid;
- expected answers pass their own verifier;
- misconception probes do not collide ambiguously without explicit priority;
- every required skill has diagnostic and independent evidence items;
- every taught skill has at least one review-capable item;
- locale text exists for required UI language.

## Stage 4 remaining work

1. Freeze the module boundary and graph.
2. Define machine-readable schemas in detail.
3. Produce a representative end-to-end content slice: diagnostic → lesson → errors/hints → independent → transfer → review.
4. Define acceptance checks for content packages.
5. Controller gate before Stage 5.


## Stage 4 finalization

### Machine-readable contract
The normative proposed contract is documented in `docs/CONTENT_CONTRACT.md`. MVP content is declarative and non-executable. Stable IDs, closed verifier/routing vocabularies, resolvable references and localization requirements are part of the contract.

### Acceptance
`docs/CONTENT_ACCEPTANCE.md` defines CA-01…CA-20 covering structure, graph integrity, verifier self-checks, diagnostic/independent/review coverage, hint progression, misconception caution, prerequisite remediation, transfer separation, Russian localization and non-executable content.

### End-to-end reference slice
`content/mathematics/fractions/add_unlike/` contains the Stage 4 executable-data target for one complete skill:
diagnostic → hypothesis/probe → prerequisite probe → explanation → worked example → guided/fading hints → independent practice → transfer/reverse transfer → review → semantic evidence.

### Stage result
The content model is now specified sufficiently to implement a parser, validator and reference lesson in Stage 5 without inventing the content semantics during coding.

### Assumptions carried forward
- Numeric mastery weights are not scientifically fixed; Stage 5 uses transparent configurable heuristics.
- Exact review intervals are not fixed.
- Diagnostic stopping thresholds/item counts are not fixed.
- The fractions graph is the MVP boundary, not a claim of complete grade-6 coverage.
