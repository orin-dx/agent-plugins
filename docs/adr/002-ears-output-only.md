# ADR-002: EARS notation restricted to output sections

**Status:** Accepted
**Date:** 2026-08-08

## Context

Early agents used EARS notation (`WHEN / IF / WHILE / WHERE / THE SYSTEM SHALL`) throughout prompts — in backstory, goal, and implementation guidance — wherever a hard constraint felt useful. This capped agents at the level of the author's imagination: every step that was EARS-encoded was a step the agent couldn't improve on. Two alternatives were considered: (a) EARS throughout, (b) EARS only at the boundary (output contracts and never-do rules).

## Decision

EARS notation is permitted only in `<output>` sections, encoding hard constraints on what the agent must produce, must not produce, or must do under a specific condition. The interior — backstory, goal, judgment — is intentionally unconstrained. EARS is the fence; backstory and goal fill the interior with judgment.

## Consequences

Authors can precisely specify output contracts and never-do rules without over-specifying search strategy or reasoning approach. Agents remain capable of adapting their interior approach to novel situations. Auditing EARS placement is mechanical: if EARS appears outside `<output>`, it's a violation.
