---
name: design-schema
description: Design a versioned shared JSON Schema for an inter-agent handoff. Use when a workflow needs a durable producer-consumer contract or an existing contract must evolve.
---

# Design the boundary before the prompt

Model the artifact's consumers, producers, durable evidence, and failure modes before deciding on fields. A schema exists to make handoffs stable across models and harnesses, not to serialize every thought.

## Discovery

1. Read the relevant existing files in `shared/schemas/` and identify the nearest compatible contract.
2. Name the producer, every consumer, lifecycle point, and whether the artifact is persisted.
3. Separate required decision data from optional evidence, from the non-consumed `reasoning` scratchpad.
4. Decide whether the change is compatible. Breaking changes require a new `<name>@<N+1>.json`; never mutate an existing version's contract.

## Schema requirements

Create a Draft 2020-12 schema at `shared/schemas/<name>@<version>.json` with:

- `$id` matching its versioned filename stem.
- A title and field descriptions that explain consumer use.
- Explicit `required` fields and `additionalProperties: false` at every closed object boundary.
- A `reasoning` string for producer scratchpad when the artifact is structured output.
- Precise enums, arrays, and nested shapes where consumers depend on them.

## Validation and output

Validate representative valid and invalid examples against the draft. Report the producer/consumer map, compatibility decision, filename, validation evidence, and prompt sites that must cite the exact relative schema path.

## Team use

Before delegating, read `agent-roles/README.md`; use `recon` to inventory existing contracts and `adversary` to pressure-test consumer assumptions before the primary agent authors the schema.

When teams are available, one teammate may inventory existing contracts while another pressure-tests consumer needs. The schema author owns the compatibility decision and final draft. Without teams, do those passes in order.
