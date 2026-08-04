# verify-first Plugin Design Spec

**Date:** 2026-08-04
**Status:** Draft
**Author:** Gabriel Castro (Orin DX)

---

## Goal

Prevent the class of agent errors that arise from acting on unverified assumptions — about what code is compiled, what a spec actually says, what a plan covers, whether implementation is truly complete. These errors are upstream of bugs: they corrupt the ground truth that all downstream work depends on.

This spec covers two deliverables:

1. **`verify-first` plugin** — a new prevention-focused plugin that installs verified ground truth at each development phase (recon, spec, plan, implement, exit).
2. **`bug-hunter-rust` v2 additions** — two new subagents (Phase 0 recon, Phase 5 exit gate) that close the gaps identified in adversarial review sessions.

---

## Design Principles

These principles apply to everything authored in this repo. They extend `shared/agent-best-practices.md` and are baked into subagent prompts at authoring time — not loaded at runtime.

### Pull over inject

Agents receive a workspace path and a goal. They use available tools (file reading, grep, shell) to discover what they need. The orchestrator does not pre-stuff context. This keeps baseline context windows lean and makes agents work from current state, not stale injections.

### Goal over procedure

Subagent prompts specify *what outcome to achieve and how to verify success* — not step-by-step scripts. The agent decides the approach. `<execution_strategy>` provides high-level heuristics (prefer reading compiled artifacts over inferring from directory layout), not numbered steps.

### Minimum viable prompt

A subagent prompt is: role + goal + output shape + a few heuristics. Target under 200 words for the body. If it is longer, it is over-specified.

### Self-contained prompts (cross-platform)

Subagent prompts make no runtime filesystem references to `shared/`. Shared principles are read by the human or orchestrating agent at authoring time and relevant excerpts baked in. This ensures prompts work identically on Claude Code and AGY regardless of execution environment.

### Model and effort tiering

| Task class | Model | Effort |
|---|---|---|
| Mechanical — manifest building, file enumeration, schema validation | haiku | low |
| Analysis — finding bugs, cross-referencing, evaluating findings | sonnet | medium |
| Judgment — exit gate verdicts, architectural review, adversarial verification | opus | high |

Apply the cheapest tier that can do the job. Escalate only when judgment is genuinely required.

### Schema as inter-agent contract

Agents communicate via schema-constrained structured output. Schemas are defined at authoring time and embedded in the relevant subagent prompts — not loaded from disk at runtime. Small schemas inline cleanly; they do not warrant separate files.

### Authoring-time vs runtime

`shared/` is an authoring resource. Authors read it when writing plugins; agents do not reference it at runtime. This distinction is what makes cross-platform compatibility unconditional.

---

## Plugin: `verify-first`

### Purpose

Installs a verified ground truth checkpoint at each phase of development. Activates automatically via CSO routing when the agent is about to begin a phase that requires grounded knowledge.

### Activation signals (CSO trigger)

- User asks to verify a spec against code, audit a plan for coverage gaps, or check whether work is complete
- Orchestrator is about to begin implementation without a recon phase
- User references a design doc, plan, or spec and asks to "check it" or "make sure it's right"
- Post-implementation review or "are we done?" signals

### Skills

**`verify-first`** (one skill, one SKILL.md)

Describes when to activate and routes to the appropriate subagent based on the current phase. The skill body is kept lean — it is a router, not an instruction manual.

### Subagents

#### `verify-first-recon`

**Model:** haiku / low effort

**Goal:** Produce a verified workspace manifest — every compiled module, its crate/package path, and whether it is reachable from the crate root. Output is a structured report distinguishing active from dead code.

**Output shape:**
```
{
  "workspace_root": string,
  "compiled_modules": [{ "path": string, "reachable": bool, "declared_in": string }],
  "dead_files": [string],
  "confidence": "high" | "medium" | "low"
}
```

