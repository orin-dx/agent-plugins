<div align="center">
  <img src="./assets/logo.svg" alt="Orin Agent Plugins" width="400px" />
</div>

<p align="center">
  <i>Nine cooperating plugins covering the full development lifecycle, connected by shared JSON schemas and a common verification gate.</i>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License" /></a>
  <a href="marketplace.json"><img src="https://img.shields.io/badge/Marketplace-v2.0.0-success.svg" alt="Marketplace v2.0.0" /></a>
  <a href="ARCHITECTURE.md"><img src="https://img.shields.io/badge/Docs-Architecture-informational.svg" alt="Architecture" /></a>
</p>

---

## The Lifecycle Ecosystem

Nine plugins cover the complete path from raw idea to shipped release. Each plugin produces a typed output schema consumed by the next stage. They are composable — install only the stages your workflow needs.

```mermaid
flowchart LR
    gr[graph\nneed] -->|"requirement@1"| tr[trace\nresearch]
    tr -->|"research-report@1"| ca[canon\nspec]
    ca -->|"spec@1"| ve[vector\nplan]
    ve -->|"plan@1"| la[lambda\ncode]
    la -->|"changeset@1"| ax[axiom\ngate]
    ax -->|"verdict@1"| de[delta\nship]
    de -. iterate .-> gr

    pr([proof\naudit]) -.->|"finding-report@1"| de
    ba([basis\nmeta]) -. scaffold .-> gr
```

| Plugin | Stage | Purpose | Output |
| :--- | :--- | :--- | :--- |
| [`graph`](./plugins/graph/) | Need | Captures and structures requirements | `requirement@1` |
| [`trace`](./plugins/trace/) | Research | Surveys prior art, risks, and patterns | `research-report@1` |
| [`canon`](./plugins/canon/) | Spec | Drafts and gates unambiguous specifications | `spec@1` |
| [`vector`](./plugins/vector/) | Plan | Decomposes specs into sequenced, testable tasks | `plan@1` |
| [`lambda`](./plugins/lambda/) | Code | Implements tasks via TDD, gates on exit | `changeset@1` |
| [`axiom`](./plugins/axiom/) | Gate | Cross-artifact verification gate (reusable) | `verdict@1` |
| [`delta`](./plugins/delta/) | Ship | Commits, PRs, changelogs, and release notes | `release-artifact@1` |
| [`proof`](./plugins/proof/) | Audit | Fast cross-language bug scan before any release | `finding-report@1` |
| [`basis`](./plugins/basis/) | Meta | Scaffolds and audits new plugins | — |

---

## Design Principles

Four decisions shape how every plugin and agent in this repository is built. They are enforced by `shared/constitution.md` and explained in `shared/agent-best-practices.md`.

**Schema-Driven Development** — every handoff between agents is a typed JSON document. Schemas use JSON Schema draft-2020-12 with `additionalProperties: false`: a downstream agent cannot silently ignore a field, and a schema-invalid output halts the pipeline before any agent acts on bad data. Schema versions are immutable — a breaking change creates `<name>@2.json` rather than mutating the existing file. Every schema includes a `reasoning` scratchpad field that agents use for chain-of-thought; it is never forwarded downstream.

**EARS output contracts** — agent prompts use EARS notation (`WHEN / IF / WHILE / WHERE / THE SYSTEM SHALL`) exclusively in their `<output>` sections, encoding hard constraints on what the agent must produce, must not produce, or must do under a specific condition. The interior of a prompt — how the agent searches, reasons, and decides — is left unconstrained. EARS is the fence; the backstory and goal fill the interior with judgment.

**4-part agent structure** — every agent body has exactly four sections: `<backstory>` (experiential perspective that shapes judgment in open situations), `<goal>` (intent, not steps), `<judgment>` (the specific failure mode that looks like success), and `<output>` (schema reference and EARS contracts). No role labels. No success-criteria checklists. The structure encodes the difference between telling an agent what to pretend to be and telling it what it has learned.

**Cognitive mode separation** — agents are dispatched by the cognitive mode they require, not their pipeline position. A scanner (exhaustive pattern matching, no filtering) and an adversary (default-to-skepticism, requires a concrete failing scenario) run sequentially but cannot share a mental mode — combining them produces an agent worse at both. Model and effort tiers follow the same logic: `haiku / low` for mechanical enumeration, `sonnet / medium` for analysis, `opus / high` for binding judgment.

