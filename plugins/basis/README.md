# basis — Plugin Authoring

**Stage:** Meta · **Output:** conformant plugin directory · **Version:** 1.0.1

The tool for building tools. Scaffolds new plugins, audits existing ones for ecosystem conformance, and designs inter-agent JSON schema contracts. Output from `basis-scaffolder` is a ready-to-install plugin directory — `plugin.json`, `SKILL.md`, stub subagents, and the `shared` symlink already wired.

---

## When to Use

- You want to build a new plugin and need the correct directory structure
- You've written a plugin and want to verify it conforms to ecosystem rules
- You need to design a new JSON schema for a new inter-agent artifact type
- You want to generate a single conformant subagent `.md` file for an existing plugin

**Invoke with:** `"Create a plugin called X that does Y"`, `"Audit the X plugin for conformance"`, `"Design a schema for an artifact that carries Z"`, `"Write a subagent for task T at opus/high tier"`

---

## Sub-skills

| Sub-skill | What it does |
| :--- | :--- |
| `basis/scaffold` | Generates a complete, ready-to-install plugin directory given a plugin ID and description |
| `basis/audit` | Audits an existing plugin directory against all ecosystem conformance rules; returns structured pass/fail/warn per check |
| `basis/schema` | Designs a new JSON Schema (draft 2020-12) for an inter-agent artifact; checks for conflicts with existing schemas |
| `basis/subagent` | Generates a single conformant subagent `.md` file using the 4-part structure |

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `basis-scaffolder` | Scaffolder | sonnet / medium | Generates a complete plugin directory: `plugin.json`, `SKILL.md`, stub subagents, `shared` symlink. |
| `basis-auditor` | Conformance Auditor | sonnet / medium | Audits a plugin directory for ecosystem conformance across all required fields, structure rules, and authoring principles. |
| `basis-schema-designer` | Schema Designer | sonnet / medium | Designs a new JSON Schema for a proposed inter-agent artifact; checks for conflicts with existing schemas. |

---

## Conformance Checks (basis-auditor)

The auditor checks all of the following. A plugin that fails any check is not ecosystem-conformant:

| Check | Rule |
| :--- | :--- |
| Manifest fields | `plugin.json` has all required fields: `id`, `name`, `version`, `description`, `author`, `skills`, `agents` |
| Skill file | `skills/<id>/SKILL.md` exists with valid YAML frontmatter and a `description` trigger string |
| Agent files | All agents listed in `plugin.json` have a corresponding `.md` file |
| Agent descriptions | 80–200 words each; start with "Delegate to this subagent when…" |
| 4-part body structure | Agent body has exactly: backstory, goal, judgment, output — no success_criteria, no role sections, EARS only in output |
| Model/effort tiering | Mechanical → haiku/low; Analysis → sonnet/medium; Judgment → opus/high |
| `shared` symlink | Points to `../../shared` — never copied or embedded |
| No authoring-time refs | Agent bodies do not reference `shared/agent-best-practices.md` at runtime |

---

## Directory Layout

Plugins produced by `basis-scaffolder` follow this exact layout:

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

---

## Key Authoring Principles

basis enforces these conventions when scaffolding and auditing:

- **Pull over inject** — agents receive a workspace path and a goal; they discover what they need via tools
- **Goal over procedure** — prompts express the desired outcome, not step-by-step scripts
- **Minimum viable prompt** — body target under 200 words; role + goal + output shape + a few heuristics
- **Self-contained** — prompts run identically on Claude Code and AGY; no runtime references to `shared/` in bodies (except `shared/references/*.md` resources)

---

## References

- `shared/agent-best-practices.md` — full authoring checklist (basis authors use this; subagent bodies do not reference it at runtime)
- `shared/schemas/` — existing schemas to check against when designing a new one

---

## Install

**Claude Code** — add the marketplace once, then install by ID:
```
/plugin marketplace add orin-dx/agent-plugins
/plugin install basis
```

**AGY** — installs the full repo; see the [root README](../../README.md#quick-start) for instructions.
