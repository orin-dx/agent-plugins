# Orin DX AI Agent & Skill Specification (`AGENTS.md`)

This guide defines the top-level repository guidelines for AI coding agents (Claude Code, AGY, Cursor, Copilot, Codex) working on or utilizing `orin-dx/agent-plugins`.

---

## 1. Authoritative Sources

All hard rules for plugin and agent authoring live in one place:

- [**`shared/constitution.md`**](./shared/constitution.md): EARS-format authoritative constraints. The fence all plugin development must stay inside. Read this first and last.
- [**`shared/agent-best-practices.md`**](./shared/agent-best-practices.md): Principles behind the constitution, explained with examples. Authoring-time only — never loaded by agents at runtime.
- [**`shared/debugging-laws.md`**](./shared/debugging-laws.md): Core proof laws, read-only investigation rules, Red-to-Green verification standards.
- [**`shared/references/modern-cli-tools.md`**](./shared/references/modern-cli-tools.md): Global preference directive for modern CLI tools (`bat`, `zoxide`, `ripgrep`, `fd`, `eza`, `delta`, `jq`, `fzf`, `gh`).

---

## 2. Directory Layout Standard

```text
plugins/<plugin-id>/
├── plugin.json                   <-- Plugin Manifest (id, version, skills, agents)
├── README.md                     <-- Purpose, trigger phrases, agent table, install
├── CHANGELOG.md                  <-- Semver history
├── skills/
│   └── <plugin-id>/
│       └── SKILL.md              <-- Skill definition (dispatch matrix, pipeline)
└── agents/
    ├── recon.md                  <-- haiku/low  — deterministic enumeration
    ├── scanner.md                <-- sonnet/med — pattern matching
    ├── adversary.md              <-- sonnet/med — adversarial verification
    └── exit-gate.md              <-- opus/high  — binding judgment
```

Agents are organized by **cognitive mode** (enumeration, tracing, adversarial, systemic, behavioral, judgment, repair) — not by pipeline position. See `shared/constitution.md` for the model/effort tier rules.

---

## 3. Quick Checklist for Adding New Plugins

1. **Use `basis`** — run `scaffolder` to generate the full directory structure and stubs.
2. **4-part agent structure** — every agent body: `<backstory>`, `<goal>`, `<judgment>`, `<output>`. No `<role>` body sections. No `success_criteria` checklists.
3. **EARS in output only** — WHEN/IF/WHILE/WHERE notation belongs only in `<output>` contracts and never-do rules.
4. **Progressive context loading** — one `<load_first>` block per agent, naming only the reference file for its cognitive phase.
5. **Schema-first handoffs** — define `shared/schemas/<name>@<version>.json` before writing the agent that produces it.
6. **Abstract tool language** — "use your file reading tool", never `view_file`, `read_file`, or `Bash tool`.
7. **Manifest registration** — add an entry to root `marketplace.json` and validate: `jq . marketplace.json`.
8. **Legal attribution** — set `"author": "Gabriel Castro (Orin DX)"` in `plugin.json`.
