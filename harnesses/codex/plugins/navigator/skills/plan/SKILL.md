---
name: plan
description: Turn an approved persisted specification into an executable implementation plan, amend a plan after a spec correction, estimate a plan, or adversarially challenge one. Use for “write a plan”, “break this spec into tasks”, “estimate this plan”, or “challenge this plan”.
---

# Plan implementation

## Outcome

Produce a durable `plan@1` that maps every specification criterion to a bounded implementation task, concrete verification, and a sensible compilation-boundary batch.

## Workflow

1. Read the source spec from `spec_file_path` when set; validate it with `shared/schemas/spec@1.json`. If the path is absent, record the coverage gap and do not pretend conversation context is durable.
2. Inspect the live workspace: manifests, package or crate boundaries, existing APIs, adjacent tests, build commands, and current baseline. Read API definitions before placing them in implementation steps.
3. Compute `spec_hash` from the raw persisted spec bytes. Carry `linked_spec`, `spec_file_path`, and `linked_requirement` into the plan.
4. Decompose by cohesive compilation boundaries. Each task needs exact file targets, chosen implementation approach, concrete code baseline, tests that prove its `covers_criteria`, dependencies, and a conventional commit message.
5. Challenge the plan for orphaned criteria, invalid ordering, missing error paths, over-sized batches, and test gaps. Revise only concrete blockers; cap review churn at two rounds.
6. For amendment mode, read the corrected spec and existing plan, patch only tasks linked to changed criterion IDs, then rerun the challenge.
7. After a passing challenge and user authorization, persist the plan at `docs/projects/<linked_spec>.json`, set `plan_file_path`, and commit the artifact.

## Contract

- Input schema: `shared/schemas/spec@1.json`
- Output schema: `shared/schemas/plan@1.json`
- Durable spec path: `docs/specs/<id>.json` through `spec_file_path`
- Durable plan path: `docs/projects/<linked_spec>.json` through `plan_file_path`
- Consumer: `smith:implement` executes the persisted plan against the persisted spec.

## Teams and fallback

Before delegating, read `agent-roles/README.md`; use `recon` for subsystem inventory and `adversary` only for an independent challenge after interfaces are fixed.

Use teams only for independent subsystem batches after the primary agent has established interfaces and task boundaries. A teammate may inspect a crate or package and propose task evidence, but the primary agent owns cross-batch ordering, criterion coverage, and the final plan. On a small change, perform planning and challenge in one agent.

## Boundaries

- Do not use clock-time estimates as the reason to split a task; use transactional compilation and verification boundaries.
- Do not invent exact code without inspecting the live APIs it touches.
- Do not persist or commit a plan without user authorization.
- Do not continue a plan when its persisted spec hash no longer matches; record drift and amend from the current spec.
