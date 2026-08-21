# GitHub Reference

## PR Description Template

```markdown
## Summary
- What changed (1-3 bullets, user-facing language)
- Why it was needed

## Test Plan
- [ ] How to verify the change works
- [ ] Edge cases to check
- [ ] Regression check

## Related
Closes #<issue>
Spec: <link to spec doc>
```

## Voice

Summary bullets first, test plan as a checklist — never a prose recap of the diff. Lead with the conclusion (why this matters to a reviewer), not a chronology of what was touched. Active voice, ≤20 words/sentence average, no banned words (*delve, leverage, seamless, robust, elevate, foster, unlock, empower, testament, pivotal, showcase, meticulous, game-changer, utilize*). Full standard: `shared/references/docs-voice.md`.

When triaging or drafting comments on someone else's PR, prefix intent: `praise:` `nitpick:` `suggestion:` `issue:` `question:` (Conventional Comments), or `Nit:` / `Optional:` / `FYI:` (Google style) — pick one vocabulary and stay consistent.

## PR Review Checklist

When reviewing a PR:
- Does the change match the linked spec/requirement?
- Are tests present for each acceptance criterion?
- Are breaking changes documented in the changeset?
- Is the commit history clean (conventional commits, no "WIP" merges)?

## gh CLI Commands

```bash
# Create PR
gh pr create --title "feat(proof): add cross-language recon agent" --body "$(cat body.md)"

# List open PRs
gh pr list

# View PR diff
gh pr diff <number>

# Check PR status
gh pr status

# Review a PR
gh pr review <number> --approve
gh pr review <number> --request-changes --body "..."

# Merge
gh pr merge <number> --squash --delete-branch

# Link issue to PR
gh pr create --title "..." --body "Closes #123"
```

## Issues

```bash
# Create issue
gh issue create --title "..." --body "..." --label "bug"

# List issues
gh issue list --label "enhancement"

# Close issue
gh issue close <number>
```

## GitHub Actions Annotations

```
::error file=src/lib.rs,line=42,col=5::Error message here
::warning file=src/lib.rs,line=10::Warning message here
::notice file=src/lib.rs,line=1::Notice message here
```

## Labels Convention

| Label | Meaning |
|---|---|
| `bug` | Confirmed defect |
| `enhancement` | New feature or improvement |
| `breaking` | Breaking change |
| `needs-spec` | Requires a canon spec before implementation |
| `needs-plan` | Requires a vector plan before implementation |
| `in-progress` | Actively being worked |
| `blocked` | Cannot proceed without external resolution |
