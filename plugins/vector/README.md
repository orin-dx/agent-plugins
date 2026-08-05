# vector — Implementation Planning

**Stage:** Plan · **Output:** `plan@1` · **Version:** 1.0.1

Decomposes a `spec@1` into a sequenced, testable implementation plan. Every task in `plan@1` is self-contained: exact file paths, a failing test, the minimal implementation to pass it, and a conventional commit message. An implementer with no domain knowledge can execute the plan without making a design decision.

---

## When to Use

- You have a `spec@1` and need a concrete, ordered task list before implementation begins
- You want to identify which tasks can be parallelized and which have blocking dependencies
- You need time estimates for scheduling
- You want an adversarial review of a draft plan before handing it to an implementer

**Invoke with:** `"Plan the implementation for this spec"`, `"Break this spec into tasks"`, `"What's the implementation order for this?"`, `"Estimate the work in this plan"`, `"Challenge this implementation plan"`

---

## Sub-skills

| Sub-skill | What it does |
| :--- | :--- |
| `vector/plan` | Decomposes a spec into ordered, self-contained implementation tasks |
| `vector/estimate` | Produces per-task time estimates, identifies parallelizable tasks, and lists blocking dependencies |
| `vector/challenge` | Adversarially reviews a draft plan for missing tasks, wrong ordering, under-specified steps, and missing error handling |

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `vector-planner` | Planner | sonnet / medium | Decomposes the spec into ordered tasks. Each task has exact file paths, a failing test, minimal implementation, and a conventional commit message. |
| `vector-estimator` | Estimator | sonnet / medium | Produces per-task time estimates, identifies parallelizable tasks, and lists blocking dependencies. |
| `vector-challenger` | Challenger | opus / high | Adversarially reviews the plan for missing tasks, wrong ordering, under-specified steps, and missing error handling. |

---

## Pipeline

```
spec@1 → vector-planner → vector-challenger → [vector-estimator] → plan@1
```

`vector-estimator` is optional — run it when scheduling matters. The challenger always runs; its findings are fed back to the planner for targeted fixes.

---

## Task Requirements

Every task in `plan@1` must include all of the following. Tasks missing any field are rejected:

- **Exact file paths** to create or modify (no "create a file for X")
- **A failing test** written before any implementation code, with the command to run it
- **Expected failure output** from the failing test (red phase confirmation)
- **The minimal implementation** that makes the test pass
- **A conventional commit message** for the task

No TBDs. No "the implementer will decide."

---

## Output Schema

`plan@1` — see `shared/schemas/plan@1.json`

The plan is an ordered array of tasks. Each task has: `id`, `description`, `files`, `test`, `implementation`, `commit_message`, `depends_on`.

---

## Install

**Claude Code** — add the marketplace once, then install by ID:
```
/plugin marketplace add orin-dx/agent-plugins
/plugin install vector
```

**AGY** — installs the full repo; see the [root README](../../README.md#quick-start) for instructions.

---

## Next Stage

Feed `plan@1` to **[lambda](../lambda/)** (TDD implementation).
