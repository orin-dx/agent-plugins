# Ecosystem Research Synthesis

**Date:** 2026-08-04
**Purpose:** Prior art synthesis to inform plugin ecosystem design decisions.
**Frameworks studied:** CrewAI, LangGraph, Semantic Kernel, Haystack, DSPy, Autogen, Google ADK, Anthropic multi-agent guidance, VS Code extensions, OpenAI plugin system, MCP, Continue.dev, Composio

---

## 1. Plugin Manifest — Static Registry Before Code Loads

**Source: VS Code, ADK AgentCards, OpenAI plugins**

VS Code's most important architectural insight: the host reads manifests and builds a capability registry *before* any plugin code executes. Activation is lazy — a plugin that provides Rust formatting only loads when a `.rs` file opens.

The manifest is purely declarative. It answers "what does this plugin provide?" without running anything. This is what makes cold-start plugin discovery feasible and safe.

**For our system:**

```json
{
  "id": "my-research-plugin",
  "version": "1.2.0",
  "fulfills": "research",
  "exclusivity": "additive",
  "produces": "research-report@1",
  "consumes": "requirement@1",
  "description": "Searches the web and internal docs...",
  "triggers": [
    { "on": "stage-start", "when": "stage == 'research'" }
  ],
  "entrypoint": "./plugin.js"
}
```

The host builds a stage-capability graph at startup: `{stage → [plugins]}`. It can answer "who handles research?" without loading any plugin.

**Additive vs. exclusive stages** (VS Code pattern):
- Additive: all plugins fulfilling the stage run; results are merged via reducer
- Exclusive: one plugin runs; priority-based selection; conflicts surfaced explicitly

Declare in manifest: `"exclusivity": "additive" | "singleton"`.

---

## 2. Schema Contracts — The Public API

**Source: LangGraph, Haystack, DSPy, VS Code**

**Haystack's insight:** typed socket connections are validated at *pipeline construction time*, not at runtime. You cannot connect a `List[Document]` output to a `str` input — the build fails. This is the strongest contract system studied.

**LangGraph's insight:** `TypedDict` + `Annotated` reducers. Every field that multiple plugins write to declares a reducer (`operator.add`, custom merge). Nodes declare `input_schema` (what they *see*) narrower than the full pipeline state (what *exists*). This scope isolation is key for plugin safety.

**What this means for `shared/schemas/`:**

Schemas are immutable — new version = new filename (`research-report@2.json` alongside `research-report@1.json`). Plugins declare exact version compatibility. The runtime validates at wiring time that `produces` and `consumes` schemas are compatible before any execution begins.

```
shared/schemas/
  requirement@1.json
  research-report@1.json
  research-report@2.json    ← new version, old one stays
  spec@1.json
  plan@1.json
  finding@1.json
  verdict@1.json
  changeset@1.json
```

Schemas are the public API. Breaking change = new file, never mutate in place.

**Conflict on concurrent writes:** if two additive plugins write to the same output field in the same stage, a reducer must be declared. Without one, the host raises an error at wiring time.

---

## 3. Output Enforcement — Constrain What Agents Return, Not How They Reason

**Source: DSPy, Autogen, CrewAI**

All three frameworks converge on the same principle: internal reasoning is unconstrained; output shape is enforced at the handoff boundary.

**DSPy's pattern:** include a `reasoning: str` output field as a scratchpad. The LLM writes its chain-of-thought there before producing the typed output fields. Reasoning is unconstrained; output is validated. The `reasoning` field travels with the artifact for debugging but is not forwarded to the next stage as input.

**Autogen's enforcement:** `output_content_type=MyPydanticModel` forces JSON schema mode at the model API level — the model cannot return a malformed response. This is the strongest enforcement: at generation, not post-hoc.

**CrewAI's retry:** `guardrails=[validate_fn]` runs validation inside the execution loop, not as a filter. The agent *sees* why it failed and adjusts. Up to 3 retries with specific failure messages.

**For our agents:**

Every handoff schema includes a `reasoning: str` field (output only, never consumed downstream). Output type is enforced at generation where possible (structured output mode). If validation fails, the agent retries with the specific failure message — not a silent rejection.

The agent's system message expresses the goal. The schema constrains what comes back. The agent decides how to get there.

---

## 4. Stage Routing

**Source: LangGraph, Autogen, VS Code**

**Three routing patterns — use the right one for each scenario:**

