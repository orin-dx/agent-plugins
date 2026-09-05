---
name: receive-feedback
description: Assemble a neutral evidence package for incoming PR feedback. Use when the user asks to understand, triage, or respond to review comments on their own pull request.
---

# Prepare review-response context

This skill organizes evidence for the author; it does not decide whether a reviewer is right. Keep review comments, repository facts, and unresolved questions distinct.

## Workflow

1. Identify the PR, its current diff, base branch, review comments, and thread state.
2. Read only linked requirements, specs, plans, or prior verdicts that bear on a comment.
3. Gather the most relevant test results and source locations for each discussion thread.
4. Produce a response package with factual context, open questions, and suggested investigation paths.

## Output

For each thread, include:

- The comment and target location.
- Evidence that supports or complicates it.
- Related lifecycle criterion or artifact path, if one exists.
- Test or inspection evidence.
- An explicit unresolved question when the evidence does not settle the issue.

Do not label comments as valid, invalid, high priority, or ready to resolve. Those are author decisions after reviewing the package.

## Team use

Before delegating, read `agent-roles/README.md`; use `recon` only for separate review-thread evidence packages with no shared-diff ambiguity.

For several independent review threads, agent teams may gather context per non-overlapping thread. Keep each response package independent and reconcile shared-diff facts before returning. Complete the same thread-by-thread investigation yourself when teams are unavailable.
