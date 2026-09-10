# Documentation Voice

Write for the person who must use, review, or maintain the artifact. Be succinct, friendly, direct, and technically honest.

## Choose the reader

| Artifact | Lead with | Include when relevant |
| :--- | :--- | :--- |
| User guide or README | What the user can do and when to use it | Prerequisites, examples, limits, recovery |
| Contributor or architecture doc | System responsibility and decision | Boundaries, invariants, tradeoffs, evidence |
| PR or review | Outcome and approval-relevant risk | Verification, gaps, migration, follow-up |
| Changeset or release note | Observable consumer impact | Old behavior, new behavior, required action |
| Reference | Decision the guidance supports | Applicability, evidence, refutation, disposition |

Use the reader's language. User-facing docs describe tasks and outcomes before internal agents, schemas, or implementation details. Contributor docs may use precise engineering terms when those terms help the reader act.

## Voice

- Lead with the outcome. Add context only when it changes understanding or action.
- Use active voice, present tense, and second person for instructions.
- Prefer familiar, concrete words. Define unavoidable domain terms once.
- Keep one main idea per sentence and one actionable rule per list item.
- Be friendly without ceremony: respectful, calm, and helpful; no praise, apology, or enthusiasm added as padding.
- Practice radical candor: state the concern, evidence, consequence, and confidence. Label blockers plainly. Do not manufacture praise, hide impact behind soft language, or imply certainty the evidence does not support.
- State mechanisms, behavior, and observed results instead of promotional adjectives.
- Let length follow the reader's need. Preserve non-obvious rationale, constraints, migration steps, and risks.

## Structure

- Use the smallest form that makes the relationship clear: prose for one connected idea, bullets for short parallel items, tables for repeated fields, and diagrams for structure or flow.
- Split a bullet when it contains independently actionable rules. Convert it to prose when its explanation is more important than enumeration.
- Use numbered steps only when order affects correctness.
- State a rationale once, next to the decision it changes.
- Link to authoritative detail instead of copying it.

## Cut

- Conversational preambles, scene-setting, and process narration.
- Restatements of a title, signature, diff, table, or preceding sentence.
- Synonymous claims that add emphasis but no information.
- Hedge phrases such as “essentially,” “basically,” “in order to,” and “it is worth noting.”
- Empty quality claims such as “robust,” “seamless,” “powerful,” or “comprehensive” without the mechanism or evidence that earns them.
- Rhetorical hooks, inflated contrasts, and adjective clusters.

Words are warning signs, not a substitute for judgment. Keep a word when it is the clearest accurate term; remove it when it stands in for evidence.

## Self-check

- Can the intended reader find the outcome first?
- Does each sentence change what the reader knows or does?
- Are material concerns direct, evidenced, and calibrated?
- Can any paragraph, bullet, heading, or example be removed without loss?
- Does user-facing text explain user impact before internal machinery?
