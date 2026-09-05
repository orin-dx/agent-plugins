# ADR-010: Ecosystem brand becomes "Wisp Plugins"

**Status:** Accepted
**Date:** 2026-09-03
**Supersedes:** the umbrella-brand clause of ADR-007. Plugin ids, skill names, categories, and the `persona:action` convention from ADR-007 are unchanged.

## Context

ADR-007 named the ten-plugin family **Wisp**. Separately, `orin-axi/wisp` is the local-first project-intelligence library these plugins consume — it validates and persists the `spec@1`/`plan@1` artifacts the plugins hand off, and compiles the briefings `smith`, `sentinel`, and `scribe` will read. Two different things carried one name across two repositories, and every cross-reference between them had to disambiguate by hand.

## Decision

- The library keeps **Wisp**.
- The plugin ecosystem is **Wisp Plugins**. This is a brand change only: no `plugin.json` `id`, `name`, or version changes; no skill renames; no schema changes.
- In this repository, "Wisp" alone refers to the library. The ecosystem is written "Wisp Plugins" in prose and headings.
- The repository directory and remote name (`agent-plugins`) are unchanged by this ADR.

## Consequences

- `README.md` and any current-facing doc that says "together they're Wisp" says "Wisp Plugins".
- Historical changelog entries and ADR-007's own text stay as written; they record what the brand was when the rename shipped.
- The Wisp library's docs refer to this ecosystem as "Wisp Plugins (`agent-plugins`)". The artifact schemas stay authored here in `shared/schemas/`; Wisp vendors them at a pinned revision with checksums (Wisp D-010).
