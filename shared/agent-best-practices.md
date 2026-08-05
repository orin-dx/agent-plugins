# Universal AI Context Engineering & Agent Authoring Manual

This document is the authoritative reference for Context Engineering, Skill Authoring, Subagent Prompting, and Multi-Agent Orchestration across Google Antigravity (AGY) and Anthropic Claude Code.

---

<table_of_contents>

1. Core Context Engineering Philosophy
2. CSO Trigger Description Writing Guide
3. The 3-Tier Progressive Disclosure Architecture
4. Tool-Agnostic Dynamic Discovery Matrix
5. The 4-Stage Agentic Lifecycle Loop
6. Superpowers 5-Section Subagent Framework
7. Google Antigravity (`agy`) vs Claude Code Operational Guide
8. LLM Prompt Quality & Formatting Directives
9. Plugin Ecosystem Authoring Principles

</table_of_contents>

---

<context_engineering_philosophy>

## 1. Core Context Engineering Philosophy

High-performing AI agents do not rely on massive, static system prompts. They rely on **Dynamic Context Engineering**—delivering the precise context required for a task at the exact moment it is needed while keeping baseline context windows lean.

### The 6 Foundational Rules

1. **Outcome & Pattern Focus**: Specify *what outcome to achieve and how to verify success*, rather than micromanaging step-by-step scripts or hardcoding file paths.
2. **Tool-Agnostic Dynamic Discovery**: Instruct agents to discover workspace tools, test runners, and package managers before executing commands.
3. **CSO Trigger Descriptions**: Write metadata descriptions aimed at model routing evaluators (100–200 words) rather than human documentation.
4. **Progressive Disclosure**: Divide context into 3 layers (Metadata ➔ Body ➔ References).
5. **Positive Framing & XML Sectioning**: Direct behavior positively using `<xml_tags>` for structural attention.
6. **Empirical Verification**: Gated by the Red-to-Green Law (verify test fails red pre-fix, passes green post-fix).

</context_engineering_philosophy>

---

<cso_trigger_guide>

## 2. CSO Trigger Description Writing Guide

Descriptions in `SKILL.md` and subagent `.md` files are **trigger mechanisms** for model routing evaluators. They dictate when the agentic system activates a skill or delegates a task to a subagent.

### Target Length & Budget
Aim for **100 to 200 words** per description using Context-Specific Optimization (CSO).

### Skill Description vs Subagent Description

| Type | Focus | Key Content to Include |
| :--- | :--- | :--- |
| **Skill Description** | **User Intent Focus** | User prompt triggers, request phrasing, target file types, adjacent engineering domains, boundary edge cases. |
| **Subagent Description** | **Delegation Scenario Focus** | When the orchestrator should delegate to this subagent, input payload format, specialist tasks, and returned structured result. |

### CSO Skill Description Template (User Intent Focus)

```yaml
description: >-
  Trigger this skill when the user asks to perform a bug hunt, code audit, spec verification, or defect search in a <Language/Framework> codebase. Use when checking for <Hazard 1>, <Hazard 2>, <Hazard 3>, <Hazard 4>, <Hazard 5>, or <Hazard 6>. Also activate when the user requests an adversarial audit across <Framework> components, monorepo dependencies, or CI/CD pipelines.
```

### CSO Subagent Description Template (Delegation Scenario Focus)

```yaml
description: >-
  Delegate to this subagent when <Orchestrator Trigger Condition> across a <Language/Framework> workspace to identify candidate defects in <Target Domain>. Specialized for auditing <Taxonomy A>, <Taxonomy B>, and <Taxonomy C>. Returns a structured markdown report detailing candidate defect signals with exact file:line citations for adversarial verification.
```

</cso_trigger_guide>

---

<progressive_disclosure>

## 3. The 3-Tier Progressive Disclosure Architecture

