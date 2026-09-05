---
name: audit-spec
description: Adversarially review a spec for ambiguity, untestable criteria, missing error behavior, and scope defects. Use for “audit this spec”, “is this spec complete?”, or before gate-spec.
---

# Audit specification quality

## Outcome

Identify actionable defects in a `spec@1` and provide precise replacement language where possible.

## Workflow

1. Validate the artifact with `shared/schemas/spec@1.json`.
2. Examine every criterion for a visible pass/fail observation, hidden implementation choices, undefined terms, missing failure behavior, and conflict with the stated scope or non-goals.
3. Search relevant existing specs for overlap only when the workspace exposes them; read candidates before calling a collision.
4. Produce an issue list with criterion ID, defect type, evidence, and a rewritten suggested fix. State a non-binding pass/fail assessment.
5. Return the revised draft only when the user asks to apply the fixes. The terminal decision remains with `scribe:gate-spec`.

## Contract

- Input schema: `shared/schemas/spec@1.json`
- Output: read-only quality report with actionable issues
- Next step: revise via `scribe:draft-spec` or `scribe:correct-spec`, then run architecture audit and the gate.

## Teams and fallback

Before delegating, read `agent-roles/README.md`; assign the `adversary` card to an independent reading and reconcile its evidence in the primary agent.

Use a teammate only for an independent adversarial reading of a large spec; reconcile findings and remove duplicates yourself. A single-agent audit is complete and valid.

## Boundaries

- Do not reject a criterion merely because it leaves implementation shape open.
- Do not confuse internal consistency with architectural fit; use `scribe:audit-architecture` for that question.
