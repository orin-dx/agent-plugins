---
name: meta
description: >-
  Trigger this skill when the user asks to build a new plugin, create a plugin for a specific domain, scaffold a plugin directory, audit an existing plugin for conformance, check plugin conformance against ecosystem schemas, design a schema for inter-agent communication, add a new schema to shared/schemas/, write an agent for a given task, or create a skill for a new capability. Activate when the user wants to understand the correct plugin directory layout, plugin.json format, SKILL.md description writing conventions, the 4-part agent structure (backstory, goal, judgment, output), shared schema design rules, or the symlink setup for shared/. Also use when replacing or migrating agent-plugin-builder work. basis knows the full ecosystem conventions end-to-end and its output is a ready-to-install plugin directory.
version: 1.2.0
---

# basis — Meta-Plugin for Building Plugins

<overview>
basis accelerates plugin ecosystem growth by making the right way to build a plugin the easy way. It scaffolds compliant plugin directories, audits existing plugins for conformance, and designs inter-agent schema contracts following the authoring principles in shared/constitution.md and shared/agent-best-practices.md.
</overview>

---

<sub_skills>

| Sub-skill | Agent | Model | Effort | What it does |
| :--- | :--- | :--- | :--- | :--- |
| `basis/scaffold` | `scaffolder` | sonnet | medium | Generates a complete plugin directory — `plugin.json`, `skills/<id>/SKILL.md`, starter subagent files using the 4-part structure, and the `shared` symlink. Output is ready to install. |
| `basis/audit` | `auditor` | sonnet | medium | Audits an existing plugin directory against all ecosystem conformance rules; returns a structured pass/fail/warn report per check. |
| `basis/schema` | `schema-designer` | sonnet | medium | Designs a new JSON Schema (draft 2020-12) for an inter-agent artifact; checks for conflicts with existing schemas in shared/schemas/. |
| `basis/subagent` | — | sonnet | medium | Generates a single conformant subagent `.md` file using the 4-part structure for a given task description and model/effort tier. |

</sub_skills>

---

<key_conventions>

## Key Conventions to Enforce

### Pull Over Inject
Agents receive a workspace path and a goal. They discover what they need via tools. Inject only what the agent cannot pull: the goal, the output schema, and a few heuristics for where to look first.

### Goal Over Procedure
Subagent prompts express the desired outcome and how to verify it — not step-by-step scripts. `<execution_strategy>` provides heuristics, not recipes. If a prompt reads like a numbered tutorial, trim it until it reads like a mission brief.

### Minimum Viable Prompt
Body target: under 200 words. Role + goal + output shape + a few heuristics. Prompts over 300 words should be audited for procedure masquerading as guidance.

### Self-Contained Cross-Platform Prompts
No runtime references to `shared/` paths inside subagent bodies (except `shared/references/*.md` runtime resources). Prompts must run identically on Claude Code and AGY.

### Model and Effort Tiering
| Task class | Model | Effort |
|---|---|---|
| Mechanical — manifest building, file enumeration, schema validation | haiku | low |
| Analysis — finding bugs, cross-referencing, evaluating findings | sonnet | medium |
| Judgment — exit gate verdicts, architectural review, adversarial verification | opus | high |

### Reasoning Scratchpad
Every structured output includes `reasoning: string` — the agent's chain-of-thought. Never consumed downstream; present for debugging.

### Tool Count Limit
Design agents with 8–15 tools. Above 20 tools, selection accuracy degrades. Split wide agents into focused subagents with clean handoffs.

### Public Agent Description
Every subagent's YAML `description` is the public routing key. Write it for two audiences: concrete enough for LLM routing, accurate enough for human discovery.

</key_conventions>

---

<directory_layout>

## Required Plugin Directory Layout

```
plugins/<id>/
├── plugin.json                  # id, name, version, description, author, skills, agents
├── shared -> ../../shared       # symlink — never copy
├── skills/
│   └── <id>/
│       └── SKILL.md             # YAML frontmatter + body (sub-skills, conventions, dispatch)
└── agents/
    └── <agent-name>.md          # one file per agent declared in plugin.json
```

### Symlink Convention
```bash
cd plugins/<id> && ln -s ../../shared shared
```

Every plugin symlinks `shared` — it never copies or embeds shared content.

</directory_layout>
