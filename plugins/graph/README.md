# graph — Requirement Capture

**Stage:** Need · **Output:** `requirement@1`

Converts raw need statements into structured, testable requirements. Asks one clarifying question at a time until a spec writer could produce an accurate spec from the requirement alone.

---

## Subagents

| Subagent | Role | Tier | Description |
| :--- | :--- | :--- | :--- |
| `graph-intake` | Intake Structurer | haiku/low | Converts free text into a `requirement@1` draft. Infers all fields it can; leaves gaps noted in `reasoning`. |
| `graph-clarifier` | Clarifier | sonnet/medium | Identifies the most critical gap in the draft and asks one focused question, or returns the completed requirement if all dimensions are met. |
| `graph-auditor` | Auditor | sonnet/medium | Cross-references a completed `requirement@1` against stated stakeholder needs to confirm it is complete and internally consistent. |

## Pipeline

```
[free text] → graph-intake → graph-clarifier (× N) → graph-auditor → requirement@1
```

The clarifier loops until `done_when` criteria are specific enough to write a failing test against each, the stakeholder is identified with enough context, and `out_of_scope` boundaries are explicit.

## Output Schema

`requirement@1` — see `shared/schemas/requirement@1.json`

Required: `id`, `statement`, `stakeholder`, `why`, `done_when`

## Next Stage

Feed the completed `requirement@1` to **trace** (research) or directly to **canon** (spec) if no research is needed.
