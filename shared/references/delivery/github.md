# GitHub Reference

## Pull requests

A PR body gives a reviewer with no prior context enough information to understand the outcome, inspect the risky decisions, and verify the change. Ground it in the live base-branch diff and observed checks.

```markdown
## Summary
- Outcome and why it matters
- Important behavioral or architectural decision, when needed for review

## Verification
- [x] `exact command or inspection` — observed result
- [ ] Not run: reason and resulting coverage gap

## Risk and follow-up
<!-- Include only migrations, compatibility risks, limitations, rollout work, or intentional deferrals. -->

## Related
<!-- Include only links that exist: issue, requirement, spec, plan, or changeset. -->
```

Omit empty optional sections and placeholder links. Use enough summary bullets to explain one coherent change; if the bullets reveal independent topics, split the PR or explain why they must ship together.

Verification records evidence already observed. Never turn an unrun check into an unchecked instruction without stating why it was not run and what remains unverified.

Call out breaking behavior under `Risk and follow-up` with the old behavior, new behavior, and required migration.

## Voice

- Lead with user-visible or architectural intent, not a file inventory or development chronology.
- Use direct, active language and concrete outcomes.
- State material concerns, evidence, consequence, and confidence without softening blockers or overstating certainty.
- Keep technical detail that changes approval; link to deeper artifacts instead of copying them.
- Do not restate the diff.

## Review comments

Prefix intent when it prevents ambiguity. Use one vocabulary consistently:

- Conventional Comments: `praise:`, `nitpick:`, `suggestion:`, `issue:`, `question:`, `thought:`; add `(non-blocking)` when needed.
- Google style: `Nit:`, `Optional:`, `Consider:`, `FYI:` for non-blocking feedback.

Do not manufacture praise. When a material issue exists, state the problem, cite the evidence, explain the consequence, and mark whether it blocks approval. Recommend one fix only when the constraints make it uniquely correct; otherwise describe the required outcome.

## Review focus

- Does the change satisfy its linked requirement or specification?
- Does every changed behavior have discriminating evidence at the relevant boundary?
- Are skipped checks and residual risks explicit?
- Are breaking changes, migrations, and consumer-facing effects documented?
- Do shared contracts, generated artifacts, and supported harnesses remain aligned when affected?
- Does the change contain unrelated scope or unresolved sibling defects?

## `gh` commands

```bash
gh pr create --title "feat(ranger): add cross-language audit" --body-file body.md
gh pr list
gh pr diff <number>
gh pr status
gh pr review <number> --approve
gh pr review <number> --request-changes --body-file review.md
gh pr merge <number> --squash --delete-branch
```

Show the exact target, title, body, labels, and review text before any remote mutation. Never invent issue links, results, or artifact paths.

## Issues

```bash
gh issue create --title "..." --body-file issue.md --label bug
gh issue list --label enhancement
gh issue close <number>
```

## GitHub Actions annotations

```text
::error file=src/lib.rs,line=42,col=5::Error message here
::warning file=src/lib.rs,line=10::Warning message here
::notice file=src/lib.rs,line=1::Notice message here
```

## Labels

| Label | Meaning |
| :--- | :--- |
| `bug` | Confirmed defect |
| `enhancement` | New capability or improvement |
| `breaking` | Consumer migration required |
| `needs-spec` | Specification required before implementation |
| `needs-plan` | Plan required before implementation |
| `in-progress` | Active work |
| `blocked` | External resolution required |
