# Orin Visual & Design Specification (`orin-visual-standard.md`)

This standard defines the shared visual identity, diagramming color palettes, typography, and documentation voice across all **Orin DX** (`orin-dx`) and **Orin Axiom** (`orin-axi`) repositories and agent plugins.

---

## 1. Unified 6-Color Semantic Palette

All Mermaid diagrams, architectural charts, and terminal highlights must strictly adhere to the unified Orin semantic color tokens:

```text
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                          ORIN SEMANTIC PALETTE                                                 │
├──────────────┬─────────────┬─────────────┬─────────────┬───────────────────────────────────────────────────────┤
│ TOKEN NAME   │ FILL (HEX)  │ STROKE (2PX)│ TEXT (HEX)  │ SEMANTIC PURPOSE & COMPONENT ROLES                    │
├──────────────┼─────────────┼─────────────┼─────────────┼───────────────────────────────────────────────────────┤
│ Orin Indigo  │ `#EEF2FF`   │ `#6366F1`   │ `#1E1B4B`   │ Ingestion Sources, Entrypoints, Orchestrators, CLI    │
│ Orin Slate   │ `#F8FAFC`   │ `#64748B`   │ `#0F172A`   │ Data Stores, Sandboxes, In-Memory IR, AST Models      │
│ Orin Violet  │ `#F5F3FF`   │ `#8B5CF6`   │ `#4C1D95`   │ Analysis Engines, Accumulators, Tarjan DAG, Graders   │
│ Orin Amber   │ `#FFFBEB`   │ `#F59E0B`   │ `#78350F`   │ Routers, Deciders, Circuit Breakers, Snapshot Mergers │
│ Orin Emerald │ `#ECFDF5`   │ `#10B981`   │ `#064E3B`   │ Verified Outputs, Clean Reports, Scorecards, TUI Pass │
│ Orin Rose    │ `#FFF1F2`   │ `#F43F5E`   │ `#881337`   │ Failing Assertions, Anomaly Detection, Bug Flags      │
└──────────────┴─────────────┴─────────────┴─────────────┴───────────────────────────────────────────────────────┘
```

---

## 2. Standard Mermaid Class Definitions

Copy-paste these standard `classDef` blocks into any Mermaid flowchart:

```mermaid
flowchart TD
    classDef source fill:#eef2ff,stroke:#6366f1,stroke-width:2px,color:#1e1b4b,rx:8px,ry:8px;
    classDef store fill:#f8fafc,stroke:#64748b,stroke-width:2px,color:#0f172a,rx:8px,ry:8px;
    classDef engine fill:#f5f3ff,stroke:#8b5cf6,stroke-width:2px,color:#4c1d95,rx:8px,ry:8px;
    classDef router fill:#fffbeb,stroke:#f59e0b,stroke-width:2px,color:#78350f,rx:8px,ry:8px;
    classDef output fill:#ecfdf5,stroke:#10b981,stroke-width:2px,color:#064e3b,rx:8px,ry:8px;
    classDef alert fill:#fff1f2,stroke:#f43f5e,stroke-width:2px,color:#881337,rx:8px,ry:8px;
```

### Subgraph Styling Spec
```text
style SubgraphName fill:#fafafa,stroke:#cbd5e1,stroke-width:1.5px,stroke-dasharray: 4 4,rx:10px,ry:10px
```

### Sequence Diagram Theme Initialization
```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#eef2ff', 'primaryBorderColor': '#6366f1', 'primaryTextColor': '#1e1b4b', 'actorBkg': '#f8fafc', 'actorBorder': '#64748b', 'actorTextColor': '#0f172a', 'actorLineColor': '#94a3b8', 'signalColor': '#334155', 'signalTextColor': '#0f172a', 'labelBoxBkgColor': '#f5f3ff', 'labelBoxBorderColor': '#8b5cf6', 'labelTextColor': '#4c1d95', 'sequenceNumberColor': '#6366f1' }}}%%
```

---

## 3. Node & Edge Formatting Standards

1. **Card Typographic Hierarchy**:
   - Header in bold: `<b>Entity Name</b>`
   - Subtitle / Spec in code or small tag: `<code>file/path.ext</code>` or `<br/>Description`
2. **Action-Annotated Edges**:
   - Always label transitions with concrete latency bounds or operation verbs:
     `A -->|< 0.08ms sniff| B`
     `B -->|Zero-copy streaming| C`
3. **Shape Rules**:
   - Components & Modules: Rounded Rectangles `["..."]` with `rx:8px, ry:8px`
   - Active Functions & Sniffers: Stadiums `(["..."])`
   - In-Memory IR & Transcripts: Cylinders `[("...")]`
   - Gates & Assertions: Hexagons `{{"..."}}`

---

## 4. Prose & Voice Guidelines

Moved to `shared/references/docs-voice.md` — the canonical voice standard across `orin-dx` and `orin-axi`. This section previously duplicated a subset of it; do not re-add voice rules here.

Formatting conventions specific to this file's diagramming/visual scope:
- Use centered hero headers with badges on root READMEs.
- Use GFM alerts (`> [!TIP]`, `> [!NOTE]`, `> [!IMPORTANT]`).
- Use `<details><summary><b>...</b></summary>...</details>` for dense reference catalogs.
- Technical precision: state memory allocations, time complexities ($O(N)$, $O(V+E)$), and latency targets explicitly; use LaTeX for math ($\text{Cost}(t)$, $\text{Hit Ratio}$).
