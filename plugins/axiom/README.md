# axiom — Verification Gate

**Stage:** Gate · **Output:** `verdict@1` · **Version:** 1.0.1

A reusable, artifact-agnostic verification gate. Any artifact — spec, plan, changeset, finding report — can be run through axiom. Produces a definitive `verdict@1` with a pass/fail decision and specific, actionable blockers. Default disposition is **fail**; unverifiable criteria are treated as failures unless explicitly waived.

Axiom is standalone — its `plugin.json` declares `consumes: []`, and nothing invokes its agents automatically. `exit-gate` and `exit-gate` are separate, dedicated agents that independently implement the same recon → verify → judge discipline axiom formalizes, tailored to `spec@1` and `changeset@1` respectively; neither calls into axiom's actual agents. Install axiom when you want that same protocol available on demand against any artifact — including as an independent second-opinion pass on top of canon's or lambda's own gate.

---

## When to Use

- You want to verify a spec, plan, or changeset against a defined set of criteria
- You want an independent second opinion on whether an implementation meets its spec
- You need a formal pass/fail verdict with specific blockers before shipping
- You want to check a finding report for completeness before handing it off

**Invoke with:** `"Gate this spec"`, `"Verify this implementation against the spec"`, `"Run the verification gate"`, `"Check whether this changeset meets all acceptance criteria"`, `"Is this finding report complete?"`

---

## Sub-skills

| Sub-skill | What it does |
| :--- | :--- |
| `axiom/gate` | Full pipeline — builds manifest, verifies each criterion, produces verdict |
| `axiom/verify` | Standalone criterion verification against a specific artifact and source file set |

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `recon` | Artifact Recon | haiku / low | Builds the verification manifest: artifact path, criteria to check, source files to read. No judgment. |
| `verifier` | Verifier | sonnet / medium | Reads each source file and classifies every criterion as `verified`, `failed`, or `unverifiable`. Neutral — reports evidence only, not verdicts. |
| `exit-gate` | Exit Gate | opus / high | Produces a final `verdict@1`. Default: fail. Unverifiable criteria are failures unless explicitly waived. |

---

## Pipeline

```
artifact + criteria → recon → verifier → exit-gate → verdict@1
```

Recon and verifier are deliberately separate: recon makes no judgments, verifier reports evidence without a verdict. Only the exit gate decides pass/fail — with higher model effort to match the stakes.

---

## Retry Protocol

On `fail`, the orchestrator returns the `blockers` array directly to the producing agent for a **targeted patch** — not a full regeneration. On retry 2, escalate to a higher-effort model. After 3 retries, escalate to the human.

`retry_count` is tracked in `verdict@1` and incremented by the exit gate on each pass.

---

## Output Schema

`verdict@1` — see `shared/schemas/verdict@1.json`

| Field | Description |
| :--- | :--- |
| `verdict` | `pass` or `fail` |
| `confidence` | Gate's confidence in the verdict |
| `blockers` | Array of specific, actionable failures — each maps to a criterion |
| `verdict_summary` | Human-readable summary (≤300 chars) |
| `artifact_type` | What was gated (spec, plan, changeset, finding-report) |
| `retry_count` | Number of times this artifact has been through the gate |

---

## Install

**Claude Code** — add the marketplace once, then install by ID:
```
/plugin marketplace add orin-dx/agent-plugins
/plugin install axiom
```

**AGY** — installs the full repo; see the [root README](../../README.md#quick-start) for instructions.

---

## Used By

Axiom is not invoked by any other plugin — **[canon](../canon/)** and **[lambda](../lambda/)** each run their own dedicated exit-gate agent following the same protocol axiom formalizes, not axiom itself. Install axiom to run that protocol standalone against any artifact, including `spec@1` from canon or `changeset@1` from lambda, as an independent check alongside their own gates. Nothing in the pipeline consumes axiom's `verdict@1` automatically — **[delta](../delta/)** consumes `changeset@1` directly from lambda; wiring axiom's verdict into a shipping decision is a caller choice, not a declared dependency.
