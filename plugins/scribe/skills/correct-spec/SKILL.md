---
name: correct-spec
description: >-
  Trigger when implementer reports that a spec criterion contradicts what the system actually does: a spec_contradiction status from smith. Given a spec_file_path, the criterion_id of the affected acceptance criterion, and a contradiction report (what the spec says vs. what the system actually does), revises the affected criterion — and any criteria that depend on it — and returns a corrected spec@1 with revision_note set. Use this when implementation reveals the spec itself is wrong, not merely hard to satisfy.
version: 2.0.0
---

# Scribe — Correct Spec

<overview>
Re-enters the drafting pipeline for one criterion instead of restarting from scratch: `drafter` runs in correction mode, then the corrected spec still goes through `scribe/verify-spec` → `scribe/audit-spec` → `scribe/gate-spec` before it overwrites the file on disk — a correction is not exempt from adversarial review.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **drafter** (correction mode) | sonnet / medium | A spec_contradiction report from implementer names a specific criterion that needs revising. |
</dispatch>

<orchestration>
WHEN the corrected spec@1 passes `scribe/gate-spec`, THE SKILL SHALL overwrite the existing file at the same `spec_file_path` — the path does not change across a correction — and commit the change. The spec's `id` stays the same; `revision_note` records what changed and why.

WHEN a corrected spec@1 is handed to `navigator`, it SHALL run in amend mode — patching only the tasks tied to the affected criteria — rather than re-decomposing the entire plan. The amended plan still passes through `challenger` before `smith` resumes.

IF the same `criterion_id` triggers `spec_contradiction` a second time after already being corrected, escalate to a human rather than routing to `scribe/correct-spec` again.
</orchestration>

<references>
`shared/schemas/spec@1.json`
</references>

<io>
**Consumes**: `spec_file_path`, `criterion_id`, contradiction report (what the spec claims vs. observed system behavior)
**Produces**: corrected `spec@1` with `revision_note` set, re-entering `scribe/verify-spec` → `scribe/audit-spec` → `scribe/gate-spec`.
</io>
