# Changesets

## Outcome

Record one coherent consumer-facing change in `changeset@2` so release tooling can preserve its meaning and calculate semver without reinterpreting prose. See `shared/schemas/changeset@2.json`.

## Consumer impact

| Value | Use when |
| :--- | :--- |
| `behavior-change` | Existing observable behavior changes for a consumer |
| `new-capability` | A consumer can do something new |
| `internal-only` | No behavior changes outside the repository |

`release-summarizer` omits `internal-only` entries from consumer release notes.

## Topic boundary

Use one changeset per independently releasable topic. Use these signals in priority order:

1. A shared linked requirement, spec, or plan defines one scope.
2. The author explicitly identifies a coordinated delivery scope.
3. The live diff shows one part exists because of another.

Do not split one outcome by package or file count. Do not bundle changes that could ship independently merely because they share a branch. When the boundary remains uncertain, state the ambiguity in `reasoning` and prefer the split that preserves accurate impact classification.

Verify `consumer_impact`, `semver_impact`, changed files, tests, and criteria evidence against that topic's own diff slice.

## Semver

| Change | Impact |
| :--- | :--- |
| Documentation or self-description only | `none` |
| Internal refactor or test-only change | `none` |
| Bug fix in runtime agent or skill behavior | `patch` |
| New optional schema field | `minor` |
| New schema or skill | `minor` |
| New plugin | `minor` |
| Removed or renamed schema field | `major`; create a new schema version |
| Renamed plugin ID or incompatible consumer behavior | `major` |

The release version is the highest `semver_impact` among included changesets. Classification comes from the structured field, not wording intensity.

## Breaking changes

Each breaking entry states:

- Old behavior.
- New behavior.
- Required consumer action.

Do not call an internal implementation change breaking unless it changes a supported consumer contract.

## Voice

Lead with observable consumer impact. Include a reason only when it changes understanding or action. Omit internal agent, file, and implementation detail unless the consumer must know it. State limitations and migration work directly. Full standard: `shared/references/docs-voice.md`.

## Changeset, commit, and release note

| Artifact | Reader | Focus |
| :--- | :--- | :--- |
| Commit | Maintainer reading history | Technical outcome and non-obvious reason |
| Changeset | Package consumer and release tooling | Observable impact and semver |
| Release note | Consumer deciding whether or how to upgrade | Grouped impact and required action |

Write a changeset when a PR changes runtime behavior, adds a consumer capability, changes a model or effort tier, changes a shared schema, adds a skill or plugin, or changes a verification protocol. Skip documentation, reference-only, internal refactor, and test-only changes unless they alter runtime instructions consumed by an agent.

## Release shape

```markdown
## v2.0.0 (2026-08-04)

### Breaking Changes
- Old behavior → new behavior. Required action.

### New Features
- Consumer-visible capability.

### Bug Fixes
- Corrected consumer-visible behavior.
```
