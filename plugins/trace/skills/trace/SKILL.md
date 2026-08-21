---
name: research
description: >-
  Activate when the user says "I need to understand X before deciding", "is there a way to do Y", "what are the options for Z", "research this", "investigate this", "what does the codebase already do for X", "prior art on Y", or "what are the risks of approach Z". Also activate when about to write a spec or plan and the approach is unclear, when checking what dependencies exist for a feature, or when any design question needs an evidence base before commitment. Trace investigates the question across internal sources (existing specs, docs, codebase patterns, manifests) and external sources as needed, then produces a research-report@1 that explicitly distinguishes confirmed findings from likely inferences from unverified assumptions. The report includes a falsifiable recommendation with an explicit confidence level so a spec writer (canon) can proceed without being surprised by implementation reality.
version: 1.2.1
---

# Trace Research Skill

<overview>
Trace builds a documented evidence base before committing to a solution direction. It separates what is known from what is assumed, surfaces contradictions, and delivers a recommendation a spec writer can act on directly.

One skill, one pipeline — not a menu of separately-invokable modes. `recon` maps sources (internal specs/docs/code, dependency manifests, external references), `reader` reads only what the map points at, `synthesizer` resolves the findings into one report, `risk-assessor` reviews the resulting approach. The pipeline narrows itself to what's asked: a question answerable from internal sources alone gets `scope: internal` from recon and never touches external search; a request for risk review of an already-decided approach can hand `risk-assessor` that approach directly.
</overview>

---

<language_agnostic_note>
Recon detects the workspace language from manifest files present (Cargo.toml → Rust, package.json → Node/TypeScript, pyproject.toml → Python, etc.), then loads the appropriate shared/references search heuristics for that ecosystem. The skill is not language-specific.
</language_agnostic_note>

---

<subagent_dispatch_matrix>

| Agent | Role | Model / Effort | Delegate When |
| :--- | :--- | :--- | :--- |
| **recon** | Source mapper | haiku / low | Start every research task here. Maps internal sources, external keywords, and existing implementations. |
| **reader** | Evidence extractor | sonnet / medium | Given the source map, reads each source and extracts findings with citations and confidence levels. |
| **synthesizer** | Recommendation producer | sonnet / medium | Given findings, synthesizes a research-report@1 with a falsifiable recommendation and confidence level. |
| **risk-assessor** | Risk prioritizer | sonnet / medium | Given a proposed approach or research-report@1, identifies and prioritizes technical risks with mitigations. |

</subagent_dispatch_matrix>

---

<output>
All research concludes in a `research-report@1` (schema: `shared/schemas/research-report@1.json`). The report distinguishes:
- **confirmed** — read directly from source
- **likely** — strong inference from evidence
- **assumed** — unverified, flagged explicitly

The recommendation is falsifiable: a spec or plan written from it will not be surprised by implementation reality.
</output>
