---
name: capture-need
description: >-
  Trigger when the user describes a raw need in free text: "we need X", "the problem is Y", "users are asking for Z". Converts unstructured text into a structured requirement@1 draft — id, statement, stakeholder, why, done_when — without asking clarifying questions. Fields that cannot be inferred are omitted, not fabricated. out_of_scope is intentionally left empty for weaver/connect-requirement or a human to fill in.
version: 2.0.0
---

# Weaver — Capture Need

<overview>
The entry point for turning a raw idea or pain point into something a spec can be drafted from. Delegates to `intake`. Every `done_when` criterion must be a testable proposition confirmable from outside the implementation — not a design decision in disguise.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **intake** | sonnet / medium | A free-text need statement needs converting into a requirement@1 draft. |
</dispatch>

<references>
`shared/schemas/requirement@1.json`
</references>

<io>
**Consumes**: free-text need statement
**Produces**: `requirement@1` draft (fields that couldn't be inferred are omitted, noted in `reasoning`). Route to `weaver/clarify-requirement` to close gaps before `scribe/draft-spec`.
</io>
