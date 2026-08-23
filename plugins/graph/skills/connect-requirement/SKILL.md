---
name: connect-requirement
description: >-
  Trigger when the user asks whether a specific requirement already exists or relates to other work: "is this already captured?", "does this overlap with an existing requirement?", "what does this relate to?". Given one requirement@1 (or a small named set), searches the workspace for related specs and implementation files, and checks for duplicate or overlapping requirements. Returns coverage status and duplicate_of references scoped to just the requirement(s) given — not a full backlog sweep.
version: 2.0.0
---

# Graph — Connect Requirement

<overview>
The single-requirement version of `graph/audit-backlog` — same agent, narrower scope. Delegates to `auditor` in its connect mode: given one requirement instead of the whole open backlog, it surfaces what that one requirement relates to.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **auditor** (connect mode) | sonnet / medium | One requirement@1 (or a small named set) needs its coverage, duplicates, and related artifacts checked without sweeping the full backlog. |
</dispatch>

<references>
`shared/schemas/requirement@1.json`
</references>

<io>
**Consumes**: one or a few `requirement@1` objects, workspace access
**Produces**: same per-requirement shape as `graph/audit-backlog` (status, evidence, duplicate_of), scoped to the given requirement(s).
</io>
