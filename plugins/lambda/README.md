# lambda — Implementation

**Stage:** Code · **Output:** `changeset@1` · **Version:** 1.0.1

Executes implementation tasks from a `plan@1` using strict TDD. Each task runs in a fresh subagent with isolated context — no state bleeds between tasks. After all tasks complete, an adversarial exit gate reads the codebase from scratch, assumes the implementation is incomplete, and returns a formal `verdict@1` before producing `changeset@1`.

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
| `lambda-recon` | Workspace Recon | haiku / low | Discovers test runner, build tool, and baseline test state before any code is written. |
| `lambda-implementer` | Implementer | sonnet / medium | Executes one task: writes the failing test, implements minimal code to pass it, commits. |
| `lambda-reviewer` | Reviewer | sonnet / medium | Post-task code review — checks for missed sibling functions, code quality issues, and regressions. |
| `lambda-exit-gate` | Exit Gate | opus / high | Adversarially verifies the complete implementation: all acceptance criteria implemented and tested, all tests pass, no regressions. |

---

## Pipeline

```
plan@1 → lambda-recon → [lambda-implementer → lambda-reviewer] × N tasks → lambda-exit-gate → changeset@1
```

Each task runs in a fresh `lambda-implementer` context. The reviewer runs after each individual task. The exit gate runs once after all tasks complete.

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

## Exit Gate

After all tasks are complete, `lambda-exit-gate` runs independently. It does not inherit context from the implementer — it reads the current code state from scratch, assumes the implementation is incomplete, and runs the full axiom verification protocol against the spec. It returns a `verdict@1` before `changeset@1` is produced.

If the exit gate fails, blockers are returned to the implementer for targeted fixes (max 3 retries).

---

## Output Schema

`changeset@1` — see `shared/schemas/changeset@1.json`

| Field | Required | Description |
| :--- | :--- | :--- |
| `summary` | yes | Human-readable summary of what was implemented |
| `files_changed` | yes | Array of files created or modified |
| `acceptance_criteria_met` | yes | Array of spec criteria satisfied, with evidence |
| `reasoning` | yes | Scratchpad — never forwarded downstream |

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

Feed `changeset@1` to **[axiom](../axiom/)** for standalone gate verification and **[delta](../delta/)** for commit, PR, and release tooling.
