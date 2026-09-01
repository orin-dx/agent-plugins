<div align="center">
  <img src="./assets/logo.svg" alt="Orin Agent Plugins" width="400px" />
</div>

<p align="center">
  <i>Ten cooperating plugins covering the full development lifecycle, connected by shared JSON schemas and a common verification gate.</i>
</p>

<p align="center">
  <b>Use this when you're building non-trivial software with AI coding agents and need to know every acceptance criterion was implemented and tested — not assumed.</b> The specific problem: agents working across long sessions silently drop criteria as context compresses. Specs live on disk. Agents read from disk. Drift is detectable, not silent.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License" /></a>
  <a href="marketplace.json"><img src="https://img.shields.io/badge/Marketplace-v4.2.0-success.svg" alt="Marketplace v4.2.0" /></a>
  <a href="ARCHITECTURE.md"><img src="https://img.shields.io/badge/Docs-Architecture-informational.svg" alt="Architecture" /></a>
</p>

---

## Wisp — the Lifecycle Ecosystem

Ten plugins, each a specialist persona covering one stage of the development lifecycle — together they're **Wisp**. Each produces a typed output schema consumed by the next stage. They're composable: install only the personas your workflow needs.

**The primary flow** — one direction, no side-taps:

```mermaid
%%{init: {'flowchart': {'curve': 'basis', 'nodeSpacing': 44, 'rankSpacing': 68}}}%%
flowchart LR
    classDef define fill:#eef2ff,stroke:#6366f1,stroke-width:1.5px,color:#1e1b4b,rx:10,ry:10,font-size:16px,font-weight:600;
    classDef design fill:#f5f3ff,stroke:#8b5cf6,stroke-width:1.5px,color:#4c1d95,rx:10,ry:10,font-size:16px,font-weight:600;
    classDef build fill:#eff6ff,stroke:#3b82f6,stroke-width:1.5px,color:#1e3a8a,rx:10,ry:10,font-size:16px,font-weight:600;
    classDef ship fill:#ecfdf5,stroke:#10b981,stroke-width:1.5px,color:#064e3b,rx:10,ry:10,font-size:16px,font-weight:600;

    we[Weaver\nneed] -->|"requirement@1"| va[Vanguard\nresearch]
    va -->|"research-report@1"| sc[Scribe\nspec]
    mu[Muse\ncomponent spec] -->|"spec@1"| na[Navigator\nplan]
    sc -->|"spec@1"| na
    na -->|"plan@1"| sm[Smith\ncode]
    sm -->|"changeset@2"| co[Courier\nship]
    co -. iterate .-> we

    class we,va define
    class sc,mu design
    class na,sm build
    class co ship
```

**Verification** — Sentinel and Ranger attach to the flow above but aren't stops in its sequence; the muted dashed boxes below are the same personas shown only as attachment points:

```mermaid
%%{init: {'flowchart': {'curve': 'basis', 'nodeSpacing': 40, 'rankSpacing': 60}}}%%
flowchart LR
    classDef anchor fill:#f8fafc,stroke:#cbd5e1,stroke-width:1px,color:#64748b,rx:10,ry:10,font-size:13px,stroke-dasharray:4 3;
    classDef verify fill:#fffbeb,stroke:#f59e0b,stroke-width:1.5px,color:#78350f,rx:10,ry:10,font-size:15px,font-weight:600;

    sc2[Scribe]:::anchor
    sm2[Smith]:::anchor
    co2[Courier]:::anchor

    se([Sentinel\ngate])
    ra([Ranger\naudit])

    sc2 -.->|"spec@1"| se
    sm2 -.->|"changeset@2"| se
    se -.->|"verdict@1"| co2

    sm2 -->|"live code"| ra
    ra -.->|"finding-report@1"| co2
    ra -.->|"finding-report@1"| sc2

    class se,ra verify
```

