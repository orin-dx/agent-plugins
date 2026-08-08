# Rust Tooling Reference

_Loaded by: mutator, remediator. Contains test commands, build checks, and the non-negotiables that every fix must satisfy. Do not load for scanning or smell analysis._

---

## Test Commands

```bash
# Run all tests
cargo nextest run

# Run a specific test by name
cargo nextest run test_name

# Run with stdout (for debugging)
cargo nextest run -- --nocapture

# Type-check only (no build artifacts)
cargo check --all-features

# Lint — treat all warnings as errors
cargo clippy --all-features -- -D warnings

# Mutation testing (mutator agent)
cargo mutants --workspace
```

---

## Workspace Test Discovery

Before running tests, confirm the test runner in use:

```bash
# Check for task runners
ls justfile Makefile moonrepo.yml .moon/ 2>/dev/null

# Run via task runner if present
just test
moon run :test

# Otherwise fall back to cargo nextest
cargo nextest run
```

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
