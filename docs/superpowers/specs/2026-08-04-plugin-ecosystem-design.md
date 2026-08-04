# Plugin Ecosystem Design

**Date:** 2026-08-04
**Status:** Draft
**Author:** Gabriel Castro (Orin DX)

---

## Overview

A set of nine cooperating plugins covering the full software development lifecycle, connected by a shared schema contract system and a common verification gate (`axiom`). Plugins are composable: you can install graph + trace + canon for requirements work without lambda or delta. Third parties can substitute any stage implementation (e.g., replace `graph` with a Jira plugin) as long as they honor the shared schema.

Each plugin has a clear goal, a defined output artifact, and a success criterion. Agents inside each plugin pull context from the workspace — they are not pre-stuffed with context by the orchestrator.

**Framework:** `torii` — an MCP server toolkit for publishing these plugins as discoverable services. Named for the gate (torii) at the end of the path (michi).

---

## The Development Lifecycle

```
graph (need) → trace (research) → canon (spec) → vector (plan) → lambda (code)
     ↑                                                                  ↓
     └──────────────────── delta (ship) ← axiom (validate) ────────────┘
```

Each stage consumes the previous stage's artifact, transforms it, and hands off a typed artifact to the next stage. `axiom` can gate any stage transition, not just the final one. `basis` is the meta-plugin for building new plugins; `proof` is the cross-cutting bug-finding tool that operates across any stage.

---

## Plugin Inventory

### `graph` — Need Definition

**Goal:** Capture and structure what needs to be built before anyone writes code or specs. Make requirements explicit, connected to actual stakeholder intent, and queryable by downstream stages.

**Outcome:** A `requirement@1` artifact — a structured statement of what is needed, why, who it serves, and what out-of-scope means.

**Success:** A downstream spec writer (canon) can read the requirement and produce an accurate spec without asking clarifying questions. The requirement is specific enough to write a failing test against.

**Skills:**

- `graph/capture` — Triggered when a user describes a need ("we need X", "the problem is Y"). Prompts for missing dimensions: who's affected, what the constraint is, what done looks like. Produces a draft requirement.
- `graph/prioritize` — Orders open requirements by impact and urgency. Produces a sorted backlog with explicit rationale.
- `graph/connect` — Links a requirement to an existing spec or code section to confirm whether it's already addressed.
- `graph/audit` — Surfaces requirements that have no corresponding spec, plan, or implementation.

**Agents:**

| Agent | Model | Effort | Purpose |
|---|---|---|---|
| `graph-intake` | haiku | low | Structured capture of a user's raw need |
| `graph-clarifier` | sonnet | medium | Identify missing dimensions, ask focused questions |
| `graph-auditor` | sonnet | medium | Cross-reference requirements against existing work |

**Consumes:** User's raw need statement (text)
**Produces:** `requirement@1`

**Extensibility point:** Third parties who use Jira or Linear replace this plugin with one that reads from their issue tracker and emits the same `requirement@1` schema.

---

### `trace` — Research

**Goal:** Investigate a question or requirement thoroughly before committing to a solution direction. Build a documented evidence base so decisions are grounded in what's actually known, not assumptions.

**Outcome:** A `research-report@1` artifact — sources read, key findings, open questions, and a recommended direction with explicit confidence level.

**Success:** A spec writer (canon) can read the report and write a spec that won't be surprised by implementation reality. The report distinguishes "confirmed" from "assumed" and says why.

**Skills:**

- `trace/question` — Triggered by "I need to understand X before deciding" or "is there a way to do Y". Researches internal codebase and external sources, produces a structured report.
- `trace/prior-art` — Surveys existing implementations of a pattern in the codebase or ecosystem. Useful before writing a spec for something that might already exist.
- `trace/dependency` — Investigates a specific dependency: what version is in use, what its API surface is, whether there are known issues relevant to the current requirement.
- `trace/risk` — Surfaces technical risks in a proposed approach before implementation begins.

**Agents:**

| Agent | Model | Effort | Purpose |
|---|---|---|---|
| `trace-recon` | haiku | low | Enumerate available sources, map the search space |
| `trace-reader` | sonnet | medium | Read sources, extract findings, assess confidence |
| `trace-synthesizer` | sonnet | medium | Merge findings, identify gaps, produce report |
| `trace-risk-assessor` | opus | high | Judge severity and likelihood of risks, prioritize |

**Consumes:** `requirement@1` or a free-form question
**Produces:** `research-report@1`

**Language-agnostic.** The recon agent detects the workspace language from `Cargo.toml`, `package.json`, etc., then pulls `shared/references/rust.md` or `shared/references/typescript.md` using its file-reading tool for language-specific search heuristics.

