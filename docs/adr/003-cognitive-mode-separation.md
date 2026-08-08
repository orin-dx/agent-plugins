# ADR-003: Cognitive mode separation

**Status:** Accepted
**Date:** 2026-08-08

## Context

Early plugin agents combined scanning and analysis in a single invocation — a single agent would grep for hazards and then assess whether each match was a real bug. This produced agents that were worse at both jobs: the scanner filtered matches because they "looked harmless," creating false negatives the downstream agent could never recover; the analyst had insufficient depth because it was also doing exhaustive enumeration. The alternative considered was one agent per cognitive mode.

## Decision

Agents are dispatched by the cognitive mode they require, not by pipeline position. Distinct modes: enumeration (mechanical completeness, no judgment — recon, scanner), tracing (systematic data-flow following — boundary-tracer), adversarial (default-to-skepticism, requires concrete failing scenario — adversary), systemic (cross-finding pattern recognition — architect), behavioral testing (tool execution and gap identification — mutator), judgment (weighing competing evidence for a binding decision — exit-gate, verifier), repair (minimum change + red-green verification — remediator, implementer). A plugin with multiple cognitive phases has a dedicated agent per mode. Model and effort tiers follow the same logic: `haiku/low` for enumeration, `sonnet/medium` for analysis, `opus/high` for binding judgment.

## Consequences

Each agent is optimized for exactly one cognitive mode and cannot self-corrupt by switching modes mid-task. A scanner cannot filter (its judgment criterion is "did you emit every match"); an adversary cannot enumerate (its judgment criterion is "can you state a concrete failing scenario"). Adding a new cognitive phase to a plugin always means a new agent file.
