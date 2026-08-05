# axiom — Verification Gate

**Stage:** Gate · **Output:** `verdict@1`

A reusable, artifact-agnostic verification gate. Any artifact type (spec, plan, changeset, finding report) can be run through axiom. Produces a definitive `verdict@1` — pass or fail with specific, actionable blockers.

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `axiom-recon` | Artifact Recon | haiku/low | Builds the verification manifest: artifact path, criteria to check, source files to read. No judgment. |
| `axiom-verifier` | Verifier | sonnet/medium | Reads each source file and classifies every criterion as `verified`, `failed`, or `unverifiable`. Neutral — reports evidence, not verdicts. |
| `axiom-exit-gate` | Exit Gate | opus/high | Produces a final `verdict@1`. Default: fail. Unverifiable criteria are treated as failures unless explicitly waived. |

## Pipeline

```
artifact + criteria → axiom-recon → axiom-verifier → axiom-exit-gate → verdict@1
```

## Retry Protocol

On `fail`, the orchestrator returns the `blockers` array directly to the producing agent for a targeted patch (not a full regeneration). On retry 2, escalate to a higher-effort model. After 3 retries, escalate to the human.

`retry_count` is tracked in `verdict@1` and incremented by the exit gate on each pass.

## Output Schema

`verdict@1` — see `shared/schemas/verdict@1.json`

Fields: `verdict` (pass/fail), `confidence`, `blockers[]`, `verdict_summary` (≤300 chars), `artifact_type`, `retry_count`

## Usage

Axiom gates run automatically within `canon` (spec gate) and `lambda` (implementation gate). Run axiom standalone to gate any artifact outside the standard pipeline.
