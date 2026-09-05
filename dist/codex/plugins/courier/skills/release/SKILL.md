---
name: release
description: Aggregate approved changesets into a release artifact. Use when the user asks to cut a release, calculate a version bump, or generate release notes from changesets.
---

# Aggregate release evidence

Release notes are an aggregation of already-classified changesets, not a second interpretation of the diff. Validate inputs before computing the release.

## Workflow

1. Validate every candidate entry against `shared/schemas/changeset@2.json`.
2. Exclude entries whose `consumer_impact` is `internal-only`.
3. Apply the largest remaining `semver_impact` to the supplied prior version.
4. Carry each approved changeset summary forward without rewriting its consumer meaning.
5. Produce `shared/schemas/release-artifact@2.json` with the computed version, date, changesets, and any breaking-change or migration information already present in the inputs.

## Evidence and failure handling

- Report the input set, excluded entries, and version calculation.
- Stop when the prior version, release date, or changeset set is missing; name the missing input rather than guessing.
- A release with no consumer-facing changesets has no version calculation to invent.

## Team use

Before delegating, read `agent-roles/README.md`; use `recon` only for separate changeset validation, while the primary agent owns release synthesis.

When agent teams are available, parallelize only independent schema validation of separate changesets. Perform filtering, semver maximum selection, and final artifact assembly in one place. If teams are unavailable, validate each entry yourself.

## Safety

Producing a release artifact does not authorize creating a git tag, GitHub release, publishing a package, or modifying version files. Present those as separate actions requiring user approval.
