# axiom — Verification Gate

**Stage:** Gate · **Output:** `verdict@1` · **Version:** 1.2.3

One skill, one three-agent pipeline, artifact-agnostic. Point axiom at a requirement, spec, plan, implementation, PR, changeset, or finding-report and it returns a binding `verdict@1` — pass or fail, with specific, actionable blockers on fail. Default disposition is **fail**: unverifiable criteria count as failures unless explicitly waived.

Axiom is standalone. Its `plugin.json` declares `consumes: []`, and nothing invokes it automatically. `canon`'s and `lambda`'s own exit-gate agents already implement the same recon → verify → judge discipline axiom formalizes, tailored to `spec@1` and `changeset@2` respectively — neither calls into axiom's agents. Install axiom when you want that same protocol available on demand against *any* artifact, including as an independent second opinion on top of canon's or lambda's own gate.

---

## When to Use

- You want to verify a spec, plan, or changeset against a defined set of criteria
- You want an independent second opinion on whether an implementation meets its spec
- You need a formal pass/fail verdict with specific blockers before shipping
- You want to check a finding report for completeness before handing it off

**Invoke with:** `"Gate this spec"`, `"Verify this implementation against the spec"`, `"Run the verification gate"`, `"Check whether this changeset meets all acceptance criteria"`, `"Is this finding report complete?"`

---

## How It Works

Axiom is a single skill (`axiom:axiom` — the frontmatter `name: gate` is a cosmetic label, not the routing key; skills route by directory name) — not a set of per-artifact-type sub-skills. The same three-agent chain runs unchanged no matter what you hand it; `recon` is what determines the artifact type and derives its criteria, so nothing about the pipeline itself needs to vary by type.

```mermaid
flowchart LR
    classDef source fill:#eef2ff,stroke:#6366f1,stroke-width:2px,color:#1e1b4b,rx:8px,ry:8px;
    classDef store fill:#f8fafc,stroke:#64748b,stroke-width:2px,color:#0f172a,rx:8px,ry:8px;
    classDef engine fill:#f5f3ff,stroke:#8b5cf6,stroke-width:2px,color:#4c1d95,rx:8px,ry:8px;
    classDef router fill:#fffbeb,stroke:#f59e0b,stroke-width:2px,color:#78350f,rx:8px,ry:8px;
    classDef output fill:#ecfdf5,stroke:#10b981,stroke-width:2px,color:#064e3b,rx:8px,ry:8px;

    Art[artifact + criteria] --> Recon["recon
    haiku / low"]
    Recon --> Ver["verifier
    sonnet / medium"]
    Ver --> Gate["exit-gate
    opus / high"]
    Gate --> Done(["verdict@1"])

    class Art source
    class Recon store
    class Ver engine
    class Gate router
    class Done output
```

Recon and verifier are deliberately separate: recon makes no judgments, verifier reports evidence without a verdict. Only `exit-gate` decides pass/fail — at the highest effort tier, to match the stakes.

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `recon` | Artifact Recon | haiku / low | Builds the verification manifest: artifact type, path, criteria to check, source files to read. No judgment. |
| `verifier` | Verifier | sonnet / medium | Reads each source file and classifies every criterion as `verified`, `failed`, or `unverifiable`. Neutral — reports evidence only, not verdicts. |
| `exit-gate` | Exit Gate | opus / high | Produces the final `verdict@1`. Default: fail. Unverifiable criteria are failures unless explicitly waived. |

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
| `artifact_type` | What was gated (spec, plan, changeset, finding-report, ...) |
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

Nothing invokes axiom automatically. **[canon](../canon/)** and **[lambda](../lambda/)** each run their own dedicated exit-gate agent following the same protocol axiom formalizes, not axiom itself. Install axiom to run that protocol standalone against any artifact — `spec@1` from canon, `changeset@2` from lambda — as an independent check alongside their own gates. **[delta](../delta/)** consumes `changeset@2` directly from lambda; wiring axiom's verdict into a shipping decision is a caller choice, not a declared dependency.
