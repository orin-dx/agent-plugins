# Implementation Review Evidence

Load only the evidence needed for the current review.

## Language rules

- Rust: load `shared/references/hazards/rust.md` and `shared/references/hazards/rust-boundaries.md` for defect checks; load `shared/references/architecture/rust.md` for semantic-model and architecture signals.
- TypeScript or JavaScript: load `shared/references/hazards/typescript.md` and `shared/references/hazards/typescript-boundaries.md` for defect checks; load `shared/references/architecture/typescript.md` for semantic-model and architecture signals.
- Python: load `shared/references/hazards/python.md` and `shared/references/hazards/python-boundaries.md` for defect checks; load `shared/references/architecture/python.md` for semantic-model and architecture signals.
- Go: load `shared/references/hazards/go.md` and `shared/references/hazards/go-boundaries.md` for defect checks; load `shared/references/architecture/go.md` for semantic-model and architecture signals.
- Other languages: perform the core review and record the missing language pack as a coverage gap.
- If the diff adds or changes comments, load `shared/references/authoring/comments.md`.

## Required evidence

- Scope: each change maps to the task or a required sibling repair.
- Behavior: tests prove specified outcomes rather than implementation shape.
- Verification: method choice, boundary coverage, environment assumptions, and external-state freshness follow `shared/references/verification/evidence.md`.
- Hazards: changed code does not introduce a language-specific violation.
- Siblings: the search covers matching syntax and candidate sites with equivalent domain behavior.
- Structure: repeated defects are assessed for a missing concept, state, operation, boundary, abstraction, invariant, or enforcement mechanism.

A taxonomy match is a search lead, not proof. Cite live code for every issue and structural assessment.
