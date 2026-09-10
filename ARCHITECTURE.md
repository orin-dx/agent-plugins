# Architecture

System design for plugin authoring, lifecycle contracts, generated Codex distribution, validation, and release safety.

---

## 1. Progressive Disclosure

Context is loaded on demand. Every agent's context window contains only what its current task requires.

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis', 'nodeSpacing': 40, 'rankSpacing': 56}, 'themeVariables': {'fontFamily': 'Inter, ui-sans-serif, system-ui, sans-serif', 'fontSize': '14px', 'lineColor': '#94a3b8', 'edgeLabelBackground': '#ffffff'}}}%%
flowchart LR
    classDef source fill:#eef2ff,stroke:#6366f1,stroke-width:1.5px,color:#1e1b4b,rx:10px,ry:10px,font-weight:600;
    classDef engine fill:#f5f3ff,stroke:#8b5cf6,stroke-width:1.5px,color:#4c1d95,rx:10px,ry:10px;
    classDef store fill:#f8fafc,stroke:#64748b,stroke-width:1.5px,color:#0f172a,rx:10px,ry:10px;

    T1["<b>Tier 1 · Metadata</b><br/>Always-on routing description"]
    T2["<b>Tier 2 · Instructions</b><br/>Loaded when a skill or agent activates"]
    T3[("<b>Tier 3 · References</b><br/>Schemas and guidance loaded on demand")]

    T1 -->|"activate"| T2
    T2 -->|"load when needed"| T3

    class T1 source
    class T2 engine
    class T3 store
