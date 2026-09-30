# REPETITOR Content Contract v0.1

Status: Stage 4 proposal; becomes binding after Controller approval.

## Design rule

Content is declarative data. The application core owns algorithms; content packages provide skills, problems, pedagogical metadata, explanations, misconception patterns and routing hints.

Content MUST NOT execute arbitrary code in the MVP.

## Identifiers

IDs are globally unique strings using dotted namespaces.

Examples:
- `math.g6.fractions.add_unlike`
- `frac.add.independent.001`

IDs are immutable after released content has learner history attached to them. Renaming requires an explicit migration/alias strategy.

## Skill

Required:
- id
- subject
- grade_band
- module
- title_ru
- objectives (>=1)
- prerequisites (list; may be empty only for declared entry skills)
- mastery_policy
- misconceptions (list)

Optional:
- secondary_prerequisites
- tags
- representations
- notes

## Problem

Required:
- id
- primary_skill
- purpose
- prompt_ru
- verifier

Optional:
- secondary_skills
- representation
- transfer
- choices
- hints
- misconception_probes
- explanation
- metadata

Allowed MVP purposes:
- diagnostic
- misconception_probe
- prerequisite_probe
- guided
- independent
- transfer
- reverse_transfer
- review

## Verifier contract

Every verifier has `type` and `expected`.

MVP types:
- exact_integer
- rational_equivalence
- multiple_choice
- numeric_tolerance
- finite_set
- symbolic_equivalence (only for explicitly supported expression subset)

Optional constraints are verifier-specific, e.g. `require_simplified`.

The content validator MUST run each expected answer through its own verifier during package validation.

## Hints

Each hint requires:
- level: positive integer
- kind
- text_ru

Levels must be strictly increasing and unique per problem.

MVP kinds:
- socratic
- focus
- representation
- subgoal
- step
- worked_step
- worked_example

A hint that reveals an answer or decisive worked step must be marked by a kind that the Learning Engine can treat as answer-revealing.

## Misconceptions

A misconception definition requires:
- id
- description_ru
- response_ru

Optional:
- example
- confirmation
- remediation_skill

A problem may map recognizable responses to a misconception hypothesis. This mapping creates a hypothesis/evidence event; it MUST NOT directly mark the misconception as confirmed.

## Lesson route

A lesson definition may contain:
- entry
- branches
- explanations
- worked_examples
- progression
- exit

All referenced problem, skill, explanation and worked-example IDs must resolve within the package/dependency set.

Routing conditions are a closed vocabulary interpreted by the application; content cannot execute expressions or Python.

## Evidence policy

Content may emit semantic evidence labels such as `strong_positive`, `positive`, `neutral`, `negative`.

Numeric state-update weights belong to the application Learning Engine configuration, not individual content files. This prevents content authors from silently redefining the mastery algorithm.

## Localization

Russian is mandatory for MVP. Localizable learner-facing strings must use a locale-specific field or future locale map. IDs and machine enums are language-neutral.

## Versioning

Each content package will have:
- package id
- schema version
- content version
- minimum compatible core version

[ASSUMPTION] Semantic versioning is the preferred version notation; exact migration machinery is deferred to Stage 5/7.

## Safety

MVP content packages are trusted, bundled packages. No arbitrary executable plugin code is loaded from content. URLs/media, when later introduced, require explicit validation and provenance policy.
