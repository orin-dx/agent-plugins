---
name: release
description: >-
  Trigger when the user asks to cut a release or summarize what's in one: "cut a release", "what's in this release", "generate release notes". Aggregates changeset@2 entries since the last release into a release-artifact@2: filters consumer_impact: internal-only entries, computes the version as max(semver_impact) across the rest applied to the prior version, and carries each changeset's summary through unedited.
version: 2.0.0
---

# Delta — Release

<overview>
A release is an aggregation of changesets already written correctly at authoring time — this skill does not re-narrate anything, it groups and computes the version bump. Delegates entirely to `release-summarizer`.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **release-summarizer** | sonnet / medium | A set of `changeset@2` entries needs aggregating into a `release-artifact@2` with a computed version bump. |
</dispatch>

<references>
`shared/references/changesets.md` — the Semver Decision Guide (now machine-enforced via each changeset's `semver_impact`) and Release Notes Generation format.
</references>

<io>
**Consumes**: list of `changeset@2` entries, the prior released version, a release date
**Produces**: `release-artifact@2` conforming to `shared/schemas/release-artifact@2.json`.
</io>
