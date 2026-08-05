# Contributing

---

## Authoring a New Plugin

The fastest way to scaffold a new plugin is with the `basis` plugin:

```
"Create a plugin called <id> that does <goal>"
```

`basis-scaffolder` generates the full directory structure, `plugin.json`, `SKILL.md`, and stub subagent files. Run `basis-auditor` afterward to verify conformance.

To scaffold manually:

```bash
mkdir -p plugins/<id>/skills/<id> plugins/<id>/subagents
ln -s ../../shared plugins/<id>/shared
```

Then create `plugin.json`, `skills/<id>/SKILL.md`, and `subagents/*.md` following the conventions below.

---

## Plugin Structure

```
plugins/<id>/
├── plugin.json
├── README.md
├── skills/<id>/SKILL.md
├── subagents/
│   ├── <id>-recon.md       (haiku/low — mechanical recon)
│   ├── <id>-worker.md      (sonnet/medium — analysis)
│   └── <id>-exit-gate.md   (opus/high — judgment)
└── shared -> ../../shared
```

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

## Subagent Authoring Checklist (Section 9)

Read `shared/agent-best-practices.md` Section 9 before authoring. The hard requirements:

### Description field (YAML frontmatter)
- [ ] Starts with `"Delegate to this subagent when…"`
- [ ] 80–200 words
- [ ] Covers: routing condition, expected input, what it returns, key behavioral constraints

### Body (below the closing `---`)
- [ ] Under 200 words
- [ ] Begins with the goal — what the agent must produce
- [ ] Includes a compact JSON output example with every field named
- [ ] Marks `reasoning` as scratchpad: "not forwarded downstream"
- [ ] No `<context>` or `<role>` sections that restate the description
- [ ] No filler phrases: "your job is to", "make sure to", "please ensure"

### Model and effort
- [ ] `haiku` / `low` — deterministic enumeration only (manifest building, file inventory)
- [ ] `sonnet` / `medium` — analysis (scanning, drafting, planning, reviewing)
- [ ] `opus` / `high` — judgment (exit gates, adversarial review, final verdicts)

### Tool language
- [ ] Uses abstract tool language: "use your file reading tool", "use your search tool"
- [ ] No tool-specific calls (`view_file`, `read_file`, `grep_search`, etc.)
- [ ] No absolute paths

### Schema conformance
- [ ] If the output is a named schema (e.g. `spec@1`), the inline JSON shape matches the schema in `shared/schemas/` exactly — no undeclared fields, no missing required fields
- [ ] `additionalProperties: false` schemas: verify every field in the output shape is declared in the schema

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
