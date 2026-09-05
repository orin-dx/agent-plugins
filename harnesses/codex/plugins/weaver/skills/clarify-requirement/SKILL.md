---
name: clarify-requirement
description: Find and close the single highest-value gap in a requirement draft. Use when a requirement needs to be ready for specification, or the user asks what is missing from it.
---

# Clarify a requirement

## Outcome

Return either one focused question that removes the blocking ambiguity or a completed `requirement@1` ready for specification.

## Workflow

1. Validate the draft against `shared/schemas/requirement@1.json` before judging completeness.
2. Inspect `done_when` first: each condition must be observable from outside the implementation and distinguish success from failure.
3. Then inspect stakeholder, why, and out-of-scope boundaries. Prefer the gap that would most alter the resulting spec or prevent a testable criterion.
4. Ask exactly one question when a material fact is missing. Explain the decision it unlocks in one sentence.
5. When no material fact is missing, return the updated artifact with explicit `out_of_scope` entries. Persist only with user authorization at `docs/requirements/<id>.json`.

## Contract

- Schema: `shared/schemas/requirement@1.json`
- Input: one `requirement@1` draft and any answer to a prior clarification
- Output: one question or a valid completed `requirement@1`
- Next step: repeat after an answer, then route the completed artifact to `scribe:draft-spec`.

## Teams and fallback

This is a judgment task over one artifact, so complete it in the current agent. Do not delegate a question merely to use a team.

## Boundaries

- Never manufacture stakeholder intent, scope, or acceptance conditions.
- Never ask a batch of questions; the user should be able to answer and continue in one turn.
