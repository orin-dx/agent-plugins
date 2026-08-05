# lambda — Implementation

**Stage:** Code · **Output:** `changeset@1`

Executes implementation tasks from a `plan@1` using TDD. Each task is implemented by a fresh subagent with isolated context. An adversarial exit gate verifies the complete implementation before producing a `changeset@1`.

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `lambda-recon` | Workspace Recon | haiku/low | Discovers test runner, build tool, and baseline test state before any code is written. |
| `lambda-implementer` | Implementer | sonnet/medium | Executes one task: writes the failing test, implements the minimal code to pass, commits. |
| `lambda-reviewer` | Reviewer | sonnet/medium | Post-task code review — checks for missed sibling functions, severity of code quality issues, and regressions. |
| `lambda-exit-gate` | Exit Gate | opus/high | Adversarially verifies the complete implementation: all acceptance criteria implemented and tested, all tests pass, no regressions. |

## Pipeline

```
plan@1 → lambda-recon → [lambda-implementer → lambda-reviewer] × N tasks → lambda-exit-gate → changeset@1
```

Each task runs in a fresh `lambda-implementer` context. The reviewer runs after each task. The exit gate runs once after all tasks.

## TDD Cycle (per task)

1. Write failing test → confirm it fails
2. Write minimal implementation → confirm test passes
3. Run full test suite → confirm no regressions
4. Commit

## Output Schema

`changeset@1` — see `shared/schemas/changeset@1.json`

Required: `summary`, `files_changed`, `acceptance_criteria_met`

## Next Stage

Feed `changeset@1` to **axiom** (gate) and **delta** (ship).
