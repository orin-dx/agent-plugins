# trace — Research Synthesis

**Stage:** Research · **Output:** `research-report@1` · **Version:** 1.0.1

Surveys prior art, existing implementations, and technical risks before a spec is written. Reads internal code, docs, and external sources, then synthesizes findings into a confidence-classified research report. The adversarial risk assessor reviews the proposed approach before any spec is committed to.

---

## When to Use

- You have a requirement and want to understand the technical landscape before designing a solution
- You suspect there are existing patterns in the codebase worth reusing
- You want a risk assessment of a proposed approach before anyone writes code
- The domain is unfamiliar and you need a structured prior art survey

**Invoke with:** `"Research how X is typically implemented"`, `"Survey the codebase for existing patterns related to Y"`, `"What are the risks of approach Z"`, `"Run trace on this requirement"`

---

## Sub-skills

| Sub-skill | What it does |
| :--- | :--- |
| `trace/survey` | Full pipeline — maps sources, reads them, synthesizes findings, assesses risks |
| `trace/scan` | Targeted scan of a specific source type (internal code, docs, or external references) |
| `trace/risk` | Adversarial risk assessment of a proposed approach without a full research sweep |

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `recon` | Source Mapper | haiku / low | Maps available sources — internal code, docs, and external search terms — without reading them. No content analysis. |
| `reader` | Source Reader | sonnet / medium | Reads each source identified by recon and extracts relevant findings with confidence classification. |
| `synthesizer` | Synthesizer | sonnet / medium | Aggregates findings across all sources into a coherent `research-report@1`. Resolves contradictions and notes open questions. |
| `risk-assessor` | Risk Assessor | sonnet / medium | Reviews the proposed approach for technical risks before the spec is written. Surfaces risks neutrally without recommending whether to proceed. |

---

## Pipeline

```
requirement@1 → recon → reader → synthesizer → risk-assessor → research-report@1
```

Recon runs first and maps all sources before any reading begins. Reader and synthesizer are separate to keep source extraction honest — synthesizer cannot retroactively shape what was read. Risk assessor runs last with full context.

---

## Output Schema

`research-report@1` — see `shared/schemas/research-report@1.json`

Each finding is classified as one of:

| Confidence | Meaning |
| :--- | :--- |
| `confirmed` | Directly verified in source — code or authoritative doc read |
| `likely` | Strong inference from multiple sources, no direct verification |
| `assumed` | Reasonable assumption; no source found — flagged for follow-up |

The risk assessor appends a `risks` section: each risk has a description, likelihood, and suggested mitigation.

---

## Install

**Claude Code** — add the marketplace once, then install by ID:
```
/plugin marketplace add orin-dx/agent-plugins
/plugin install trace
```

**AGY** — installs the full repo; see the [root README](../../README.md#quick-start) for instructions.

---

## Next Stage

Feed `research-report@1` alongside `requirement@1` to **[canon](../canon/)** (spec drafting).