See [`ARCHITECTURE.md §7`](./ARCHITECTURE.md#7-agent-authoring-principles) for the full authoring guide, and [`docs/pipeline-walkthrough.md`](./docs/pipeline-walkthrough.md) for a concrete end-to-end example showing schemas at each stage.

---

## Shared Schema Contract

All inter-plugin handoffs are typed. Schemas live in `shared/schemas/` and use JSON Schema draft-2020-12 with `additionalProperties: false`. Schema versions are immutable — a breaking change requires a new file (e.g. `requirement@2.json`). Every schema includes a `reasoning` scratchpad field that is never forwarded downstream.

| Schema | Produced by | Consumed by |
| :--- | :--- | :--- |
| `requirement@1` | graph | trace, canon |
| `research-report@1` | trace | canon |
| `spec@1` | canon | vector, axiom |
| `plan@1` | vector | lambda |
| `changeset@1` | lambda | delta, axiom |
| `verdict@1` | axiom | any gate consumer |
| `finding-report@1` | proof | delta, humans, canon-architect |
| `field-survival-map@1` | proof-boundary-tracer | proof-adversary |
| `mutation-report@1` | lambda-mutator | lambda-exit-gate, lambda-implementer |
| `release-artifact@1` | delta | humans |

---

## Shared References

Runtime-pullable guides in `shared/references/`. Agents pull these themselves during task execution — they are not loaded into context at startup. Language reference files are split by concern so each agent loads only its phase slice.

| File | Purpose | Loaded by |
| :--- | :--- | :--- |
| `rust-hazards.md` | Rust hazard taxonomies T1–T10, grep patterns, before/after examples | scanner, adversary, boundary-tracer |
| `rust-smells.md` | Rust architectural smells and resolving trait designs | architect |
| `rust-tooling.md` | Rust test commands, NAPI rules, non-negotiables | mutator, remediator |
| `rust.md` | Thin index → routes to the three files above | — |
| `typescript-hazards.md` | TS hazard taxonomies T1–T10, grep patterns, before/after examples | scanner, adversary, boundary-tracer |
| `typescript-smells.md` | TS architectural smells and interface/type designs | architect |
| `typescript-tooling.md` | TS test commands (Stryker, Vitest), non-negotiables | mutator, remediator |
| `typescript.md` | Thin index → routes to the three files above | — |
| `conventional-commits.md` | Type/scope conventions and scope table | delta |
| `github.md` | PR template, `gh` CLI commands, labels | delta |
| `changesets.md` | Changeset vs commit distinction, semver decision guide | delta |
| `mcp-protocol.md` | MCP server lifecycle, tool definition format, A2A AgentCard | — |
| `modern-cli-tools.md` | ripgrep, fd, bat, jq, delta, fzf usage patterns | — |

---

## Quick Start

### Claude Code

Add this repo as a marketplace, then install the plugins you need:

```
/plugin marketplace add orin-dx/agent-plugins
/plugin install graph
/plugin install trace
/plugin install canon
/plugin install vector
/plugin install lambda
/plugin install axiom
/plugin install delta
```

Install `proof` and `basis` as needed:

```
/plugin install proof
/plugin install basis
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
agy-plugin add graph@orin-dx
agy-plugin add trace@orin-dx
agy-plugin add canon@orin-dx
agy-plugin add vector@orin-dx
agy-plugin add lambda@orin-dx
agy-plugin add axiom@orin-dx
agy-plugin add delta@orin-dx
agy-plugin add proof@orin-dx
agy-plugin add basis@orin-dx
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
    ├── graph/                    ← Requirement capture
    ├── trace/                    ← Research synthesis
    ├── canon/                    ← Specification drafting and gating
    ├── vector/                   ← Implementation planning
    ├── lambda/                   ← TDD implementation
    ├── axiom/                    ← Verification gate
    ├── delta/                    ← Ship tooling
    ├── proof/                    ← Fast cross-language bug scan
    └── basis/                    ← Plugin scaffolding
```

---

## License

MIT © Gabriel Castro (Orin DX)