This is the foundational agent. Downstream agents (scanner, spec verifier, exit gate) build on its output rather than re-discovering workspace structure independently.

#### `verify-first-spec-verifier`

**Model:** sonnet / medium effort

**Goal:** Given a spec document and a workspace manifest, verify that every claim in the spec matches actual code. Produce a list of confirmed matches, mismatches, and unverifiable claims.

**Output shape:**
```
{
  "verified": [{ "claim": string, "evidence": string }],
  "mismatches": [{ "claim": string, "actual": string, "file": string, "line": int }],
  "unverifiable": [{ "claim": string, "reason": string }]
}
```

Agents read the spec and the code. They do not rely on summary or memory.

#### `verify-first-exit-gate`

**Model:** opus / high effort

**Goal:** Determine whether the current implementation is complete and correct relative to the stated goal. Return a structured verdict with specific blockers if incomplete.

**Output shape:**
```
{
  "complete": bool,
  "confidence": "high" | "medium" | "low",
  "blockers": [{ "description": string, "file": string, "line": int }],
  "sibling_gaps": [string],
  "verdict_summary": string
}
```

This agent is adversarial by disposition. It looks for what is missing or wrong, not for confirmation that things are right.

---

## Plugin: `bug-hunter-rust` v2 Additions

Two new subagents close the gaps identified in adversarial sessions.

### `bug-hunter-recon-rust` (Phase 0)

**Model:** haiku / low effort

**Goal:** Before any scanning begins, build a verified module manifest for the Rust workspace. Distinguish files that are compiled (declared via `mod` in a crate root or parent module) from files that exist in the tree but are unreachable. Return the manifest so all subsequent scanner and adversary agents operate only on live code.

This prevents the single largest source of false findings in prior audit rounds: scanners reporting bugs in dead code.

Integrates into the existing bug-hunter-rust orchestration as a mandatory Phase 0, before the Scanner subagent runs.

### `bug-hunter-exit-gate-rust` (Phase 5)

**Model:** opus / high effort

**Goal:** After remediation, independently verify that all confirmed findings are resolved, no sibling functions were missed, no regressions were introduced, and the workspace compiles and tests pass. Return a structured verdict.

This is an independent agent — it does not inherit context from the remediator. It reads the current code state from scratch.

---

## `shared/agent-best-practices.md` Additions

A new section (Section 9) covering the principles above: pull over inject, goal over procedure, minimum viable prompt, self-contained cross-platform prompts, model/effort tiering, and the authoring-time vs runtime distinction for shared resources.

This section becomes the authoritative reference that plugin authors read when writing new subagents. It does not replace any existing section — it extends the manual.

---

## Directory Layout

```text
plugins/
├── verify-first/
│   ├── plugin.json
│   ├── skills/
│   │   └── verify-first/
│   │       └── SKILL.md
│   └── subagents/
│       ├── verify-first-recon.md
│       ├── verify-first-spec-verifier.md
│       └── verify-first-exit-gate.md
│
└── bug-hunter-rust/
    └── subagents/
        ├── bug-hunter-recon-rust.md       ← new
        └── bug-hunter-exit-gate-rust.md   ← new

shared/
└── agent-best-practices.md               ← Section 9 added
```

---

## Cross-Platform Compatibility

All subagent prompts:

- Use abstract tool language ("use your file reading tool", "grep for X") matching the platform matrix in `shared/agent-best-practices.md` Section 7
- Make no runtime references to local file paths in `shared/`
- Use standard GFM output readable on both Claude terminal and AGY auxiliary pane
- Use YAML frontmatter (`name`, `role`, `description`) compatible with both `claude` and `agy` subagent invocation APIs

---

## Scope Boundaries

This spec does not cover:

- Language support beyond Rust for the recon and exit-gate patterns (future plugins)
- Execution infrastructure (CI integration, scheduled audits)
- UI surfaces beyond what both CLIs natively render
- Changes to `bug-hunter-ts` (separate plugin, separate scope)
