---
name: changeset
description: >-
  Trigger when the user asks to add a changeset or document a change: "add a changeset", "document this change", "what changed here". Extracts the consumer-facing meaning of a diff: classifies consumer_impact (behavior-change, new-capability, internal-only) and semver_impact (major, minor, patch, none) per the decision table in shared/references/changesets.md, then writes a summary whose detail scales with that classification. When the change was implemented via lambda, pass along the criteria_evidence implementer collected during the TDD run — changeset-analyzer uses those exact locations instead of reconstructing approximate ones from the diff.
version: 2.0.0
---

# Delta — Changeset

<overview>
A changeset is the changelog entry, written once at authoring time and later aggregated — not rewritten — into a release. `changeset-analyzer` classifies consumer_impact and semver_impact directly from the diff before writing anything, and scales the summary's detail to match: terse for a patch, one sentence for a minor, full old-behavior-to-new-behavior-to-required-action detail for a major. Delegates entirely to `changeset-analyzer`.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **changeset-analyzer** | sonnet / medium | A git diff needs a structured `changeset@2` with consumer/semver classification and acceptance criteria mapping. |
</dispatch>

<references>
`shared/references/changesets.md` — changeset format, the Consumer Impact Classification table, the Semver Decision Guide, and the voice standard for this artifact.
</references>

<io>
**Consumes**: git diff, optionally a linked `spec@1`, optionally lambda's aggregated `criteria_evidence`
**Produces**: `changeset@2` conforming to `shared/schemas/changeset@2.json`. Route to `delta/pr` or `delta/release` depending on the next stage.
</io>
