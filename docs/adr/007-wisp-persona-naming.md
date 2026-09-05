# ADR-007: Wisp persona naming — plugin ID rename

**Status:** Accepted; umbrella-brand clause superseded by ADR-010 (the family is now **Wisp Plugins**; "Wisp" alone is the library)
**Date:** 2026-08-27
**Supersedes:** none — this is a naming/identity change, not a structural one. All prior ADRs (001-006) remain in force under the new plugin ids.

## Context

The ecosystem's plugin ids were abstract math and CS nouns — `graph`, `trace`, `canon`, `vector`, `lambda`, `proof`, `axiom`, `delta`, `basis` — chosen when the ecosystem had a handful of plugins and the words mapped loosely to each plugin's domain concept (a requirement graph, a research trace, an architectural canon, a planning vector, a lambda calculus of implementation, formal proof, a verification axiom, a changeset delta, a basis for scaffolding). As the ecosystem grew past nine plugins, this stopped working as a memory aid. The ids no longer reliably cued which plugin did what: `canon` versus `axiom` versus `basis` gave no intuitive signal about spec-writing versus gating versus scaffolding, and `proof` versus `trace` versus `vector` required already knowing the mapping rather than being able to infer it. New contributors and even experienced users were routing skill invocations by looking up a table rather than by recall. A tenth plugin (component specification) was also being added, compounding the problem — an eleventh abstract noun was not going to help.

## Alternatives Considered

- **Keep the abstract-noun scheme and add a lookup table to every doc.** Rejected: this treats the symptom (poor discoverability) without fixing the cause (the names carry no intrinsic signal), and a lookup table itself becomes another thing to keep in sync as plugins are added.
- **Rename to literal function names** (e.g. `spec-writer`, `bug-hunter`, `verifier`, `planner`). Considered seriously — this maximizes literal clarity. Rejected because several plugins are hard to compress into one literal word without collision (`canon`/spec-writing and `muse`/component-spec-writing would both want "spec-writer"; `axiom` and the exit-gate concept it wraps are hard to name without stealing a word every plugin's own exit-gate agent already uses internally) and because a persona gives room for the skill name to carry the literal action instead, avoiding the collision entirely.
- **Persona-based naming**, where the plugin id is a character or craft-role archetype and the *skill* name (not the plugin id) carries the literal action. Accepted — see Decision.

## Decision

Every plugin id is renamed to a persona — a character or craft-role archetype evocative of that plugin's function — under a single umbrella brand for the whole family: **Wisp**. The literal action moves to the skill name, following the convention `persona:action` (e.g. `ranger:audit`, `sentinel:gate`). For the five single-skill plugins, where the skill name previously duplicated the plugin id, the skill is renamed to the literal action it performs. For the four multi-skill plugins, which already had distinct literal skill names (`draft-spec`, `changeset`, `capture-need`, `scaffold-plugin`, etc.), only the plugin-id prefix changes in any documented invocation — the skill names themselves are unchanged.

A tenth plugin, `muse`, is added in the same change: a component-specification plugin (Design category, alongside `scribe`) that turns UI/design intent into testable component specs — props, variants, per-state behavior, accessibility criteria — gated the same way `scribe` gates a spec. It reuses the existing `spec@1`/`verdict@1` schemas unchanged; no new schema was needed.

### Full mapping

| Old id | New id (persona) | Category | Skill(s) |
| :--- | :--- | :--- | :--- |
| `graph` | `weaver` | Requirements | `capture-need`, `clarify-requirement`, `prioritize-backlog`, `connect-requirement`, `audit-backlog` (unchanged) |
| `trace` | `vanguard` | Research | `research` (was `trace`) |
| `canon` | `scribe` | Design | `draft-spec`, `verify-spec`, `spec-drift`, `audit-spec`, `gate-spec`, `correct-spec`, `architect` (unchanged) |
| — | `muse` *(new)* | Design | `component` |
| `vector` | `navigator` | Planning | `plan` (was `vector`) |
| `lambda` | `smith` | Implementation | `implement` (was `lambda`) |
| `proof` | `ranger` | Verification | `audit` (was `proof`) |
| `axiom` | `sentinel` | Verification | `gate` (was `axiom`) |
| `delta` | `courier` | Shipping | `commit`, `pr`, `changeset`, `receive-feedback`, `post-review`, `release` (unchanged) |
| `basis` | `mason` | Meta | `scaffold-plugin`, `audit-plugin`, `design-schema`, `scaffold-subagent` (unchanged) |

Each renamed plugin's `plugin.json` `id`/`name` fields, directory, and single-skill directory (where applicable) were updated together, and the plugin's own `version` was bumped to the next major version — the same precedent this repo already set for the `bug-hunter-rust → proof` plugin-ID rename documented in `shared/references/conventional-commits.md` (`feat!:` with `BREAKING CHANGE: plugin ID changed`). Every cross-plugin reference across agent prompts, skill docs, shared references, schemas, and root-level documentation was updated to match.

## Consequences

The plugin id now gives a real memory hook: a `ranger` hunts bugs, a `sentinel` guards a gate, a `smith` forges implementation, a `scribe` writes specs, a `muse` inspires component design — the mapping is inferable rather than memorized. This is a breaking change for anyone with the old ids hardcoded in scripts, CI, or muscle memory; every plugin's `plugin.json` `id` changed, so `/plugin install <old-id>` and `<old-id>:<skill>` invocations stop resolving and must be updated to the new id. The five single-skill plugins also changed their skill name (previously identical to the plugin id), which is a second breaking surface for anyone invoking `<old-id>/<old-id>` directly rather than through the plugin's natural-language trigger phrases. No schema, agent behavior, or pipeline logic changed — this is a naming-layer change only, and every ADR 001-006 still governs agent structure and behavior unchanged. `mason:scaffolder` and `mason:auditor` were checked against the new naming convention (skill-name-equals-literal-action for single-skill plugins) so future scaffolds default to the correct pattern rather than reintroducing a plugin-id-as-skill-name naming collision.
