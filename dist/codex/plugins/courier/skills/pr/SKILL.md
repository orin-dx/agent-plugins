---
name: pr
description: Draft or open a reviewer-ready pull request from verified work. Use when the user asks to create a PR or write its description; require confirmation before any remote action.
---

# Open a reviewable pull request

Ground the PR in the actual branch diff, target branch, linked lifecycle artifacts, and executed verification. A reviewer should be able to understand the intent, evidence, and residual risk without reconstructing the branch history.

## Evidence to collect

- Compare the current branch to its intended base and inspect the full diff.
- Read linked `shared/schemas/requirement@1.json`, `shared/schemas/spec@1.json`, or persisted artifact paths only when they apply to the change.
- Record verification commands and their observed outcomes. Do not claim checks that were not run.
- Identify migrations, operational follow-up, known limitations, and intentionally deferred work.

## Draft shape

Write a concise title and body with:

- Summary of user-visible or architectural intent.
- Scope and non-scope.
- Evidence: criteria, tests, and relevant paths.
- Risks, migration notes, or follow-up work.

Show the exact title, body, labels, base branch, and repository target before creating anything remotely. Create the PR only after explicit user confirmation.

## Team use

Before delegating, read `agent-roles/README.md`; use `recon` for linked-criteria inventory or `reviewer` for verification-output review, never for the final PR narrative.

When agent teams are available, use parallel work only for independent evidence collection: one teammate may inventory linked criteria while another summarizes verification output. Reconcile both against the live diff yourself. If teams are unavailable, collect those inputs sequentially and produce the same result.

## Safety

- Do not publish a draft as a PR, assign reviewers, add labels, or alter the target branch without user confirmation.
- Do not fabricate issue links, test results, or acceptance evidence.
