---
name: gate-spec
description: >-
  Trigger when a spec@1 needs a definitive pass/fail judgment before it enters planning: "gate this spec", "is this spec ready?", "check this spec before we plan it". Default disposition is fail — the spec must earn a pass. Passes only if every acceptance criterion is testable with no vague language, no TBDs remain, error cases are explicitly covered, and scope is narrow enough for one planning cycle. On fail, returns blockers specific enough for canon/draft-spec to act on without further clarification.
version: 2.0.0
---

# Canon — Gate Spec

<overview>
The binding exit gate for a spec entering planning. Delegates to `exit-gate`. On pass, this skill — not the agent — performs the disk-write orchestration below; that step is load-bearing, not decoration.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **exit-gate** | opus / high | A spec@1 (after `canon/verify-spec` and `canon/audit-spec`) needs a terminal binding pass/fail verdict before planning. |
</dispatch>

<orchestration>
After `exit-gate` returns a pass verdict, THE SKILL SHALL, before handing off to `vector`:
1. Write the spec@1 JSON to `<workspace_root>/.claude/specs/<id>.json`. Create the directory if it does not exist.
2. Commit the file to version control. An uncommitted spec file is invisible to a fresh checkout, a future session, and `canon/spec-drift` — it exists only in the current working tree.
3. Set `spec_file_path` to the workspace-relative path (e.g. `.claude/specs/SPEC-001.json`) in the spec@1 object.
4. Pass the updated spec@1 — with `spec_file_path` set — to `vector`.

Without `spec_file_path` set, downstream agents fall back to reading the spec from conversation context, which is lossy under compression and cannot be independently verified.

**2-Round Circuit Breaker**: drafter ↔ auditor review loops (via `canon/draft-spec` and `canon/audit-spec`) are capped at 2 iterations before reaching this gate. On round 2, unresolved debates about internal helper names or line citations are demoted to non-blocking `api_notes` rather than looping further.
</orchestration>

<references>
`shared/schemas/spec@1.json`, `shared/schemas/verdict@1.json`
</references>

<io>
**Consumes**: `spec@1` (post-verify, post-audit-spec)
**Produces**: `verdict@1`. On pass, a persisted `spec@1` with `spec_file_path` set, routed to `vector`. On fail, blockers routed back to `canon/draft-spec`.
</io>
