---
name: component
description: Turn UI intent into an implementation-ready component specification. Use when the user asks to specify, audit, or gate a component design before planning or implementation.
---

# Specify observable component behavior

Convert the supplied design intent into a component contract that an implementer and a tester can independently use. Inspect existing repository components, tokens, conventions, and accessibility patterns before inventing new APIs.

## Inputs

- A `requirement@1` artifact conforming to `shared/schemas/requirement@1.json`, or explicit free-text UI intent.
- Existing component API, design-system primitives, and similar component behavior when they exist.
- Platform and accessibility evidence relevant to keyboard, focus, semantics, announcements, contrast, and motion.

## Workflow

1. Inventory what is known, unknown, and constrained by the surrounding codebase.
2. Draft a `spec@1` conforming to `shared/schemas/spec@1.json` with props, variants, state transitions, observable outcomes, error cases, and accessibility criteria.
3. Make every acceptance criterion falsifiable from outside the implementation. Mark invalid combinations or error paths with `is_error_case: true`.
4. Audit the draft for missing states, contradictory criteria, ambiguous language, and accessibility gaps.
5. Emit a `verdict@1` conforming to `shared/schemas/verdict@1.json`. On failure, return only actionable blockers to the draft. On pass, persist the spec at `docs/specs/<id>.json` with `spec_file_path` set, then hand off the persisted artifact.

## Decisions and stopping

Do not leave TBD markers in the spec. Put deliberately deferred topics in `non_goals`; put unavoidable uncertainty in `reasoning` and name its implementation impact. Cap draft-audit revision at two rounds; unresolved naming or phrasing disputes become non-blocking notes rather than an infinite loop. Escalate after three failed gate retries.

## Team use

Before delegating, read `agent-roles/README.md`; use `reviewer` for independent behavior or accessibility review after the primary `author` has fixed the draft.

When teams are available, use parallel review only for independent behavior and accessibility passes after a shared draft exists. Reconcile findings into one spec and one verdict. If teams are unavailable, perform both passes yourself before gating.
