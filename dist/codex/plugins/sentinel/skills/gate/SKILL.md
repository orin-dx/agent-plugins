---
name: gate
description: Independently verify an artifact against its criteria before it crosses a lifecycle boundary. Use for requirements, specs, plans, implementations, PRs, and explicit readiness checks.
---

# Gate a lifecycle artifact with evidence

Sentinel judges an existing artifact; it does not author a replacement. Begin by identifying what the artifact claims, where it is persisted, and which criteria actually govern it.

## Workflow

1. Identify `artifact_type`, `artifact_path`, the authoritative criteria, linked artifacts, and source files that can prove or disprove each criterion.
2. Read persisted files when a path is present rather than relying on conversation summaries.
3. Build an evidence table that classifies each criterion as verified, failed, or unverifiable, with exact paths and test or inspection evidence.
4. Produce `verdict@1` conforming to `shared/schemas/verdict@1.json`.
5. Pass only when every applicable criterion is verified. On failure, return specific blockers that the producing workflow can act on.

## Retry protocol

On a retry, inspect only the revised artifact and the previous blockers. Do not reopen unrelated review scope. Set `retry_count` accurately and escalate to the caller after the third failed retry rather than looping indefinitely.

## Evidence and safety

- Do not treat a passing test alone as proof of a criterion it does not exercise.
- Mark evidence unverifiable when the relevant source, environment, or criterion is absent; do not convert uncertainty into a pass.
- Do not edit the artifact, create a PR, or publish a verdict externally unless the user asks for a separate action.

## Team use

Before delegating, read `agent-roles/README.md`; use `recon` for fixed evidence collection, but reserve the binding decision for the primary `judge`.

When teams are available, split criterion verification only across independent subsystems after the artifact and criteria are fixed. The owner reconciles coverage and delivers one binding verdict. Without teams, verify each criterion sequentially with the same standard.
