# Changelog

— mason

## [3.2.2] - 2026-09-10

### Changed
- Scaffolding and audits now require concern-first reference paths and keep human indexes out of runtime load chains.
- Reference conformance now includes exact paths, local Markdown links, retired pointer forms, immutable-path replacements, and runtime callers.

## [3.2.1] - 2026-09-09

### Changed
- Scaffolding and audits now assess runtime references by outcome, applicability, confirming and refuting evidence, and disposition.
- Cross-language claims must cover each named language or disclose the gap; agents also apply the shared radical-candor rule.

## [3.2.0] - 2026-09-09

### Added
- `mason:evaluate`, with isolated `evaluation-run@1` execution evidence and independent adjudication, for fixed hidden-oracle behavioral fixtures.
- `harness-evaluation@2` records exact harness, model, role, plugin version, source revision, workspace state, defect metrics, and available usage data.
- Scaffolding and audits now generate and check evidence-depth rules only when a workflow makes the corresponding verification claim.

## [3.1.0] - 2026-09-09

### Added
- Instruction-economy scaffolding and audits: direct atomic rules, no repeated rationale or process narration, and numbered procedures only when order affects correctness.
- Length thresholds now trigger evidence-based review rather than automatic failure.
- Cross-harness guidance now defines exact shared paths as runtime dependencies and requires transitive Codex packaging.

## [3.0.1] - 2026-09-04

### Changed
- `audit-plugin`/`scaffold-plugin` now cite `shared/harness-authoring.md` when the audited plugin has or will have a Codex-native source, following the new cross-harness authoring convention.

## [3.0.0] - 2026-08-27

### Changed
- **BREAKING**: Plugin ID renamed `basis` → `mason`. Skill names unchanged. See [ADR-007](../../docs/adr/007-wisp-persona-naming.md).

## [2.1.2] - 2026-08-23

### Fixed
- `auditor`'s "no authoring-time refs" check only grepped agent bodies, missing the same pattern in `SKILL.md` files. Broadened to scan every `SKILL.md`, carving out `basis`'s own scaffolding skills, which legitimately author agents per that guide.

## [2.1.1] - 2026-08-23

### Fixed
- `auditor`'s frontmatter, README, and `<goal>` gave three disagreeing check counts. Dropped the hard-coded count from frontmatter and pointed it at the README table as source of truth.
- `auditor` was never actually instructed to check for authoring-time references despite the README promising it. Added the missing instruction.

## [2.1.0] - 2026-08-23

### Added
- **`scaffolder`**: generates an optional `<load_first>` block and drafts SKILL.md routing for any non-terminal output status — both previously unhandled, so every plugin scaffolded before this could ship with either gap silent.
- **`auditor`**: two new checks — `<load_first>` correctness and orchestration completeness (every output status routed or documented terminal).
- **`auditor`**: version agreement, reference-file size, and schema validity are now checked by running the repo's own scripts and `jq` directly, instead of re-deriving the same judgment through reasoning.

### Fixed
- `scaffolder`'s and `auditor`'s own frontmatter descriptions exceeded the word guideline they enforce on every other agent. Trimmed both.
- **`auditor`**: the 5th `<constitution>` section (ADR-006) would have failed its own "exactly backstory/goal/judgment/output" check. Now checks the 5-part structure and verifies `<constitution>` is byte-identical to a reference agent.
- **`scaffolder`**: was about to generate agents missing `<constitution>` entirely. Now copies it byte-for-byte from an existing agent — any deviation breaks prompt-cache sharing.

## [2.0.0] - 2026-08-20

### Breaking
- Single `meta` skill replaced by four targeted skills: `scaffold-plugin`, `audit-plugin`, `design-schema`, `scaffold-subagent`. `/basis:basis` must switch to the new names.
- `audit` collides with `proof`'s existing plugin-level skill — named `audit-plugin` instead.
### Added
- `basis/scaffold-subagent` skill: generates one conformant agent file for an existing plugin, alongside `scaffolder`'s existing full-plugin mode.

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
