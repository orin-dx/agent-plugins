---
name: need
description: >-
  Trigger this skill when the user describes a need ("we need X", "the problem is Y", "users are asking for Z"), when they want to define or capture a requirement, when they ask what is in the backlog, or when they ask whether a need is already captured or addressed. Use when someone wants to structure a raw idea or pain point into a formal requirement before any spec or code is written. This skill transforms free-text need statements into structured requirement@1 artifacts containing: a one-sentence statement, stakeholder identification, the underlying why, testable done-when criteria, and explicit out-of-scope boundaries. Integrates with GitHub Issues by default — requirements are created as issues with a machine-readable requirement@1 block. Extensible: any issue tracker that produces the requirement@1 schema (Jira, Linear, Notion) can substitute as the backing store. Also activate for backlog audits, duplicate requirement detection, and coverage gap analysis against existing specs and implementation files.
version: "1.1.0"
---

# Graph — Need Definition Skill

<overview>
Graph is the requirement capture layer. It converts raw need statements into structured requirement@1 artifacts before anyone writes a spec or touches code. It coordinates three subagents across four sub-skills: intake, clarification, connection, and audit.
</overview>

---

<sub_skills>

| Sub-skill | Agent | Model | Effort | What it does |
| :--- | :--- | :--- | :--- | :--- |
| `graph/capture` | `intake` | sonnet | medium | Converts a free-text need into a requirement@1 draft — no questions asked, all inferred fields noted. |
| `graph/prioritize` | — | sonnet | medium | Ranks requirement@1 drafts by impact, urgency, and dependency order; returns an ordered list with rationale. |
| `graph/connect` | — | sonnet | medium | Links a requirement to related requirements, specs, or implementation files; surfaces dependencies and duplicates. |
| `graph/audit` | `auditor` | sonnet | medium | Cross-references all open requirements against specs, plans, and implementation files; identifies gaps, coverage, and duplicates. |

</sub_skills>

---

<output_schema>
All captured requirements conform to `requirement@1` (schema at `shared/schemas/requirement@1.json`).

Key fields:
- `statement` — one sentence describing the need
- `stakeholder` — who this serves
- `why` — the underlying pain or opportunity
- `done_when` — array of testable propositions, each confirmable true/false from the outside
- `out_of_scope` — explicit boundaries that prevent scope creep
</output_schema>

---

<extensibility>
Third parties using Jira, Linear, or another issue tracker can replace this plugin with one that reads from their tracker and emits the same requirement@1 schema. The downstream spec and implementation pipeline is agnostic to the backing store — it only consumes requirement@1.
</extensibility>
