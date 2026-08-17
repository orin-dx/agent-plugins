# Rust Tooling Reference

_Loaded by: mutator, remediator. Contains test commands, build checks, and the non-negotiables that every fix must satisfy. Do not load for scanning or smell analysis._

---

## Workspace Test Discovery & Execution

Before running tests, check for project task runners to respect repo-specific workflows:

```bash
# Check for task runners
ls justfile Makefile moonrepo.yml .moon/ 2>/dev/null
```

1. **Task Runner First**: If a task runner exists (`just`, `moon`, `make`), invoke tests through the task runner using targeted arguments where supported (e.g. `just test <test_name>`).
2. **Native Fallback**: If no task runner is present, use the project's native test framework (`cargo nextest run <test_name>` or `cargo test -p <crate> --test <target>`).
3. **Context Efficiency**: Target the specific test or module under active development during inner TDD cycles to avoid flooding context with passing test output.

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
