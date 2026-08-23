# Changelog

— proof

## [2.2.3] - 2026-08-23

### Added
- **`adversary`**: genuine `plausible` verdict path — `finding-report@1` has promised this value since it was defined, but adversary was strictly binary (confirm-with-scenario or refute) and could never emit it. Now emits `plausible` when no refutation can be constructed but reachability depends on state outside the code (config, an external caller, environment) rather than stretching thin evidence into `confirmed`.
- **`exit-gate`**: `flagged_for_review` in the verdict output — carries `plausible` findings forward for human judgment without treating them as remediation targets or blockers.

### Fixed
- `README.md`'s Output Schema table documented only `verdict: confirmed`; corrected to cover both verdict values.

## [2.2.2] - 2026-08-22

### Changed
- **Hazard reference split**: T7 and T10 — `boundary-tracer`'s entire scope — extracted into `rust-hazards-t7-t10.md`/`typescript-hazards-t7-t10.md`, both now under 120 lines (were 150/167, over the reference-file cap). `boundary-tracer` loads only the split file instead of the full ten-taxonomy set. `adversary` now branches on the candidate's `taxonomy` field to load only the matching file instead of the full set on every call — real savings on the agent invoked once per candidate, at the opus tier. `scanner` and `reviewer` (lambda) load both files where they need the complete set; behavior and taxonomy coverage are unchanged. Also removed a dead "Workspace Discovery" section neither file's consuming agent ever referenced — recon already provides the same information via its manifest.

### Fixed
- `skills/proof/SKILL.md`'s dispatch matrix mistagged `adversary` as `sonnet/medium`; its frontmatter has always been `opus/high`. Corrected the doc.

## [2.2.1] - 2026-08-21

### Fixed
- `SKILL.md` and `README.md` both documented a "Sub-skills" table (`proof/scan`, `proof/focus`, `proof/verify`, `proof/remediations`) styled like independently-invokable skills — the way `delta/commit` or `canon/draft-spec` genuinely are. proof has exactly one skill directory; none of those four were real. Replaced with an honest description of the one fixed pipeline adapting to what the request contains.
- `README.md`'s version line said `2.0.0` while `plugin.json` said `2.2.0` — out of sync since at least the 2.1.0 release. Both now match.
### Changed
- `README.md`'s pipeline diagram upgraded from a plain-text arrow chain to a styled Mermaid flowchart using the palette in `shared/references/orin-visual-standard.md`.

## [2.2.0] - 2026-08-17

### Changed
- **Fast Symbol Discovery**: Updated scanning and adversary workflows to use targeted `rg` patterns for symbol inspection.

## [2.1.0] - 2026-08-17

### Added
- **Module-Batched Sweeps**: `adversary` now audits candidate defect signals grouped by crate module in a single pass.
- **Dead-Code Pre-Filtering**: Automatically filters out inactive code before scanning to eliminate false alarms.

### Changed
- **Lean Agent Names**: Agents now display cleanly as `proof:scanner`, `proof:adversary`, and `proof:exit-gate`.
- **Fast Candidate Refutation**: Routed initial candidate reviews to Sonnet, reserving Opus for the final binding exit gate.

## [2.0.1] - 2026-08-05
### Fixed
- `plugin.json`: `author` changed to object, `agents` entries changed to relative file paths
### Changed
- Skill name renamed `proof` → `audit` (displays as `/proof:audit`)

## [2.0.0] - 2026-08-04
### Added
- Initial release, superseding `bug-hunter-rust` and `bug-hunter-ts`
- 4-phase pipeline: recon → scan → adversary → exit-gate
- Cross-language support: Rust, TypeScript, JavaScript
- Runtime language heuristics via `shared/references/rust.md` and `shared/references/typescript.md`
- `finding-report@1` output schema
- Subagents: recon, scanner, adversary, exit-gate
