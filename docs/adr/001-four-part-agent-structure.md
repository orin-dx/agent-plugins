# ADR-001: 4-part agent structure

**Status:** Accepted
**Date:** 2026-08-08

## Context

Agent prompts were written with a `<role>` XML section labelling the agent ("Senior Rust Engineer") and a `success_criteria` checklist. Role labels shape posture, not judgment. Success criteria checklists let agents tick boxes without producing correct output — an agent can satisfy every criterion while still confirming a false positive. Two alternatives were considered: (a) keep role labels as routing metadata only, (b) replace with experiential backstory. The plugin ecosystem routes via frontmatter `role:` field anyway, making the XML `<role>` section redundant.

## Decision

Every agent body defines exactly four XML sections: `<backstory>` (2–4 sentences of experiential perspective — what has this agent been burned by, what does it value as a result), `<goal>` (intent, not steps), `<judgment>` (the specific failure mode that looks like success), `<output>` (schema reference and EARS contracts). No `<role>` body section. No `success_criteria` checklist. The `role:` frontmatter field is retained as platform routing metadata only.

## Consequences

Backstory shapes judgment in genuinely ambiguous situations where a role label would not. Judgment makes the most likely failure mode explicit before the agent encounters it. The agent's interior — how it searches and reasons — is unconstrained by the structure. Adds an authoring obligation: authors must think about what failure mode the agent is most likely to fool itself with.