**1. Static sequential edges** (LangGraph): for fixed stage order (requirement → research → spec → plan). Declared at wiring time, auditable, no LLM cost. The default.

**2. Schema-based substitution** (VS Code contribution points): for "which plugin fulfills this stage?" — registry lookup at wiring time based on `fulfills` + version constraints. Deterministic, no LLM.

**3. Description-based LLM routing** (Autogen SelectorGroupChat): for "which agent should speak next given the conversation?" — a coordinator LLM reads agent descriptions. Use only for dynamic workflows where the next step is genuinely unknown at design time.

**The GPT Plugin lesson:** routing by prose description alone degrades when multiple plugins compete. Schema-based `fulfills` declaration is deterministic. Descriptions still matter for LLM selection but are not the primary routing mechanism.

**Conditional routing** (LangGraph Command primitive): a plugin can return `Command(update={...}, goto="next-stage")` to control its own routing. Use for conditional advancement ("skip spec if one already exists") without requiring a central coordinator.

---

## 5. Cooperation Within a Stage

**Source: LangGraph Send API, CrewAI context DAG**

When multiple additive plugins fulfill the same stage (e.g., three research plugins run in parallel), use LangGraph's **Send API + Annotated reducer pattern**:

1. A fan-out node sends each plugin its own `Send("research", {"artifact": input, "plugin_config": cfg})`
2. Each plugin runs independently with its own isolated state payload
3. Results accumulate via reducer: `Annotated[list[ResearchReport], operator.add]`
4. A merge node selects or combines the collected reports

The key: `Send` payloads carry plugin-private keys that don't pollute the shared stage state. Plugin-specific configuration travels with the work item.

