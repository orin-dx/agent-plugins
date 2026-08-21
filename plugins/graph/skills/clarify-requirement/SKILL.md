---
name: clarify-requirement
description: >-
  Trigger when a requirement@1 draft from graph/capture-need has gaps to close before a spec can be written: "is this requirement complete?", "what's missing from this requirement". Given a requirement@1, evaluates gaps in priority order — testability of done_when, specificity of stakeholder, explicitness of out_of_scope — and either asks one focused question or returns the completed requirement with out_of_scope populated. One question per invocation, never a list.
version: 2.0.0
---

# Graph — Clarify Requirement

<overview>
Closes the gap between "captured" and "ready for canon/draft-spec" one question at a time. Delegates to `clarifier`. This skill was previously undocumented as a sub-skill despite having a real backing agent — added here alongside the rest of the split.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **clarifier** | sonnet / medium | A requirement@1 draft needs its most critical gap identified and either closed with one question or confirmed complete. |
</dispatch>

<references>
`shared/schemas/requirement@1.json`
</references>

<io>
**Consumes**: `requirement@1` draft
**Produces**: either one clarifying question (requirement unchanged) or a completed `requirement@1` with `out_of_scope` populated. Loop back into `graph/clarify-requirement` after each answered question; route the completed requirement to `canon/draft-spec`.
</io>
