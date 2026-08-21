# lambda — Implementation

**Stage:** Code · **Output:** committed code, `verdict@1` · **Version:** 1.2.0

Executes implementation tasks from a `plan@1` using strict TDD. Each task runs in a fresh subagent with isolated context — no state bleeds between tasks. `recon` reads the spec directly from disk at `spec_file_path` and, when the plan carries a `spec_hash`, flags whether the spec changed since the plan was made. As each task goes green, `implementer` records exactly where — test file/line, implementation file/line — as `criteria_evidence`, a byproduct of the TDD cycle it already runs. After each task commits, a mutation gate verifies the test suite would catch real faults before the next task begins. If an implementer discovers that a criterion contradicts what the system actually does — not merely that it's hard to implement — it stops and reports the contradiction rather than faking a pass; the caller routes that back to canon for correction before any further task proceeds. After all tasks complete, an adversarial exit gate reads the codebase from scratch, assumes the implementation is incomplete, uses the aggregated `criteria_evidence` as pointers to check (never as proof by itself), and returns a formal `verdict@1`. Lambda does not assemble `changeset@2` itself — the caller hands its accumulated `criteria_evidence` to **[delta](../delta/)**, which produces `changeset@2` from it.

---

## When to Use

- You have a `plan@1` and want to execute it task-by-task via TDD
- You have a `spec@1` but no plan and want to implement directly
- You want to generate a test suite for a module or spec without changing implementation code
- You want a plain-language explanation of what a module does and why
- You need to refactor code without changing observable behavior, with tests staying green throughout

**Invoke with:** `"Implement this"`, `"Execute the plan"`, `"Build this feature"`, `"Write tests for this spec"`, `"Generate tests for X"`, `"Explain what this code does"`, `"Refactor this without changing behavior"`

---

## Sub-skills

| Sub-skill | What it does |
| :--- | :--- |
| `lambda/implement` | Executes a single task from `plan@1` via full TDD: failing test → minimal code → commit |
| `lambda/generate-tests` | Writes a complete test suite for a spec or module — no implementation code changed |
| `lambda/explain` | Reads a module or function and produces a plain-language explanation of what it does and why |
| `lambda/refactor` | Restructures code for clarity or performance; tests must stay green throughout |

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `recon` | Workspace Recon | haiku / low | Detects language, test runner, and build tool. Inventories plan files. Confirms baseline passes before any code is written. Verifies the spec file exists at `spec_file_path` and flags `spec_drift_warning` if the plan's `spec_hash` no longer matches the file on disk. |
| `implementer` | TDD Executor | sonnet / medium | Executes one task: writes the failing test, implements minimal code to pass it, commits. Re-invoked when mutation gate returns precision tests. Reports `spec_contradiction` instead of implementing when a criterion contradicts observed system behavior. |
| `mutator` | Mutation Testing Gate | sonnet / medium | Runs mutation testing on implemented files (cargo-mutants for Rust, Stryker for TypeScript). Identifies surviving mutants and designs precision tests that kill them. |
| `reviewer` | Pre-Gate Reviewer | sonnet / medium | Neutral post-task review — checks scope adherence, non-negotiable violations, sibling gaps, and test quality before the exit gate runs. |
| `exit-gate` | Adversarial Verifier | opus / high | Reads code from scratch. Verifies all acceptance criteria are implemented and tested, all tests pass, mutation gate ran, no regressions. Produces `verdict@1`. |

---

## Pipeline

```
plan@1 → recon → [implementer → mutator → reviewer] × N tasks → exit-gate → changeset@2
```

Each task runs in a fresh `implementer` context. After the implementer commits, `mutator` runs and may feed precision tests back into a second `implementer` cycle before the reviewer and next task proceed. The exit gate runs once after all tasks complete and must confirm the mutation gate ran.

---

## TDD Cycle (per task)

Every task follows this exact sequence — no shortcuts:

1. Write the failing test exactly as specified in the plan
2. Run the test — confirm it fails with the expected error **(red phase required; a test that passes before implementation is broken)**
3. Write the minimal implementation to make it pass — no more
4. Run the test — confirm it passes (green)
5. Run the full test suite — confirm no regressions
6. Commit with the conventional commit message from the plan

---

## Mutation Gate (per task)

After each task commits, `mutator` runs mutation testing scoped to the changed files:

- **Rust** workspaces: `cargo-mutants`
- **TypeScript/JavaScript** workspaces: Stryker
- Language detected from workspace root (`Cargo.toml` → rust; `package.json` → typescript)

For each surviving mutant, `mutator` returns a precision test — a specific, targeted assertion that would fail if that mutation were present. Those tests are fed back to `implementer` as additional failing tests to write and make green. Only when zero mutants survive (or the tool is unavailable) does the pipeline proceed to `reviewer`.

---

## Exit Gate

After all tasks are complete, `exit-gate` runs independently. It does not inherit context from any prior agent — it reads the current code state from scratch and assumes the implementation is incomplete. It confirms that `mutator` ran (or recorded a `tool_unavailable` gap) and produces a `verdict@1` before `changeset@2` is released.

If the exit gate fails, blockers are returned to `implementer` for targeted fixes (max 3 retries; escalates to human after that).

---

## Output Schema

`verdict@1` — see `shared/schemas/verdict@1.json`. Produced by `exit-gate`; pass/fail with specific blockers on failure.

Each `implementer` task also returns `criteria_evidence` — an array of `{criterion_id, test_file, test_line, implementation_file, implementation_line}` entries, one per criterion the task proves. The caller accumulates these across the run and hands them to `changeset-analyzer` when shipping, which uses them to populate `changeset@2.criteria_evidence` — see `shared/schemas/changeset@2.json`.

---

## Install

**Claude Code** — add the marketplace once, then install by ID:
```
/plugin marketplace add orin-dx/agent-plugins
/plugin install lambda
```

**AGY** — installs the full repo; see the [root README](../../README.md#quick-start) for instructions.

---

## Next Stage

Feed the `verdict@1` to **[axiom](../axiom/)** for standalone gate verification, and hand the accumulated `criteria_evidence` to **[delta](../delta/)** for commit, PR, changeset, and release tooling.
