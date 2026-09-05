---
name: changeset
description: Classify verified changes and produce one changeset per independent consumer-facing topic. Use when the user asks to add a changeset, document a change, or determine release impact.
---

# Record release intent at authoring time

Read the actual diff and any available implementation evidence before writing a changeset. A changeset is the durable consumer-facing statement that release aggregation consumes later; do not re-derive its intent from a vague summary.

## Workflow

1. Inspect the diff and group files by independent product or API topic.
2. Read `shared/references/changesets.md` before choosing `consumer_impact` or `semver_impact`.
3. For each topic, connect changed behavior to the linked requirement, spec, plan, or exact criteria evidence when available.
4. Produce one object per topic conforming to `shared/schemas/changeset@2.json`.
5. Validate required fields, especially `files_changed` and `acceptance_criteria_met`, against observed evidence.

## Classification rules

- Use `internal-only` only when a consumer cannot observe any behavior, API, configuration, or operational change.
- Use the largest required semver impact for the topic; do not dilute a breaking change because it is bundled with a smaller feature.
- Preserve uncertainty in `reasoning`; do not invent evidence or line numbers.

## Team use

Before delegating, read `agent-roles/README.md`; use `recon` only for non-overlapping diff-topic inventory and keep the final changeset classification with the primary agent.

When independent diff topics exist and agent teams are available, delegate topic classification by non-overlapping file groups. Merge only after checking that the groups are genuinely independent and each object validates. Otherwise work through the topics yourself.

## Output

Return the structured `changeset@2` object or objects and a short human-readable summary. Do not write, commit, or publish files unless the user asks for that action.
