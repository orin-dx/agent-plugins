---
name: gate-spec
description: Issue the binding pass or fail decision for a specification before planning begins. Use for “gate this spec”, “is this ready to plan?”, or “check this spec before implementation”.
---

# Gate a specification

## Outcome

Produce a `verdict@1` that a spec must earn through testable criteria, explicit error behavior, bounded scope, and resolved upstream audit findings.

## Workflow

1. Validate the candidate with `shared/schemas/spec@1.json` and inspect the actual JSON, not a summary passed through conversation.
2. Confirm each criterion has a falsifiable observation, no unresolved TBD language, and a clear relationship to scope and non-goals.
3. Read prior grounding, quality, and architecture audit evidence when supplied. Recheck material blockers yourself instead of trusting a label.
4. Default to fail when evidence is insufficient. On failure, return minimal blockers that name the exact criterion or field and the corrective action.
5. On pass, present the verdict and proposed persistence action. Only after user authorization, write the spec to `docs/specs/<id>.json`, set `spec_file_path`, and commit it as a durable handoff.

## Contract

- Input schema: `shared/schemas/spec@1.json`
- Output schema: `shared/schemas/verdict@1.json`
- Passing persistence: `docs/specs/<id>.json` containing the same valid `spec@1` with `spec_file_path`
- Next step: `navigator:plan` consumes the persisted artifact.

## Teams and fallback

Before delegating, read `agent-roles/README.md`; use `recon` only for fixed evidence collection and reserve the final decision for the primary `judge`.

The final gate is one accountable judgment and runs in the current agent. A team may supply bounded evidence before the gate, but cannot replace the final independent reading.

## Boundaries

- Do not persist or commit without user authorization.
- Do not pass a spec because a prior reviewer approved it.
- Do not reopen architecture design that an architecture audit has already resolved unless new contradictory evidence appears.
