# ADR-005: Axiom as artifact-agnostic verification gate

**Status:** Accepted
**Date:** 2026-08-08

## Context

Early pipeline designs had each stage perform its own output validation inline — lambda checked its own changeset, canon checked its own spec. This duplicated verification logic across stages and created inconsistent quality bars. An alternative was a single hardcoded "code review" gate at the end. The requirement was a gate reusable across all artifact types (spec, plan, changeset, finding report) with a consistent retry protocol.

## Decision

`axiom` is a reusable, artifact-agnostic verification gate. Any artifact type can be run through it by passing the artifact and evaluation criteria. The gate runs three agents in sequence: `recon` (haiku/low — builds a structured understanding of what the artifact claims), `verifier` (sonnet/medium — checks claims against evidence), `exit-gate` (opus/high — weighs evidence and issues a binding `verdict@1`). On fail, the orchestrator passes only the blockers array to the producing agent — not the full verification context — for a targeted patch. `retry_count` is tracked in `verdict@1` and incremented by the exit gate. Effort escalates on retry 2. Circuit breaks after 3 retries and escalates to human.

## Consequences

Any pipeline stage that produces an artifact can be quality-gated without duplicating verification logic. The retry protocol is consistent across all stages. Callers must implement the retry loop and must not forward full verification context on retry (a constitution-level rule). The gate's reusability means a substandard artifact at any stage gets the same quality treatment — not a lenient inline check.
