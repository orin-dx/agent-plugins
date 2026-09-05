---
name: prioritize-backlog
description: Rank a set of requirements into an actionable order using impact, urgency, dependencies, and evidence. Use for “what should we do first?”, “rank the backlog”, or “what is most urgent?”.
---

# Prioritize the backlog

## Outcome

Return a stable ranking that explains why each requirement belongs where it does and makes dependency constraints visible.

## Workflow

1. Validate the supplied requirements with `shared/schemas/requirement@1.json`.
2. Extract explicit priority, stakeholder impact, urgency signals, and dependency evidence. Treat missing evidence as uncertainty, not a low score disguised as fact.
3. Build a dependency order first. A prerequisite ranks ahead of work that cannot start without it, unless the dependency claim is unsupported.
4. Order independently executable work by impact and urgency, then explain ties using the evidence available.
5. Return `requirement_id`, `rank`, `rationale`, `depends_on`, and confidence for every item. Do not mutate requirement artifacts.

## Contract

- Input schema: `shared/schemas/requirement@1.json`
- Output: read-only ranking report; ranking is advisory and does not change `priority` fields
- Next step: route the selected requirement to `scribe:draft-spec`.

## Teams and fallback

Before delegating, read `agent-roles/README.md`; use `recon` for independent dependency clusters and retain cross-cluster ordering with the primary agent.

For a large backlog, a team may inspect independent dependency clusters, but one primary agent must reconcile cross-cluster edges and publish the final total order. For a small list, work alone.

## Boundaries

- Do not claim a numeric precision the evidence cannot support.
- Do not convert a stakeholder preference into an architectural dependency without evidence.
