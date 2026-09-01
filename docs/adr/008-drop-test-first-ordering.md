# ADR-008: Drop mandatory write-test-first ordering in smith

**Status:** Accepted
**Date:** 2026-09-01

## Context

`smith` (formerly `lambda`) mandated a strict TDD cycle for every task: write the failing test, confirm it fails (red), write the minimal implementation, confirm it passes (green), commit. `navigator`'s `planner` encoded this into `plan@1` itself — every task specified "a failing test written before any implementation code" and "expected failure output" as required fields, and rejected any task not in that order.

The rationale for this ordering was that the red phase is the only moment you know a test would actually fail if the code were wrong — without it, a test could be written after the fact to match whatever the implementation happened to do, producing coverage numbers rather than evidence.

A controlled comparison of TDD-in-the-agent-loop versus non-TDD agent workflows (Birgitta Böckeler, ThoughtWorks, published on martinfowler.com, "TDD inside the agent loop — theater or actual value?") found:

- Agent-written code showed no discernible quality difference between TDD and non-TDD workflows when blind-judged by another model — non-TDD solutions were ranked as good or slightly better in most batches.
- TDD workflows used 2.96x–8.50x more tokens across small/medium/large tasks, with no corresponding benefit.
- Mutation scores — a harder, more direct signal of whether a test suite would catch a wrong implementation than pass/fail alone — showed no meaningful difference between TDD and non-TDD runs. Regression-catching capability was equal either way.
- The mechanism: "the TDD instructions actively work against \[an] up front design step. The design in those runs emerged from the sum of many locally-minimal decisions and was rarely revisited, so it tended to land on whatever shape the first test happened to lock in." Non-TDD runs "created the full design (architecture, data types, edge cases, contracts) before writing any code or tests."

The stated rationale for TDD's red phase — confidence, discipline, permission to relax — is a psychological effect for a human implementer. It does not obviously transfer to an agent, which has no fear to manage and no confidence to build. This repo's own `mutator` agent already runs mutation testing after every task, independent of write order — the finding above suggests that gate is what was actually verifying test quality all along, not the red-then-green sequence layered on top of it.

## Decision

`smith`'s `implementer` no longer requires a failing test to exist before implementation. The task cycle becomes: read the criteria, design the approach, write the implementation, write comprehensive tests proving each `covers_criteria` criterion, run the full suite, commit. Test quality is verified by `mutator`'s mutation-testing gate (unchanged) — a survived mutant is the concrete signal a test doesn't check what it claims to, regardless of which was written first.

`navigator`'s `planner` no longer requires "a failing test written before any implementation code" or "expected failure output" as task fields. A task now specifies a brief implementation approach (decided first, so tests prove a chosen design rather than accidentally locking one in), the exact implementation, and the exact tests proving its criteria — order between the latter two is not mandated.

This does not touch `mutator`, `reviewer`, or `exit-gate` — every downstream check ("does the full suite pass," "did mutation testing run," "is every criterion proven") is unchanged. It also does not touch bug-repair workflows elsewhere in the ecosystem where reproducing a failure before fixing it remains the right practice (see `shared/agent-best-practices.md`'s "Repair" cognitive mode) — that case has a clear causal reason for the ordering (proving the bug is real) that doesn't apply to fresh feature implementation from a spec.

This updates the "repair" cognitive mode's characterization in `docs/adr/003-cognitive-mode-separation.md` ("minimum change + red-green verification") for `implementer` specifically — that ADR is left as historical record rather than rewritten; this decision supersedes it for `smith`'s fresh-implementation case, not for genuine bug-repair workflows where reproduce-then-fix still applies.

## Consequences

Lower token cost per task (the Böckeler comparison suggests several times lower, though this repo has not run its own controlled comparison). Implementation approach is decided before any test exists to lock it in prematurely. The safety net that previously came from "the test failed first" now comes entirely from mutation testing — if a target workspace's mutation tool is unavailable, `mutator` already records this as a coverage gap rather than a hard block (pre-existing behavior), which means test-quality assurance is weaker in that specific case than it would be under strict TDD's red-phase guarantee; this is an accepted tradeoff, not an oversight. This change is based on one practitioner's controlled comparison, not a study of this ecosystem's own agents — if evidence emerges that this repo's tasks behave differently, this decision should be revisited the same way it was made: by measuring, not by argument.
