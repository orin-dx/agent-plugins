# ADR-009: Implementer may adapt the plan's code shape; task sizing is by compilation boundary, not clock time

**Status:** Accepted
**Date:** 2026-09-01

## Context

Two related over-prescription patterns were identified on review:

1. `navigator`'s `planner` required "the exact implementation code" for every task, and `smith`'s `implementer` had no stated latitude to deviate from it — the plan effectively pre-decided the code's shape before the implementer, the agent with the most direct context on the actual codebase state at execution time, ever engaged. This is the same failure mode ADR-008 identified and fixed for test-write ordering (forcing a specific artifact into existence too early locks in a shape that is rarely revisited), applied one level higher in the pipeline, at a larger scale — a locked-in test is one assertion; locked-in "exact code" is the entire task. `navigator`'s own `challenger` already checks for a narrower version of this ("steps so rigid they leave no room to adapt" — its example is dictating private variable names), which shows the architecture already recognized over-prescription as a real failure mode, just scoped too narrowly to catch the structural version of it.

2. `planner` capped every task at "under fifteen minutes." `shared/agent-best-practices.md`'s own Subsystem Compilation Batching rule already argues against exactly this: "decompose plans by transactional crate/package compilation boundaries rather than arbitrary 15-minute intervals." The two rules were in direct tension. A clock-time estimate is also a human-ergonomics measure (a natural break point in a human working session) with no clear meaning for an agent that doesn't work in wall-clock sessions — the same category of mismatch ADR-008 found in TDD's red phase (a ritual calibrated to human psychology, not to what actually produces good agent output).

## Decision

**Implementer shape latitude:** `planner`'s exact implementation code is now explicitly a concrete baseline — proof that the task is achievable within its stated file targets and scope — not a transcript `implementer` must copy verbatim. `implementer` may use a better-shaped approach at execution time, provided it still satisfies the same file targets, `covers_criteria`, and tests the plan specified. Any such deviation is recorded in the `concerns` field, not silently applied and not silently withheld. The boundary is explicit: deviation is about implementation *shape* (how), never about *scope* (what) — a plan whose scope looks wrong is a `spec_contradiction` or `needs_architecture` case, not a quiet rewrite.

**Task sizing by compilation boundary, not clock time:** `planner` no longer sizes tasks by an estimated duration. A task must be one independently reviewable unit of change, sized to its Subsystem Batch's compilation boundary — the same criterion `agent-best-practices.md` already prescribed for batching, now applied consistently to task sizing itself rather than existing as a second, conflicting sizing rule.

## Consequences

`planner`'s plans remain fully concrete (no TBDs, no "implement as appropriate") — that discipline is unchanged and still exists for the same reason it always did: an unambiguous plan is what `challenger` can adversarially review and what prevents the original failure mode of implementer-invented scope decisions conflicting with the spec. What changes is narrower: the plan's code is a baseline whose *shape* is negotiable at execution time, while its *scope* (files, criteria, tests) remains binding. This does put more trust in `implementer`'s judgment than before — the countervailing control is that any deviation must be logged in `concerns`, giving `reviewer` and `exit-gate` a visible trail rather than an invisible one. Task sizing now has one consistent criterion (compilation-boundary cohesion) instead of two potentially conflicting ones (a batching rule and a per-task clock estimate), removing a standing inconsistency between `shared/agent-best-practices.md` and `navigator/agents/planner.md`.
