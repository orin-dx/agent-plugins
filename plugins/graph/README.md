# graph — Need Definition

**Stage:** Need · **Output:** `requirement@1` · **Version:** 1.0.1

Converts a raw need statement — a one-liner, a vague complaint, a stakeholder ask — into a structured `requirement@1` artifact that a spec writer can act on without asking a single follow-up question. Works with GitHub Issues by default; any issue tracker that emits `requirement@1` can substitute.

---

## When to Use

- You have a fuzzy idea and want to structure it before anyone writes code
- You need to capture a stakeholder request as a formal, traceable requirement
- You want to audit the backlog for gaps, duplicates, or requirements with no matching spec
- You need to link a requirement to related requirements, existing specs, or implementation files

**Invoke with:** `"We need X"`, `"Users are asking for Y"`, `"The problem is Z"`, `"Capture this requirement"`, `"Audit the backlog"`

---

## Sub-skills

| Sub-skill | What it does |
| :--- | :--- |
| `graph/capture` | Converts a free-text need into a `requirement@1` draft — no questions asked, all inferred fields noted |
| `graph/prioritize` | Ranks a set of requirement drafts by impact, urgency, and dependency order |
| `graph/connect` | Links a requirement to related requirements, specs, and implementation files already in the workspace |
| `graph/audit` | Cross-references all open requirements against specs, plans, and implementation files — surfaces gaps, coverage, and duplicates |

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `intake` | Intake Structurer | sonnet / medium | Converts free text into a `requirement@1` draft. Infers all fields it can; leaves gaps noted in `reasoning`. |
| `clarifier` | Clarifier | sonnet / medium | Identifies the most critical gap in the draft and asks one focused question, or returns the completed requirement if all dimensions are met. |
| `auditor` | Auditor | sonnet / medium | Cross-references a completed `requirement@1` against stated stakeholder needs to confirm it is complete and internally consistent. |

---

## Pipeline

```
[free text] → intake → clarifier (× N) → auditor → requirement@1
```

The clarifier loops until each `done_when` criterion is specific enough to write a failing test against it, the stakeholder is identified with enough context, and `out_of_scope` boundaries are explicit.

---

## Output Schema

`requirement@1` — see `shared/schemas/requirement@1.json`

| Field | Required | Description |
| :--- | :--- | :--- |
| `id` | yes | Unique requirement identifier |
| `statement` | yes | One sentence describing the need |
| `stakeholder` | yes | Who this serves, with enough context to understand their perspective |
| `why` | yes | Underlying pain or opportunity |
| `done_when` | yes | Array of testable propositions, each confirmable true/false from the outside |
| `out_of_scope` | yes | Explicit boundaries that prevent scope creep |
| `reasoning` | yes | Scratchpad — never forwarded downstream |

A requirement is complete when a downstream spec writer can read it and produce an accurate, unambiguous spec without asking clarifying questions.

---

## Install

**Claude Code** — add the marketplace once, then install by ID:
```
/plugin marketplace add orin-dx/agent-plugins
/plugin install graph
```

**AGY** — installs the full repo; see the [root README](../../README.md#quick-start) for instructions.

---

## Next Stage

Feed `requirement@1` to **[trace](../trace/)** for research, or directly to **[canon](../canon/)** if no prior art survey is needed.

---

## Extensibility

Any issue tracker (Jira, Linear, Notion) can substitute as the backing store as long as it emits `requirement@1`. The downstream pipeline is agnostic — it only consumes the schema.
