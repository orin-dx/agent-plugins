# trace — Research Synthesis

**Stage:** Research · **Output:** `research-report@1`

Surveys prior art, existing implementations, and technical risks before a spec is written. Produces a structured research report with confidence-classified findings.

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `trace-recon` | Source Mapper | haiku/low | Maps available sources — internal code, docs, and external search terms — without reading them. No content analysis. |
| `trace-reader` | Source Reader | sonnet/medium | Reads each source identified by recon and extracts relevant findings with confidence classification. |
| `trace-synthesizer` | Synthesizer | sonnet/medium | Aggregates findings across all sources into a coherent `research-report@1`. Resolves contradictions and notes open questions. |
| `trace-risk-assessor` | Risk Assessor | opus/high | Adversarially reviews the proposed approach for technical risks before the spec is written. |

## Pipeline

```
requirement@1 → trace-recon → trace-reader → trace-synthesizer → trace-risk-assessor → research-report@1
```

## Output Schema

`research-report@1` — see `shared/schemas/research-report@1.json`

Each finding is classified as `confirmed`, `likely`, or `assumed`. The risk assessor adds a `risks` section.

## Next Stage

Feed `research-report@1` alongside the `requirement@1` to **canon** (spec drafting).
