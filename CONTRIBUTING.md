# Contributing

---

## Authoring a New Plugin

The fastest way to scaffold a new plugin is with the `basis` plugin:

```
"Create a plugin called <id> that does <goal>"
```

`scaffolder` generates the full directory structure, `plugin.json`, `SKILL.md`, and stub subagent files. Run `auditor` afterward to verify conformance.

To scaffold manually:

```bash
mkdir -p plugins/<id>/skills/<id> plugins/<id>/agents
ln -s ../../shared plugins/<id>/shared
```

Then create `plugin.json`, `skills/<id>/SKILL.md`, and `agents/*.md` following the conventions below.

---

## Plugin Structure

```
plugins/<id>/
├── plugin.json
├── README.md
├── CHANGELOG.md
├── skills/<id>/SKILL.md
└── agents/
    ├── <id>-scanner.md       (sonnet/medium — pattern matching)
    ├── <id>-worker.md        (sonnet/medium — analysis)
    ├── <id>-adversary.md     (opus/high — adversarial reasoning)
    └── <id>-exit-gate.md     (opus/high — final judgment)
```

Organize agents by **cognitive mode**, not pipeline position. A scan agent and an analysis agent require different mental modes — split them even if they run sequentially.

### `plugin.json`

```json
{
  "id": "my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "description": "One sentence.",
  "author": "Gabriel Castro (Orin DX)",
  "skills": ["my-plugin"],
  "agents": ["my-plugin-recon", "my-plugin-worker", "my-plugin-exit-gate"]
}
```

### `SKILL.md`

The skill prompt is what the user invokes. It should:
- Have a frontmatter `description` (80–200 words) explaining when to activate this skill
- Describe the agent pipeline: which subagents run in what order, and what each returns
- Reference shared schemas by name, not by file path

---

## Agent Authoring Checklist

Read `shared/agent-best-practices.md` before authoring. The hard requirements:

### 4-part structure (frontmatter + body)
- [ ] **Backstory** — 2–4 sentences. What has this agent been burned by? What does it value? Guides judgment without constraining method.
- [ ] **Goal** — what the agent must produce and why. Intent, not steps.
- [ ] **Judgment** — how to tell if the goal was genuinely achieved vs. output that merely looks like it was. Name the key failure mode.
- [ ] **Output** — structured shape; reference a schema from `shared/schemas/` when output flows to another agent.

No `<role>` section in the body — that's what `<backstory>` replaced. The frontmatter `role:` field is platform metadata (short display label for routing) and should be kept. No `success_criteria:` checklist. No filler: "your job is to", "make sure to", "please ensure".

### Progressive context loading
- [ ] Declares a `<load_first>` block naming the specific `shared/references/` file for this agent's phase
- [ ] Does not load reference files outside its cognitive mode (scanner loads hazards, not smells)

### EARS placement
- [ ] EARS notation (`WHEN`, `IF`, `WHILE`, `WHERE`) used only in output contracts and never-do rules
- [ ] No EARS in implementation steps, search strategies, or reasoning guidance

### Model and effort
- [ ] `haiku` / `low` — deterministic enumeration only (manifest building, file inventory)
- [ ] `sonnet` / `medium` — analysis (scanning, drafting, planning, tracing)
- [ ] `opus` / `high` — judgment (adversarial reasoning, exit gates, final verdicts)

### Tool language
- [ ] Uses abstract tool language: "use your file reading tool", "use your search tool"
- [ ] No tool-specific calls (`view_file`, `read_file`, `grep_search`, etc.)
- [ ] No absolute paths

### Schema conformance
- [ ] If the output is a named schema (e.g. `finding-report@1`), every field in the output shape is declared in `shared/schemas/` — no undeclared fields, no missing required fields

---

## Adding a Shared Schema

Shared schemas in `shared/schemas/` are the inter-plugin API. To add one:

1. Create `shared/schemas/<name>@<version>.json` using JSON Schema draft-2020-12
2. Set `additionalProperties: false`
3. Include a `reasoning: string` field
4. Document which plugin produces it and which consume it
5. **Never modify an existing versioned schema** — create `<name>@<version+1>.json` instead

---

## Registering in `marketplace.json`

Add an entry to the `"plugins"` array:

```json
{
  "id": "my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "path": "./plugins/my-plugin",
  "description": "One sentence description.",
  "category": "lifecycle"
}
```

---

## Engineering Invariants

1. **No absolute paths** — all paths in prompts and skill files must be relative
2. **Self-contained subagents** — each subagent prompt must be readable in isolation; no cross-subagent references
3. **Pull, don't inject** — subagents pull `shared/references/` files themselves; the host does not pre-load them
4. **No runtime references to `shared/agent-best-practices.md`** — authoring-time only
5. **Abstract tool language** — keeps prompts portable across Claude Code and AGY
6. **Conventional commits** — `feat:`, `fix:`, `docs:`, `refactor:`, `chore:` with plugin scope where applicable
7. **Clean writing** — no AI filler, no marketing language, no ALL CAPS except for genuine danger warnings

---

## Development Setup

```bash
git clone https://github.com/orin-axi/agent-plugins.git
cd agent-plugins

# Validate all plugin manifests
jq . marketplace.json > /dev/null
jq . plugins/*/plugin.json > /dev/null

# Check schema files parse correctly
jq . shared/schemas/*.json > /dev/null
```
