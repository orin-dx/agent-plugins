<h1 align="center">Orin DX Agent Plugins</h1>

<p align="center">
  <b>Official AI Agent Plugins & Skills Marketplace for Antigravity (AGY), Claude Code, and Cursor.</b><br />
  <i>Self-contained, domain-focused AI agent plugins for bug hunting, infrastructure, web guidance, security, and release engineering.</i>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License" /></a>
  <a href="marketplace.json"><img src="https://img.shields.io/badge/Schema-marketplace.json%20v1.0-success.svg" alt="Schema" /></a>
</p>

---

## Plugin Categories

`orin-dx/agent-plugins` hosts modular plugins across 4 core engineering domains:

1. **Language & Framework Bug Hunters**: `bug-hunter-rust`, `bug-hunter-ts`, `bug-hunter-python`, `bug-hunter-go`
2. **Infrastructure & CI/CD Pipelines**: `github-actions-auditor`, `docker-security-audit`, `terraform-gcp-architect`
3. **Web, Accessibility & UX**: `a11y-auditor`, `modern-web-guidance`, `chrome-devtools`
4. **Security & Release Engineering**: `sec-audit-owasp`, `release-engineering`

---

## Available Plugins

| Plugin ID | Domain / Category | Description | Manifest |
| :--- | :--- | :--- | :--- |
| **`bug-hunter-rust`** | Language (Rust) | 6 Rust Hazard Taxonomies (Unused flags, fixpoint staleness, UTF-8 BOM, crash-safety `.sync_all()`). | [`plugin.json`](./plugins/bug-hunter-rust/plugin.json) |
| **`bug-hunter-ts`** | Language (TypeScript) | 6 TS Hazard Taxonomies (`as any` casting, floating promises, SSR hydration, falsy traps, event leak cleanups). | [`plugin.json`](./plugins/bug-hunter-ts/plugin.json) |

---

## Shared Framework Files (Non-Plugin Context)

Shared debugging laws and report evaluation standards are stored centrally in `shared/` and referenced by plugins on demand:

- [**`shared/debugging-laws.md`**](./shared/debugging-laws.md): Core debugging principles, proof requirements, and red-to-green verification steps.
- [**`shared/report-template.md`**](./shared/report-template.md): Technical report evaluation format for confirmed findings.

---

## Quick Start (3 Setup Options)

### Option 1: Antigravity CLI (`agy`)

#### Global Installation (All Local Projects)
```bash
git clone https://github.com/orin-dx/agent-plugins.git ~/.gemini/config/plugins/agent-plugins
```

#### CLI Marketplace Command
```bash
agy plugin add orin-dx/agent-plugins/bug-hunter-rust
agy plugin add orin-dx/agent-plugins/bug-hunter-ts
```

#### Workspace Project Submodule
Add directly into a specific repository (e.g., `callisto`):
```bash
git submodule add https://github.com/orin-dx/agent-plugins.git .agents/plugins/agent-plugins
```

---

### Option 2: Claude Code

```bash
claude plugin add orin-dx/agent-plugins/bug-hunter-rust
claude plugin add orin-dx/agent-plugins/bug-hunter-ts
```

---

## Repository Architecture

```text
agent-plugins/
├── marketplace.json                        <-- Marketplace Index (AGY & Claude Code)
├── AGENTS.md                               <-- AI Agent Rules & Invariants
├── CLAUDE.md                               <-- Claude Code Specific Guidelines
├── README.md                               <-- Marketplace Home Page & Sitemap
├── CONTRIBUTING.md                         <-- Plugin Authoring & PR Guide
├── ARCHITECTURE.md                         <-- Multi-Agent Pipeline & Token Rationale
├── shared/                                 <-- SHARED CONTEXT (NOT PLUGINS)
│   ├── debugging-laws.md                   <-- Universal Debugging Principles
│   └── report-template.md                  <-- Technical Report Standard
└── plugins/
    ├── bug-hunter-rust/                    <-- Rust Bug Hunter Plugin
    │   ├── plugin.json
    │   ├── skills/bug-hunter-rust/SKILL.md
    │   └── subagents/
    │       ├── bug-hunter-scanner-rust.md
    │       ├── bug-hunter-adversary-rust.md
    │       └── bug-hunter-remediator-rust.md
    └── bug-hunter-ts/                      <-- TS Bug Hunter Plugin
        ├── plugin.json
        ├── skills/bug-hunter-ts/SKILL.md
        └── subagents/
            ├── bug-hunter-scanner-ts.md
            ├── bug-hunter-adversary-ts.md
            └── bug-hunter-remediator-ts.md
```

---

## Key Architectural Principles

1. **Domain-Scoped Plugins**: Plugins are focused on specific stacks or tasks (Rust, TS, GitHub Actions, Web Accessibility). Repositories load only the plugins required for their domain, reducing prompt token overhead by ~80%.
2. **On-Demand Context References**: Shared principles live in `shared/`. Plugins link to shared files using relative Markdown links, keeping prompt turns token-lean until a task is executed.
3. **Hazard-Taxonomy Partitioning**: Multi-agent audits partition subagents by failure category (Scanner ➔ Adversary ➔ Remediator) across the target codebase.
4. **Red-to-Green Verification Law**: Remediator subagents write a failing regression test first (red) before applying minimal code fixes (green).

---

## License

MIT © Gabriel Castro (Orin DX)