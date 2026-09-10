---
name: implement
description: Execute an approved plan or specification with targeted implementation, tests, evidence, review, and independent verification. Use for “implement this”, “execute the plan”, “build this feature”, “write the code”, or “refactor without changing behavior”.
---

State material concerns, evidence, consequence, and confidence directly. Do not soften blockers, manufacture praise, or claim certainty beyond the evidence.

# Implement with evidence

## Outcome

Make the requested workspace change in bounded batches and return a scoped verdict grounded in current code, risk-based verification, and defect-family review.

## Workflow

1. Prefer a persisted `plan@1`. Read it from `plan_file_path` and its source spec from `spec_file_path`; validate them with `shared/schemas/plan@1.json` and `shared/schemas/spec@1.json`.
2. Verify the plan’s `spec_hash` against the raw spec file bytes. Stop and report drift if it differs; a stale plan cannot silently govern implementation.
3. Produce `workspace-manifest@1` from current repository state, every affected language, project-native verification capabilities, baseline tests, and exposed workflow provenance.
4. Execute one cohesive subsystem batch. Choose the smallest safe implementation and verification methods from the changed risks and `shared/references/verification/evidence.md`.
5. Record `implementation-result@1` with exact criterion locations, commands, observations, boundaries, and environment evidence.
6. Use available mutation tooling against changed behavior or a safe deliberate-fault check. Record `mutation-report@2`; unavailable evidence is a coverage gap.
7. Produce `implementation-review@2`. Judge verification fit, sibling completeness, semantic models, and architecture.
8. Before completion, account for every planned batch and started verification task, reread persisted artifacts and current code, independently challenge semantic completeness, and emit scoped `verdict@3`. Commit only after user authorization.

## Defect-family review

Before reviewing, load `shared/references/verification/implementation-review.md` and the evidence it selects. For each changed defect, assess:

- Syntactic siblings with the same code shape or algorithm.
- Semantic siblings with the same domain responsibility or failure state.
- Candidate sites supporting semantic completeness, including zero-match claims.
- The shared root cause for related instances.
- Missing concepts, states, operations, boundaries, abstractions, invariants, or enforcement.
- One disposition: fix instances, unify implementation, escalate architecture, or explicitly defer.
- Boundary reach, input-space method, relevant environments, external-state freshness, and coverage gaps.

Use the current architecture model when available to derive candidate responsibilities and canonical abstractions. Resolve `changes_requested` findings before the exit gate. Route `needs_architecture` to `scribe:architect`; gate the resulting spec, amend the plan, then resume.

## Contract

- Input schemas: `shared/schemas/plan@1.json` and `shared/schemas/spec@1.json`
- Workspace schema: `shared/schemas/workspace-manifest@1.json`
- Batch schema: `shared/schemas/implementation-result@1.json`
- Mutation schema: `shared/schemas/mutation-report@2.json`
- Review schema: `shared/schemas/implementation-review@2.json`
- Output schema: `shared/schemas/verdict@3.json`
- Durable inputs: `docs/projects/<linked_spec>.json` and `docs/specs/<id>.json` when their path fields are set
- Evidence: per-task `criteria_evidence` points to current implementation and tests; it is not a substitute for final inspection.

## Teams and fallback

Before delegating, read `agent-roles/README.md`; use `implementer` only for an isolated batch and `reviewer` only after its diff and verification output exist.

Use teams only for independent subsystem batches with no shared files or undecided interfaces. Give each teammate a batch, criteria, current manifest, and persisted paths. Reconcile changed files and observed outputs; track every started task to a terminal result. Work alone for coupled boundaries or when teams are unavailable.

## Exceptions and recovery

- If the implementation contradicts a spec criterion, halt remaining work and report `spec_contradiction` with the criterion ID, spec claim, observed behavior, and evidence. Route the correction to `scribe:correct-spec`, then replan in amend mode.
- If the safe solution needs an architectural boundary beyond plan scope, stop that batch and report an architecture escalation grounded in live code. Do not commit an unsafe shape just to complete the plan.
- If related defects reveal a missing domain concept, state, operation, boundary, abstraction, invariant, or enforcement mechanism, route `implementation-review@2` to `scribe:architect` before continuing.
- If one batch cannot be implemented safely within plan scope, route its `implementation-result@1` architecture escalation to `scribe:architect`.
- If a test or build fails, diagnose from the observed output and fix only the relevant defect before continuing. Do not mask a failure by weakening verification.

## Boundaries

- Do not make external releases, push branches, or commit without user authorization.
- Do not claim success from a passing targeted test when the applicable full suite has not been considered.
- Do not accept teammate summaries without reading the changed files, test output, and evidence yourself.
- Do not require mutation, property, fuzz, boundary, or environment checks when the changed risk does not justify them.
- Do not claim support from a named tool alone; record what it exercised and observed.
