# vector — Implementation Planning

**Stage:** Plan · **Output:** `plan@1`

Decomposes a `spec@1` into a sequenced, testable implementation plan. Every task is self-contained — an implementer with no domain knowledge can execute it without making a design decision.

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `vector-planner` | Planner | sonnet/medium | Decomposes the spec into ordered tasks, each with exact file paths, a failing test, minimal implementation, and a conventional commit message. |
| `vector-estimator` | Estimator | sonnet/medium | Produces per-task time estimates, identifies parallelizable tasks, and lists blocking dependencies. |
| `vector-challenger` | Challenger | opus/high | Adversarially reviews the plan for missing tasks, wrong ordering, under-specified steps, and missing error handling. |

## Pipeline

```
spec@1 → vector-planner → vector-challenger → [vector-estimator] → plan@1
```

`vector-estimator` is optional — run it when scheduling matters.

## Task Requirements

Every task in `plan@1` must include:
- Exact file paths to create or modify
- A failing test written before any implementation code
- The command to run the test with expected failure output
- The minimal implementation that makes the test pass
- A conventional commit message

No TBDs. No "the implementer will decide."

## Output Schema

`plan@1` — see `shared/schemas/plan@1.json`

## Next Stage

Feed `plan@1` to **lambda** (implementation).
