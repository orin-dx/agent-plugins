---
name: pr
description: Draft or open a reviewer-ready pull request from verified work. Use when the user asks to create a PR or write its description; require confirmation before any remote action.
---

State material concerns, evidence, consequence, and confidence directly. Do not soften blockers, manufacture praise, or claim certainty beyond the evidence.

# Open a reviewable pull request

Ground the PR in the actual branch diff, target branch, linked lifecycle artifacts, and executed verification. A reviewer should be able to understand the intent, evidence, and residual risk without reconstructing the branch history.

## Evidence to collect

- Compare the current branch to its intended base and inspect the full diff.
- Read linked `shared/schemas/requirement@1.json`, `shared/schemas/spec@1.json`, or persisted artifact paths only when they apply to the change.
- Record verification commands and their observed outcomes. Do not claim checks that were not run.
- Identify migrations, operational follow-up, known limitations, and intentionally deferred work.

## Draft shape

Write a concise title and body with:

- An outcome-led summary of user-visible or architectural intent.
- Observed verification with exact commands or inspections and results.
- Reasons and coverage gaps for checks not run.
- Risks, migrations, limitations, or follow-up only when they apply.
- Existing issue, requirement, spec, plan, or changeset links only when they help review.

Use enough summary bullets to explain one coherent change. If the summary reveals independent topics, recommend separate PRs or state the dependency that requires one delivery.

Show the exact title, body, labels, base branch, and repository target before creating anything remotely. Create the PR only after explicit user confirmation.

## Team use

Before delegating, read `agent-roles/README.md`; use `recon` for linked-criteria inventory or `reviewer` for verification-output review, never for the final PR narrative.

When agent teams are available, use parallel work only for independent evidence collection: one teammate may inventory linked criteria while another summarizes verification output. Reconcile both against the live diff yourself. If teams are unavailable, collect those inputs sequentially and produce the same result.

## Safety

- Do not publish a draft as a PR, assign reviewers, add labels, or alter the target branch without user confirmation.
- Do not fabricate issue links, test results, or acceptance evidence.
