# Orin DX AI Agent & Skill Specification (`AGENTS.md`)

This guide defines the top-level repository guidelines for AI coding agents (Antigravity/AGY, Claude, Cursor, Copilot, Codex) working on or utilizing `orin-dx/agent-plugins`.

---

## 1. Authoring Standards & Single Source of Truth

To prevent rule duplication and context drift, all authoring principles, context engineering standards, and platform guides are centralized in `shared/`:

- [**`shared/agent-best-practices.md`**](./shared/agent-best-practices.md): Authoritative manual for Context Engineering, CSO trigger frontmatter (100–200 words), 3-tier progressive disclosure, dynamic tool discovery, 4-stage agentic loop (Explore ➔ Plan ➔ Code ➔ Verify), Superpowers subagent framework, and Google Antigravity (`agy`) vs Claude Code operational guidance.
- [**`shared/debugging-laws.md`**](./shared/debugging-laws.md): Core proof laws, read-only investigation rules, and Red-to-Green test verification standards.
- [**`shared/references/modern-cli-tools.md`**](./shared/references/modern-cli-tools.md): Global preference directive for modern CLI tools (`bat`, `zoxide`, `ripgrep`, `fd`, `eza`, `delta`, `jq`, `fzf`, `gh`).

---

## 2. Directory Layout Standard

```text
plugins/<plugin-id>/
├── plugin.json                 <-- Plugin Manifest
├── skills/
│   └── <plugin-id>/
│       ├── SKILL.md            <-- Primary Skill (CSO User Intent Frontmatter)
│       └── references/         <-- On-Demand Subdocuments (Tier 3)
└── agents/
    ├── <plugin>-scanner-<lang>.md   <-- Scanner Subagent (Superpowers Framework)
    ├── <plugin>-adversary-<lang>.md <-- Adversary Subagent (Superpowers Framework)
    ├── <plugin>-remediator-<lang>.md<-- Remediator Subagent (Superpowers Framework)
    └── <subagent-name>.md           <-- Additional Domain Subagents
```

---

## 3. Quick Checklist for Adding New Plugins

1. **CSO Triggers**: Write 100–200 word frontmatter descriptions (User Intent for Skills, Delegation Scenarios for Subagents).
2. **Progressive Disclosure**: Link to `shared/` context files via relative Markdown links.
3. **Non-Prescriptive Design**: Focus on goals, search patterns, and verification metrics rather than rigid step-by-step scripts.
4. **Manifest Registration**: Add plugin entry to root `marketplace.json` and validate syntax (`jq . marketplace.json`).
5. **Legal Attribution**: Set `"author": "Gabriel Castro (Orin DX)"` in `plugin.json`.
