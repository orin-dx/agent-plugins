# Changelog

— mason

## [3.0.0] - 2026-08-27

### Changed
- **BREAKING**: Plugin ID renamed from `basis` to `mason` as part of the ecosystem-wide Wisp persona-naming rename — abstract math-noun plugin ids became hard to recall as the ecosystem grew past 9 plugins. This is the meta-plugin scaffolding/auditing plugin; no single-skill rename applies; skill names scaffold-plugin, audit-plugin, design-schema, and scaffold-subagent are unchanged. See `docs/adr/007-wisp-persona-naming.md` for the full rationale and old→new mapping. `plugin.json` `id`/`name` updated; every cross-plugin reference across the ecosystem updated to match.

## [2.1.2] - 2026-08-23

### Fixed
- `auditor`'s "no authoring-time refs" check only grepped agent bodies, not `SKILL.md` files — missed exactly this pattern in `axiom`'s `SKILL.md` (fixed the same day, in `axiom` v1.2.3). Broadened the check to also scan every `SKILL.md` in the audited plugin, carving out the one legitimate exception: `basis`'s own scaffolding skills, whose job is authoring agents per that guide.

## [2.1.1] - 2026-08-23

### Fixed
- `auditor`'s frontmatter claimed "nine categories" while the README's Conformance Checks table listed 11 and `<goal>` gave a third, shorter count — three disagreeing enumerations of the same check set. Dropped the hard-coded count from the frontmatter (it will drift again the next time a check is added) and pointed it at the README table as the source of truth.
- `auditor` was never actually instructed to check "no authoring-time references to `shared/agent-best-practices.md`" despite the README's Conformance Checks table promising it — added the missing instruction to `<output>`.

Both found by an adversarial re-read of this session's own `2.1.0` changes, not the original pass.

## [2.1.0] - 2026-08-23

### Added
- **`scaffolder`**: generates an optional `<load_first>` block (immediately after `<constitution>`) whenever a scaffolded agent's task implies a lookup, and drafts SKILL.md routing entries for any output status that isn't a single terminal pass/fail — both were previously unhandled, meaning every plugin scaffolded before this version could ship with either gap silently.
- **`auditor`**: two new checks — `<load_first>` correctness (present when needed, target resolves) and orchestration completeness (every output status routed in SKILL.md, or documented terminal). The second check exists specifically because this pattern shipped unfixed in `lambda` this session before being caught by hand.
- **`auditor`**: version agreement, reference-file size, and schema JSON validity are now checked by running `scripts/check-versions.sh`, `scripts/check-reference-size.sh`, and `jq` directly and reading this plugin's own result, instead of re-deriving the same judgment through reasoning — removes a redundant, driftable second source of truth for facts the repo's own scripts already check deterministically.

### Fixed
- `scaffolder`'s and `auditor`'s own frontmatter descriptions exceeded the 80-200 word guideline they enforce on every other agent (233 and 221 words) after the additions above — trimmed both back under 200.

### Fixed
- **`auditor`**: the 5th `<constitution>` section (ADR-006) meant its own conformance check — "body contains exactly backstory, goal, judgment, output sections" — would have failed every conformant agent in the ecosystem. Now checks for the 5-part structure and verifies `<constitution>` is byte-identical to a reference agent's, not just present.
- **`scaffolder`**: was about to generate new agents missing `<constitution>` entirely. Now generates the 5-part structure and copies `<constitution>` byte-for-byte from an existing agent — explicitly never regenerated or paraphrased, since any deviation breaks prompt-cache sharing across the ecosystem.

## [2.0.0] - 2026-08-20

### Breaking
- Single `meta` skill replaced by four targeted skills: `scaffold-plugin`, `audit-plugin`, `design-schema`, `scaffold-subagent`. Anything invoking `/basis:basis` must switch to the new per-skill names.
- `audit` was the natural bare-word name for the conformance-check skill but collides with `proof`'s existing plugin-level skill (`name: audit`) — named `audit-plugin` instead, per the constitution's Skill Names rule.
- A follow-up pass renamed `scaffold` → `scaffold-plugin`, `schema` → `design-schema`, `subagent` → `scaffold-subagent`: bare nouns/verbs left the object ambiguous in slash-command autocomplete, and `scaffold-plugin`/`scaffold-subagent` now read as siblings instead of `scaffold` sounding like the only "real" scaffolding skill.
### Added
- `basis/scaffold-subagent` skill: generates one conformant agent file for an existing plugin. `scaffolder.md` now documents a single-subagent mode (skips plugin.json/SKILL.md/symlink) alongside its existing full-plugin mode — no new agent needed, the old SKILL.md listed this sub-skill with no agent behind it.

## [1.2.0] - 2026-08-17

### Added
- **JIT Hook Scaffolding**: Added reference hook generation in `shared/hooks/` for cross-platform lifecycle context injection.

## [1.1.0] - 2026-08-17

### Added
- **Lean Plugin Scaffolding**: `scaffolder` generates clean agent names without redundant plugin prefixes.
- **Cache-Aware Audits**: `auditor` checks that new plugin prompts follow static prefix caching standards.

### Changed
- **Lean Agent Names**: Agents now display cleanly as `basis:scaffolder`, `basis:auditor`, and `basis:schema-designer`.

## [1.0.1] - 2026-08-05
### Fixed
- `plugin.json`: `author` changed to object, `agents` entries changed to relative file paths
### Changed
- Skill name renamed `basis` → `meta` (displays as `/basis:meta`)

## [1.0.0] - 2026-08-04
### Added
- Initial release, superseding `agent-plugin-builder`
- Plugin scaffolding, conformance auditing, and schema contract design
- Subagents: scaffolder, auditor, schema-designer
