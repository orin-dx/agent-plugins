---
name: receive-feedback
description: >-
  Trigger when the user asks to process or triage incoming review feedback: "address the feedback", "respond to review comments", "what do these comments mean", "triage this review". Assembles a review package — diff summary, linked spec, test results, open questions — so the author has full context to respond without re-reading the whole thread. Does not categorize individual comments by priority; that's the caller's judgment call, made with `shared/references/github.md`'s vocabulary in hand. This is for feedback received on the user's own PR — critiquing someone else's PR is the built-in `code-review` skill's job, not this one.
version: 2.0.0
---

# Courier — Receive Feedback

<overview>
Bundles a review package — diff summary, linked spec, test results, open questions — so the author can respond without re-reading the whole thread. Delegates entirely to `review-preprocessor`. Mechanical assembly only; `review-preprocessor`'s own judgment explicitly refuses to categorize comment priority, since it has no visibility into whether the underlying code is right — that's what produced the comments in the first place, and it's the caller's call to make, informed by `shared/references/github.md`'s vocabulary.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **review-preprocessor** | haiku / low | Before or during a PR review, bundle diff, linked spec, test results, and open questions the author needs before responding. |
</dispatch>

<references>
`shared/references/github.md` — the Conventional Comments / Google review-label vocabulary (`praise:`/`nitpick:`/`issue:`/`suggestion:`/`question:` or `Nit:`/`Optional:`/`FYI:`) the caller applies by hand when triaging the assembled package; `review-preprocessor` does not load or apply it.
</references>

<io>
**Consumes**: PR diff, optionally linked `spec@1` or `requirement@1`, test results, incoming review comments
**Produces**: review package (diff summary, linked spec, test results, open questions) — the caller triages the incoming comments against it using `shared/references/github.md`'s vocabulary; `review-preprocessor` does not categorize them.
</io>
