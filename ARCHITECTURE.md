# Architecture Specification (`ARCHITECTURE.md`)

This document specifies the technical architecture, subagent orchestration pipeline, and token-window optimization strategies of `orin-dx/agent-plugins`.

---

## 1. Multi-Agent Orchestration Loop (Plan ➔ Execute ➔ Validate)

The Bug Hunter framework uses a 4-phase multi-agent loop to discover, verify, and remediate defects across any repository:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   BUG HUNTER ORCHESTRATION PIPELINE                    │
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
│ │ (Static RegEx│ Signal│ (Trace/Disprove)│Confirmed│ (Red-to-Green) │    │
│ └──────────────┘       └─────────────────┘      └─────────────────┘    │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### Phase Roles

1. **Orchestrator**: Inspects workspace stack, identifies target languages, and launches language-specific scanner subagents.
2. **Scanner Subagents** (`bug-hunter-scanner-*`): Executes ripgrep regex patterns against language hazard taxonomies (Taxonomies 1 & 4). Emits candidate defect signals.
3. **Adversary Subagents** (`bug-hunter-adversary-*`): Attempts to disprove signals. Traces execution paths end-to-end and constructs concrete failing payloads or state conditions (Taxonomies 2 & 3).
4. **Remediator Subagents** (`bug-hunter-remediator-*`): Implements Red-to-Green verification: writes a failing unit test first (red), applies the fix, and runs test runners to verify clean pass (green) (Taxonomies 5 & 6).

---

## 2. Context Window Optimization & Token Footprints

To prevent context window bloat during long coding sessions, the architecture enforces strict prompt isolation:

- **Monolithic Polyglot Risk**: Loading Rust, TypeScript, Python, and Go rules simultaneously consumes ~10,000+ tokens per request turn, sifting model attention.
- **Language-Scoped Plugin Solution**: Repositories load *only* their target language plugin (`bug-hunter-rust` or `bug-hunter-ts`). Prompt footprint is capped at **~1,200 to 1,800 tokens**, achieving an **~80% reduction in token overhead**.
- **On-Demand Reference Loading**: Shared laws in `shared/debugging-laws.md` are not inlined in primary skill prompts. AI agents inspect shared files via `view_file` only when an audit task is actively running.

---

## 3. Compatibility Standard

Plugins adhere to the open Agent Plugin format supported natively by:
- **Google Antigravity (`agy`)**: Discovers plugins in `.agents/plugins/` or `~/.gemini/config/plugins/`.
- **Claude Code**: Discovers plugins in `.claude/plugins/` or `~/.claude/plugins/`.
- **Cursor**: Discovers skill definitions in `.agents/skills/`.
