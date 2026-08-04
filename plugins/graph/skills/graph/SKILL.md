---
name: graph
description: >-
  Trigger this skill when the user describes a need ("we need X", "the problem is Y", "users are asking for Z"), when they want to define or capture a requirement, when they ask what is in the backlog, or when they ask whether a need is already captured or addressed. Use when someone wants to structure a raw idea or pain point into a formal requirement before any spec or code is written. This skill transforms free-text need statements into structured requirement@1 artifacts containing: a one-sentence statement, stakeholder identification, the underlying why, testable done-when criteria, and explicit out-of-scope boundaries. Integrates with GitHub Issues by default — requirements are created as issues with a machine-readable requirement@1 block. Extensible: any issue tracker that produces the requirement@1 schema (Jira, Linear, Notion) can substitute as the backing store. Also activate for backlog audits, duplicate requirement detection, and coverage gap analysis against existing specs and implementation files.
version: "1.0.0"
---

# Graph — Need Definition Skill

<overview>
Graph is the requirement capture layer. It converts raw need statements into structured requirement@1 artifacts before anyone writes a spec or touches code. It coordinates three subagents across four sub-skills: intake, clarification, connection, and audit.
</overview>

---

<sub_skills>

### graph/capture
Convert a free-text need statement into a requirement@1 draft. Delegates to `graph-intake`, which fills in statement, stakeholder, why, and done_when from context alone — without asking questions.

### graph/prioritize
Given a set of requirement@1 drafts, rank them by impact, urgency, and dependency order. Returns an ordered list with brief rationale for each position.

### graph/connect
Link a requirement to related requirements, specs, or implementation files already in the workspace. Surfaces dependencies, blockers, and duplicates before the requirement enters the backlog.

### graph/audit
Cross-reference all open requirements against existing specs, plans, and implementation files. Delegates to `graph-auditor` to identify gaps (requirements with no spec), coverage (requirements with matching implementation), and duplicates. Returns a structured audit report.

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

<success_criteria>
A requirement is complete when a downstream spec writer can read it and produce an accurate, unambiguous spec without asking any clarifying questions.
</success_criteria>

---

<extensibility>
Third parties using Jira, Linear, or another issue tracker can replace this plugin with one that reads from their tracker and emits the same requirement@1 schema. The downstream spec and implementation pipeline is agnostic to the backing store — it only consumes requirement@1.
</extensibility>
