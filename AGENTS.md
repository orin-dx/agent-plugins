# Orin DX Agent Plugins Guidelines (`AGENTS.md`)

This guide provides architectural rules, engineering invariants, and contribution workflows for AI coding agents (Antigravity/AGY, Claude, Cursor, Copilot, Codex) working on or utilizing the `orin-dx/agent-plugins` repository.

---

## 1. Repository Purpose & Architecture

`orin-dx/agent-plugins` is the central, universal AI Agent Plugin & Skill Marketplace for Orin DX. It provides modular, self-contained plugins for language-specific bug hunting, code quality auditing, and multi-agent orchestration across **Antigravity (AGY)** and **Claude Code**.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   AGENT PLUGINS MARKETPLACE ARCHITECTURE               │
├───────────────────┬────────────────────────────────────────────────────┤
│ COMPONENT         │ PURPOSE                                            │
├───────────────────┼────────────────────────────────────────────────────┤
│ marketplace.json  │ Global marketplace index listing available plugins │
├───────────────────┼────────────────────────────────────────────────────┤
│ shared/           │ Universal debugging laws & evaluation standards    │
│                   │ (Not plugins themselves; referenced on-demand)     │
├───────────────────┼────────────────────────────────────────────────────┤
│ plugins/          │ Language-specific, self-contained plugins          │
│ ├── bug-hunter-rust│ (6 Rust Hazard Taxonomies & Rust Subagents)       │
│ └── bug-hunter-ts │ (6 TS Hazard Taxonomies & TS Subagents)           │
└───────────────────┴────────────────────────────────────────────────────┘
```

---

## 2. Core Architectural Invariants

Agents modifying or adding plugins in this repository MUST enforce the following 5 invariants:

### 1. Self-Contained Language Scoping
- Language plugins MUST remain strictly self-contained under `plugins/<plugin-name>/`.
- Do NOT mix rules for multiple languages into a single plugin. Rust hazard rules belong in `bug-hunter-rust`, TypeScript hazard rules belong in `bug-hunter-ts`.
- Keep plugin prompt footprints token-lean (~1,200 to 1,800 tokens max per skill).

### 2. On-Demand Shared Context References
- Shared rules (like core debugging principles or evaluation report templates) live in `shared/` at the root of the repository.
- Plugins reference shared context using relative Markdown links (e.g. `[General Debugging Laws](../../../shared/debugging-laws.md)`). Agents inspect shared files via `view_file` on demand during an audit.

### 3. Red-to-Green Verification Law
- All remediation subagents (`bug-hunter-remediator-*`) MUST follow the **Red-to-Green Law**:
  > Write a failing regression unit/integration test first (red), apply the code fix, and verify all tests pass cleanly (green).

### 4. Hazard-Taxonomy Subagent Partitioning
- Multi-agent bug hunts MUST partition subagents by **Hazard Category** across the target codebase:
  - **Scanner Subagents**: Discarded parameters, unused CLI flags, silent `unwrap_or` defaults.
  - **Adversary Subagents**: Fixpoint solver staleness, graph cascade re-enqueueing, spec compliance drift.
  - **Remediator Subagents**: Boundary inputs (UTF-8 BOM, CRLF), file I/O `.flush()`/`.sync_all()`, subprocess parameter escaping.

### 5. Superpowers 5-Section Subagent Structure
All subagent prompt definitions (`.md`) MUST be structured into 5 goal-driven sections inspired by `obra/superpowers`:
1. **Context**: Workspace state, tech stack, and background environment.
2. **Role**: Specialized persona (e.g. `Static & Regex Hazard Scanner`, `Adversarial Verifier`).
3. **Goal**: Singular, outcome-focused objective.
4. **Execution Rules & Strategy**: High-efficiency search heuristics and evaluation guidelines.
5. **Success Criteria**: Explicit, verifiable checklist of conditions required for task completion.

### 6. Clean Technical Style (No Emoji Directive)
- Plugin descriptions, subagent prompts, skills, and documentation MUST remain clean, technical, scannable, and devoid of emojis or AI bot filler phrases.

---

## 3. Authoring a New Plugin

To add a new language plugin (e.g. `bug-hunter-python` or `bug-hunter-go`):

1. Create directory `plugins/<plugin-id>/`.
2. Add `plugin.json` defining `id`, `name`, `version`, `skills`, and `agents`.
3. Add skill definition at `plugins/<plugin-id>/skills/<plugin-id>/SKILL.md`.
4. Add 3 specialized subagent prompts under `plugins/<plugin-id>/subagents/`:
   - `<plugin-id>-scanner.md`
   - `<plugin-id>-adversary.md`
   - `<plugin-id>-remediator.md`
5. Register the new plugin entry in `marketplace.json` at the repository root.
