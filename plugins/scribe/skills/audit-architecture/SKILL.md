---
name: audit-architecture
description: >-
  Trigger when a draft spec@1 needs checking against the workspace's whole-system architecture — not another spec, and not a single signature — before it reaches scribe/gate-spec: "check this spec against our architecture", "does this fit the system", "audit this against the arch model". Given a spec@1, checks it against the persisted arch-model@1 for boundary violations, competing abstractions, and invariant conflicts, building or refreshing the model first if it's absent or stale for the area the spec touches. Returns specific, rewritten fixes on fail, the same standard as scribe/audit-spec but at system scope instead of spec scope.
version: 1.0.0
---

# Scribe — Audit Architecture

<overview>
Closes the gap `scribe/audit-spec` leaves open: a spec can be internally consistent — testable criteria, no TBDs, no vague language — and still be wrong for the system it's joining. Delegates to `arch-auditor`. Runs after `scribe/audit-spec` and before `scribe/gate-spec`, so a spec doesn't reach the binding gate without a system-scope check, not just a spec-scope one.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **arch-auditor** | claude-fable-5-1 / high | A spec@1 (post `scribe/audit-spec`) needs checking against the workspace's persisted architecture model before `scribe/gate-spec`. Also invoked directly in build mode to construct or refresh the model on demand. |
</dispatch>

<references>
`shared/schemas/spec@1.json`, `shared/schemas/arch-model@1.json`, `shared/schemas/arch-audit@1.json`
</references>

<orchestration>
WHEN `arch-auditor` runs in build mode and returns an `arch-model@1`, THE SKILL SHALL write it to `<workspace_root>/docs/architecture/model.json` (creating the directory if absent) and commit it — the model is maintained state, not a per-id gated artifact, so a build/refresh pass overwrites the same file rather than creating a new one. An uncommitted model is invisible to a future session on the same terms as an uncommitted spec or plan.

Check mode produces no disk write of its own — it only reads the existing model.
</orchestration>

<io>
**Consumes**: `spec@1` (post-audit-spec), the persisted `arch-model@1` at `docs/architecture/model.json` if present
**Produces**: `arch-audit@1` in check mode (route to `scribe/gate-spec` on pass, back to `scribe/draft-spec` on fail — same 2-round circuit breaker as `scribe/audit-spec`); `arch-model@1` in build mode, persisted per the orchestration above
</io>
