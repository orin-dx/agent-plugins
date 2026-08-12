---
name: plan
description: >-
  Trigger this skill when the user says "write a plan for X", "how do we implement this spec", "break this down into tasks", "what are the implementation steps", "create an implementation plan", or "plan this out". Also activate when a spec (spec@1) exists and the user is ready to move to implementation but hasn't broken it down yet. Produces a plan@1 artifact where every task includes exact file paths, TDD steps with failing test first, exact implementation code, expected test output, a conventional commit message, and covers_criteria linking the task to specific acceptance criteria. spec_file_path and linked_requirement are propagated from the source spec. No TBDs. No "implement as appropriate." Every step is mechanically executable by a developer with zero domain context.
version: "1.2.0"
---

# Vector Planning Skill

<overview>
Vector decomposes a spec@1 into a sequenced, bite-sized plan@1 that a developer or agent can execute without making any design decisions. Every task is independently testable, time-bounded, and fully specified down to exact code and commit messages.
</overview>

---

<sub_skills>

### vector/plan
Invoke vector-planner to decompose a spec@1 into an ordered sequence of implementation tasks. Each task includes exact file paths, a failing test, minimal implementation, expected test output, a commit message, and covers_criteria linking it to specific acceptance criteria. Reads the spec from disk at spec_file_path when set, and propagates spec_file_path, spec_hash, and linked_requirement into the plan@1 output. Also runs in amend mode: given an existing plan@1, a corrected spec@1, and the criterion_ids that changed, patches only the affected tasks instead of re-decomposing the whole plan.

### vector/estimate
Invoke vector-estimator to assign effort estimates (in minutes) to each task in a plan@1, identify parallelizable tasks, and surface blocking dependencies.

### vector/challenge
Invoke vector-challenger to adversarially review a plan@1 for missing tasks, wrong ordering, under-specified steps, over-sized tasks, missing error handling, and acceptance criteria orphaned from every task's covers_criteria. An amended plan (from vector/plan's amend mode) is not exempt from this review.

### vector/decompose
Decompose a large or ambiguous task into smaller, dependency-ordered sub-tasks before planning. Use when a single task in the plan would exceed 15 minutes or require the implementer to make a design choice.

</sub_skills>

---

<subagent_dispatch_matrix>

| Agent | Role | Model / Effort | Delegate When |
| :--- | :--- | :--- | :--- |
| **vector-planner** | Plan author | sonnet / medium | Decompose a spec@1 into ordered, self-contained implementation tasks. |
| **vector-estimator** | Effort estimator | sonnet / medium | Assign time estimates, identify parallelizable tasks, and surface blocking dependencies. |
| **vector-challenger** | Adversarial reviewer | opus / high | Stress-test a draft plan@1 before any implementation begins. |

</subagent_dispatch_matrix>

---

<artifact_contracts>

**Consumes**: `spec@1` (or its `spec_file_path`, read from disk when set)
**Produces**: `plan@1` — carries `spec_file_path`, `spec_hash`, and `linked_requirement` propagated from the source spec

</artifact_contracts>

---

<tdd_requirement>

Every task in a plan@1 follows this exact sequence:

1. Write the failing test
2. Run the test — confirm it fails with the expected error
3. Write the minimal implementation to make the test pass
4. Run the test — confirm it passes
5. Commit with the conventional commit message

A task that starts with implementation before a failing test violates this requirement.

</tdd_requirement>

---

<no_placeholders_rule>

Every step must show exact code. "Implement the feature", "add appropriate error handling", and "write tests as needed" are not steps — they are abdications. If the exact code is not known, it must be derived from the spec and documented as a concrete choice, not deferred as a TBD.

</no_placeholders_rule>
