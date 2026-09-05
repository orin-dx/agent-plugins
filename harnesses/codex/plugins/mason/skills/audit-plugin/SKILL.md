---
name: audit-plugin
description: Audit a plugin against the repository's concrete authoring and packaging rules. Use when the user asks whether a plugin conforms, is installable, or is ready to release.
---

# Audit a plugin from its declared contract

Inspect the named plugin and its declared harnesses rather than evaluating style in the abstract. For cross-harness work, read `shared/harness-authoring.md` and its change record first. Start from manifests and paths, then trace every declared route to its implementation and contract.

## Checks

- Source manifest identity, semver, skills path, declared agents, and file presence.
- Skill frontmatter, trigger discrimination, concrete workflow, safety boundaries, and artifact schema paths.
- Agent prompt structure, model/effort routing, shared constitution prefix, progressive context loading, and handoff contracts.
- Shared schema versioning, required `reasoning`, and `additionalProperties: false` when a new handoff is introduced.
- README, changelog, marketplace registration, and current installation guidance.
- For Codex, `.codex-plugin/plugin.json`, native skill directories, interface metadata, generated bundle parity, and no unresolved source symlinks in distributable output.

## Evidence standard

Return one row per check with status `pass`, `fail`, or `warn`, the observed path, and repair guidance. A missing file is a fail only when a manifest, contract, or required convention declares it. Do not call a plugin ready based on filenames alone.

## Team use

Before delegating, read `agent-roles/README.md`; use `recon` for surface inventory and `reviewer` for an independent conformance reading before the primary agent reconciles findings.

When teams are available, split independent inspection by surface: source plugin, Codex adaptation, and generated distribution. The owner must reconcile findings against shared manifests and avoid duplicate reports. Perform the same passes sequentially when teams are unavailable.

## Safety

This is read-only by default. Do not repair, regenerate, install, or publish a plugin unless the user asks for that follow-on work.
