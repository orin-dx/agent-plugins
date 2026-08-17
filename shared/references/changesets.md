# Changesets Reference

Changesets are structured records of what changed and why, used to generate release notes and communicate changes to consumers.

## The changeset@1 Schema

```json
{
  "summary": "Add cross-language recon agent to proof plugin",
  "files_changed": ["plugins/proof/subagents/recon.md"],
  "tests_added": [],
  "acceptance_criteria_met": ["SPEC-001-AC-3", "SPEC-001-AC-4"],
  "breaking_changes": [],
  "commits": ["abc1234"],
  "linked_spec": "SPEC-001",
  "linked_plan": "PLAN-001"
}
```

## Changeset vs. Commit Message

- **Commit message**: for developers reading git history. Explains the technical change.
- **Changeset summary**: for consumers of the package. Explains the user-visible impact.

Same change, two framings:
- Commit: `refactor(proof): extract language detection into recon subagent`
- Changeset: `Proof plugin now detects workspace language automatically before scanning`

## Release Notes Generation

The `delta/release` skill aggregates changeset summaries by type:

```markdown
## v2.0.0 (2026-08-04)

### Breaking Changes
- Plugin IDs renamed: bug-hunter-rust → proof, agent-plugin-builder → basis

### New Features
- axiom exit gate with retry-with-feedback for all stage transitions
- proof plugin with cross-language recon and adversarial verification

### Bug Fixes
- ...
```

## When to Write a Changeset

Write a changeset for every PR that:
- Adds a new skill or subagent
- Changes a subagent's model or effort tier
- Modifies a shared schema (always breaking if fields removed)
- Renames a plugin ID
- Changes the axiom protocol or retry behavior

Skip changesets for:
- Pure documentation changes
- Reference file updates
- Internal refactors with no behavioral change

## Semver Decision Guide

| Change | Version bump |
|---|---|
| New plugin, no schema change | minor |
| New field in existing schema (optional) | minor |
| Removed or renamed field in existing schema | major + new file |
| New schema file | minor |
| Bug fix in subagent prompt | patch |
| New skill within existing plugin | minor |
| Renamed plugin ID | major |
