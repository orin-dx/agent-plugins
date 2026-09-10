---
name: pr
description: >-
  Trigger when the user asks to open a PR or write a PR description: "open a PR", "create a pull request", "write the PR description". Given a diff, a linked spec, and a linked requirement, produces a PR title and body a reviewer with zero context can act on, then opens the PR via `gh pr create` after user confirmation.
version: 2.0.1
---

# Courier — PR

<overview>
Produces a PR title and body from a diff plus optional linked spec/requirement, then opens the PR. Delegates the narrative to `pr-narrator`; opening the PR is a visible external action and always requires explicit confirmation before the `gh pr create` call fires.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **pr-narrator** | sonnet / medium | A PR needs a title and body a reviewer with zero context can act on. |
</dispatch>

<references>
`shared/references/github.md` — outcome-led PR structure, observed verification, risk disclosure, review voice, labels, and `gh` commands.
</references>

<io>
**Consumes**: git diff, optionally linked `spec@1` or `requirement@1`
**Produces**: opened PR (title, body, labels). Confirm the drafted title/body with the user before running `gh pr create` — this is a shared-visibility action, not a local one.
</io>
