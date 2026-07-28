# Orin DX Agent Plugins Guidelines (`AGENTS.md`)

This guide provides architectural rules, engineering invariants, and contribution workflows for AI coding agents (Antigravity/AGY, Claude, Cursor, Copilot, Codex) working on or utilizing the `orin-dx/agent-plugins` repository.

---

## 1. Core Best Practices for AI Agents

When authoring or executing AI agents in production engineering environments, adhere to these 6 foundational pillars:

### 1. Goal-Driven Autonomy (Outcome-Oriented Prompting)
Define **what outcome to achieve** and **how to verify success**, rather than micromanaging step-by-step instructions. Giving agents explicit **Success Criteria** allows them to reason, adapt to unexpected edge cases, and persevere until verification is complete.

### 2. Empirical Verification ("Show Me, Don't Tell Me")
Never claim a task is resolved, a bug is fixed, or code is working until concrete, empirical verification commands have passed in the current session.
- **Red-to-Green Law**: For code fixes, verify that a regression test fails on pre-fix code (red pass) and passes post-fix (green pass).

### 3. Context Window Hygiene & Least-Privilege Scope
Keep system prompts and skill definitions token-lean (~1,200 to 1,800 tokens max). Store detailed reference materials in subdocuments (`references/`) and inspect them on demand via `view_file`. Overloaded prompts cause attention dilution, leading to rule violations and hallucinations.

### 4. Single-Responsibility Subagents
Avoid monolithic "do-everything" agents. Partition subagents into single-responsibility roles (Scanner ➔ Adversary ➔ Remediator) focused on specific failure taxonomies.

### 5. Silent Log Inspection & Traceability
Never guess implementation logic, variable names, or schemas. Inspect authoritative source files and un-truncated error logs before diagnosing runtime failures.

### 6. Structured Output & Ledger Persistence
Format all outputs using standardized schemas (`Status`, `Location`, `Classification`, `Root Cause`, `Failing Scenario`, `Verification Strategy`). Persist findings in ledger files (`FINDINGS.md`) to prevent duplicate work across agent runs.

---

## 2. Repository Purpose & Architecture

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

## 3. Core Architectural Invariants

Agents modifying or adding plugins in this repository MUST enforce the following 6 invariants:

### 1. Self-Contained Language Scoping
Language plugins MUST remain strictly self-contained under `plugins/<plugin-name>/`. Do NOT mix rules for multiple languages into a single plugin.

### 2. On-Demand Shared Context References
Shared rules live in `shared/` at the root of the repository. Plugins reference shared context using relative Markdown links (e.g. `[General Debugging Laws](../../../shared/debugging-laws.md)`).

### 3. Red-to-Green Verification Law
All remediation subagents (`bug-hunter-remediator-*`) MUST follow the Red-to-Green Law.

### 4. Hazard-Taxonomy Subagent Partitioning
Multi-agent bug hunts MUST partition subagents by Hazard Category across the target codebase (Scanner ➔ Adversary ➔ Remediator).

### 5. Superpowers 5-Section Subagent Structure
All subagent prompt definitions (`.md`) MUST be structured into 5 goal-driven sections (Context, Role, Goal, Execution Rules & Strategy, Success Criteria).

### 6. Clean Technical Style (No Emoji Directive)
Documentation, skills, and prompts MUST remain clean, technical, scannable, and devoid of emojis or AI bot filler phrases.