---

### `canon` — Specification

**Goal:** Turn a requirement and research report into an unambiguous, testable specification. Make every claim either verifiable or explicitly marked as a judgment call with stated rationale.

**Outcome:** A `spec@1` artifact — a structured document with: purpose, scope, non-goals, API surface (if applicable), behavior under error conditions, and a set of acceptance criteria each phrased as a testable proposition.

**Success:** A developer can read the spec and write the implementation without asking the spec author a single clarifying question. Every acceptance criterion can be translated directly into a test case. The spec has no TBDs.

**Skills:**

- `canon/draft` — Triggered by "write a spec for X" or following a `trace` report. Produces a draft spec from requirement + research.
- `canon/review` — Triggered by "review this spec" or "is this spec complete". Checks for ambiguity, missing error cases, and untestable claims.
- `canon/verify` — Compares an existing spec against actual code to find drift. Reports confirmed matches, contradictions, and uncovered claims.
- `canon/changeset` — Given a diff or PR description, checks whether the spec needs to be updated to reflect the change.

**Agents:**

| Agent | Model | Effort | Purpose |
|---|---|---|---|
| `canon-drafter` | sonnet | medium | Produce draft spec from requirement + research |
| `canon-auditor` | sonnet | medium | Audit for ambiguity, missing cases, testability |
| `canon-verifier` | sonnet | medium | Cross-reference spec claims against code |
| `canon-exit-gate` | opus | high | Final judgment: is this spec ready? |

**Consumes:** `requirement@1`, `research-report@1` (optional)
**Produces:** `spec@1`

---

### `vector` — Planning

**Goal:** Decompose a spec into a sequenced, bite-sized implementation plan that a developer or agent can execute without design judgment.

**Outcome:** A `plan@1` artifact — an ordered list of tasks, each with: files to touch, exact code to write, test to run first (TDD), expected test output, and a commit message. No TBDs. No "add appropriate error handling."

**Success:** A developer with zero domain context can execute the plan mechanically and produce a working, tested implementation. Every task takes 5–15 minutes. Every task produces a passing test before implementation.

**Skills:**

- `vector/plan` — Triggered by "write a plan for X" or "how do we implement this spec". Produces a full implementation plan.
- `vector/estimate` — Produces a rough effort estimate with explicit assumptions.
- `vector/challenge` — Adversarially reviews a plan: what did we miss, what assumptions are wrong, what's over-engineered.
- `vector/decompose` — Breaks a large plan into independent sub-plans that can be parallelized or sequenced.

**Agents:**

| Agent | Model | Effort | Purpose |
|---|---|---|---|
| `vector-planner` | sonnet | medium | Produce plan from spec |
| `vector-estimator` | sonnet | low | Rough effort estimate |
| `vector-challenger` | opus | high | Adversarial review of plan |

**Consumes:** `spec@1`
**Produces:** `plan@1`

---

### `lambda` — Implementation

**Goal:** Execute an implementation plan: write tests first, write minimal passing code, commit frequently. Produce working, reviewed, committed code with no unresolved review comments.

**Outcome:** Passing tests + committed code implementing the spec. A `changeset@1` artifact describing what was changed and why.

**Success:** `axiom` exit-gate passes: all tests pass, all spec acceptance criteria are met, no sibling functions were missed, no regressions introduced.

**Skills:**

- `lambda/implement` — Triggered by "implement this" or "execute the plan". Runs TDD cycle per task.
- `lambda/generate-tests` — Given a spec or existing code, generates a test suite.
- `lambda/explain` — Given a piece of code, explains what it does in terms of the spec it implements.
- `lambda/refactor` — Refactors a section of code without changing behavior, with tests as the safety net.

**Agents:**

| Agent | Model | Effort | Purpose |
|---|---|---|---|
| `lambda-recon` | haiku | low | Verify workspace manifest before writing code |
| `lambda-implementer` | sonnet | medium | Execute one plan task: test + implementation |
| `lambda-reviewer` | sonnet | medium | Self-review of committed changes |
| `lambda-exit-gate` | opus | high | Verify all criteria met, no gaps, no regressions |

**Consumes:** `plan@1`
**Produces:** `changeset@1`

---

### `proof` — Bug Hunting

**Goal:** Find real bugs in live code before they reach users. Distinguish confirmed bugs from noise. Produce a structured report with evidence and a remediation path.

**Outcome:** A `finding-report@1` artifact — confirmed findings with: description, evidence (file, line), severity, root cause, and a remediation sketch. Findings that couldn't be confirmed are excluded.

