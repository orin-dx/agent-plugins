# Architecture

This document describes the technical architecture of the plugin ecosystem: how plugins are structured, how agents communicate, how context is managed, and how the verification gate works.

---

## 1. Progressive Disclosure (3-Tier Context Model)

Context is loaded on demand, not upfront. This keeps every agent's context window focused on its task.

| Tier | Content | When loaded |
| :--- | :--- | :--- |
| **Metadata** | Frontmatter `description` (80–200 words) | Always — used by model router to match skill or subagent |
| **Body** | `SKILL.md` or `subagents/*.md` prompt body (<200 words) | On trigger — when a skill activates or a subagent is dispatched |
| **References** | `shared/references/*.md`, `shared/schemas/*.json` | On demand — when the agent explicitly pulls them during task execution |

Subagents pull reference files themselves using their file reading tool. The host does not pre-load them.

---

## 2. Plugin Structure

Each plugin is a directory under `plugins/`:

```
plugins/<id>/
├── plugin.json              ← Manifest: id, version, skills, agents list
├── README.md                ← Plugin-level documentation
├── skills/<id>/SKILL.md     ← Skill prompt (what the user invokes)
├── subagents/*.md           ← Individual subagent prompts
└── shared -> ../../shared   ← Symlink for local reference access
```

`plugin.json` declares:
- `id` — unique plugin identifier
- `version` — semver
- `skills` — list of skill IDs (each has a corresponding `SKILL.md`)
- `agents` — list of subagent names declared in `subagents/`

---

## 3. The Lifecycle Pipeline

The nine ecosystem plugins form a directed pipeline. Stages communicate via shared schemas — the output of one stage is the typed input of the next.

```
graph → trace → canon → vector → lambda → axiom → delta
```

**Composable:** install any contiguous subset. A team that handles requirements externally can start at `canon`. A team that doesn't use changelogs can end at `axiom`.

**Substitutable:** any stage implementation can be replaced as long as it honours the shared schema contract. A Jira plugin can replace `graph` as long as it emits `requirement@1`.

**Cross-cutting:** `proof` runs adversarial bug hunting against live code at any point. `basis` scaffolds and audits new plugins.

---

## 4. Shared Schema Contract

Schemas in `shared/schemas/` are the inter-agent API. Every cross-plugin handoff is typed. Rules:

- Format: JSON Schema draft-2020-12
- `additionalProperties: false` on all schemas — unknown fields are rejected
- Every schema includes `reasoning: string` — an unconstrained scratchpad that is **never forwarded downstream**
- Versioned by filename: `requirement@1.json`, `requirement@2.json` — versions are immutable; a breaking change requires a new file
- Validation happens at wiring time (before agent execution), not at runtime

---

## 5. Model and Effort Tiering

Each subagent declares `model` and `effort` in its frontmatter. These are routing hints — the host uses them to select the appropriate model and reasoning budget. AGY applies its own model routing; Claude Code honours the `model`/`effort` fields directly.

| Tier | Model | Effort | Use when |
| :--- | :--- | :--- | :--- |
| Mechanical | haiku | low | Deterministic enumeration: manifest building, file inventory, commit message writing |
| Analysis | sonnet | medium | Scanning, drafting, planning, implementing, reviewing |
| Judgment | opus | high | Adversarial review, exit gates, final verdicts |

A subagent should use the lowest tier that produces correct output. Opus is for decisions that require weighing competing evidence and producing a binding verdict.

---

## 6. The Axiom Gate Protocol

`axiom` is a reusable verification gate. Any artifact type can be run through it.

```
axiom-recon → axiom-verifier → axiom-exit-gate
```

1. **recon (haiku/low):** Builds an artifact manifest — what file to check, what criteria to verify against, what source files to read.
2. **verifier (sonnet/medium):** Reads each source file and classifies every criterion as `verified`, `failed`, or `unverifiable`.
3. **exit-gate (opus/high):** Produces a final `verdict@1`. On `fail`, emits specific blockers — each blocker is actionable enough for the producing agent to fix without further clarification.

On `fail`, the orchestrator returns blockers to the producing agent for a targeted retry. After 3 retries, escalate to the human.

---

## 7. Subagent Authoring Principles (Section 9)

These rules govern how subagent prompts are written. See `shared/agent-best-practices.md` Section 9 for the full checklist. Key constraints:

- **Description:** 80–200 words, starts with "Delegate to this subagent when…"
- **Body:** <200 words. Goal + output shape + minimal non-obvious heuristics. No `<context>` or `<role>` sections that restate the description.
- **Self-contained:** No runtime references to `shared/agent-best-practices.md` — that is an authoring-time resource. Subagents pull `shared/references/` files when they need domain knowledge.
- **Output shape:** Include a compact JSON example inline. If the output is a named schema (e.g. `spec@1`), reference the schema file and include the key fields.
- **Tool language:** Use abstract tool language ("use your file reading tool") — not tool-specific API calls. This keeps prompts portable across Claude Code and AGY.
- **Reasoning scratchpad:** Always include `reasoning: string` in the output shape. Mark it "not forwarded downstream."

---

## 8. Cross-Platform Compatibility

Plugins run natively in Claude Code and AGY without a custom server framework.

- `model`/`effort` frontmatter fields are Claude Code-specific hints. AGY ignores them and applies its own model routing.
- Tool calls use abstract language (no `view_file` vs `read_file` differences).
- Shared symlinks (`plugins/<id>/shared -> ../../shared`) enable the same relative paths to work from any plugin directory.
- No absolute paths anywhere in prompts or skill files.
