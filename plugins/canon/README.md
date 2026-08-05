# canon — Specification

**Stage:** Spec · **Output:** `spec@1` · **Version:** 1.0.1

Drafts, audits, and gates unambiguous, testable specifications. A spec that exits canon can be handed to a developer who has never spoken to the product team and implemented without clarifying questions. An adversarial exit gate enforces this guarantee — default disposition is fail.

---

## When to Use

- You have a `requirement@1` (and optionally a `research-report@1`) and are ready to write a spec
- You want to check whether an existing spec still matches the current code (drift detection)
- You need a pass/fail gate on a spec before it enters planning
- You want to audit a spec for vague criteria, missing error cases, or unverifiable claims

**Invoke with:** `"Write a spec for this requirement"`, `"Draft a spec based on this research"`, `"Check whether this spec still matches the code"`, `"Gate this spec"`, `"Audit the spec for ambiguities"`

---

## Sub-skills

| Sub-skill | What it does |
| :--- | :--- |
| `canon/draft` | Drafts a `spec@1` from a `requirement@1` and optional `research-report@1` — no TBDs permitted |
| `canon/audit` | Adversarially reviews a spec for vague criteria, missing error cases, and unverifiable claims |
| `canon/verify` | Detects spec drift — checks whether an existing spec still matches the current code |
| `canon/gate` | Runs the exit gate to produce a formal pass/fail verdict before the spec enters planning |

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `canon-drafter` | Drafter | sonnet / medium | Produces a `spec@1` from a `requirement@1` and optional `research-report@1`. No TBDs permitted. |
| `canon-auditor` | Auditor | sonnet / medium | Adversarially reviews the spec for vague criteria, missing error cases, and unverifiable claims. |
| `canon-verifier` | Drift Detector | sonnet / medium | Checks whether an existing spec still matches the current code — detects spec drift. |
| `canon-exit-gate` | Exit Gate | opus / high | Final pass/fail verdict before the spec enters planning. Default disposition: fail. |

---

## Pipeline

```
requirement@1 [+ research-report@1] → canon-drafter → canon-auditor → canon-exit-gate → spec@1
```

`canon-verifier` runs independently against an existing spec and codebase to detect drift — it is not part of the main drafting pipeline.

---

## Exit Gate Conditions

The exit gate enforces four conditions. All must pass:

1. Every acceptance criterion is a testable proposition (binary true/false from outside the system)
2. No TBDs remain
3. Error cases are marked `is_error_case: true`
4. Scope fits a single planning cycle

On fail, specific blockers are returned to `canon-drafter` for targeted retry. Maximum 3 retries before escalation to a human.

---

## Output Schema

`spec@1` — see `shared/schemas/spec@1.json`

| Field | Required | Description |
| :--- | :--- | :--- |
| `id` | yes | Unique spec identifier |
| `purpose` | yes | One-sentence statement of what this spec accomplishes |
| `scope` | yes | What is in scope for this spec |
| `non_goals` | yes | Explicit list of what this spec does NOT cover |
| `acceptance_criteria` | yes | Array of testable propositions; each has `is_error_case` flag |
| `reasoning` | yes | Scratchpad — never forwarded downstream |

---

## Install

**Claude Code** — add the marketplace once, then install by ID:
```
/plugin marketplace add orin-dx/agent-plugins
/plugin install canon
```

**AGY** — installs the full repo; see the [root README](../../README.md#quick-start) for instructions.

---

## Next Stage

Feed `spec@1` to **[vector](../vector/)** (implementation planning) or run it through **[axiom](../axiom/)** for standalone verification against an existing implementation.
