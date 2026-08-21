# Claude Code Guidelines (`CLAUDE.md`)

Quick reference guide for Claude Code CLI and Claude AI agents interacting with `orin-dx/agent-plugins`.

---

## 1. Quick Reference & Commands

- **Install Plugin in Claude Code**:
  ```bash
  claude plugin add orin-dx/agent-plugins/proof
  claude plugin add orin-dx/agent-plugins/basis
  ```
- **Install Plugin in AGY**:
  ```bash
  agy plugin add orin-dx/agent-plugins/proof
  agy plugin add orin-dx/agent-plugins/basis
  ```
- **Local Manifest Validation**:
  ```bash
  jq . marketplace.json > /dev/null
  jq . plugins/*/plugin.json > /dev/null
  ```
- **Mermaid Diagram Validation** (run after touching any mermaid-fenced block — a syntax error still reads as valid markdown, only an actual render catches it):
  ```bash
  ./scripts/check-mermaid.sh
  ```
- **Version Consistency** (run after any version bump — checks `plugin.json`, README, CHANGELOG, and `marketplace.json` agree):
  ```bash
  ./scripts/check-versions.sh
  ```
- **Skill Doc Accuracy** (run after adding/removing/renaming a skill directory — checks every skill a README's table documents actually exists):
  ```bash
  ./scripts/check-skills-doc.sh
  ```

---

## 2. Authoring Guidelines & Single Source of Truth

All authoring rules and principles are centralized in:

- [**`shared/constitution.md`**](./shared/constitution.md): EARS-format authoritative rules — the fence all plugin development must stay inside. Read this first.
- [**`shared/agent-best-practices.md`**](./shared/agent-best-practices.md): Principles behind the constitution with examples — 4-part agent structure, EARS placement, cognitive modes, schema-driven handoffs, model/effort tiers.
- [**`AGENTS.md`**](./AGENTS.md): Repository standards, directory layout, and new-plugin checklist.

---

## 3. Directory Conventions

Ensure new plugins conform to the open format:

```text
plugins/<plugin-id>/
├── plugin.json                 <-- Plugin Manifest
├── skills/<plugin-id>/SKILL.md <-- Skill Definition
└── agents/*.md                 <-- Agent Prompt Files
```
