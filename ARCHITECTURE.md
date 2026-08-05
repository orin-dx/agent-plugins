# Architecture

How plugins are structured, how agents communicate, how context is managed, and how the verification gate works.

---

## 1. Progressive Disclosure

Context is loaded on demand. Every agent's context window contains only what its current task requires.

```mermaid
flowchart TD
    T1["**Tier 1 · Metadata**
    Frontmatter description · 80–200 words
    Always active — used by model router to match skill or subagent"]

    T2["**Tier 2 · Body**
    SKILL.md or subagents/*.md · under 200 words
    Loaded on trigger when a skill activates or subagent is dispatched"]

    T3["**Tier 3 · References**
    shared/references/*.md · shared/schemas/*.json
    Pulled on demand by the agent during task execution"]

    T1 -->|on trigger| T2
    T2 -->|on demand| T3
```

Subagents pull reference files themselves using their file reading tool. The host never pre-loads them.

---

## 2. Plugin Structure

```
plugins/<id>/
├── plugin.json              ← Manifest: id, version, skills, agents list
├── README.md                ← Plugin documentation
├── skills/<id>/SKILL.md     ← Skill prompt (what the user invokes)
├── subagents/*.md           ← Individual subagent prompts
└── shared -> ../../shared   ← Symlink for local reference access
```

`plugin.json` fields: `id`, `version` (semver), `skills` (list of skill IDs), `agents` (list of subagent names).

---

## 3. The Lifecycle Pipeline

Nine plugins form a directed pipeline. Each stage produces a typed artifact consumed by the next.

```mermaid
flowchart LR
    gr["**graph**\nneed"] -->|requirement@1| tr["**trace**\nresearch"]
    tr -->|research-report@1| ca["**canon**\nspec"]
    ca -->|spec@1| ve["**vector**\nplan"]
    ve -->|plan@1| la["**lambda**\ncode"]
    la -->|changeset@1| ax["**axiom**\ngate"]
    ax -->|verdict@1| de["**delta**\nship"]
    de -. iterate .-> gr

    pr(["**proof**\naudit"]) -. finding-report@1 .-> de
    ba(["**basis**\nmeta"]) -. scaffold .-> gr
```

**Composable:** any contiguous subset installs cleanly. Start at `canon` if requirements come from an external tracker. End at `axiom` if automated release notes aren't needed.

**Substitutable:** any stage can be replaced by a different implementation that honours the same schema contract. A Jira plugin replacing `graph` just needs to emit `requirement@1`.

---

## 4. Shared Schema Contract

Schemas in `shared/schemas/` are the inter-agent API surface. Rules:

- **Format:** JSON Schema draft-2020-12
- **Strict:** `additionalProperties: false` on all schemas — unknown fields are rejected at validation time
- **Scratchpad:** every schema includes `reasoning: string`, an unconstrained chain-of-thought field that is never forwarded downstream
- **Immutable versions:** `requirement@1.json` never changes; breaking changes produce `requirement@2.json`
- **Validation timing:** wiring time, before agent execution — not at runtime inside the agent

---

## 5. Model and Effort Tiering

Each subagent declares `model` and `effort` in its frontmatter. These are routing hints. Claude Code honours them directly; AGY applies its own model routing and ignores them.

```mermaid
flowchart TD
    H["**haiku · low**
    Mechanical — deterministic enumeration
    Manifest building, file inventory, commit message writing"]

    S["**sonnet · medium**
    Analysis — multi-step reasoning
    Scanning, drafting, planning, implementing, reviewing"]

    O["**opus · high**
    Judgment — weighing competing evidence
    Adversarial review, exit gates, final verdicts"]

    H --> S --> O
```

Use the lowest tier that produces correct output. Opus is reserved for decisions that produce a binding verdict with downstream consequences.

---

## 6. The Axiom Gate Protocol

`axiom` is a reusable, artifact-agnostic verification gate. Any artifact type — spec, plan, changeset, finding report — can be run through it.

```mermaid
flowchart LR
    Art[artifact + criteria] --> Recon["axiom-recon
    haiku / low"]
    Recon --> Ver["axiom-verifier
    sonnet / medium"]
    Ver --> Gate["axiom-exit-gate
    opus / high"]

    Gate -->|pass| Done(["verdict@1 · pass"])
    Gate -->|fail| Fix["producing agent
    targeted patch on blockers"]
    Fix -->|"retry ≤ 3"| Art
    Fix -->|"retry > 3"| Esc(["escalate to human"])
```

On `fail`, the orchestrator passes **only the blockers array** back to the producing agent — not the full artifact context — so it can make a targeted fix. On retry 2, the effort level escalates. After 3 retries, the circuit breaks and control passes to the human.

`retry_count` is tracked inside `verdict@1` and incremented by the exit gate on each pass.

---

## 7. Subagent Authoring Principles (Section 9)

Full checklist: `shared/agent-best-practices.md` Section 9. Key constraints:

| Constraint | Rule |
| :--- | :--- |
| **Description** | 80–200 words, starts with "Delegate to this subagent when…" |
| **Body** | Under 200 words — goal + output shape + non-obvious heuristics only |
| **XML sections** | No `<context>` or `<role>` that restate what the description already says |
| **Output shape** | Compact inline JSON example; if a named schema, reference the file |
| **Tool language** | Abstract ("use your file reading tool") — never tool-specific API names |
| **Reasoning** | Always in the output shape, always marked "not forwarded downstream" |
| **Runtime refs** | Subagents pull `shared/references/` files; never reference `agent-best-practices.md` at runtime |

---

## 8. Cross-Platform Compatibility

Plugins run natively in Claude Code and AGY — no custom server framework required.

| Concern | Approach |
| :--- | :--- |
| Model routing | `model`/`effort` frontmatter for Claude Code; AGY uses its own router |
| Tool calls | Abstract language — portable across both platforms |
| Paths | Relative only — `shared` symlink provides consistent paths from any plugin dir |
| Schema validation | Wiring-time, host-side — agents never validate JSON Schema directly |