```

Agents pull reference files themselves using their file reading tool. The host never pre-loads them.

---

## 2. Plugin Structure

```
plugins/<id>/
├── plugin.json              ← Manifest: id, version, skills, agents list
├── README.md                ← Plugin documentation
├── CHANGELOG.md             ← Version history
├── skills/<id>/SKILL.md     ← Skill prompt (what the user invokes)
└── agents/*.md              ← Individual agent prompts
```

`plugin.json` fields: `id`, `version` (semver), `description`, `skills` (path to skills dir), `agents` (list of agent file paths).

A plugin defaults to one skill directory named after the plugin id. IF the plugin's scope covers several genuinely independent, heterogeneous intents on the same artifact — not a linear pipeline invoked as one flow — `skills/<id>/` may split into `skills/<skill-name>/SKILL.md` per skill instead; `courier`, `scribe`, `weaver`, and `mason` all do. The routing key is the directory name, not the frontmatter `name:` field. See `shared/constitution.md`'s Plugin Structure and Skill Names sections.

---

## 3. The Lifecycle Pipeline

Ten plugins form a directed pipeline. Structured handoffs use typed artifacts; implementation and shipping also exchange verified workspace state.

**The primary flow** — one direction, no side-taps:

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis', 'nodeSpacing': 40, 'rankSpacing': 56}, 'themeVariables': {'fontFamily': 'Inter, ui-sans-serif, system-ui, sans-serif', 'fontSize': '14px', 'lineColor': '#94a3b8', 'edgeLabelBackground': '#ffffff'}}}%%
flowchart LR
    classDef source fill:#eef2ff,stroke:#6366f1,stroke-width:1.5px,color:#1e1b4b,rx:10px,ry:10px,font-weight:600;
    classDef engine fill:#f5f3ff,stroke:#8b5cf6,stroke-width:1.5px,color:#4c1d95,rx:10px,ry:10px;
    classDef router fill:#fffbeb,stroke:#f59e0b,stroke-width:1.5px,color:#78350f,rx:10px,ry:10px,font-weight:600;
    classDef output fill:#ecfdf5,stroke:#10b981,stroke-width:1.5px,color:#064e3b,rx:10px,ry:10px,font-weight:600;

    we["<b>Weaver</b><br/>capture need"] -->|"requirement@1"| va["<b>Vanguard</b><br/>research"]
    va -->|"research-report@1"| sc["<b>Scribe</b><br/>specify"]
    mu["<b>Muse</b><br/>component spec"] -->|"spec@1"| na["<b>Navigator</b><br/>plan"]
    sc -->|"spec@1"| na
    na -->|"plan@1"| sm["<b>Smith</b><br/>implement"]
    sm -->|"verified change"| co["<b>Courier</b><br/>ship"]
    co -.->|"next need"| we

    class we,mu source
    class va,sc,sm engine
    class na router
    class co output
```

**Verification** — Sentinel and Ranger attach to the flow above but aren't stops in its sequence; the muted dashed boxes below are the same personas shown only as attachment points:

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis', 'nodeSpacing': 40, 'rankSpacing': 56}, 'themeVariables': {'fontFamily': 'Inter, ui-sans-serif, system-ui, sans-serif', 'fontSize': '14px', 'lineColor': '#94a3b8', 'edgeLabelBackground': '#ffffff'}}}%%
flowchart LR
    classDef store fill:#f8fafc,stroke:#64748b,stroke-width:1.5px,color:#0f172a,rx:10px,ry:10px;
    classDef router fill:#fffbeb,stroke:#f59e0b,stroke-width:1.5px,color:#78350f,rx:10px,ry:10px,font-weight:600;

    sc2["Scribe"]:::store
    sm2["Smith"]:::store
    co2["Courier"]:::store

    se{{"<b>Sentinel</b><br/>independent gate"}}
    ra{{"<b>Ranger</b><br/>defect audit"}}

    sc2 -.->|"spec@1"| se
    sm2 -.->|"code + verdict@3"| se
    sm2 -.->|"implementation-review@2"| sc2
    se -.->|"verdict@3"| co2

    sm2 -->|"live code"| ra
    ra -.->|"finding-report@2"| sc2

    class se,ra router
```

![Define](https://img.shields.io/badge/-Define-6366f1) ![Design](https://img.shields.io/badge/-Design-8b5cf6) ![Build](https://img.shields.io/badge/-Build-3b82f6) ![Verify](https://img.shields.io/badge/-Verify-f59e0b) ![Ship](https://img.shields.io/badge/-Ship-10b981)

*Pill-shaped nodes are cross-cutting checkpoints, not sequence stops. Solid arrows are direct handoffs; dashed arrows are verification side-channels. Ranger's input is the live codebase Smith just wrote, not a schema handoff — the one solid arrow in the second diagram.*

Smith resolves scoped defect families before its exit gate. A structural family enters Scribe as `implementation-review@2`, returns through the normal spec and plan gates, and ends with an architecture-model refresh after implementation passes.

**Composable:** any contiguous subset installs cleanly. Start at `scribe` if requirements come from an external tracker. End at `smith` if automated shipping tooling isn't needed. Layer `sentinel` in at any stage for an independent verification pass.

**Substitutable:** any stage can be replaced by a different implementation that honours the same schema contract. A Jira plugin replacing `weaver` just needs to emit `requirement@1`.

**Cross-cutting, not inline:** `sentinel`'s `plugin.json` declares `consumes: []` — nothing invokes it automatically. Smith's and Ranger's exit gates independently implement the same recon → verify → judge discipline Sentinel formalizes; they do not call Sentinel's agents. Install Sentinel for a standalone second opinion.

---

## 4. Shared Schema Contract

Schemas in `shared/schemas/` are the inter-agent API surface. Rules:

- **Format:** JSON Schema draft-2020-12
- **Strict:** `additionalProperties: false` on all schemas — unknown fields are rejected at validation time
- **Scratchpad:** every schema includes `reasoning: string`, a private reasoning field that is never forwarded downstream
- **Immutable versions:** `requirement@1.json` never changes; breaking changes produce `requirement@2.json`
- **Validation timing:** build checks validate wiring; each produced artifact validates before downstream consumption

`implementation-review@2` carries lineage, independent semantic candidate sites, boundary and input-space evidence, coverage gaps, related instances, structural assessments, and disposition. `verdict@3` separates verified scope, blockers, gaps, and pending checks.

### Verification evidence model

Verification is claim-driven, not tool-driven. Workflows choose available project-native checks from the language, repository capabilities, changed behavior, and failure cost.

| Claim | Evidence that can support it |
| :--- | :--- |
| A boundary preserves behavior | An observation at the nearest executable compile, serialization, process, network, storage, render, or environment boundary |
| Generated inputs explore the risk | A named generator plus a behavioral oracle that can reject bad output |
| A defect family is exhausted | Candidate sites derived independently from domain responsibility, state transitions, and architecture, with an outcome for each site |
| A fix is structurally complete | A shared root cause and an explicit decision: scoped repair, consolidation, or Scribe architecture remediation |
| Mutable or asynchronous behavior passes | Fresh state and terminal results for every relevant started check |

Unavailable or disproportionate checks become explicit coverage gaps; invoking a tool without a relevant oracle proves nothing. Rust, TypeScript/JavaScript, Python, and Go references suggest compatible tools without making one command mandatory.

`mason:evaluate` tests workflow behavior with hidden-oracle fixtures. It records the fixture, route, harness, host, model, mode, roles, plugin versions, source revisions, workspace state, detections, false passes, corrections, duration, and available usage counts. Structural parity remains a build check; behavioral improvement requires comparable evidence.

---

## 5. Model and Effort Tiering

Each Claude/AGY source subagent declares `model` and `effort` as routing hints. Claude Code honours them directly; AGY applies its own routing. Codex uses host-selected models and native role cards, so tier intent carries across harnesses without copying model configuration.

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis', 'nodeSpacing': 40, 'rankSpacing': 56}, 'themeVariables': {'fontFamily': 'Inter, ui-sans-serif, system-ui, sans-serif', 'fontSize': '14px', 'lineColor': '#94a3b8', 'edgeLabelBackground': '#ffffff'}}}%%
flowchart LR
    classDef store fill:#f8fafc,stroke:#64748b,stroke-width:1.5px,color:#0f172a,rx:10px,ry:10px;
    classDef engine fill:#f5f3ff,stroke:#8b5cf6,stroke-width:1.5px,color:#4c1d95,rx:10px,ry:10px;
    classDef router fill:#fffbeb,stroke:#f59e0b,stroke-width:1.5px,color:#78350f,rx:10px,ry:10px,font-weight:600;

    H["<b>haiku · low</b><br/>deterministic enumeration"]
    S["<b>sonnet · medium</b><br/>analysis and execution"]
    O{{"<b>opus · high</b><br/>binding judgment"}}

    H -.->|"judgment needed"| S
    S -.->|"binding verdict needed"| O

    class H store
    class S engine
    class O router
```

Use the lowest tier that produces correct output. Opus is reserved for decisions that produce a binding verdict with downstream consequences.

---

## 6. The Sentinel Gate Protocol

`sentinel` is a reusable, artifact-agnostic verification gate. Any artifact type — spec, plan, changeset, finding report — can be run through it.

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis', 'nodeSpacing': 40, 'rankSpacing': 56}, 'themeVariables': {'fontFamily': 'Inter, ui-sans-serif, system-ui, sans-serif', 'fontSize': '14px', 'lineColor': '#94a3b8', 'edgeLabelBackground': '#ffffff'}}}%%
flowchart LR
    classDef source fill:#eef2ff,stroke:#6366f1,stroke-width:1.5px,color:#1e1b4b,rx:10px,ry:10px,font-weight:600;
    classDef store fill:#f8fafc,stroke:#64748b,stroke-width:1.5px,color:#0f172a,rx:10px,ry:10px;
    classDef engine fill:#f5f3ff,stroke:#8b5cf6,stroke-width:1.5px,color:#4c1d95,rx:10px,ry:10px;
    classDef router fill:#fffbeb,stroke:#f59e0b,stroke-width:1.5px,color:#78350f,rx:10px,ry:10px,font-weight:600;
    classDef output fill:#ecfdf5,stroke:#10b981,stroke-width:1.5px,color:#064e3b,rx:10px,ry:10px,font-weight:600;
    classDef alert fill:#fff1f2,stroke:#f43f5e,stroke-width:1.5px,color:#881337,rx:10px,ry:10px,font-weight:600;

    Art["<b>Artifact</b><br/>criteria + current state"]

    subgraph check [Verification Chain]
        direction LR
        Recon["<b>Recon</b><br/>haiku · low"] --> Ver["<b>Verifier</b><br/>sonnet · medium"] --> Gate{{"<b>Exit gate</b><br/>opus · high"}}
    end

    Art --> Recon

    Fix["<b>Producing agent</b><br/>targeted blocker patch"]

    Gate -->|"pass"| Done(["verdict@3 · pass"])
    Gate -->|"fail"| Fix
    Fix -.->|"retry ≤ 3"| Art
    Fix -.->|"retry > 3"| Esc(["human escalation"])

    class Art source
    class Recon store
    class Ver engine
    class Gate router
    class Done output
    class Fix router
    class Esc alert

    style check fill:#fafafa,stroke:#cbd5e1,stroke-width:1.5px,stroke-dasharray: 4 4,rx:10px,ry:10px
```

On `fail`, the orchestrator passes **only the blockers array** back to the producing agent — not the full artifact context — so it can make a targeted fix. On retry 2, the effort level escalates. After 3 retries, the circuit breaks and control passes to the human.

`retry_count` is tracked inside `verdict@3` and incremented by the exit gate on each attempt.

---

## 7. Agent Authoring Principles

Full guide: `shared/agent-best-practices.md`. Key constraints:

**5-part agent structure** — every Claude/AGY source agent defines:

| Part | Purpose |
| :--- | :--- |
| **Constitution** | Ecosystem-wide invariants, byte-identical across every agent — the shared cache prefix. Never authored per-agent; copied verbatim. |
| **Backstory** | 2–4 sentences of experiential perspective. What has this agent been burned by? What does it value? Guides judgment in the open interior. |
| **Goal** | What the agent must produce and why. Intent, not steps. |
| **Judgment** | How to know if the goal was genuinely achieved vs. output that looks like it was. Names the key failure mode. |
| **Output** | Structured output shape, referencing a schema from `shared/schemas/` when the output flows to another agent. |

Codex skills and role cards use native structures. Cross-harness parity applies to route names, artifacts, evidence, and acceptance intent—not prompt sections or delegation topology.

**Cognitive mode dispatch** — agents are dispatched by the cognitive mode they require, not their pipeline position.
- A scanner (exhaustive pattern matching, no filtering) and an adversary (default-to-skepticism, requires a concrete failing scenario) cannot share a mental mode — combining them produces an agent worse at both
- Modes: enumeration (haiku/low), tracing/analysis/repair (sonnet/medium), adversarial judgment (opus/high)
- A plugin with distinct scanning, tracing, adversarial, and repair phases has a dedicated agent per mode

**Progressive context loading** — each agent loads only the reference file for its cognitive phase.
- A `<load_first>` block names the specific `shared/references/` file — scanner loads hazards, architect loads smells, mutator loads tooling
- Never load all reference files into all agents — attention degrades when the context window contains material the agent won't use

**Reference guidance** — runtime references improve judgment without replacing it.
- A heuristic is a candidate signal until live evidence confirms a reachable outcome
- Applicability, refutation, and disposition keep repository preferences from becoming universal defects or fixes
- Cross-language guidance covers each named target or records the unsupported target as a gap

**Radical candor** — agents state material concerns, evidence, consequence, and confidence directly. Friendly language stays respectful without softening blockers, manufacturing praise, or overstating certainty.

**EARS for edges only** — EARS notation (`WHEN`, `IF`, `WHILE`, `WHERE`) belongs in output contracts and never-do rules.
- Not in implementation steps or search strategies — those are the interior where agent judgment is the point
- Over-constraining the interior caps the agent at the level of the author's imagination

**Schema-driven handoffs** — where one agent's output is another's input, both reference the same schema file from `shared/schemas/`. The schema is the contract; the prompt describes the intent.

---

## 8. Cross-Harness Distribution

The repository has one lifecycle contract and harness-specific execution packages. Claude Code and AGY consume the authored plugins directly; Codex consumes a generated, materialized marketplace. No custom server framework is required.

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis', 'nodeSpacing': 40, 'rankSpacing': 56}, 'themeVariables': {'fontFamily': 'Inter, ui-sans-serif, system-ui, sans-serif', 'fontSize': '14px', 'lineColor': '#94a3b8', 'edgeLabelBackground': '#ffffff'}}}%%
flowchart LR
    classDef source fill:#eef2ff,stroke:#6366f1,stroke-width:1.5px,color:#1e1b4b,rx:10px,ry:10px,font-weight:600;
    classDef store fill:#f8fafc,stroke:#64748b,stroke-width:1.5px,color:#0f172a,rx:10px,ry:10px;
    classDef engine fill:#f5f3ff,stroke:#8b5cf6,stroke-width:1.5px,color:#4c1d95,rx:10px,ry:10px;
    classDef output fill:#ecfdf5,stroke:#10b981,stroke-width:1.5px,color:#064e3b,rx:10px,ry:10px,font-weight:600;

    ClaudeSource["<b>Claude source</b><br/>manifest · skills · agents"] --> Claude(["Claude Code + AGY<br/>source marketplace"])
    SharedManifest[("<b>Shared manifest</b><br/>ID · version · contracts")] --> Build["<b>Codex generator</b><br/>validate + materialize"]
    CodexSource["<b>Native Codex source</b><br/>manifest · skills · resources"] --> Build
    Catalog[("<b>Codex catalog</b><br/>order · runtime files")] --> Build
    Schemas[("<b>Shared schemas</b><br/>versioned contracts")] --> Claude
    Schemas --> Build
    Build --> Codex(["Codex<br/>generated marketplace"])

    class ClaudeSource,CodexSource source
    class SharedManifest,Catalog,Schemas store
    class Build engine
    class Claude,Codex output
```

| Concern | Claude Code and AGY | Codex |
| :--- | :--- | :--- |
| Plugin metadata | `plugins/<id>/plugin.json` | Native `.codex-plugin/plugin.json`, version- and author-checked against the shared manifest |
| Workflow implementation | Authored skills and specialist agents | Separately authored skills in `harnesses/codex/plugins/<id>/skills/` |
| Delegation | Named agents where the host supports them | Optional agent teams using packaged cognitive-mode role cards; complete single-agent fallback |
| Durable handoffs | Versioned JSON schemas in `shared/schemas/` | Identical bytes materialized only where the native workflow needs them |
| Runtime paths | Relative paths; source symlinks may provide shared context | Regular files only; generated output contains no symlinks |
| Marketplace root | Repository root marketplace files | `.agents/plugins/marketplace.json`, pointing at `dist/codex/` |

`plugins/<id>/plugin.json` remains authoritative for shared ID, version, author, and produced/consumed artifacts. `harnesses/codex/plugins/<id>/` owns the Codex manifest, skills, category, capability, resource, and team-use choices. `harnesses/codex/catalog.json` owns marketplace order and runtime-file materialization. `tools/build-codex-marketplace.py` atomically packages `dist/codex` and writes the root discovery manifest; generated files are reviewed and released with their sources, never edited by hand.

The schema is the cross-harness contract. Named agents, model routing, prompt wording, tool availability, and delegation strategy are harness-specific implementation details.

- A source change is shared only when it affects plugin identity or a versioned artifact contract.
- A workflow change is compatible only when both harnesses preserve the intended schema, evidence, and acceptance criteria; transcript or prose identity is not required.
- Codex may use an agent team for independent work, but a missing team capability never blocks the single-agent workflow.

Repository-local Entire adapters under `.agents/skills/`, `.claude/skills/`, `.cursor/`, `.gemini/skills/`, and `.opencode/` expose session-history search across supported hosts. They are Entire-managed development integrations, not Wisp plugin sources or Codex marketplace build inputs.

---

## 9. Codex Marketplace Build System

`dist/codex` is a reproducible build artifact, not a second authored plugin tree. The generator packages native Codex sources without rewriting them, while rejecting ID, version, author, and skill-set drift from the shared plugin contract.

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis', 'nodeSpacing': 40, 'rankSpacing': 56}, 'themeVariables': {'fontFamily': 'Inter, ui-sans-serif, system-ui, sans-serif', 'fontSize': '14px', 'lineColor': '#94a3b8', 'edgeLabelBackground': '#ffffff'}}}%%
flowchart LR
    classDef source fill:#eef2ff,stroke:#6366f1,stroke-width:1.5px,color:#1e1b4b,rx:10px,ry:10px,font-weight:600;
    classDef store fill:#f8fafc,stroke:#64748b,stroke-width:1.5px,color:#0f172a,rx:10px,ry:10px;
    classDef engine fill:#f5f3ff,stroke:#8b5cf6,stroke-width:1.5px,color:#4c1d95,rx:10px,ry:10px;
    classDef router fill:#fffbeb,stroke:#f59e0b,stroke-width:1.5px,color:#78350f,rx:10px,ry:10px,font-weight:600;
    classDef output fill:#ecfdf5,stroke:#10b981,stroke-width:1.5px,color:#064e3b,rx:10px,ry:10px,font-weight:600;

    Manifest[("<b>Shared manifest</b><br/><code>plugins/id/plugin.json</code>")] --> Builder["<b>Marketplace builder</b><br/><code>build-codex-marketplace.py</code>"]
    ClaudeSkills[("<b>Skill inventory</b><br/><code>plugins/id/skills</code>")] --> Builder
    Native["<b>Native Codex source</b><br/>manifest · skills · resources"] --> Builder
    Catalog[("<b>Codex catalog</b><br/>order · runtime files")] --> Builder
    Schemas[("<b>Shared schemas</b><br/>versioned contracts")] --> Builder
    Builder --> Temp[("temporary regular-file bundle")]
    Temp --> Check{{"<b>Check mode</b><br/>tree + byte comparison"}}
    Temp --> Publish["<b>Publish mode</b><br/>atomic replace"]
    Publish --> Discovery[("<b>Discovery manifest</b><br/><code>.agents/plugins/marketplace.json</code>")]
    Discovery --> Bundle(["<b>Codex bundle</b><br/><code>dist/codex</code>"])

    class Native source
    class Manifest,ClaudeSkills,Catalog,Schemas,Temp,Discovery store
    class Builder,Publish engine
    class Check router
    class Bundle output
```

| Input | Authoritative for | Generator behavior |
| :--- | :--- | :--- |
| `plugins/<id>/plugin.json` | Shared plugin ID, version, author, `consumes`, and `produces` | Verifies the catalog ID plus native version and author match the shared source |
| `plugins/<id>/skills/*/SKILL.md` | Required skill-name inventory | Requires exact native Codex skill-name parity; does not copy or transform Claude prompt bodies |
| `harnesses/codex/plugins/<id>/` | Native Codex manifest, workflows, resources, and team policy | Copies authored regular-file content byte-for-byte into the bundle |
| `harnesses/codex/catalog.json` | Marketplace identity, plugin order, and runtime dependencies | Rejects unknown or duplicate plugin IDs and materializes only declared runtime files |
| `shared/schemas/` | Durable inter-harness artifact contracts | Materializes declared regular-file schema copies into the relevant Codex plugins |

### Build guarantees

- The generator resolves every input path beneath the repository root and rejects links that escape it.
- Runtime source links are dereferenced into regular files; generated bundles contain no symlinks.
- Authored native manifests and skill files are copied byte-for-byte; generated marketplace order follows the catalog.
- A normal build writes into a sibling temporary directory, then replaces `dist/codex` only after successful generation.
- If a build fails after moving the previous output aside, the generator restores the previous output.
- `--check` builds the expected tree in a temporary directory and fails on missing files, stale files, symlinks, or byte differences without changing generated artifacts.

## 10. Generated Marketplace Contract

Codex discovers marketplaces only from the repository-root `.agents/plugins/marketplace.json`. The generator writes that discovery manifest with entry paths into `dist/codex`; the bundle also carries a self-contained manifest for local bundle testing.

```text
.agents/plugins/marketplace.json           # Git discovery entries -> ./dist/codex/plugins/<id>
dist/codex/
├── .agents/plugins/marketplace.json       # Standalone bundle entries -> ./plugins/<id>
└── plugins/<id>/
    ├── .codex-plugin/plugin.json          # Authored native Codex manifest
    ├── skills/<skill>/SKILL.md             # Authored native Codex workflow
    ├── agent-roles/*.md                    # Packaged cognitive-mode delegation cards
    ├── shared/schemas/*.json               # Materialized contracts needed by this plugin
    └── shared/references/*.md              # Materialized only when a native skill declares it
```

The generated bundle intentionally omits Claude agent files. A Codex skill owns its workflow, uses shared JSON contracts, and may request a team only when that runtime capability exists. It selects a packaged role card before delegation; the role card guides cognitive mode and ownership but is not a TOML runtime configuration. This prevents a host-specific Claude agent topology from becoming a false Codex runtime contract.

## 11. Validation and Release Model

Validation is layered so each check owns a distinct failure class.

| Gate | Command or mechanism | Failure prevented |
| :--- | :--- | :--- |
| JSON shape | `jq` in CI | Invalid marketplace, manifest, schema, or Codex catalog JSON |
| Source wiring | `shared/scripts/validate-wiring.sh` | Missing schema files or producer/consumer declarations with no source |
| Source documentation | `scripts/check-skills-doc.sh` | Documented skills without a matching source directory |
| Version consistency | `scripts/check-versions.sh` | Plugin version disagreement across manifest, README, changelog, and marketplace |
| Native build behavior | `tests/test_build_codex_marketplace.py` | Native manifest/skill rewriting, source/native skill drift, version drift, stale output retention, unsafe runtime collisions, and symlink output |
| Native source contract | `tests/test_codex_native_sources.py` | Missing native sources, invalid required manifest or skill metadata, source/native skill inventory drift, or rewritten release files |
| Cross-harness compatibility | `tests/test_cross_harness_artifacts.py` | Changed portable contract bytes or missing lifecycle producer/consumer links |
| Release drift | `tools/build-codex-marketplace.py --check` | Generated root discovery or `dist/codex` artifacts that differ from source inputs |
| Diagram syntax | `scripts/check-mermaid.sh` | Markdown diagrams that cannot render |

CI runs the catalog JSON, native build, compatibility, drift, version, source-documentation, reference-size, and Mermaid checks. The release payload and its native-source, catalog, and schema change belong in the same review; a generated-only change is not a valid release.

## 12. Failure Containment and Compatibility Boundaries

| Condition | System response | Recovery |
| :--- | :--- | :--- |
| Malformed catalog, missing native skill, duplicate plugin ID, or native/shared identity mismatch | Generator exits before replacing the existing bundle | Correct the authored input, regenerate, and run `--check` |
| Runtime file resolves outside the repository | Generator rejects the path | Use a repository-contained source file or copy the required artifact into a tracked source location |
| Source or generated marketplace artifacts change without regeneration | Drift check fails | Regenerate `.agents/plugins/marketplace.json` and `dist/codex`, then review source plus output together |
| Portable schema changes incompatibly | Existing consumers cannot safely assume the old shape | Add a new schema version; do not mutate the existing version |
| Agent teams are unavailable | Codex skill does not delegate | Complete the same workflow in one agent and preserve the same artifact contract |
| Two harnesses produce different prose or reasoning | Not automatically a compatibility failure | Run [`docs/codex-behavioral-evaluation.md`](./docs/codex-behavioral-evaluation.md) and compare valid artifacts, evidence, and acceptance criteria |

The compatibility fixture covers the core `requirement@1 → research-report@1 → spec@1 → plan@1` lifecycle plus Smith's `implementation-review@2 → scribe:architect` structural escalation. It proves shared schema validity, materialized schema identity, and declared handoff links; it does not prove model-equivalent judgment, tool use, or transcript content.
