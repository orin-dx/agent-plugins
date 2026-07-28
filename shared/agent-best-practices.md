# Advanced AI Context Engineering & Agent Best Practices

This reference documents industry best practices for Context Engineering, Skill Authoring, and Multi-Agent Orchestration derived from Google Antigravity, Anthropic Claude, and production AI engineering.

---

<context_engineering_vs_prompt_engineering>

## 1. Context Engineering over Prompt Engineering

High-performing AI agents do not rely on massive, monolithic system prompts. They rely on **Dynamic Context Engineering**—providing the exact context required at the right moment while keeping baseline token footprints minimal.

### The 3-Tier Hierarchy

1. **Tier 1: Global Invariants (`AGENTS.md` / `CLAUDE.md`)**:
   Persistent memory defining workspace build systems, core architectural rules, dual-licensing constraints, and testing command standards.
2. **Tier 2: Triggered Metadata (CSO Skill Descriptions)**:
   CSO-formatted descriptions (100–200 words) defining user intent and delegation scenarios. Loaded into active skill registries.
3. **Tier 3: On-Demand References (`references/` Subdocuments)**:
   Detailed domain guides, hazard taxonomies, and schema definitions. Inspected via `view_file` on demand only when executing active tasks.

</context_engineering_vs_prompt_engineering>

---

<agentic_loop>

## 2. The 4-Stage Agentic Lifecycle Loop

All task execution and subagent operations follow a strict 4-stage lifecycle loop:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        THE AGENTIC LIFECYCLE                           │
├──────────────┬─────────────────────────────────────────────────────────┤
│ STAGE        │ OBJECTIVE & TOOL RESTRICTIONS                           │
├──────────────┼─────────────────────────────────────────────────────────┤
│ 1. EXPLORE   │ Read-only inspection. Trace call sites, read logs,      │
│              │ inspect design specs. Zero code mutations allowed.      │
├──────────────┼─────────────────────────────────────────────────────────┤
│ 2. PLAN      │ Formulate explicit hypotheses, test strategies, and     │
│              │ success criteria before writing code.                   │
├──────────────┼─────────────────────────────────────────────────────────┤
│ 3. CODE      │ Implement minimal, robust code modifications.           │
├──────────────┼─────────────────────────────────────────────────────────┤
│ 4. VERIFY    │ Execute empirical test commands. Confirm red-to-green   │
│              │ test pass and zero workspace regressions.               │
└──────────────┴─────────────────────────────────────────────────────────┘
```

</agentic_loop>

---

<reasoning_directives>

## 3. Interleaved Thinking & Reasoning Blocks

Encourage subagents to output structured `<thinking>` or `<hypothesis>` reasoning blocks before executing destructive code modifications or terminal commands.

### Benefits of Interleaved Reasoning

- **Catches Logic Errors Early**: Reasoning aloud exposes invalid assumptions before modifying files.
- **Reduces Hallucinated Refactors**: Prevents agents from making sweeping, unrequested changes across unrelated files.
- **Enhances Traceability**: Provides a transparent audit trail of the agent's decision-making process.

</reasoning_directives>

---

<context_hygiene>

## 4. Context Window Hygiene & Subagent Isolation

Long-running single-session agent conversations accumulate token pollution, degrading reasoning performance over time (U-shaped attention curve).

### Subagent Isolation Strategy

- **Delegate and Reclaim**: Spawn specialized subagents (`bug-hunter-scanner-*`, `bug-hunter-adversary-*`, `bug-hunter-remediator-*`) with single-responsibility roles.
- **Structured Return Payloads**: Subagents report structured markdown results back to the main orchestrator and terminate cleanly.
- **Context Resets**: The parent orchestrator maintains a clean context window, relying on subagent reports and persistent ledgers (`FINDINGS.md`).

</context_hygiene>
