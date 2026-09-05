---
name: post-review
description: Deliver already-drafted PR comments or reviews. Use when the user asks to post a prepared reply, submit review comments, or resolve a named thread; never author or post content without confirmation.
---

# Deliver approved review content

This skill performs a visible external action only. It does not critique code, determine whether feedback is correct, or rewrite the user's prepared response.

## Required input

- Exact comment or review body.
- Precise repository and pull-request target.
- Thread identifier when replying to or resolving a specific thread.
- Intended operation: comment, review submission, reply, or resolve.

## Workflow

1. Verify that the target exists and that the requested operation matches the supplied identifiers.
2. Show the exact text, target, and operation verbatim.
3. Ask for explicit confirmation.
4. Perform only the confirmed external action and report its resulting URL or identifier.

## Safety

- Never post, submit, or resolve a thread from a summary, inferred intent, or prior confirmation for different text.
- Do not combine several comments into one action unless the user sees and confirms every target and body.
- If the text needs authoring or substantive review, route that work to the user or the relevant review workflow before returning here.

## Team use

Do not request an agent team. This is a narrow, externally visible delivery step.
