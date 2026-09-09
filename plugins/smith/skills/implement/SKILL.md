---
name: implement
description: >-
  Activate for implementation, implementation tests, or behavior-preserving refactoring. Execute bounded batches with risk-based verification, defect-family review, and an independent scoped verdict. Do not activate for explanation-only requests.
version: 1.7.0
---

# Smith — Implementation Skill

<capability>
Smith executes cohesive subsystem batches. Workspace discovery records languages and available capabilities; implementation selects evidence from changed risks; review checks verification and defect families; the exit gate limits its verdict to observed scope.
</capability>

<io>
**Consumes**: `plan@1` or `spec@1` when no plan exists.

**Produces**: committed code when authorized, `workspace-manifest@1`, `implementation-result@1`, `mutation-report@2`, `implementation-review@2`, and `verdict@3`.

The caller aggregates `criteria_evidence` for exit-gate and later passes it with the diff to `courier:changeset`.
</io>

<implementation_cycle>
For each subsystem batch, read persisted criteria, implement the smallest safe solution, and choose verification from `shared/references/verification-evidence.md` plus capabilities in `workspace-manifest@1`. Record exact commands, observations, boundaries, and criterion locations in `implementation-result@1`. Commit only with explicit authorization.
</implementation_cycle>

<mutation_gate>
Use project-native mutation tooling when available and relevant. A safe deliberate fault may provide equivalent discrimination evidence. Return meaningful survivors as precision tests; record unavailable evidence as a gap in `mutation-report@2`.
</mutation_gate>

<review_gate>
After discrimination testing, `reviewer` produces `implementation-review@2` using `shared/schemas/implementation-review@2.json`. It judges verification fit and records positive or negative evidence for both sibling-search modes.

Review each changed defect as a possible family. The review must cover:

- Syntactic siblings with the same code shape or algorithm.
- Semantic siblings with the same domain responsibility or failure state.
- Candidate sites supporting semantic completeness, including zero-match claims.
- The shared root cause for related instances.
- Missing concepts, states, operations, boundaries, abstractions, invariants, or enforcement.
- Boundary reach, input-space method, relevant environments, external-state freshness, and coverage gaps.
- One disposition: fix instances, unify implementation, escalate architecture, or explicitly defer.

Route the result:

- `approved` → continue.
- `changes_requested` → return must-fix issues and unresolved families to `implementer`, then repeat mutation and review.
- `needs_architecture` → halt the batch and route the review to `scribe:architect`. Gate the resulting spec, amend and challenge the plan, then resume Smith.
</review_gate>

<exit_gate>
After every planned batch has a terminal result and approved review, `exit-gate` reads persisted artifacts and current code independently. It challenges semantic completeness, verifies current state and dispositions, and emits scoped `verdict@3` using `shared/schemas/verdict@3.json`.
</exit_gate>

<subagent_dispatch_matrix>
| Agent | Role | Tier | Delegate when |
| :--- | :--- | :--- | :--- |
| `recon` | Workspace manifest | haiku / low | Before edits: record state, languages, capabilities, baseline, and drift. |
| `implementer` | Batch implementation | sonnet / medium | Implement and test one subsystem batch. |
| `mutator` | Mutation gate | sonnet / medium | Test whether changed behavior is meaningfully covered. |
| `reviewer` | Pre-gate analysis | sonnet / medium | Inspect scope, quality, and defect families after mutation. |
| `exit-gate` | Binding verification | opus / high | Verify the complete changeset after all reviews pass. |
</subagent_dispatch_matrix>

<context_management>
Pass only the current batch, recon manifest, persisted paths, current precision tests, and authorization state to `implementer`. Track each planned batch and started verification task until it has a terminal result; unresolved work reaches exit-gate as `pending_checks`.
</context_management>

<recovery>
- `needs_context`: resolve the named missing file or baseline state before retrying.
- `spec_contradiction`: halt remaining work; route the evidence to `scribe:correct-spec`, then amend and challenge the plan. Escalate if the same criterion contradicts twice.
- Implementer `needs_architecture`: route the complete `implementation-result@1` to `scribe:architect`, then gate, amend, and challenge before resuming.
- Reviewer `needs_architecture`: route the complete `implementation-review@2` to `scribe:architect` so the structural spec retains every family instance and assessment.
</recovery>
