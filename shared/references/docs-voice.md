# Documentation Voice Reference

Canonical voice standard for this repo: commit messages, PR bodies, changesets, release notes, and prose docs (READMEs, `basis`-scaffolded plugin docs). Succinct, engineering-focused, scannable. No AI slop.

Agents load only the subset embedded in their own task reference file (`conventional-commits.md`, `github.md`, `changesets.md`) — see each for the operational rules. This file is the full standard, for humans and for `basis` when scaffolding new docs.

## Rules

1. Lead with the conclusion. Answer before justification (inverted pyramid) — readers scan ~20-28% of page text, they don't read top to bottom.
2. Active voice, present tense, second person for instructions.
3. One idea per sentence. Average sentence length ≤20 words.
4. Bullets or tables over paragraphs whenever the content is enumerable.
5. Separate *what changed* (factual, reference-like) from *why* (one sentence, no more) — don't blend them into one block.
6. State the mechanism, not the adjective. Numbers and behavior over "robust" / "powerful" / "seamless."
7. Cut hedge and filler qualifiers: "essentially," "basically," "in order to," "it's worth noting that."
8. Self-edit pass: after drafting, re-read once checking rules 5 and 9 specifically before output. Banned-word avoidance alone misses ~20% of slop without this pass.

## Banned words and phrases

*delve, leverage, seamless, robust, elevate, foster, unlock, empower, testament, pivotal, showcase, tapestry, landscape, underscore, meticulous, game-changer, cutting-edge, unprecedented, transformative, utilize (use "use"), dive into, supercharge, empowers, elevate*

Banned structures: "It isn't just X, it's Y." Rhetorical-question hooks. Triplets of adjectives as padding.

## Review-feedback vocabulary

When a change involves triaging or drafting comments on someone else's work (not narrating your own diff), prefix intent so it reads unambiguously before tone does. Two equivalent vocabularies — pick one per context and stay consistent within it:

- **Conventional Comments**: `praise:` `nitpick:` `suggestion:` `issue:` `question:` `thought:` — optionally decorated `(non-blocking)`.
- **Google code review style**: `Nit:` `Optional:` / `Consider:` `FYI:` for anything that isn't a blocking request.

Always include at least one positive comment when reviewing someone else's work, not only problems. State the problem and let the author decide the fix when more than one valid fix exists — don't dictate unless there's exactly one correct answer.

## Source

Distilled from: Google Developer Documentation Style Guide, Microsoft Writing Style Guide, Diátaxis, Keep a Changelog, Federal Plain Language Guidelines, NN/g F-pattern reading research, Conventional Comments (conventionalcomments.org), Google's code review developer guide.