**Success:** Every confirmed finding is a real, reproducible bug in code that is actually compiled and reachable. No findings in dead code. No "potential issue" hedging — each finding includes the exact trigger condition.

**Skills:**

- `proof/scan` — Full sweep of the codebase for the configured hazard taxonomy.
- `proof/focus` — Targeted scan of a specific module or file.
- `proof/verify` — Given a reported bug, independently verify whether it's real.
- `proof/remediations` — Given a finding report, produce a remediation plan.

**Agents:**

| Agent | Model | Effort | Purpose |
|---|---|---|---|
| `proof-recon` | haiku | low | Build workspace manifest; distinguish live from dead code |
| `proof-scanner` | sonnet | medium | Scan for bugs in a specific hazard category |
| `proof-adversary` | opus | high | Try to refute each candidate finding; confirm or reject |
| `proof-exit-gate` | opus | high | Final verdict: is the finding real, is the remediation correct? |

**Consumes:** workspace path (or `changeset@1` for targeted post-implementation scan)
**Produces:** `finding-report@1`

**Language references:** `shared/references/rust.md` and `shared/references/typescript.md` contain hazard taxonomies and search heuristics for each language. The recon agent detects the workspace language and loads the appropriate reference at runtime.

**Replaces:** `bug-hunter-rust`, `bug-hunter-ts` — those become proof's language-specific configurations, not separate plugins.

---

### `axiom` — Verification Gate

**Goal:** Confirm that a stage's artifact meets its criteria before the next stage begins. This is the cross-cutting prevention plugin — it installs exit gates at every stage transition.

**Outcome:** A `verdict@1` artifact — pass or fail, confidence level, specific blockers, and the criteria against which the artifact was evaluated.

**Success:** If verdict is pass: the downstream stage can begin with confidence that its input is correct. If verdict is fail: the producing stage has specific, actionable blockers — not a generic rejection.

**Skills:**

- `axiom/verify-requirement` — Checks a requirement for completeness and specificity.
- `axiom/verify-spec` — Checks a spec for ambiguity, missing error cases, and untestable claims.
- `axiom/verify-plan` — Checks a plan for missing tasks, over-specification, and incorrect task order.
- `axiom/verify-implementation` — Checks an implementation against its spec: are all criteria met, any regressions, any sibling gaps?
- `axiom/verify-pr` — Checks a PR description and diff against a spec or requirement.
- `axiom/exit-gate` — The generic exit gate: given an artifact and a set of criteria, produce a verdict.

**Agents:**

| Agent | Model | Effort | Purpose |
|---|---|---|---|
| `axiom-recon` | haiku | low | Inventory the artifact and available verification criteria |
| `axiom-verifier` | sonnet | medium | Cross-reference artifact against criteria |
| `axiom-exit-gate` | opus | high | Judgment: pass or fail, with specific blockers |

**Consumes:** any typed artifact + the criteria to verify against
**Produces:** `verdict@1`

**This plugin is cross-cutting.** Every other plugin's exit-gate subagent runs the axiom protocol. The distinction:
- Other plugins' exit gates verify their own output before handing off
- The `axiom` plugin is user-invokable to run a verification pass at any time, on any artifact

**Retry:** if the verdict is fail, the producing plugin's agent receives the specific blockers and retries (up to 3 times). On repeated failure, escalates to the user.

---

### `delta` — Shipping

**Goal:** Take completed, verified code and shepherd it through the shipping process: write a meaningful commit, assemble a PR with context a reviewer can act on, address review feedback, and track what shipped in what changeset.

**Outcome:** Merged code + a `release-artifact@1` — what was in the release, what requirement it addressed, and any breaking changes.

**Success:** A reviewer who has no context can read the PR description and understand what changed, why, and how to verify it. Review feedback is addressed completely. The changeset entry is accurate.

**Skills:**

- `delta/commit` — Triggered by "commit this" or "write a commit message". Analyzes staged changes and produces a conventional commit.
- `delta/pr` — Triggered by "open a PR" or "create a pull request". Reads the diff, the spec, and the linked requirement to produce a PR narrative.
- `delta/review` — Triggered by "review this PR" or "address the feedback". Reads review comments and produces a remediation plan.
- `delta/receive` — Triggered when a review has arrived. Parses feedback, categorizes by type (must-fix, suggestion, question), and produces a response plan.
- `delta/changeset` — Triggered by "add a changeset" or "document this change". Produces a structured changeset entry for the release log.
- `delta/release` — Triggered by "cut a release" or "what's in this release". Summarizes all changesets since the last release.

**Agents:**

