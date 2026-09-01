---
name: plan
description: >-
  Trigger this skill when the user says "write a plan for X", "how do we implement this spec", "break this down into tasks", "what are the implementation steps", "create an implementation plan", or "plan this out". Also activate when a spec (spec@1) exists and the user is ready to move to implementation but hasn't broken it down yet. Produces a plan@1 artifact where every task includes exact file paths, a brief implementation approach, exact implementation code, the exact tests proving each criterion, a conventional commit message, and covers_criteria linking the task to specific acceptance criteria. spec_file_path and linked_requirement are propagated from the source spec. No TBDs. No "implement as appropriate." Every step is mechanically executable by a developer with zero domain context.
version: 1.5.0
---

# Navigator Planning Skill

<overview>
Navigator decomposes a spec@1 into a sequenced, bite-sized plan@1 that a developer or agent can execute without making any design decisions. Every task is independently testable, time-bounded, and fully specified down to exact code and commit messages.
</overview>

---

<behavior>

navigator is one skill, `plan`. Behavior adapts to what's asked, dispatching to whichever agent below fits the request — there is no separate `navigator/estimate` or `navigator/challenge` skill to invoke; estimating and challenging both happen inside this one skill.

- **Decompose a spec into a plan** — `planner` reads a spec@1, produces an ordered sequence of implementation tasks (exact file paths, a brief implementation approach, exact implementation code, the tests proving each criterion, a commit message, covers_criteria), and groups tasks into cohesive Subsystem Batches aligned with crate/package compilation boundaries as part of that decomposition — not a separate step. Reads the spec from disk at spec_file_path when set, and propagates spec_file_path, spec_hash, and linked_requirement into the plan@1 output. Also runs in amend mode: given an existing plan@1, a corrected spec@1, and the criterion_ids that changed, patches only the affected tasks instead of re-decomposing the whole plan.

- **Estimate an existing plan** — `estimator` assigns effort estimates (in minutes) to each task in a plan@1, identifies parallelizable tasks, and surfaces blocking dependencies.

- **Challenge a draft plan** — `challenger` adversarially reviews a plan@1 for missing tasks, wrong ordering, under-specified steps, over-sized tasks, missing error handling, and acceptance criteria orphaned from every task's covers_criteria. An amended plan (from planner's amend mode) is not exempt from this review.

</behavior>

---

<subagent_dispatch_matrix>

| Agent | Role | Model / Effort | Delegate When |
| :--- | :--- | :--- | :--- |
| **planner** | Plan author | sonnet / medium | Decompose a spec into ordered, subsystem-batched implementation tasks. |
| **estimator** | Effort estimator | sonnet / medium | Assign time estimates, identify parallelizable tasks, and surface blocking dependencies. |
| **challenger** | Adversarial reviewer | sonnet / medium | Stress-test a draft plan@1 (max 2 review rounds) before any implementation begins. |

</subagent_dispatch_matrix>

---

<artifact_contracts>

**Consumes**: `spec@1` (or its `spec_file_path`, read from disk when set)
**Produces**: `plan@1` — carries `spec_file_path`, `spec_hash`, and `linked_requirement` propagated from the source spec

</artifact_contracts>

---

<implementation_requirement>

Every task in a plan@1 specifies, in this order:

1. A brief implementation approach — decided before the test steps are written, so the tests prove a chosen design rather than locking one in by accident
2. The exact implementation code — a concrete baseline proving the task is achievable within its file targets and scope, not a shape smith's implementer must copy verbatim
3. The exact tests proving each of this task's covers_criteria criteria
4. The command confirming the full suite passes
5. The conventional commit message

Test steps are not required to precede implementation steps within a task. Smith's mutation-testing gate — not step order — is what verifies a test would actually catch a wrong implementation; a controlled comparison found no quality advantage from write-test-first ordering for agent-written code, at several times the token cost, and found it suppressed upfront design work agents otherwise did well ([Böckeler, "TDD inside the agent loop"](https://martinfowler.com/articles/exploring-gen-ai/tdd-in-the-agent-loop.html)).

A task that specifies implementation code with no corresponding test proving a covers_criteria criterion violates this requirement — the criterion has no evidence, regardless of write order. Smith's implementer may still adapt the baseline's shape at execution time, provided the same files, criteria, and tests are satisfied — see [ADR-009](../../../../docs/adr/009-implementer-shape-latitude.md).

</implementation_requirement>

---

<no_placeholders_rule>

Every step must show exact code. "Implement the feature", "add appropriate error handling", and "write tests as needed" are not steps — they are abdications. If the exact code is not known, it must be derived from the spec and documented as a concrete choice, not deferred as a TBD.

</no_placeholders_rule>
