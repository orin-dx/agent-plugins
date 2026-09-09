---
name: implement
description: >-
  Activate for implementation, test generation tied to implementation, or behavior-preserving refactoring. Execute a persisted plan when available. For each subsystem batch, design the approach, implement it, prove covered criteria with tests, run mutation checks, and review the result. Review includes syntactic and semantic sibling defects, their shared root cause, and evidence of missing domain concepts or architectural constraints. Resolve scoped families locally; route structural families to `scribe:architect`. Finish with an independent verdict. Do not force plain explanation requests through this workflow.
version: 1.6.0
---

# Smith — Implementation Skill

<capability>
Smith executes implementation work in cohesive subsystem batches. Each batch passes through implementation, mutation, and review before the final exit gate. Tests prove criteria; mutation checks test precision; `implementation-review@1` records issues and related-defect families.
</capability>

<io>
**Consumes**: `plan@1` or `spec@1` when no plan exists.

**Produces**: committed code when authorized, per-criterion evidence, `implementation-review@1`, and `verdict@1`.

The caller aggregates `criteria_evidence` for exit-gate and later passes it with the diff to `courier:changeset`.
</io>

<implementation_cycle>
For each subsystem batch:

1. Read its `covers_criteria` from the persisted spec.
2. Choose the implementation shape before tests lock it in.
3. Implement the smallest scoped solution.
4. Write tests that fail when each covered criterion is violated.
5. Run targeted tests, then the relevant full suite.
6. Record exact implementation and test locations for each criterion.
7. Commit only when the caller records user authorization as `commit_authorized: true`.
</implementation_cycle>

<mutation_gate>
Run mutation testing against changed behavior after each batch. Return surviving mutants as precision tests for `implementer`; repeat until they are killed. Record unavailable tooling as a coverage gap.
</mutation_gate>

<review_gate>
After mutation, `reviewer` produces `implementation-review@1` using `shared/schemas/implementation-review@1.json`. It records workspace and batch lineage plus positive or negative evidence for both sibling-search modes.

Review each changed defect as a possible family. The review must cover:

- Syntactic siblings with the same code shape or algorithm.
- Semantic siblings with the same domain responsibility or failure state.
- The shared root cause for related instances.
- Missing concepts, states, operations, boundaries, abstractions, invariants, or enforcement.
- One disposition: fix instances, unify implementation, escalate architecture, or explicitly defer.

Route the result:

- `approved` → continue.
- `changes_requested` → return must-fix issues and unresolved families to `implementer`, then repeat mutation and review.
- `needs_architecture` → halt the batch and route the review to `scribe:architect`. Gate the resulting spec, amend and challenge the plan, then resume Smith.
</review_gate>

<exit_gate>
After every batch passes review, `exit-gate` reads the persisted spec and current code independently. It treats criteria evidence as pointers, validates the final `implementation-review@1`, verifies every family disposition, and emits `verdict@1` using `shared/schemas/verdict@1.json`.
</exit_gate>

<subagent_dispatch_matrix>
| Agent | Role | Tier | Delegate when |
| :--- | :--- | :--- | :--- |
| `recon` | Workspace manifest | haiku / low | Before edits: detect language, files, test runner, baseline, and spec drift. |
| `implementer` | Batch implementation | sonnet / medium | Implement and test one subsystem batch. |
| `mutator` | Mutation gate | sonnet / medium | Test whether changed behavior is meaningfully covered. |
| `reviewer` | Pre-gate analysis | sonnet / medium | Inspect scope, quality, and defect families after mutation. |
| `exit-gate` | Binding verification | opus / high | Verify the complete changeset after all reviews pass. |
</subagent_dispatch_matrix>

<context_management>
Pass only the current batch, recon manifest, `spec_file_path`, current precision tests, and explicit `commit_authorized` state to `implementer`. Track completed task IDs, commit SHAs, and `criteria_evidence` outside the agent context.
</context_management>

<recovery>
- `needs_context`: resolve the named missing file or baseline state before retrying.
- `spec_contradiction`: halt remaining work; route the evidence to `scribe:correct-spec`, then amend and challenge the plan. Escalate if the same criterion contradicts twice.
- Implementer `needs_architecture`: convert `architecture_escalation` into a valid single-finding `finding-report@1`; route it to `scribe:architect`, then gate, amend, and challenge before resuming.
- Reviewer `needs_architecture`: route the complete `implementation-review@1` to `scribe:architect` so the structural spec retains every family instance and assessment.
</recovery>
