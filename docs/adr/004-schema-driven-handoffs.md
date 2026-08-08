# ADR-004: Schema-driven handoffs with immutable versioning

**Status:** Accepted
**Date:** 2026-08-08

## Context

Early agent handoffs were described in prose within agent prompts — "the next agent expects a JSON object with fields X, Y, Z." This created a coordination problem: upstream and downstream agents could drift without a shared enforced contract, and a breaking change in one agent's output was invisible until runtime. Three alternatives were considered: (a) prose-only description (current state), (b) TypeScript interfaces as contracts, (c) JSON Schema files as contracts.

## Decision

Every inter-agent handoff is a typed JSON Schema document in `shared/schemas/<name>@<version>.json`. Schemas use JSON Schema draft-2020-12 with `additionalProperties: false` — unknown fields are rejected at validation time. Every schema includes a `reasoning: string` scratchpad field for chain-of-thought that is never forwarded downstream. Schema versions are immutable: `requirement@1.json` never changes; a breaking change creates `requirement@2.json`. Schemas are validated at wiring time (before execution), not at runtime inside agents.

## Consequences

A schema-invalid output halts the pipeline before any agent acts on bad data. Downstream agents can declare exactly what they consume; upstream agents know exactly what to produce. Breaking changes are explicit (a new file with a new version) rather than silent. The `reasoning` field gives agents a scratchpad that never pollutes downstream consumers. Authors must write the schema before writing the agent prompt — the schema is the spec.