Structure plugin knowledge into 3 distinct layers to maintain prompt hygiene (~1,200 to 1,800 tokens max) and prevent U-shaped context attention degradation:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   PROGRESSIVE DISCLOSURE ARCHITECTURE                  │
├───────────────────┬────────────────────────────────────────────────────┤
│ LAYER             │ SCOPE, CONTENTS & RETRIEVAL MECHANISM              │
├───────────────────┼────────────────────────────────────────────────────┤
│ Tier 1: Metadata  │ Frontmatter YAML (CSO descriptions, 100-200 words).│
│ (Always Active)   │ Always loaded in context registry for routing.     │
├───────────────────┼────────────────────────────────────────────────────┤
│ Tier 2: Body      │ SKILL.md or Subagent prompt loaded into session    │
│ (On Trigger)      │ upon skill activation or subagent invocation.      │
├───────────────────┼────────────────────────────────────────────────────┤
│ Tier 3: Subdocs   │ Detailed domain guides in shared/ or references/.  │
│ (On Demand)       │ Inspected via view_file only when running tasks.   │
└───────────────────┴────────────────────────────────────────────────────┘
```

</progressive_disclosure>

---

<dynamic_discovery_matrix>

## 4. Tool-Agnostic Dynamic Discovery Matrix

Prompts must remain tool-agnostic, instructing agents to **discover existing environment tools before taking action**:

```markdown
<execution_strategy>
1. **Tool Discovery**:
   - Detect test runners: Check for `cargo nextest` vs `cargo test`, `vitest` vs `jest` vs `npm test` vs `bun test` vs `pytest`.
   - Detect package managers: Check for `pnpm-lock.yaml` vs `yarn.lock` vs `package-lock.json` vs `Cargo.lock`.
   - Detect build runners: Check for `justfile` vs `moon.yml` vs `Makefile` vs native CLI commands.
2. **Execute Verification**:
   - Use the detected workspace-native tool to execute test suites and verification checks.
</execution_strategy>
```

</dynamic_discovery_matrix>

---

<agentic_loop>

## 5. The 4-Stage Agentic Lifecycle Loop

All task execution follows a strict 4-stage lifecycle loop:

1. **Stage 1: Explore (Read-Only Inspection)**: Trace call sites, read logs, inspect design specs. Zero code mutations allowed.
2. **Stage 2: Plan & Trace**: Formulate explicit hypotheses, test strategies, and success criteria before writing code.
3. **Stage 3: Code & Remediate**: Implement minimal, robust code modifications.
4. **Stage 4: Verify & Reset**: Execute empirical test commands. Confirm red-to-green test pass and zero workspace regressions.

</agentic_loop>

---

<superpowers_framework>

## 6. Superpowers 5-Section Subagent Framework

All subagent prompt definitions (`.md`) MUST be structured into 5 goal-driven sections:

```markdown
# <Subagent Name>