| Agent | Model | Effort | Purpose |
|---|---|---|---|
| `delta-commit-analyzer` | haiku | low | Analyze staged changes for conventional commit |
| `delta-pr-narrator` | sonnet | medium | Produce PR description from diff + spec + requirement |
| `delta-changeset-analyzer` | sonnet | medium | Extract semantic meaning from diff for changeset |
| `delta-review-preprocessor` | sonnet | medium | Parse review comments, categorize, prioritize |
| `delta-release-summarizer` | sonnet | medium | Aggregate changesets into release notes |

**Consumes:** `changeset@1`, staged git changes, PR diff
**Produces:** merged PR, `release-artifact@1`

---

### `basis` — Plugin Building

**Goal:** Help developers build new plugins and subagents that conform to the ecosystem's conventions, schemas, and quality bar. Accelerate the ecosystem's growth by making the right way to do things the easy way.

**Outcome:** A new plugin directory conforming to the plugin manifest spec, with at least one skill and one subagent, connected to shared schemas, with a plugin.json declaring `fulfills`, `produces`, and `consumes`.

**Success:** `just install` works without errors. The plugin appears in the skill list. A user can trigger the skill via the CSO. The plugin's output validates against its declared output schema.

**Skills:**

- `basis/scaffold` — Triggered by "build a new plugin" or "create a plugin for X". Generates the full directory structure.
- `basis/audit` — Reviews an existing plugin for conformance: missing fields, schema mismatches, broken symlinks.
- `basis/schema` — Helps design a new shared schema, checks for conflicts with existing schemas.
- `basis/subagent` — Given a goal description, generates a well-formed subagent prompt with correct frontmatter, model/effort tiers, and output shape.

**Agents:**

| Agent | Model | Effort | Purpose |
|---|---|---|---|
| `basis-scaffolder` | sonnet | medium | Generate plugin directory and starter files |
| `basis-auditor` | sonnet | medium | Audit existing plugin for conformance |
| `basis-schema-designer` | sonnet | medium | Design or review shared schemas |

**Replaces:** `agent-plugin-builder`

---

## The `axiom` Protocol

`axiom` is the quality gate that all stage transitions must pass through. Any plugin can be an exit gate by implementing the axiom protocol in its final subagent.

**Protocol:**

```json
{
  "artifact_type": "spec@1",
  "artifact_path": "docs/specs/feature.md",
  "criteria": [
    "Every acceptance criterion is a testable proposition",
    "No ambiguous requirements (TBDs, 'as appropriate', 'etc.')",
    "Error cases are specified for each happy-path"
  ]
}
```

**Verdict:**

```json
{
  "verdict": "pass" | "fail",
  "confidence": "high" | "medium" | "low",
  "reasoning": "string (scratchpad, not forwarded)",
  "blockers": [
    { "criterion": "string", "finding": "string", "location": "string?" }
  ],
  "verdict_summary": "string"
}
```

If `verdict = fail`, blockers are returned to the producing stage. The producing agent retries with the specific blockers as context. After 3 retries without resolution, the gate escalates to the user with a structured summary.

---

## Stage Interface System

Any third party can substitute any stage implementation by publishing a plugin that:

1. Declares `"fulfills": "<stage-name>"` in `plugin.json`
2. Consumes the same input schema (e.g., `requirement@1`)
3. Produces the same output schema (e.g., `spec@1`)
4. Exposes the stage's declared `exclusivity` (additive or singleton)

The host resolves which plugin runs each stage at wiring time. If a user has a Jira plugin installed that `fulfills: "need"`, it runs in place of (or alongside) `graph`, depending on whether the stage is singleton or additive.

**Shared schemas live in `shared/schemas/`** — they are the public API. Plugins declare exact version compatibility (`requirement@1`, `research-report@2`). New versions are new files, never mutations.

**Stage registry at a glance:**

| Stage | Plugin | Exclusivity | Input | Output |
|---|---|---|---|---|
| need | graph | singleton | user text | requirement@1 |
| research | trace | additive | requirement@1 | research-report@1 |
| spec | canon | singleton | requirement@1 + research-report@1 | spec@1 |
| plan | vector | singleton | spec@1 | plan@1 |
| implementation | lambda | singleton | plan@1 | changeset@1 |
| verification | axiom | additive | any artifact | verdict@1 |
| shipping | delta | singleton | changeset@1 | release-artifact@1 |
| bug-hunting | proof | additive | workspace | finding-report@1 |
| meta | basis | singleton | user intent | plugin |

---

## `torii` — MCP Framework

`torii` is the framework for publishing these plugins as MCP servers, discoverable across Claude Code and ADK/AGY.

