# mason — Plugin Authoring

**Stage:** Meta · **Output:** conformant plugin directory · **Version:** 3.0.0

The tool for building tools. Scaffolds new plugins, audits existing ones for ecosystem conformance, and designs inter-agent JSON schema contracts. Output from `scaffolder` is a ready-to-install plugin directory — `plugin.json`, `SKILL.md`, stub subagents, and the `shared` symlink already wired.

---

## When to Use

- You want to build a new plugin and need the correct directory structure
- You've written a plugin and want to verify it conforms to ecosystem rules
- You need to design a new JSON schema for a new inter-agent artifact type
- You want to generate a single conformant subagent `.md` file for an existing plugin

**Invoke with:** `"Create a plugin called X that does Y"`, `"Audit the X plugin for conformance"`, `"Design a schema for an artifact that carries Z"`, `"Write a subagent for task T at opus/high tier"`

---

## Install

**Claude Code** — add the marketplace once, then install by ID:
```
/plugin marketplace add orin-dx/agent-plugins
/plugin install mason
```

**AGY** — installs the full repo; see the [root README](../../README.md#quick-start) for instructions.

---

## Skills

| Skill | What it does | Subagent |
| :--- | :--- | :--- |
| `mason/scaffold-plugin` | Generates a complete, ready-to-install plugin directory given a plugin ID and description | `scaffolder` |
| `mason/audit-plugin` | Audits an existing plugin directory against all ecosystem conformance rules; returns structured pass/fail/warn per check | `auditor` |
| `mason/design-schema` | Designs a new JSON Schema (draft 2020-12) for an inter-agent artifact; checks for conflicts with existing schemas | `schema-designer` |
| `mason/scaffold-subagent` | Generates a single conformant subagent `.md` file for an existing plugin — skips plugin.json/SKILL.md/symlink | `scaffolder` (single-subagent mode) |

`audit-plugin` is not bare `audit` — that word is already `ranger`'s plugin-level skill name (code/bug auditing). See `shared/constitution.md`'s Skill Names rule.

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `scaffolder` | Scaffolder | sonnet / medium | Generates a complete plugin directory: `plugin.json`, `SKILL.md`, stub subagents, `shared` symlink. |
| `auditor` | Conformance Auditor | sonnet / medium | Audits a plugin directory for ecosystem conformance across all required fields, structure rules, and authoring principles. |
| `schema-designer` | Schema Designer | sonnet / medium | Designs a new JSON Schema for a proposed inter-agent artifact; checks for conflicts with existing schemas. |

---

## Dispatch

Mason is not a linear pipeline — `scaffold-plugin` and `audit-plugin` are two independent entry points, each dispatching to its own subagent:

```mermaid
%%{init: {'flowchart': {'curve': 'basis', 'nodeSpacing': 36, 'rankSpacing': 56}}}%%
flowchart LR
    classDef skill fill:#f8fafc,stroke:#64748b,stroke-width:1.5px,color:#0f172a,rx:10,ry:10,font-size:14px,font-weight:600;
    classDef agent fill:#f5f3ff,stroke:#8b5cf6,stroke-width:1.5px,color:#4c1d95,rx:10,ry:10,font-size:13px,font-weight:500;

    SP["mason/scaffold-plugin"] --> SC["scaffolder"]
    AP["mason/audit-plugin"] --> AU["auditor"]

    class SP,AP skill
    class SC,AU agent
```

Neither path feeds the other — `scaffold-plugin` produces a new plugin directory, `audit-plugin` checks an existing one. `design-schema` and `scaffold-subagent` are narrower, on-demand skills not shown here.

---

## Conformance Checks (auditor)

The auditor checks all of the following. A plugin that fails any check is not ecosystem-conformant:

| Check | Rule |
| :--- | :--- |
| Manifest fields | `plugin.json` has all required fields: `id`, `name`, `version`, `description`, `author`, `skills`, `agents` — checked by running `scripts/check-versions.sh` and reading this plugin's own result, not re-derived |
| Skill file | `skills/<id>/SKILL.md` exists with valid YAML frontmatter and a `description` trigger string |
| Agent files | All agents listed in `plugin.json` have a corresponding `.md` file |
| Agent descriptions | 80–200 words each; start with "Delegate to this subagent when…" |
| 5-part body structure | Agent body has: constitution (byte-identical to the rest of the ecosystem), backstory, goal, judgment, output, in that order, with an optional `<load_first>` immediately after constitution — no success_criteria, no role sections, EARS only in constitution/output |
| `<load_first>` correctness | Present whenever an agent's goal implies a lookup it can't do from memory; its named reference file actually resolves |
| Orchestration completeness | Every status an agent's own output can emit has a routing entry in its plugin's SKILL.md, or is documented as terminal |
| Model/effort tiering | Mechanical → haiku/low; Analysis → sonnet/medium; Judgment → opus/high |
| `shared` symlink | Points to `../../shared` — never copied or embedded |
| No authoring-time refs | Neither agent bodies nor `SKILL.md` reference `shared/agent-best-practices.md` at runtime — except `mason`'s own scaffolding skills, whose job is authoring agents per that guide |
| Reference file size | Every `shared/references/*.md` file stays at or under 120 lines — checked via `scripts/check-reference-size.sh`, not re-derived |

---

## Directory Layout

Plugins produced by `scaffolder` follow this exact layout — one skill directory named after the plugin id, the default for a new plugin:

```
plugins/<id>/
├── plugin.json                  # id, name, version, description, author, skills, agents
├── shared -> ../../shared       # symlink — never copy
├── skills/
│   └── <id>/
│       └── SKILL.md             # YAML frontmatter + body
└── agents/
    └── <agent-name>.md          # one file per agent in plugin.json
```

If a plugin's scope later grows to cover several genuinely independent, heterogeneous intents on the same artifact — not a linear pipeline invoked as one flow — `skills/<id>/` may split into multiple directories, one per skill (`skills/<skill-name>/SKILL.md`), each still following the frontmatter and 5-part-body rules. `courier`, `scribe`, `weaver`, and `mason` itself are all examples.

`mason/audit-plugin` checks every `SKILL.md` found under `skills/`, not just one — it doesn't assume the single-directory default.

---

## Key Authoring Principles

mason enforces these conventions when scaffolding and auditing:

- **Pull over inject** — agents receive a workspace path and a goal; they discover what they need via tools
- **Goal over procedure** — prompts express the desired outcome, not step-by-step scripts
- **Minimum viable prompt** — body target under 200 words; role + goal + output shape + a few heuristics
- **Self-contained** — prompts run identically on Claude Code and AGY; no runtime references to `shared/` in bodies (except `shared/references/*.md` resources)

---

## References

- `shared/agent-best-practices.md` — full authoring checklist (mason authors use this; subagent bodies do not reference it at runtime)
- `shared/schemas/` — existing schemas to check against when designing a new one
