---
name: code
description: >-
  Activate when the user says "implement this", "execute the plan", "write the code", "build this feature", "generate tests for X", "write tests for this spec", "refactor this without changing behavior", or "explain what this code does". Also activate when handed a plan@1 artifact and asked to execute it, or when a spec@1 exists but no plan. Every task starts TDD-first: write a failing test, confirm red, write minimal implementation, confirm green, commit. After implementation, mutation testing verifies the test suite would catch real faults — surviving mutants are returned to the implementer as precision tests before the exit gate runs. The axiom exit gate runs independently at the end to verify all spec criteria are met — it reads the codebase from scratch and assumes the implementation is incomplete. Works from plan@1 (preferred) or spec@1 directly when no plan exists.
version: 1.4.0
---

# Lambda — Implementation Skill

<capability>

lambda is one skill, not four. Every real invocation runs the same TDD pipeline through `implementer`: read the task's acceptance criteria, write a failing test, confirm red, write the minimal implementation, confirm green, commit — then `mutator` and `reviewer` gate the batch before `exit-gate` runs the final adversarial check.

The frontmatter `description` also triggers on "generate tests for X," "explain what this code does," and "refactor this without changing behavior." None of those have dedicated agent behavior — no agent here writes tests without implementation, produces a plain-language explanation, or runs a refactor-only mode. A request framed that way still routes to `implementer`'s standard TDD cycle; if that's not a fit (there is no failing test to write for "explain this"), say so rather than forcing the pipeline to produce something no agent actually defined.

</capability>

---

<io>

**Consumes**: `plan@1` (preferred) or `spec@1` directly if no plan exists.

**Produces**: committed code, and per-task `criteria_evidence` (exact test and implementation file/line for each criterion proven). No lambda agent assembles a `changeset@2` itself — that schema is produced by `changeset-analyzer` when shipping. The caller aggregates each task's `criteria_evidence` across the run and hands the collection to `changeset-analyzer` alongside the diff, so delta uses lambda's exact evidence instead of reconstructing approximate locations from the diff.

</io>

---

<tdd_cycle>

For every implementation task:

1. Write the failing test exactly as specified.
2. Run the test — confirm it fails with the expected error (red phase required; a test that passes before implementation is broken).
3. Write the minimal implementation to make it pass — no more.
4. Run the test — confirm it passes (green).
5. Commit with the conventional commit message specified in the task.

</tdd_cycle>

---

<mutation_gate>

After each implementation task commits, `mutator` runs mutation testing scoped to the files changed in that task. It detects language from the workspace root (Cargo.toml → `cargo-mutants`; package.json → Stryker) and analyzes every mutant the test suite failed to catch.

For each surviving mutant, `mutator` designs a precision test that would kill it and returns those tests to `implementer` as additional failing tests. The implementer writes them and makes them green before any further tasks proceed.

When the mutation tool is unavailable, `mutator` reports `tool_unavailable` and `exit-gate` records the gap rather than blocking.

</mutation_gate>

---

<exit_gate>

After all tasks are complete and `mutator` has run, `exit-gate` runs the axiom protocol against the spec independently. It reads the spec from `spec_file_path` on disk — not from spec content forwarded through conversation context. It reads the current code state from scratch, assumes the implementation is incomplete, and confirms that mutation testing ran (or was noted as unavailable). It returns a `verdict@1`. A spec without `spec_file_path` set is a hard block.

The caller passes the aggregated per-task `criteria_evidence` to `exit-gate` alongside the manifest. The gate uses each entry as a pointer to check — reading exactly the named file and line — rather than searching the codebase cold for every criterion. This makes verification faster without making it less adversarial: the gate still reads the actual location itself and confirms the criterion holds; it does not accept the pointer's existence as proof.

</exit_gate>

---

<subagent_dispatch_matrix>

| Agent | Role | Tier | When to delegate |
| :--- | :--- | :--- | :--- |
| **`recon`** | Workspace manifest & baseline | haiku / low | Before any code is written — detect language, test runner, inventory plan files, confirm baseline passes. |
| **`implementer`** | TDD batch execution | sonnet / medium | Executes a Subsystem Batch (or single task) from plan@1 — full red/green/commit cycle adhering to YAGNI (Ponytail layer). |
| **`mutator`** | Mutation testing gate | sonnet / medium | After each Subsystem Batch commits — verify the test suite catches real faults; returns precision tests for survivors. |
| **`reviewer`** | Pre-gate review | sonnet / medium | After batch mutation gate passes — neutral review of batch scope, non-negotiables, sibling gaps, test quality. |
| **`exit-gate`** | Adversarial exit verification | opus / high | After all batches complete — independent axiom check against spec; produces verdict@1. |

</subagent_dispatch_matrix>

---

<context_management>

Lambda executes tasks sequentially by **Subsystem Batch**. Each `implementer` invocation handles one cohesive crate/subsystem batch (or single task if unbatched), keeping subagent spawns under 8–12 total per track.

**Caller MUST pass per-invocation:**
- The current Subsystem Batch (task IDs and definitions) only (not the full `plan@1`).
- The workspace manifest from `recon` (file list + baseline status).
- `spec_file_path` from the plan@1 (propagated from spec@1) — agents read acceptance criteria directly from disk.
- Any `precision_tests` from `mutator` for the current batch.

**Caller MUST NOT pass:**
- The full `plan@1` on every invocation — a 40-task plan passed 40 times consumes 320K–600K tokens on plan context alone.
- The full `spec@1` content on every invocation — pass `spec_file_path` instead; agents read from disk. Context is lossy under compression; the file is not.
- Prior task results — the commit SHA is sufficient to verify what happened.

**Progress tracking:** The caller tracks completed task IDs, their commit SHAs, and their `criteria_evidence` entries externally (in a progress note or equivalent). On re-entry after interruption, pass the remaining tasks, not the full list. The accumulated `criteria_evidence` across all completed tasks is what gets passed to `exit-gate` and later to `changeset-analyzer` — do not discard it once a task completes.

**When `implementer` emits `needs_context`:** the caller resolves the missing information (file path, baseline commit) before re-invoking — do not retry with the same inputs.

**When `implementer` emits `spec_contradiction`:** the caller halts remaining task execution — already-completed tasks are not rolled back, but no further task proceeds against a spec known to be wrong. Route the contradiction (spec_file_path, criterion_id, spec_claim, observed_behavior) to canon/correct-spec. Once the corrected spec passes exit-gate and is written back to the same spec_file_path, route the corrected spec@1 to planner in amend mode, then through challenger — an amended plan is not exempt from adversarial review, especially for newly added tasks — before resuming lambda from the remaining tasks. The caller tracks correction attempts per criterion_id: if the same criterion_id triggers spec_contradiction a second time after already being corrected, escalate to a human rather than routing to canon/correct-spec again.

</context_management>
