# Claude Code Guidelines (`CLAUDE.md`)

Quick reference guide for Claude Code CLI and Claude AI agents interacting with `orin-dx/agent-plugins`.

---

## 1. Quick Reference & Commands

- **Install Plugin in Claude Code**:
  ```bash
  claude plugin add orin-dx/agent-plugins/bug-hunter-rust
  claude plugin add orin-dx/agent-plugins/bug-hunter-ts
  ```
- **Install Plugin in AGY**:
  ```bash
  agy plugin add orin-dx/agent-plugins/bug-hunter-rust
  agy plugin add orin-dx/agent-plugins/bug-hunter-ts
  ```
- **Local Manifest Validation**:
  ```bash
  jq . marketplace.json > /dev/null
  jq . plugins/*/plugin.json > /dev/null
  ```

---

## 2. Authoring Guidelines & Single Source of Truth

All prompt engineering standards, CSO frontmatter specifications, and cross-platform CLI operational guidance are centralized in:

- [**`shared/agent-best-practices.md`**](./shared/agent-best-practices.md): Section 7 details the complete Antigravity (`agy`) vs Claude Code Operational Matrix.
- [**`AGENTS.md`**](./AGENTS.md): Repository standards and directory layout specification.

---

## 3. Directory Conventions

Ensure new plugins conform to the open format:

```text
plugins/<plugin-id>/
├── plugin.json                 <-- Plugin Manifest
├── skills/<plugin-id>/SKILL.md <-- Skill Definition
└── agents/*.md                 <-- Agent Prompt Files
```