For DAG-style dependencies (plugin B needs plugin A's output before starting), use CrewAI's explicit `context` edge pattern — declare dependencies, the runtime synchronizes.

---

## 6. Cross-Platform Portability

**Source: ADK, Anthropic, MCP**

**MCP is the convergence point.** Both Google ADK (`McpToolset`) and Claude (native MCP support) speak MCP. A plugin exposing an MCP server works on both platforms without modification. This is the minimum viable cross-platform plugin.

**A2A AgentCard** (`/.well-known/agent.json`) is the maximum portable plugin: publishable as an MCP server AND discoverable by ADK orchestrators and AGY workflows via HTTP + JSON-RPC 2.0. Any HTTP service publishing an AgentCard can be consumed as a remote agent regardless of language or runtime.

**ADK model tiers** (directly applicable):

| Task | ADK equivalent | Our model |
|---|---|---|
| Manifest building, enumeration | Flash | haiku |
| Analysis, cross-referencing | Pro | sonnet |
| Judgment, verification | Pro (extended thinking) | opus |

**Subagent prompts must be self-contained.** No runtime references to local paths. All language-specific context is pulled from `shared/references/` by the agent at runtime using its file reading tool — *if* that tool is available. If not available (sandboxed environment), the relevant reference content must have been baked into the prompt at authoring time.

**Agent descriptions are the universal routing key.** ADK routes via child agent `description`; Claude Code routes via subagent `description` frontmatter; Autogen SelectorGroupChat routes via `description`. Write descriptions for both: concrete enough for LLM routing, accurate enough for human discovery.

**Trust boundary** (Anthropic): plugin output always goes in `tool_result` blocks, JSON-encoded, never elevated into system prompt context without sanitization.

---

## 7. Validation and Human-in-the-Loop Gates

**Source: LangGraph, CrewAI, Anthropic**

**`axiom` is the exit gate at every stage.** LangGraph's `interrupt()` is the right mechanism: execution pauses with a full checkpoint, a human (or an independent agent) reviews the artifact, and the pipeline resumes via `Command(resume=...)`. The stage transition does not proceed until the gate passes.

**Retry with feedback** (CrewAI guardrails): validation failure injects the specific failure message back into the agent's context. The agent sees "summary exceeds 200 characters, be more concise" not a generic "validation failed." Retry budget: 3 attempts before escalation.

**Verification subagent** (Anthropic): verification requires minimal context transfer by nature — it's a clean agent boundary. The verification agent receives the artifact and the criteria; it returns a structured verdict. It does not inherit the producing agent's reasoning or context.

---

## 8. Extensibility Interface

**Source: Haystack, LangGraph, VS Code, CrewAI**

**Minimum interface for a third-party stage plugin:**

1. `plugin.json` declares: `fulfills`, `produces@version`, `consumes@version`, `exclusivity`, `description`, `entrypoint`
2. Implementation at `entrypoint` with:
   - Constructor accepting the `config` block
   - `run(input: ConsumedSchema) → ProducedSchema` with typed signature
   - Optional `warm_up()` for heavy initialization (model loading, DB connections)
3. Listed in the trusted-module allowlist before instantiation (Haystack security model)

**Subgraph composition** (LangGraph): each plugin is a compiled subgraph with its own internal state and a clean `input_schema`/`output_schema` pair. The parent pipeline sees it as a black-box node. Plugin-internal complexity is invisible to the orchestrator.

**Cross-plugin API** (VS Code): plugins call each other *through the host registry*, never by direct import. `registry.resolve("research-stage", {produces: "research-report@1"})` returns a handle; the host can swap implementations without breaking callers.

**Proposed/incubating schemas** (VS Code pattern): new schemas start in `shared/schemas/proposed/` with `stability: "experimental"`. Plugins using them declare `requiresExperimental: true`. Schemas are promoted after two release cycles without breaking changes.

---

## 9. Progressive Skill Disclosure

**Source: ADK SkillToolset, existing agent-best-practices.md**

ADK's `SkillToolset` implements exactly the 3-tier model we already have:
- Tier 1 (metadata): CSO description injected as a lightweight index — always in context
- Tier 2 (body): SKILL.md loaded on trigger — on demand
- Tier 3 (references): `shared/references/*.md` and `plugins/*/references/*.md` — loaded only when the agent needs language/tool-specific detail

The ADK implementation generates three tools: `list_skills`, `load_skill(name)`, `load_skill_resource(skill, path)`. The agent decides when to load what. Unused skills consume zero tokens.

**Key limit:** 8–15 tools per specialized agent. Above 20, tool selection accuracy degrades on both Claude and Gemini. Plugin agents must be narrow.

---

## 10. Optimization Loop (Future Capability)

**Source: DSPy**

DSPy's optimizer treats the entire agent tree as a parameterized program and searches for better prompt parameters (instructions, few-shot examples). This is directly applicable to our agents.

The optimizer's input is a metric function — a programmatic definition of "did this agent do the job well?" For a cooperative stage system, the metric is: did the downstream stage successfully parse and use the artifact? Did the pipeline reach the correct terminal state?

MIPROv2 (Bayesian search over instruction variants) and SIMBA (self-reflective mini-batch) are the two most practical optimizers. Each agent module can be compiled independently with a local metric, then composed. Optimization is separable from definition.

This is not part of the initial implementation but is the path to continuous process improvement without manual prompt engineering.

---

## 11. YAML Data / Python Wiring

**Source: CrewAI, VS Code**

Plugin *identity* (id, fulfills, produces, consumes, description, version, author) lives in `plugin.json` / YAML — readable and editable without understanding the execution model. Plugin *wiring* (which tools to attach, which shared references to load, runtime config) is code.

Non-plugin authors can read and configure plugins. Plugin authors write YAML. The runtime reads both.

---

## Key Decisions This Research Drives

| Question | Decision | Source |
|---|---|---|
| How does the host know what plugins provide? | Static manifest, read before code loads | VS Code |
| How are stage contracts enforced? | JSON Schema in `shared/schemas/`, validated at wiring time | Haystack, LangGraph |
| How do agents reason vs. return? | Unconstrained reasoning, typed output schema, `reasoning` scratchpad field | DSPy, Autogen |
| How does a stage gate work? | `interrupt()` + independent verification agent + `Command(resume)` | LangGraph, Anthropic |
| What's the cross-platform protocol? | MCP for tool exposure, A2A AgentCard for discovery | ADK, Anthropic |
| How do additive plugins cooperate? | Send API fan-out + Annotated reducer merge | LangGraph |
| How does routing work? | Schema-based `fulfills` for deterministic, description-based for dynamic | VS Code, Autogen |
| How does retry work? | Validation inside execution loop with specific failure message | CrewAI |
| How is `shared/` structured? | Schemas immutable (version = filename), references runtime-pullable | Haystack, VS Code |
| How are subgraphs composed? | Each plugin is a compiled subgraph with `input_schema`/`output_schema` | LangGraph |
| What's the tool count limit? | 8–15 per agent; above 20 degrades | Anthropic, SK |
| How are schemas versioned? | Semver suffix in filename; new version = new file; never mutate | VS Code proposed API |
