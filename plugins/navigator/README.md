# navigator — Implementation Planning

**Stage:** Plan · **Output:** `plan@1` · **Version:** 2.2.0

Decomposes a `spec@1` into a sequenced, testable implementation plan. Every task in `plan@1` is self-contained: exact file paths, a brief implementation approach, exact implementation code as a concrete baseline, the exact tests proving each criterion, a conventional commit message, and the acceptance criterion IDs it covers. An implementer with no domain knowledge can execute the plan without needing to decide what to build or which criteria it must satisfy — [smith](../smith/) may still adapt the baseline's shape, provided the same files, criteria, and tests are satisfied. When the spec is corrected after implementation reveals it was wrong, planner runs in amend mode — patching only the affected tasks rather than re-decomposing the whole plan.

One skill, not several — see [Behavior](#behavior) below for how it adapts to the request.

---

## When to Use

- You have a `spec@1` and need a concrete, ordered task list before implementation begins
- You want to identify which tasks can be parallelized and which have blocking dependencies
- You need time estimates for scheduling
- You want an adversarial review of a draft plan before handing it to an implementer

**Invoke with:** `"Plan the implementation for this spec"`, `"Break this spec into tasks"`, `"What's the implementation order for this?"`, `"Estimate the work in this plan"`, `"Challenge this implementation plan"`

---

## Install

**Claude Code** — add the marketplace once, then install by ID:
```
/plugin marketplace add orin-dx/agent-plugins
/plugin install navigator
```

**AGY** — installs the full repo; see the [root README](../../README.md#quick-start) for instructions.

---

## Behavior

`navigator` is one skill (directory `skills/plan/`), not several — there is no separate `navigator/estimate` or `navigator/challenge` skill to invoke; estimating and challenging both happen inside this one `plan` skill. Behavior adapts to what's asked, dispatching to whichever agent below fits the request:

- **Decompose a spec into a plan** → `planner`
- **Estimate an existing plan** → `estimator`
- **Challenge a draft plan** → `challenger`

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `planner` | Planner | sonnet / medium | Decomposes the spec into ordered tasks, grouped into Subsystem Batches by compilation boundary. Each task has exact file paths, a brief implementation approach, the exact implementation, the exact tests proving each criterion, and a conventional commit message. Also runs in amend mode after a spec correction. |
| `estimator` | Estimator | sonnet / medium | Produces per-task time estimates, identifies parallelizable tasks, and lists blocking dependencies. |
| `challenger` | Challenger | sonnet / medium | Adversarially reviews the plan for missing tasks, wrong ordering, under-specified steps, over-sized tasks, missing error handling, acceptance criteria orphaned from every task's `covers_criteria`, and a task touching one implementer of a shared trait/interface/protocol without covering its known siblings (checked via a deterministic pre-scan, not memory). Capped at 2 review rounds. |

---

## Pipeline

```mermaid
%%{init: {'flowchart': {'curve': 'basis', 'nodeSpacing': 40, 'rankSpacing': 60}}}%%
flowchart LR
    classDef source fill:#eef2ff,stroke:#6366f1,stroke-width:1.5px,color:#1e1b4b,rx:10,ry:10,font-size:14px,font-weight:600;
    classDef store fill:#f8fafc,stroke:#64748b,stroke-width:1.5px,color:#0f172a,rx:10,ry:10,font-size:13px,font-weight:500;
    classDef engine fill:#f5f3ff,stroke:#8b5cf6,stroke-width:1.5px,color:#4c1d95,rx:10,ry:10,font-size:13px,font-weight:500;
    classDef router fill:#fffbeb,stroke:#f59e0b,stroke-width:1.5px,color:#78350f,rx:10,ry:10,font-size:14px,font-weight:600;
    classDef output fill:#ecfdf5,stroke:#10b981,stroke-width:1.5px,color:#064e3b,rx:10,ry:10,font-size:14px,font-weight:600;

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

## Output Schema

`plan@1` — see `shared/schemas/plan@1.json`

The plan is an ordered array of tasks. Each task has: `id`, `title`, `files`, `steps`, `commit_message`, `depends_on`, `covers_criteria`. The plan itself carries `spec_file_path` (propagated from the spec), `spec_hash` (a content hash of the spec file at plan time, used by `recon` to detect if the spec changed after planning), and `linked_requirement` (propagated from the spec's `linked_requirement`, so the requirement-to-code chain stays traceable without re-reading the spec).

---

## Task Requirements

Every task in `plan@1` must include all of the following. Tasks missing any field are rejected:

- **Exact file paths** to create or modify (no "create a file for X")
- **A brief implementation approach**, decided before the test steps are written
- **The exact implementation code** — a concrete baseline proving the task is achievable within its file targets and scope, not a shape smith's implementer must copy verbatim
- **The exact tests** proving each of the task's `covers_criteria` criteria, with the command confirming the full suite passes
- **A conventional commit message** for the task
- **`covers_criteria`** — the acceptance criterion IDs from the spec this task addresses

Tests are not required to precede the implementation steps within a task — [smith](../smith/)'s mutation-testing gate verifies test quality, not step order. See [ADR-008](../../docs/adr/008-drop-test-first-ordering.md) and smith's [Implementation Cycle](../smith/README.md#implementation-cycle-per-task) for that rationale, and [ADR-009](../../docs/adr/009-implementer-shape-latitude.md) for why the implementation code is a baseline smith's implementer may adapt rather than a mandate.

No TBDs. No "the implementer will decide." Every acceptance criterion must appear in at least one task's `covers_criteria` — `challenger` flags any criterion that appears in none as `orphaned-criteria`.

---

## Next Stage

Feed `plan@1` to **[smith](../smith/)** (implementation).
