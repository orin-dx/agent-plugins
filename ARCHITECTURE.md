# Architecture Specification (`ARCHITECTURE.md`)

This document specifies the technical architecture, subagent orchestration pipeline, context engineering model, and token-window optimization strategies of `orin-dx/agent-plugins`.

---

## 1. Context Engineering & Progressive Disclosure

`orin-dx/agent-plugins` enforces **Dynamic Context Engineering** to prevent context window bloat:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   PROGRESSIVE DISCLOSURE ARCHITECTURE                  │
├───────────────────┬────────────────────────────────────────────────────┤
│ LAYER             │ SCOPE & RETRIEVAL MECHANISM                        │
├───────────────────┼────────────────────────────────────────────────────┤
│ Tier 1: Metadata  │ Frontmatter metadata (CSO descriptions, 100-200    │
│ (Always Active)   │ words). Used by model router for skill/agent match.│
├───────────────────┼────────────────────────────────────────────────────┤
│ Tier 2: Body      │ SKILL.md or Subagent prompt loaded into session    │
│ (On Trigger)      │ upon skill activation or subagent invocation.      │
├───────────────────┼────────────────────────────────────────────────────┤
│ Tier 3: Subdocs   │ Detailed domain guides in shared/ or references/.  │
│ (On Demand)       │ Inspected via view_file only when running tasks.   │
└───────────────────┴────────────────────────────────────────────────────┘
```

---

## 2. Multi-Agent Orchestration Loop (4-Stage Lifecycle)

The Bug Hunter framework uses a 4-phase multi-agent loop to discover, verify, and remediate defects across any repository:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   THE 4-STAGE AGENTIC LIFECYCLE                        │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│                      ┌──────────────────────┐                          │
│                      │    ORCHESTRATOR      │                          │
│                      │   (Goal & Plan)      │                          │
│                      └──────────┬───────────┘                          │
│                                 │                                      │
│        ┌────────────────────────┼────────────────────────┐             │
│        ▼                        ▼                        ▼             │
│ ┌──────────────┐       ┌─────────────────┐      ┌─────────────────┐    │
│ │   SCANNER    │ ─────►│   ADVERSARY     │ ────►│   REMEDIATOR    │    │
│ │(1. EXPLORE)  │ Signal│ (2. PLAN/TRACE) │Confirmed│ (3. CODE/VERIFY)│    │
│ └──────────────┘       └─────────────────┘      └─────────────────┘    │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### Stage Roles

1. **Stage 1: Explore (Scanner Subagents)**: Read-only inspection. Executes ripgrep regex patterns against language hazard taxonomies (Taxonomies 1 & 4). Emits candidate defect signals without modifying code.
2. **Stage 2: Plan & Trace (Adversary Subagents)**: Traces execution paths end-to-end and evaluates disproofs. Constructs concrete failing payloads or state conditions (Taxonomies 2 & 3).
3. **Stage 3: Code & Remediate (Remediator Subagents)**: Implements Red-to-Green verification: writes a failing unit test first (red), applies minimal code fix.
4. **Stage 4: Verify & Reset (Orchestrator)**: Runs project test runners to verify green pass with zero regressions. Collects subagent reports and resets context windows.

---

## 3. Superpowers Subagent Specification

All subagents implement the **Superpowers 5-Section Framework**:
- `<context>`: Workspace boundaries and stack parameters.
- `<role>`: Specialized expert persona.
- `<goal>`: Singular outcome-driven objective.
- `<execution_strategy>`: Dynamic detection heuristics and search rules.
- `<success_criteria>`: Explicit completion checklist.

---

## 4. Compatibility Standard

Plugins adhere to the open Agent Plugin format supported natively by:
- **Google Antigravity (`agy`)**: Discovers plugins in `.agents/plugins/` or `~/.gemini/config/plugins/`.
- **Claude Code**: Discovers plugins in `.claude/plugins/` or `~/.claude/plugins/`.
- **Cursor**: Discovers skill definitions in `.agents/skills/`.
