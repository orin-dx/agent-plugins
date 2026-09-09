# Implementation Review Evidence

Load only the evidence needed for the current review.

## Language rules

- Rust: load `shared/references/rust-hazards.md` and `shared/references/rust-hazards-t7-t10.md` for defect checks; load `shared/references/rust-smells.md` for semantic-model and architecture signals.
- TypeScript or JavaScript: load `shared/references/typescript-hazards.md` and `shared/references/typescript-hazards-t7-t10.md` for defect checks; load `shared/references/typescript-smells.md` for semantic-model and architecture signals.
- If the diff adds or changes comments, load `shared/references/code-comments.md`.

## Required evidence

- Scope: each change maps to the task or a required sibling repair.
- Behavior: tests prove specified outcomes rather than implementation shape.
- Hazards: changed code does not introduce a language-specific violation.
- Siblings: the search covers matching syntax and equivalent domain behavior.
- Structure: repeated defects are assessed for a missing concept, state, operation, boundary, abstraction, invariant, or enforcement mechanism.

A taxonomy match is a search lead, not proof. Cite live code for every issue and structural assessment.
