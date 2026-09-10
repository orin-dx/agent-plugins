# Orin Visual Standard

Use this visual system for Mermaid diagrams across Orin DX and Orin Axiom repositories.

---

## Semantic Palette

| Token | Fill | Stroke | Text | Use |
| :--- | :--- | :--- | :--- | :--- |
| Indigo · `source` | `#eef2ff` | `#6366f1` | `#1e1b4b` | Inputs, entrypoints, skills, orchestrators |
| Slate · `store` | `#f8fafc` | `#64748b` | `#0f172a` | Files, schemas, manifests, inventories, passive state |
| Violet · `engine` | `#f5f3ff` | `#8b5cf6` | `#4c1d95` | Analysis, transformation, implementation |
| Amber · `router` | `#fffbeb` | `#f59e0b` | `#78350f` | Decisions, gates, escalation, control flow |
| Emerald · `output` | `#ecfdf5` | `#10b981` | `#064e3b` | Verified or published outputs |
| Rose · `alert` | `#fff1f2` | `#f43f5e` | `#881337` | Failures, blockers, anomalies |

Use semantic roles, not arbitrary stage colors. A node keeps the same token wherever it appears.

---

## Flowchart Baseline

Start flowcharts with this theme and include only the classes the diagram uses:

```mermaid
%%{init: {'theme': 'base', 'flowchart': {'curve': 'basis', 'nodeSpacing': 40, 'rankSpacing': 56}, 'themeVariables': {'fontFamily': 'Inter, ui-sans-serif, system-ui, sans-serif', 'fontSize': '14px', 'lineColor': '#94a3b8', 'edgeLabelBackground': '#ffffff'}}}%%
flowchart LR
    classDef source fill:#eef2ff,stroke:#6366f1,stroke-width:1.5px,color:#1e1b4b,rx:10px,ry:10px,font-weight:600;
    classDef store fill:#f8fafc,stroke:#64748b,stroke-width:1.5px,color:#0f172a,rx:10px,ry:10px;
    classDef engine fill:#f5f3ff,stroke:#8b5cf6,stroke-width:1.5px,color:#4c1d95,rx:10px,ry:10px;
    classDef router fill:#fffbeb,stroke:#f59e0b,stroke-width:1.5px,color:#78350f,rx:10px,ry:10px,font-weight:600;
    classDef output fill:#ecfdf5,stroke:#10b981,stroke-width:1.5px,color:#064e3b,rx:10px,ry:10px,font-weight:600;
    classDef alert fill:#fff1f2,stroke:#f43f5e,stroke-width:1.5px,color:#881337,rx:10px,ry:10px,font-weight:600;
```

Use `LR` for pipelines and handoffs. Use `TD` for branching, hierarchy, or dense fan-out. Adjust spacing only when the default harms readability.

Style subgraphs as quiet containers:

```text
style SubgraphName fill:#fafafa,stroke:#cbd5e1,stroke-width:1.5px,stroke-dasharray:4 4,rx:10px,ry:10px
```

---

## Diagram Grammar

- Give multi-line cards a bold header and short subtitle: `["<b>Entity</b><br/><code>artifact@1</code>"]`.
- Use rounded rectangles `["..."]` for active components and agents.
- Use cylinders `[("...")]` for persisted data or durable artifacts.
- Use hexagons `{{"..."}}` for gates and decisions.
- Use stadiums `(["..."])` for terminal outputs or outcomes.
- Label an edge when the label adds an operation, condition, artifact, or bound. Leave obvious sequence edges unlabeled.
- Use solid edges for primary flow and dashed edges for optional, retry, feedback, or cross-cutting flow.
- Keep node text short. Put explanation in adjacent prose when it does not change the graph.

---

## Sequence Diagram Theme

```text
%%{init: {'theme': 'base', 'themeVariables': {'fontFamily': 'Inter, ui-sans-serif, system-ui, sans-serif', 'fontSize': '14px', 'primaryColor': '#eef2ff', 'primaryBorderColor': '#6366f1', 'primaryTextColor': '#1e1b4b', 'actorBkg': '#f8fafc', 'actorBorder': '#64748b', 'actorTextColor': '#0f172a', 'actorLineColor': '#94a3b8', 'signalColor': '#334155', 'signalTextColor': '#0f172a', 'labelBoxBkgColor': '#f5f3ff', 'labelBoxBorderColor': '#8b5cf6', 'labelTextColor': '#4c1d95', 'sequenceNumberColor': '#6366f1'}}}%%
```
