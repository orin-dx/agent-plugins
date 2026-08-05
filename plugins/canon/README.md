# canon — Specification

**Stage:** Spec · **Output:** `spec@1`

Drafts, audits, and gates unambiguous, testable specifications. A spec that exits canon can be handed to a developer who has never spoken to the product team and implemented without clarifying questions.

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `canon-drafter` | Drafter | sonnet/medium | Produces a `spec@1` from a `requirement@1` and optional `research-report@1`. No TBDs permitted. |
| `canon-auditor` | Auditor | sonnet/medium | Adversarially reviews the spec for vague criteria, missing error cases, and unverifiable claims. |
| `canon-verifier` | Drift Detector | sonnet/medium | Checks whether an existing spec still matches the current code — detects spec drift. |
| `canon-exit-gate` | Exit Gate | opus/high | Final pass/fail verdict before the spec enters planning. Default disposition: fail. |

## Pipeline

```
requirement@1 [+ research-report@1] → canon-drafter → canon-auditor → canon-exit-gate → spec@1
```

`canon-verifier` runs independently against an existing spec and codebase to detect drift.

## Gates

The exit gate enforces four conditions:
1. Every acceptance criterion is a testable proposition
2. No TBDs remain
3. Error cases have `is_error_case: true`
4. Scope fits a single planning cycle

On fail, blockers are returned to `canon-drafter` for targeted retry (max 3).

## Output Schema

`spec@1` — see `shared/schemas/spec@1.json`

Required: `id`, `purpose`, `scope`, `non_goals`, `acceptance_criteria`

## Next Stage

Feed `spec@1` to **vector** (planning) or run it through **axiom** for standalone verification.