**What it provides:**
- Plugin manifest loading and capability graph construction
- Schema validation at wiring time (Haystack-style typed sockets)
- Axiom gate protocol (interrupt → retry → escalate)
- `/.well-known/agent.json` AgentCard generation from plugin.json
- Model and effort routing based on agent declarations
- Cross-platform subagent invocation (Claude `--subagent` and AGY dispatch)

**What it is NOT:** a runtime execution environment. `torii` handles wiring and verification. The agents do the work.

**Tech stack:** `michi` (output formatting) + TS MCP SDK. The framework is a thin shim — plugins do not depend on `torii` for their logic.

---

## Shared Resources

```
shared/
├── schemas/                 ← public API; versioned immutable schemas
│   ├── requirement@1.json
│   ├── research-report@1.json
│   ├── spec@1.json
│   ├── plan@1.json
│   ├── changeset@1.json
│   ├── finding-report@1.json
│   ├── verdict@1.json
│   ├── release-artifact@1.json
│   └── proposed/            ← experimental; requires requiresExperimental: true
├── references/              ← runtime-pullable by agents; language and tool guides
│   ├── rust.md              ← Rust hazard taxonomies, idioms, search heuristics
│   ├── typescript.md        ← TS/Node hazard taxonomies, idioms
│   ├── conventional-commits.md
│   ├── github.md            ← GH CLI, PR conventions, Actions annotations
│   ├── mcp-protocol.md
│   └── changesets.md
└── agent-best-practices.md  ← authoring-time manual for plugin authors
```

**Authoring-time vs runtime:** `agent-best-practices.md` and principles are for authors. Agents do not load it at runtime. `shared/references/*.md` files are for agents to pull at runtime when they need language-specific guidance. `shared/schemas/*.json` are always available to the host at wiring time.

**Symlinks:** each plugin contains a `shared -> ../../shared` symlink for local development. The installer resolves symlinks to `~/.claude/plugins/_shared/` with rewritten paths for the installed location.

---

## Directory Structure

```
plugins/
├── graph/
│   ├── plugin.json
│   ├── shared -> ../../shared
│   ├── skills/graph/SKILL.md
│   └── subagents/
│       ├── graph-intake.md
│       ├── graph-clarifier.md
│       └── graph-auditor.md
├── trace/
│   ├── plugin.json
│   ├── shared -> ../../shared
│   ├── references/          ← plugin-specific references (not in shared/)
│   ├── skills/trace/SKILL.md
│   └── subagents/
│       ├── trace-recon.md
│       ├── trace-reader.md
│       ├── trace-synthesizer.md
│       └── trace-risk-assessor.md
├── canon/  ...
├── vector/ ...
├── lambda/ ...
├── proof/  ...
├── axiom/  ...
├── delta/  ...
└── basis/  ...

shared/
├── schemas/
├── references/
└── agent-best-practices.md
```

---

## What We're Not Doing

**No plugin runtime execution engine.** Plugins are prompts and manifests. The execution layer is the host (Claude Code, AGY). We're not building a task runner.

**No centralized orchestrator.** Plugins hand off typed artifacts. The user decides when to advance stages. There's no automated pipeline running all stages in sequence without user intervention.

**No language-specific plugin splits.** `proof` replaces `bug-hunter-rust` and `bug-hunter-ts`. Language specificity lives in `shared/references/` and the recon agent handles detection.

**No prescriptive step scripts.** Plugin prompts express goals and output shapes. Agents decide how to get there.

---

## Build Order

The following order respects dependencies and maximizes early usability:

1. **`shared/schemas/`** — schemas first, everything else depends on them
2. **`axiom`** — the cross-cutting gate; needed by all other plugins
3. **`proof`** — high independent value; no dependencies on other plugins
4. **`delta`** — high independent value; users can start shipping immediately
5. **`graph` + `canon`** — requirements and spec together
6. **`trace`** — depends on knowing what to research (graph)
7. **`vector`** — depends on spec (canon)
8. **`lambda`** — depends on plan (vector)
9. **`basis`** — the meta-plugin; benefits from the full ecosystem existing

---

## Supersedes

This document supersedes `2026-08-04-verify-first-design.md`. The `verify-first` plugin is now named `axiom`. Its design remains valid as the axiom specification; this document adds the broader ecosystem context. The existing `verify-first` spec's subagent designs (`axiom-recon`, `axiom-verifier`, `axiom-exit-gate`) are adopted verbatim with name changes.

Plugin renaming:
- `bug-hunter-rust` → `proof` (with rust language reference)
- `bug-hunter-ts` → `proof` (with ts language reference)
- `agent-plugin-builder` → `basis`
- `verify-first` → `axiom`
