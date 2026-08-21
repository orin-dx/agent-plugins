---
name: post-review
description: >-
  Trigger when the user has an already-drafted review or reply and wants it posted: "post this review", "reply to this comment", "mark this thread resolved", "submit my review comments". Takes drafted content — from the built-in `code-review` skill's findings, from `delta/receive-feedback`'s response plan, or typed directly by the user — and posts it to GitHub via `gh pr review` or `gh pr comment`. Does not draft content itself; this skill is purely mechanical execution of something already written, gated by explicit user confirmation before any post fires.
version: 2.0.0
---

# Delta — Post Review

<overview>
Posting a review comment is a visible, external, hard-to-reverse action — the kind this repo's action-safety guidance already requires confirmation for. There is no subagent here: drafting a critique is a judgment task owned by `code-review` (quality) and `axiom` (spec conformance), and drafting a reply is owned by `delta/receive-feedback`'s response plan or the user directly. This skill's only job is the mechanical last step — show exactly what will be posted and where, get explicit confirmation, then run the `gh` command.
</overview>

<dispatch>
No subagent. Orchestration only: assemble the exact comment/review body and target (PR number, thread ID if replying) from the input, present it verbatim to the user, and on confirmation run `gh pr review <number> --body "..."` or `gh pr comment <number> --body "..."`.
</dispatch>

<references>
`shared/references/github.md` — `gh` CLI commands for posting reviews and comments.
</references>

<io>
**Consumes**: drafted review/reply text and its target (PR number, optionally thread ID), from `code-review`, `delta/receive-feedback`, or the user directly
**Produces**: posted GitHub review or comment. NEVER post without showing the exact text and target to the user first and getting explicit confirmation — this is an irreversible, other-visible action.
</io>
