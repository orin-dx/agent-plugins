---
name: connect-requirement
description: Check whether one requirement overlaps existing requirements, specifications, plans, or implementation. Use for “is this already captured?”, “does this overlap?”, or “what does this relate to?”.
---

# Connect a requirement

## Outcome

Produce a read-only, evidence-backed relationship assessment for the supplied requirement rather than a vague similarity judgment.

## Workflow

1. Validate each supplied requirement using `shared/schemas/requirement@1.json`.
2. Search requirement, spec, plan, implementation, test, and issue-tracker artifacts for the same stakeholder outcome, criterion language, identifiers, and affected boundaries.
3. Read every candidate before classifying it. Record file paths and exact evidence for coverage, partial coverage, missing coverage, or a duplicate.
4. Distinguish same-domain work from a duplicate: a duplicate promises materially the same outcome for the same stakeholder; an adjacent artifact does not.
5. Return a per-requirement report with `status`, `evidence`, `related_artifacts`, and `duplicate_of` when applicable. Do not modify source artifacts.

## Contract

- Schema for inputs: `shared/schemas/requirement@1.json`
- Input: one requirement or a small named set plus workspace access
- Output: read-only connection report; no new cross-harness schema is introduced
- Related artifacts may include `shared/schemas/spec@1.json` and `shared/schemas/plan@1.json` documents.

## Teams and fallback

Before delegating, read `agent-roles/README.md`; use `recon` for bounded subsystem inventory and retain duplicate classification with the primary agent.

If the requirement spans independent subsystems, teammates may each inventory one bounded subsystem while the primary agent owns duplicate classification. Otherwise search and assess alone. A team result without file evidence is not usable.

## Boundaries

- Do not mark a requirement covered from a filename, issue title, or stale plan alone.
- Do not write, close, merge, or relabel artifacts during this diagnostic.
