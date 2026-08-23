# vector — Implementation Planning

**Stage:** Plan · **Output:** `plan@1` · **Version:** 1.5.0

Decomposes a `spec@1` into a sequenced, testable implementation plan. Every task in `plan@1` is self-contained: exact file paths, a failing test, the minimal implementation to pass it, a conventional commit message, and the acceptance criterion IDs it covers. An implementer with no domain knowledge can execute the plan without making a design decision. When the spec is corrected after implementation reveals it was wrong, planner runs in amend mode — patching only the affected tasks rather than re-decomposing the whole plan.

One skill, not several — see [Behavior](#behavior) below for how it adapts to the request.

---

## When to Use

- You have a `spec@1` and need a concrete, ordered task list before implementation begins
- You want to identify which tasks can be parallelized and which have blocking dependencies
- You need time estimates for scheduling
- You want an adversarial review of a draft plan before handing it to an implementer

**Invoke with:** `"Plan the implementation for this spec"`, `"Break this spec into tasks"`, `"What's the implementation order for this?"`, `"Estimate the work in this plan"`, `"Challenge this implementation plan"`

---

## Behavior

`vector` is one skill (directory `skills/vector/`), not several — there is no separate `vector/plan`, `vector/estimate`, or `vector/challenge` skill to invoke. Behavior adapts to what's asked, dispatching to whichever agent below fits the request:

- **Decompose a spec into a plan** → `planner`
- **Estimate an existing plan** → `estimator`
- **Challenge a draft plan** → `challenger`

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `planner` | Planner | sonnet / medium | Decomposes the spec into ordered tasks, grouped into Subsystem Batches by compilation boundary. Each task has exact file paths, a failing test, minimal implementation, and a conventional commit message. Also runs in amend mode after a spec correction. |
| `estimator` | Estimator | sonnet / medium | Produces per-task time estimates, identifies parallelizable tasks, and lists blocking dependencies. |
| `challenger` | Challenger | sonnet / medium | Adversarially reviews the plan for missing tasks, wrong ordering, under-specified steps, over-sized tasks, missing error handling, acceptance criteria orphaned from every task's `covers_criteria`, and a task touching one implementer of a shared trait/interface/protocol without covering its known siblings (checked via a deterministic pre-scan, not memory). Capped at 2 review rounds. |

---

## Pipeline

```mermaid
flowchart LR
    classDef source fill:#eef2ff,stroke:#6366f1,stroke-width:2px,color:#1e1b4b,rx:8px,ry:8px;
    classDef store fill:#f8fafc,stroke:#64748b,stroke-width:2px,color:#0f172a,rx:8px,ry:8px;
    classDef engine fill:#f5f3ff,stroke:#8b5cf6,stroke-width:2px,color:#4c1d95,rx:8px,ry:8px;
    classDef router fill:#fffbeb,stroke:#f59e0b,stroke-width:2px,color:#78350f,rx:8px,ry:8px;
    classDef output fill:#ecfdf5,stroke:#10b981,stroke-width:2px,color:#064e3b,rx:8px,ry:8px;

    Spec["spec@1"] --> Planner[planner]
    Planner --> Challenger[challenger]
    Challenger -.->|"findings: targeted fix"| Planner
    Challenger --> Plan(["plan@1"])
    Plan -.->|optional| Estimator[estimator]

    class Spec source
    class Planner engine
    class Challenger router
    class Plan output
    class Estimator store
```

`estimator` is optional — run it when scheduling matters. `challenger` always runs; its findings are fed back to `planner` for targeted fixes, capped at 2 rounds before minor disagreements are demoted to non-blocking.

---

## Task Requirements

Every task in `plan@1` must include all of the following. Tasks missing any field are rejected:

- **Exact file paths** to create or modify (no "create a file for X")
- **A failing test** written before any implementation code, with the command to run it
- **Expected failure output** from the failing test (red phase confirmation)
- **The minimal implementation** that makes the test pass
- **A conventional commit message** for the task
- **`covers_criteria`** — the acceptance criterion IDs from the spec this task addresses

No TBDs. No "the implementer will decide." Every acceptance criterion must appear in at least one task's `covers_criteria` — `challenger` flags any criterion that appears in none as `orphaned-criteria`.

---

## Output Schema

`plan@1` — see `shared/schemas/plan@1.json`

The plan is an ordered array of tasks. Each task has: `id`, `title`, `files`, `steps`, `commit_message`, `depends_on`, `covers_criteria`. The plan itself carries `spec_file_path` (propagated from the spec), `spec_hash` (a content hash of the spec file at plan time, used by `recon` to detect if the spec changed after planning), and `linked_requirement` (propagated from the spec's `linked_requirement`, so the requirement-to-code chain stays traceable without re-reading the spec).

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