![Define](https://img.shields.io/badge/-Define-6366f1) ![Design](https://img.shields.io/badge/-Design-8b5cf6) ![Build](https://img.shields.io/badge/-Build-3b82f6) ![Verify](https://img.shields.io/badge/-Verify-f59e0b) ![Ship](https://img.shields.io/badge/-Ship-10b981) ![Meta](https://img.shields.io/badge/-Meta-64748b)

*Pill-shaped nodes are cross-cutting checkpoints, not sequence stops. Solid arrows are direct handoffs; dashed arrows are verification and meta side-channels. Ranger's input is the live codebase Smith just wrote, not a schema handoff — the one solid arrow in the second diagram.*

Grouped by what each persona actually does — five bands across the lifecycle, plus one that stands outside it and maintains the rest:

| Category | Persona | Job | Output |
| :--- | :--- | :--- | :--- |
| **Define** | [`weaver`](./plugins/weaver/) | Captures and structures scattered need into requirements | `requirement@1` |
| **Define** | [`vanguard`](./plugins/vanguard/) | Goes first — researches prior art, risk, and patterns before anyone commits to a direction | `research-report@1` |
| **Design** | [`scribe`](./plugins/scribe/) | Drafts and gates the unambiguous, binding spec | `spec@1` |
| **Design** | [`muse`](./plugins/muse/) | Drafts and gates component specs — props, variants, per-state behavior, accessibility | `spec@1` |
| **Build** | [`navigator`](./plugins/navigator/) | Decomposes the spec into an exact, step-by-step plan | `plan@1` |
| **Build** | [`smith`](./plugins/smith/) | Implements — design, code, comprehensive tests, mutation-tested, commit | `changeset@2` |
| **Verify** | [`sentinel`](./plugins/sentinel/) | Cross-cutting gate — confirms any artifact meets its criteria before the next stage begins | `verdict@1` |
| **Verify** | [`ranger`](./plugins/ranger/) | Hunts down real bugs through adversarial, evidence-based verification | `finding-report@1` |
| **Ship** | [`courier`](./plugins/courier/) | Commits, opens PRs, responds to review, writes changelogs and release notes | `release-artifact@2` |
| **Meta** | [`mason`](./plugins/mason/) | Lays the foundation — scaffolds new plugins, audits the rest for conformance | — |

---

## Design Principles

Four decisions shape how every plugin and agent in this repository is built. They are enforced by `shared/constitution.md` and explained in `shared/agent-best-practices.md`.

**Schema-Driven Development** — every handoff between agents is a typed JSON document.
- JSON Schema draft-2020-12 with `additionalProperties: false` — a schema-invalid output halts the pipeline before any downstream agent acts on bad data
- Schema versions are immutable — a breaking change creates `<name>@2.json`, never mutates the existing file
- Every schema includes a `reasoning` scratchpad field for chain-of-thought; never forwarded downstream

**EARS output contracts** — hard constraints live exclusively in `<output>` sections, using `WHEN / IF / WHILE / WHERE / THE SYSTEM SHALL`.
- Encodes what the agent must produce, must not produce, or must do under a specific condition
- The prompt interior — how the agent searches, reasons, and decides — is intentionally unconstrained
- EARS is the fence; backstory and goal fill the interior with judgment

**5-part agent structure** — every agent body has exactly five sections; no role labels, no success-criteria checklists.
- `<constitution>` — ecosystem-wide invariants, byte-identical across every agent (copied verbatim, never authored per-agent)
- `<backstory>` — experiential perspective that shapes judgment in open situations (not a role label)
- `<goal>` — intent, not steps
- `<judgment>` — the specific failure mode that looks like success
- `<output>` — schema reference and EARS contracts

**Cognitive mode separation** — agents are dispatched by the cognitive mode they require, not their pipeline position.
- A scanner (exhaustive pattern matching, no filtering) and an adversary (default-to-skepticism, requires a concrete failing scenario) cannot share a mental mode — combining them produces an agent worse at both
- Model and effort tiers follow the same logic: `haiku / low` for enumeration, `sonnet / medium` for analysis, `opus / high` for binding judgment

See [`ARCHITECTURE.md §7`](./ARCHITECTURE.md#7-agent-authoring-principles) for the full authoring guide, and [`docs/pipeline-walkthrough.md`](./docs/pipeline-walkthrough.md) for a concrete end-to-end example showing schemas at each stage.

---

## Shared Schema Contract

All inter-plugin handoffs are typed. Schemas live in `shared/schemas/` and use JSON Schema draft-2020-12 with `additionalProperties: false`. Schema versions are immutable — a breaking change requires a new file (e.g. `requirement@2.json`). Every schema includes a `reasoning` scratchpad field that is never forwarded downstream.

| Schema | Produced by | Consumed by |
| :--- | :--- | :--- |
| `requirement@1` | weaver | vanguard, scribe |
| `research-report@1` | vanguard | scribe |
| `spec@1` | scribe, muse | navigator, sentinel |
| `plan@1` | navigator | smith |
| `changeset@2` | smith | courier, sentinel |
| `verdict@1` | sentinel | any gate consumer |
| `verdict@2` | ranger | courier, humans (extends verdict@1 with flagged_for_review) |
| `finding-report@1` | ranger | courier, humans, architect |
| `field-survival-map@1` | boundary-tracer | adversary |
| `mutation-report@1` | mutator | exit-gate, implementer |
| `release-artifact@2` | courier | humans |

---

## Shared References

Runtime-pullable guides in `shared/references/`. Agents pull these themselves during task execution — they are not loaded into context at startup. Language reference files are split by concern so each agent loads only its phase slice.

| File | Purpose | Loaded by |
| :--- | :--- | :--- |
| `rust-hazards.md` | Rust hazard taxonomies T1–T6/T8/T9, grep patterns, before/after examples | scanner (always), adversary (non-T7/T10) |
| `rust-hazards-t7-t10.md` | Rust taxonomies T7 and T10 — boundary-tracer's entire scope | boundary-tracer (always), scanner (full scans), adversary (T7/T10) |
| `rust-smells.md` | Rust architectural smells and resolving trait designs | architect |
| `rust-tooling.md` | Rust test commands, NAPI rules, non-negotiables | mutator, remediator |
| `rust.md` | Thin index → routes to the files above | — |
| `typescript-hazards.md` | TS hazard taxonomies T1–T6/T8/T9, grep patterns, before/after examples | scanner (always), adversary (non-T7/T10) |
| `typescript-hazards-t7-t10.md` | TS taxonomies T7 and T10 — boundary-tracer's entire scope | boundary-tracer (always), scanner (full scans), adversary (T7/T10) |
| `typescript-smells.md` | TS architectural smells and interface/type designs | architect |
| `typescript-tooling.md` | TS test commands (Stryker, Vitest), non-negotiables | mutator, remediator |
| `typescript.md` | Thin index → routes to the files above | — |
| `conventional-commits.md` | Type/scope conventions and scope table | courier |
| `github.md` | PR template, `gh` CLI commands, labels | courier |
| `changesets.md` | Changeset vs commit distinction, semver decision guide | courier |
| `mcp-protocol.md` | MCP server lifecycle, tool definition format, A2A AgentCard | — |
| `modern-cli-tools.md` | ripgrep, fd, bat, jq, delta, fzf usage patterns | — |
| `interface-implementers.md` | Deterministic pre-scan for enumerating trait/interface implementers per language | challenger |
| `boundary-value-shapes.md` | Sum-type-over-bool default posture for boundary-crossing values, per-language examples | implementer |

---

## Quick Start

### Claude Code

Add this repo as a marketplace, then install the plugins you need:

```
/plugin marketplace add orin-dx/agent-plugins
/plugin install weaver
/plugin install vanguard
/plugin install scribe
/plugin install muse
/plugin install navigator
/plugin install smith
/plugin install sentinel
/plugin install courier
```

Install `ranger` and `mason` as needed:

```
/plugin install ranger
/plugin install mason
```

### Antigravity (AGY)

Install individual plugins via the native CLI (uses a Git URL):

```bash
agy plugin install https://github.com/orin-dx/agent-plugins.git
```

Or use [`agy-plugins-cli`](https://github.com/ZaunEkko/agy-plugins-cli) for an interactive TUI with update tracking:

```bash
npm install -g agy-plugins-cli
agy-plugin marketplace add orin-dx/agent-plugins
agy-plugin add weaver@orin-dx
agy-plugin add vanguard@orin-dx
agy-plugin add scribe@orin-dx
agy-plugin add muse@orin-dx
agy-plugin add navigator@orin-dx
agy-plugin add smith@orin-dx
agy-plugin add sentinel@orin-dx
agy-plugin add courier@orin-dx
agy-plugin add ranger@orin-dx
agy-plugin add mason@orin-dx
```

---

## Repository Structure

```
agent-plugins/
├── marketplace.json              ← Plugin registry
├── ARCHITECTURE.md               ← System architecture
├── CONTRIBUTING.md               ← Plugin authoring guide
├── shared/
│   ├── schemas/                  ← Versioned inter-agent JSON schemas
│   ├── references/               ← Runtime-pullable domain guides (split by concern)
│   └── agent-best-practices.md  ← Authoring-time principles
└── plugins/
    ├── weaver/                    ← Requirement capture
    ├── vanguard/                  ← Research synthesis
    ├── scribe/                    ← Specification drafting and gating
    ├── muse/                      ← Component spec drafting and gating
    ├── navigator/                 ← Implementation planning
    ├── smith/                     ← Implementation, mutation-tested
    ├── sentinel/                  ← Verification gate
    ├── courier/                   ← Ship tooling
    ├── ranger/                    ← Fast cross-language bug scan
    └── mason/                     ← Plugin scaffolding
```

---

## License

MIT © Gabriel Castro (Orin DX)
