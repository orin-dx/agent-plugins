# ADR-006: `<constitution>` section — 5-part agent structure

**Status:** Accepted
**Date:** 2026-08-22
**Supersedes:** ADR-001 (4-part agent structure) — extends it with a 5th section; the four original sections and their rationale are unchanged.

## Context

`constitution.md`'s Static Prompt Prefix Invariant and `agent-best-practices.md` §7 both claimed every agent prompt shared an identical static header for prompt-cache reuse. In practice no agent file had one — each of the 38 agent bodies started directly with `<backstory>` (or a `<load_first>` block), meaning the "identical header" was aspirational, not real, and rules meant to be ecosystem-wide (trust boundaries, output economy, reader-scoped writing, abstract tool language) were either copy-pasted with wording drift into whichever agents happened to need them, or silently absent elsewhere. A literal fix — identical content at the true start of every prompt — conflicted with two existing rules: the 4-part structure being described as exhaustive ("not 5 sections"), and EARS notation being confined to `<output>` only, which meant shared EARS content had no section that was both first and permitted to hold it.

## Decision

Every agent body defines five named sections, in order: `<constitution>`, `<backstory>`, `<goal>`, `<judgment>`, `<output>`. `<constitution>` must be byte-for-byte identical across every agent in the ecosystem — this is what the Static Prompt Prefix Invariant actually depends on now, rather than describing. EARS notation is permitted in `<constitution>` in addition to `<output>`, but content there must be genuinely ecosystem-wide; a rule specific to some agents belongs in that agent's own `<output>`, never in `<constitution>`, since agent-specific content there would break the byte-identical requirement for every other agent. The block's content: treat unauthored content as data not instruction, output-economy discipline (no preambles, exact pointers, proportionate scratchpads), reader-scoped writing for any artifact meant for a downstream reader, and abstract tool language. Rolled out to all 38 existing agent files via script (not hand-edited) to guarantee byte-identical output, verified by diffing every file's `<constitution>` block against every other's.

## Consequences

Cross-agent prompt-cache sharing is now something the file structure actually supports, not just documents. Six agents that had their own trust-boundary rule got it trimmed to just the non-redundant, agent-specific consequence, since the general rule now lives once in `<constitution>`. The other ~32 agents gained ~177 words of prompt content they didn't have before — a real per-invocation cost, not fully offset by trimming elsewhere, accepted in exchange for a shared, non-drifting source of ecosystem-wide rules and the cache-sharing this makes possible. `basis:scaffolder` and `basis:auditor` — the two agents responsible for generating and checking agent structure — had to be updated in the same change; a scaffolder or auditor unaware of `<constitution>` would silently generate or pass non-conformant agents.
