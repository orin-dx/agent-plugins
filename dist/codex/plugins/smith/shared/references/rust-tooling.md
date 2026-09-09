# Rust Tooling Reference

_Loaded by: mutator, remediator. Contains test commands, build checks, and the non-negotiables that every fix must satisfy. Do not load for scanning or smell analysis._

---

## Workspace Test Discovery & Execution

Before running tests, check for project task runners to respect repo-specific workflows:

```bash
# Check for task runners
ls justfile Makefile moonrepo.yml .moon/ 2>/dev/null
```

- Prefer the configured task runner.
- Otherwise use `cargo nextest` when configured or `cargo test` with the narrowest useful package or target.
- Use `cargo-mutants` when available and relevant to changed behavior.
- Use `proptest` or an existing fuzz target for combinatorial inputs when a structured generator and meaningful invariant are available.
- Run the applicable workspace suite before completion.

---

## NAPI Boundary Rules

_Applies only to crates with `napi` or `napi-derive` in `Cargo.toml`. Skip for CLI tools and pure Rust libraries._

- Every `#[napi]` export must have `#[napi(catch_unwind)]`.
- No `unsafe` outside the NAPI boundary.
- Return `napi::Result<T>`, not bare `T`.

---

## Non-Negotiables

Every fix must satisfy these before the green pass is claimed:

- No `unwrap()`/`expect()` in lib code (tests may use `expect` with a message).
- No `unsafe` outside an explicit FFI/NAPI boundary.
- `BTreeMap`/`BTreeSet` for output maps and error payloads — never `HashMap`/`HashSet` in user-visible or test-comparable output.
- `String::with_capacity` for strings built in loops.
- String truncation uses `floor_char_boundary`, never byte-index slicing.
- Every `pub` item has a doc comment.
- Plan/config struct fields must survive to the execution call site — confirm each field reaches the subprocess or downstream function.
