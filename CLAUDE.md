# Claude Code Guidelines (`CLAUDE.md`)

This guide provides instructions for Claude Code CLI and Claude AI agents interacting with the `orin-dx/agent-plugins` repository.

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
- **Local Dev Copy**:
  ```bash
  # Copy to local AGY plugin directory
  cp -r plugins/bug-hunter-rust ~/.gemini/config/plugins/
  # Copy to local Claude plugin directory
  cp -r plugins/bug-hunter-rust ~/.claude/plugins/
  ```

---

## 2. Directory Layout Standard

Claude Code and AGY both parse the open Agent Plugin format. Ensure directory layouts adhere to:

```text
plugins/<plugin-id>/
├── plugin.json                 <-- Plugin Manifest (JSON)
├── skills/
│   └── <plugin-id>/
│       └── SKILL.md            <-- Primary Skill Definition
└── subagents/
    ├── <plugin-id>-scanner.md  <-- Scanner Subagent Prompt
    ├── <plugin-id>-adversary.md<-- Adversary Subagent Prompt
    └── <plugin-id>-remediator.md<-- Remediator Subagent Prompt
```

---

## 3. Skill & Subagent Authoring Rules

- **Cross-Platform Compatibility**: See Section 7 of [**`shared/agent-best-practices.md`**](./shared/agent-best-practices.md) for full Antigravity (`agy`) vs Claude Code operational guidance.
- **`plugin.json` Manifest**: Must include `"id"`, `"name"`, `"version"`, `"description"`, `"skills": [...]`, and `"agents": [...]`.
- **`SKILL.md` Frontmatter (CSO User Intent Focus)**: Must include 100–200 word CSO description focused on user intent, request phrasing, adjacent domains, and boundary edge cases.
- **Subagent Prompts (`.md`)**: Must follow the Superpowers 5-Section Framework (`<context>`, `<role>`, `<goal>`, `<execution_strategy>`, `<success_criteria>`). Frontmatter must include 100–200 word CSO description focused on delegation scenarios.

---

## 4. Git Workflow & Quality Checks

- Always update `marketplace.json` when adding or updating a plugin.
- Validate JSON files (`marketplace.json`, `plugin.json`) with `jq` before committing:
  ```bash
  jq . marketplace.json > /dev/null
  ```
- Commit messages follow Conventional Commits format (`feat: ...`, `fix: ...`, `docs: ...`).
