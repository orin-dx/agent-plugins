---
name: code
description: >-
  Activate when the user says "implement this", "execute the plan", "write the code", "build this feature", "generate tests for X", "write tests for this spec", "refactor this without changing behavior", or "explain what this code does". Also activate when handed a plan@1 artifact and asked to execute it, or when a spec@1 exists but no plan. Every task starts TDD-first: write a failing test, confirm red, write minimal implementation, confirm green, commit. After implementation, mutation testing verifies the test suite would catch real faults — surviving mutants are returned to the implementer as precision tests before the exit gate runs. The axiom exit gate runs independently at the end to verify all spec criteria are met — it reads the codebase from scratch and assumes the implementation is incomplete. Works from plan@1 (preferred) or spec@1 directly when no plan exists.
version: "1.1.0"
---

# Lambda — Implementation Skill

<sub_skills>

| Sub-skill | What it does |
| :--- | :--- |
| `lambda/implement` | Executes a single task from a plan@1 via the full TDD cycle: failing test → minimal code → commit. |
| `lambda/generate-tests` | Writes a complete test suite for a spec or module without changing implementation code. |
| `lambda/explain` | Reads a module or function and produces a plain-language explanation of what it does and why. |
| `lambda/refactor` | Restructures code for clarity or performance without changing observable behavior; tests must stay green throughout. |

</sub_skills>

---

<io>

**Consumes**: `plan@1` (preferred) or `spec@1` directly if no plan exists.

**Produces**: `changeset@1`, committed code.

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

After each implementation task commits, `lambda-mutator` runs mutation testing scoped to the files changed in that task. It detects language from the workspace root (Cargo.toml → `cargo-mutants`; package.json → Stryker) and analyzes every mutant the test suite failed to catch.

For each surviving mutant, `lambda-mutator` designs a precision test that would kill it and returns those tests to `lambda-implementer` as additional failing tests. The implementer writes them and makes them green before any further tasks proceed.

When the mutation tool is unavailable, `lambda-mutator` reports `tool_unavailable` and `lambda-exit-gate` records the gap rather than blocking.

</mutation_gate>

---

<exit_gate>

After all tasks are complete and `lambda-mutator` has run, `lambda-exit-gate` runs the axiom protocol against the spec independently. It reads the spec from `spec_file_path` on disk — not from spec content forwarded through conversation context. It reads the current code state from scratch, assumes the implementation is incomplete, and confirms that mutation testing ran (or was noted as unavailable). It returns a `verdict@1`. A spec without `spec_file_path` set is a hard block.

</exit_gate>

---

<subagent_dispatch_matrix>

| Agent | Role | Tier | When to delegate |
| :--- | :--- | :--- | :--- |
| **`lambda-recon`** | Workspace manifest & baseline | haiku / low | Before any code is written — detect language, test runner, inventory plan files, confirm baseline passes. |
| **`lambda-implementer`** | TDD execution | sonnet / medium | One task at a time from the plan@1 — full red/green/commit cycle. Re-invoked when lambda-mutator returns precision tests. |
| **`lambda-mutator`** | Mutation testing gate | sonnet / medium | After each implementer commit — verify the test suite would catch real faults; return precision tests for any survivors. |
| **`lambda-reviewer`** | Pre-gate review | sonnet / medium | After mutation gate passes — neutral review of scope, non-negotiables, sibling gaps, test quality. |
| **`lambda-exit-gate`** | Adversarial exit verification | opus / high | After all tasks and mutation gate complete — independent axiom check against spec; produces verdict@1. |

</subagent_dispatch_matrix>

---

<context_management>

Lambda executes tasks sequentially. Each `lambda-implementer` invocation handles exactly one task. The orchestrating caller is responsible for keeping context lean across the sequence.

**Caller MUST pass per-invocation:**
- The current task object only (not the full `plan@1`).
- The workspace manifest from `lambda-recon` (file list + baseline status).
- `spec_file_path` from the plan@1 (propagated there by vector-planner from the spec@1) — pass it to lambda-recon so it flows through the workspace manifest to all downstream agents.
- Any `precision_tests` from `lambda-mutator` for the current task.

**Caller MUST NOT pass:**
- The full `plan@1` on every invocation — a 40-task plan passed 40 times consumes 320K–600K tokens on plan context alone.
- The full `spec@1` content on every invocation — pass `spec_file_path` instead; agents read from disk. Context is lossy under compression; the file is not.
- Prior task results — the commit SHA is sufficient to verify what happened.

**Progress tracking:** The caller tracks completed task IDs and their commit SHAs externally (in a progress note or equivalent). On re-entry after interruption, pass the remaining tasks, not the full list.

**When `lambda-implementer` emits `needs_context`:** the caller resolves the missing information (file path, baseline commit) before re-invoking — do not retry with the same inputs.

</context_management>
