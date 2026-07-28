# Orin DX AI Agent & Skill Authoring Specification (`AGENTS.md`)

This specification defines the universal architecture, prompt design principles, and progressive disclosure standards for authoring AI skills, subagents, and plugins across Orin DX repositories.

---

<core_philosophy>
AI agents and skills must be outcome-focused, tool-agnostic, and dynamically adaptable to any repository structure. Rather than enforcing rigid step-by-step scripts or hardcoded file paths, guide the model's reasoning through explicit goals, contextual detection, and empirical success criteria.
</core_philosophy>

---

## 1. The 7 Core Authoring Principles

### 1. Outcome & Pattern Focus (Adapt Across Repositories)
Focus on intent, architectural invariants, and verification goals rather than hardcoded commands or specific file paths. 
- *Dynamic Detection*: Instruct agents to detect existing project tools (e.g. `cargo nextest` vs `cargo test`, `vitest` vs `jest` vs `npm test`, `pnpm` vs `yarn` vs `bun`) before executing verification steps.
- *Pattern Discovery*: "Discover existing project conventions before acting."

### 2. CSO Trigger Format for Descriptions (100–200 Words)
Descriptions serve as **trigger mechanisms** for model routing evaluators, not human documentation.
- **Skills Description**: Focused on **User Intent** (what user requests or goals trigger this skill), including adjacent domains and boundary edge cases.
- **Agents Description**: Focused on **Delegation Scenarios** (when an orchestrator should delegate to this subagent and what structured result it returns).
- Aim for 100–200 words using Context-Specific Optimization (CSO) formatting.

### 3. Progressive Disclosure Architecture (3 Layers)
Structure skill and subagent knowledge in 3 distinct layers to maintain prompt hygiene and avoid context bloat:
- **Layer 1: Frontmatter Metadata** (Always in context; contains CSO trigger description).
- **Layer 2: Primary Body / `SKILL.md`** (Loaded when triggered; contains core logic & XML directives).
- **Layer 3: Subdocuments / `references/`** (Loaded on demand via `view_file` only when executing specific tasks).

### 4. Positive Framing & XML Section Directives
- Frame instructions positively (describe the desired behavior and resolution path).
- Structure behavioral directives, execution rules, and success criteria inside explicit `<xml_tags>` (e.g. `<context>`, `<role>`, `<goal>`, `<execution_strategy>`, `<success_criteria>`) to leverage Claude and Gemini's native structural attention.

### 5. Instruction Tone & Reserved ALL CAPS
- Explain *why* a directive exists (providing rationale increases LLM compliance).
- Keep prompts lean, generalized, and non-repetitive.
- Reserve ALL CAPS (`ALWAYS`, `NEVER`) strictly for genuinely dangerous mistakes (data loss, security holes, destructive state corruption). Treat ALL CAPS as yelling.

### 6. Context Window U-Shaped Attention Optimization
LLMs exhibit U-shaped attention curves (paying highest attention to the beginning and end of context). Place core goals and critical invariants at the very top and bottom of prompts.

### 7. Non-Duplication of Linter Capabilities
Do not waste agent context duplicating what static linters, compilers, or language servers already handle (e.g. basic syntax formatting). Focus agent context on data flow, logic bugs, crash-safety, and spec compliance.

---

## 2. Directory Layout Standard

```text
plugins/<plugin-id>/
├── plugin.json                 <-- Plugin Manifest
├── skills/
│   └── <plugin-id>/
│       ├── SKILL.md            <-- Layer 2 Primary Skill (CSO Frontmatter)
│       └── references/         <-- Layer 3 On-Demand Subdocuments
└── subagents/
    ├── <plugin-id>-scanner.md  <-- Scanner Subagent (CSO Frontmatter)
    ├── <plugin-id>-adversary.md<-- Adversary Subagent (CSO Frontmatter)
    └── <plugin-id>-remediator.md<-- Remediator Subagent (CSO Frontmatter)
```
