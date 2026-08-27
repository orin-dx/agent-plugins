---
name: spec-drift
description: >-
  Trigger when the user asks whether implemented code still matches its spec, weeks or months after implementation: "check spec drift", "does the code still match this spec?", "has this spec drifted?". Given a spec@1 (via spec_file_path) and a workspace root, reads the spec from disk and the implementation from the workspace, and reports each criterion as covered (implemented and tested), uncovered (no matching implementation), or drifted (implementation exists but diverges from the criterion's contract). This is an on-demand diagnostic, not a blocking gate — scribe/gate-spec is the blocking gate.
version: 2.0.0
---

# Scribe — Spec Drift

<overview>
Ongoing maintenance health check: does the code still do what the spec says, independent of whether it passed the gate once. When a prior changeset's `criteria_evidence` is available, its file/line pointers are a starting point, never a claim to trust — every pointer gets re-read and re-verified, since code moves. Delegates to `drift-checker`.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **drift-checker** | opus / high | A spec's `spec_file_path` plus a workspace root need checking for whether the current code still implements every acceptance criterion. |
</dispatch>

<references>
`shared/schemas/spec@1.json`
</references>

<io>
**Consumes**: `spec_file_path`, workspace root, optionally prior `criteria_evidence`
**Produces**: drift report — covered / uncovered / drifted arrays plus a summary. Not routed anywhere automatically; a human or caller decides whether drift warrants a `scribe/correct-spec` cycle.
</io>