<context>Workspace environment, tech stack, and boundary constraints.</context>
<role>Specialized expert persona (e.g. Static Scanner, Adversarial Verifier).</role>
<goal>Singular, outcome-focused objective.</goal>
<execution_strategy>Dynamic tool detection heuristics and search rules.</execution_strategy>
<success_criteria>Explicit, verifiable completion checklist.</success_criteria>
```

</superpowers_framework>

---

<platform_matrix>

## 7. Google Antigravity (`agy`) vs Claude Code Operational Guide

When authoring plugins for cross-platform deployment across Google Antigravity and Claude Code, adhere to this operational matrix:

| Feature / Aspect | Google Antigravity (`agy`) | Anthropic Claude Code (`claude`) | Cross-Platform Authoring Rule |
| :--- | :--- | :--- | :--- |
| **Plugin Directory** | `~/.gemini/config/plugins/` or `.agents/plugins/` | `~/.claude/plugins/` or `.claude/plugins/` | Author plugins under `./plugins/<plugin-id>/`. Symlink or copy to target CLI paths. |
| **Marketplace Index** | `marketplace.json` (`$schema: antigravity.google/...`) | `marketplace.json` or directory scan | Maintain root `marketplace.json` listing plugin IDs, paths, and descriptions. |
| **Agent Folder** | `agents/` | `agents/` | Place prompt files in `agents/`. Both engines resolve this canonical path natively (`plugin.json` specifies `"agents": "./agents/"`). |
| **Tool Referencing** | `run_command`, `view_file`, `grep_search`, `replace_file_content` | `Bash`, `View`, `Edit`, `Grep` | Refer to abstract tool categories ("file viewing tool", "grep search tool", "test execution tool"). |
| **Rich Artifacts** | Auxiliary Pane (`.md` artifacts, Mermaid, Carousels) | Terminal Markdown Output | Use standard GitHub Flavored Markdown (GFM) and alerts (`> [!NOTE]`, `> [!TIP]`) readable on both surfaces. |
| **Subagent Invocation** | Native `invoke_subagent` / `define_subagent` APIs | Multi-agent subprocess execution | Author subagent prompts with YAML frontmatter (`name`, `role`, `description`). |

</platform_matrix>

---

<prompt_directives>

## 8. LLM Prompt Quality & Formatting Directives

1. **Positive Framing**: Direct the model toward desired resolution behaviors rather than over-indexing on negative prohibitions.
2. **XML Sectioning**: Enclose logical directives inside `<xml_tags>` to focus model structural attention.
3. **Reserved ALL CAPS**: Reserve ALL CAPS (`ALWAYS`, `NEVER`) strictly for genuinely dangerous mistakes (data loss, security vulnerabilities, state corruption). Treat ALL CAPS as yelling.
4. **No Linter Duplication**: Do not waste agent context on basic syntax formatting handled by compilers and linters. Focus on logic, data flow, crash safety, and spec compliance.
5. **U-Shaped Attention Positioning**: Place core goals and critical invariants at the absolute top and bottom of prompts.

</prompt_directives>

---

<ecosystem_principles>

## 9. Plugin Ecosystem Authoring Principles

These principles apply to all plugins in the ecosystem. Read this section before writing any new plugin, skill, or subagent.

### Pull Over Inject

Agents receive a workspace path and a goal. They use available tools (file reading, grep, shell) to discover what they need. The orchestrator does not pre-stuff context. This keeps baseline context windows lean and makes agents work from current state, not stale injections.

Inject only what the agent cannot pull: the goal, the output schema, and a small set of heuristics for where to look first.

### Goal Over Procedure

Subagent prompts specify *what outcome to achieve and how to verify success* — not step-by-step scripts. The agent decides the approach. `<execution_strategy>` provides high-level heuristics (prefer reading compiled artifacts over inferring from directory layout), not numbered steps.

If a subagent prompt reads like a recipe, it is over-specified. Trim until it reads like a mission brief.

### Minimum Viable Prompt

A subagent prompt is: role + goal + output shape + a few heuristics. Target under 200 words for the body. Longer prompts are not more capable — they are more brittle. Every word that can be removed without losing a constraint should be removed.

**Body length signal:** if the prompt is over 300 words, audit it for procedure masquerading as guidance.

### Self-Contained Prompts (Cross-Platform)

Subagent prompts make no runtime filesystem references to `shared/`. Shared principles are read by the human or orchestrating agent at authoring time and relevant excerpts baked in. This ensures prompts work identically on Claude Code and AGY regardless of execution environment.

**Exception:** `shared/references/*.md` files (language guides, protocol references) are runtime resources — agents may pull them with their file-reading tool when language-specific heuristics are needed. Reference them by relative path: `shared/references/rust.md`.

### Model and Effort Tiering

| Task class | Model | Effort |
|---|---|---|
| Mechanical — manifest building, file enumeration, schema validation | haiku | low |
| Analysis — finding bugs, cross-referencing, evaluating findings | sonnet | medium |
| Judgment — exit gate verdicts, architectural review, adversarial verification | opus | high |

Apply the cheapest tier that can do the job. Escalate only when judgment is genuinely required. A haiku recon agent followed by a sonnet analyzer costs a fraction of running everything at opus.

### Schema as Inter-Agent Contract

Agents communicate via schema-constrained structured output. Every handoff schema includes a `reasoning: str` field (scratchpad — the agent's chain-of-thought, unconstrained) alongside the typed output fields. The `reasoning` field travels with the artifact for debugging but is **never consumed** by the next stage.

Output type is enforced at generation where possible (structured output / JSON schema mode). If validation fails, the agent retries with the specific failure message — not a silent rejection. Retry budget: 3 attempts before escalation to the user.

### Authoring-Time vs Runtime Resources

`shared/agent-best-practices.md` is an **authoring-time** resource. Authors read it when writing plugins; agents do not load it at runtime.

`shared/references/*.md` files are **runtime** resources — agents may load them on demand when they need language or tool-specific detail.

`shared/schemas/*.json` files are **wiring-time** resources — the host validates `produces` and `consumes` schema compatibility before any execution begins.

This three-way split is what makes cross-platform compatibility unconditional.

### Tool Count Limit

Design plugin agents with 8–15 tools each. Above 20 tools, selection accuracy degrades on both Claude and Gemini. Narrow, specialized agents outperform wide, general-purpose ones. When a plugin needs more than 15 tools, split it into focused subagents with clean handoffs.

### Public Agent Description

Every subagent's YAML frontmatter `description` is the public routing key — it is what the orchestrator reads to decide whether to delegate. Write it for *two audiences simultaneously*: concrete enough for LLM routing, accurate enough for human discovery. The system prompt body is private implementation detail; the description is the public contract.

</ecosystem_principles>
