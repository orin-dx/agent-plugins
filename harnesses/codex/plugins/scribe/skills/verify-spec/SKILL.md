---
name: verify-spec
description: Verify that each draft specification criterion is grounded in its requirement and research evidence. Use for “does this match the requirement?”, “is this grounded?”, or before an audit or gate.
---

# Verify specification grounding

## Outcome

Return an evidence report that distinguishes supported, unsupported, and overfitted criteria without issuing a terminal readiness verdict.

## Workflow

1. Validate the draft spec, source requirement, and optional research report against `shared/schemas/spec@1.json`, `shared/schemas/requirement@1.json`, and `shared/schemas/research-report@1.json`.
2. Map every acceptance criterion to direct requirement language, research findings, or inspected workspace evidence.
3. Mark a criterion `supported` only when its source establishes the behavior; mark it `unsupported` when no source does; mark it `overfitted` when it constrains a design more tightly than evidence requires.
4. Cite the relevant criterion IDs and source locations. Return evidence only, leaving rewrite decisions to drafting and audit.

## Contract

- Input schemas: `shared/schemas/spec@1.json`, `shared/schemas/requirement@1.json`, optionally `shared/schemas/research-report@1.json`
- Output: read-only grounding report with per-criterion classification and evidence
- Next step: `scribe:audit-spec` reviews the draft’s internal quality.

## Teams and fallback

Before delegating, read `agent-roles/README.md`; use `reviewer` only for a non-overlapping criterion set and retain final evidence classification in the primary agent.

For large specs, teams may independently trace non-overlapping criterion groups while the primary agent reconciles classifications. For normal specs, verify sequentially in the current agent.

## Boundaries

- Do not turn a weak inference into support.
- Do not issue `verdict@1`; `scribe:gate-spec` owns the terminal readiness decision.
