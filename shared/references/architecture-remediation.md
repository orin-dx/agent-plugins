# Architecture Remediation Evidence

Load the evidence needed to design a structural defect correction.

- Load `shared/references/workspace-conventions.md` to locate the persisted architecture model and gated specs.
- Rust: load `shared/references/rust-smells.md`.
- TypeScript or JavaScript: load `shared/references/typescript-smells.md`.
- Python: load `shared/references/python-smells.md`.
- Go: load `shared/references/go-smells.md`.
- Other languages: use the live architecture and persisted model; record the missing language pack as a coverage gap.

Read the live implementation and any persisted model before choosing a boundary. If the model is absent, inspect live structure and let `scribe:audit-architecture` bootstrap it before gate; absence does not prove that no constraint exists.

Use the defect-family instances and shared cause to select the smallest enforceable correction. Separate families that require different boundaries.

After implementation passes, refresh the persisted architecture model so the new boundary and invariant become durable evidence.
