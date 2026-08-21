---
name: receive-feedback
description: >-
  Trigger when the user asks to process or triage incoming review feedback: "address the feedback", "respond to review comments", "what do these comments mean", "triage this review". Categorizes incoming review comments as must-fix, suggestion, or question, using the Conventional Comments / Google review-label vocabulary, and produces a prioritized response plan. This is for feedback received on the user's own PR — critiquing someone else's PR is the built-in `code-review` skill's job, not this one.
version: 2.0.0
---

# Delta — Receive Feedback

<overview>
Bundles a review package — diff summary, linked spec, test results, open questions — and triages incoming comments by priority so the author can respond without re-reading the whole thread. Delegates entirely to `review-preprocessor`. Mechanical assembly and categorization only, no judgment about whether the underlying code is right — that's what produced the comments in the first place.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **review-preprocessor** | haiku / low | Before or during a PR review, bundle diff, linked spec, test results, and open questions, or triage incoming comments by priority. |
</dispatch>

<references>
`shared/references/github.md` — the Conventional Comments / Google review-label vocabulary (`praise:`/`nitpick:`/`issue:`/`suggestion:`/`question:` or `Nit:`/`Optional:`/`FYI:`) used to categorize incoming comments.
</references>

<io>
**Consumes**: PR diff, optionally linked `spec@1` or `requirement@1`, test results, incoming review comments
**Produces**: review package (diff summary, linked spec, test results, open questions) and a prioritized response plan (must-fix / suggestion / question).
</io>
