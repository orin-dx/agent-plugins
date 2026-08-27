# Changelog

— vanguard

## [2.0.0] - 2026-08-27

### Changed
- **BREAKING**: Plugin ID renamed from `trace` to `vanguard` as part of the ecosystem-wide Wisp persona-naming rename — abstract math-noun plugin ids became hard to recall as the ecosystem grew past 9 plugins. This is the research plugin; its skill also renamed from `trace/trace` to `vanguard/research`. See `docs/adr/007-wisp-persona-naming.md` for the full rationale and old→new mapping. `plugin.json` `id`/`name` updated; every cross-plugin reference across the ecosystem updated to match.

## [1.2.5] - 2026-08-23

### Fixed
- README's "When to Use" bullet used the banned word "landscape" (`docs-voice.md`'s banned-word list). Found by a repo-wide banned-word sweep, not the original authoring pass. Reworded to "existing patterns and prior art."

## [1.2.4] - 2026-08-23

### Fixed
- `recon`'s `<goal>` still claimed to map "specs, plans, docs" as research sources — missed in the `1.2.3` pass despite touching this same file. `plan@1` is never persisted to disk, so it was never a real source to map.

## [1.2.3] - 2026-08-23

### Added
- `recon` gained a `<load_first>` citing the new `shared/references/workspace-conventions.md` — it needed to map internal spec sources but had no stated location for them on disk.

### Changed
- `synthesizer`'s `<output>` now shows a literal `research-report@1` JSON template, matching its three siblings (`recon`, `reader`, `risk-assessor`) instead of describing required elements in prose only.

## [1.2.2] - 2026-08-22

### Changed
- `recon`'s `reasoning` scratchpad capped to 1-2 sentences — discarded, not read by a human.
- All agents now carry a `<constitution>` section — see root CHANGELOG and ADR-006. `trace`'s skill description tightened; no routing behavior changed.

## [1.2.1] - 2026-08-21

### Fixed
- `skills/trace/SKILL.md` and `README.md` each documented a "Sub-skills" list implying separately-invokable commands (`trace/question`/`trace/prior-art`/`trace/dependency`/`trace/risk` in one file, `trace/survey`/`trace/scan`/`trace/risk` in the other) — the two disagreed with each other, and both were fiction: trace has exactly one skill directory. Replaced both with one honest description of the real four-agent pipeline (recon → reader → synthesizer → risk-assessor), which narrows itself to what's asked instead of exposing named sub-modes.
- README's version line read `1.0.1`, already stale against `plugin.json`'s `1.2.0` before this fix.
### Changed
- README's pipeline section is now a Mermaid flowchart styled with the shared six-color palette (`shared/references/orin-visual-standard.md` §2), replacing the plain-text arrow chain.

## [1.2.0] - 2026-08-17

### Changed
- **Targeted Research Lookups**: Uses `rg` and `bat` patterns for fast, windowed codebase evidence gathering.

## [1.1.0] - 2026-08-17

### Changed
- **Lean Agent Names**: Agents now display cleanly as `trace:reader`, `trace:risk-assessor`, and `trace:synthesizer`.
- **High-Density Research**: `synthesizer` structures findings around exact file pointers and clear evidence assumptions.

## [1.0.1] - 2026-08-05
### Fixed
- `plugin.json`: `author` changed to object, `agents` entries changed to relative file paths
### Changed
- Skill name renamed `trace` → `research` (displays as `/trace:research`)

## [1.0.0] - 2026-08-04
### Added
- Initial release
- Evidence-based research pipeline distinguishing confirmed findings from assumptions
- `research-report@1` output schema consumed by `canon`
- Subagents: recon, reader, synthesizer, risk-assessor
