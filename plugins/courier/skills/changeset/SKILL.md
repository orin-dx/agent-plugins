---
name: changeset
description: >-
  Trigger when the user asks to add a changeset or document a change: "add a changeset", "document this change", "what changed here". Extracts the consumer-facing meaning of a diff: classifies consumer_impact (behavior-change, new-capability, internal-only) and semver_impact (major, minor, patch, none) per shared/references/changesets.md's decision table, then writes a summary scaled to that classification. A diff spanning multiple independent topics — common on a backlog/catch-up run, not just a single PR — produces one changeset per topic, not one bundled entry. When the change came via smith, pass along implementer's criteria_evidence — changeset-analyzer uses those exact locations instead of reconstructing approximate ones from the diff.
version: 2.1.0
---

# Courier — Changeset

<overview>
A changeset is the changelog entry, written once at authoring time and later aggregated — not rewritten — into a release. `changeset-analyzer` first checks how many independent topics the diff actually contains, then classifies consumer_impact and semver_impact per topic before writing anything, and scales each summary's detail to match: terse for a patch, one sentence for a minor, full old-behavior-to-new-behavior-to-required-action detail for a major. Delegates entirely to `changeset-analyzer`.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **changeset-analyzer** | sonnet / medium | A git diff needs one or more structured `changeset@2` entries with consumer/semver classification and acceptance criteria mapping. |
</dispatch>

<references>
`shared/references/changesets.md` — changeset format, the Consumer Impact Classification table, the Semver Decision Guide, and the voice standard for this artifact.
</references>

<io>
**Consumes**: git diff (a single PR's, or a larger backlog/catch-up diff since the last release), optionally a linked `spec@1`, optionally smith's aggregated `criteria_evidence`
**Produces**: one or more `changeset@2` entries conforming to `shared/schemas/changeset@2.json` — one per independent topic found in the diff, never one entry bundling unrelated topics together. Route to `courier/pr` or `courier/release` depending on the next stage.
</io>
