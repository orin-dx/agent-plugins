# Rust Language Reference for Agent Plugins

Runtime-pullable by agents when scanning or implementing Rust code. Contains hazard taxonomies, search heuristics, and workspace conventions.

## Workspace Discovery

```bash
# Find crate root
find . -name "Cargo.toml" -not -path "*/target/*"

# List workspace members
cargo metadata --no-deps --format-version 1 | jq '.workspace_members'

# Check what's actually compiled (live code only)
# A file is live if it's declared via `mod` in lib.rs, main.rs, or a parent module
grep -r "^mod " src/ --include="*.rs"
```

**Dead code detection:** files in `src/` that are not reachable from `lib.rs` or `main.rs` via `mod` declarations are dead. Do not report findings in dead code.

## Hazard Taxonomies

### 1. Discarded Parameters
- **Signal:** `fn foo(_param: T)` — leading underscore on a parameter
- **Search:** `fn\s+\w+[^{]*\b_[a-zA-Z][a-zA-Z0-9_]*:\s*`
- **Risk:** User-provided value is silently ignored
- **False positive check:** Confirm the parameter is not a trait requirement (e.g., `trait Foo { fn bar(&self, _: T) }` is intentional)

### 2. Silent Unwrap Fallbacks
- **Signal:** `.unwrap_or(default)`, `.unwrap_or_default()`, `.unwrap_or_else(|| ...)`
- **Search:** `\.unwrap_or\b|\.unwrap_or_default\b|\.unwrap_or_else\b`
- **Risk:** Error is swallowed; wrong behavior proceeds silently
- **False positive check:** Is the default semantically correct for all callers? Is the error logged?

### 3. Panic in Lib Code
- **Signal:** `.unwrap()`, `.expect("...")`, `panic!(...)`
- **Search:** `\.unwrap\(\)|\.expect\(|panic!\(`
- **Risk:** Unrecoverable crash propagates to caller
- **False positive check:** Test code and `fn main` are acceptable

### 4. Missing Error Propagation
- **Signal:** `let _ = result;`, `drop(result)`
- **Search:** `let _\s*=|drop\(\w*result\w*\)`
- **Risk:** Error is discarded; subsequent code runs on invalid state

### 5. Integer Overflow in Release
- **Signal:** Arithmetic on user-controlled integers without checked ops
- **Search:** `\b(usize|u32|u64|i32|i64)\b.*[+\-\*]`
- **Risk:** Wraps in release mode; panics in debug
- **False positive check:** Is this in a context where overflow is impossible or handled?

### 6. Unsafe Boundary Violations
- **Signal:** `unsafe` blocks, raw pointer dereference outside NAPI boundary
- **Search:** `unsafe\s*\{`
- **Risk:** Memory unsafety, UB
- **False positive check:** Is this in an `#[napi]` context or FFI shim? If yes, review carefully but lower severity.

## Architectural Smell Sweeps

### UTF-8 Boundary Issues
- Never use `&s[..n]` — use `s.floor_char_boundary(n)` or `s.chars().take(n)`
- Search: `&\w+\[\.\.[\w\d]+\]`

### Missing `BTreeMap` for Output
- Maps that appear in agent-visible output must use `BTreeMap` (deterministic key order)
- `HashMap` is fine for internal state
- Search: `HashMap<` in response/render code

### String Pre-allocation
- Strings built with repeated `push_str` or `format!` in a loop must use `String::with_capacity`
- Search: `String::new()` followed by `.push_str` in loops

### Float Rendering
- `f64` values in agent output must handle `NaN` and `Inf` explicitly
- Search: `f64` in render/display code; check for guard

## NAPI Boundary Rules

- Every `#[napi]` export must have `#[napi(catch_unwind)]`
- No `unsafe` outside the NAPI boundary
- Return `napi::Result<T>` not bare `T`

## Test Commands

```bash
# Run all tests
cargo nextest run

# Run specific test
cargo nextest run test_name

# Run with output
cargo nextest run -- --nocapture

# Check without running
cargo check --all-features

# Clippy
cargo clippy --all-features -- -D warnings
```

## Non-Negotiables (from CLAUDE.md)

- No `unwrap()`/`expect()` in lib code (tests OK with message)
- No `unsafe` outside NAPI boundary
- `BTreeMap` for output maps
- `String::with_capacity` for pre-allocation
- Truncation uses `floor_char_boundary`
- Every `pub` item has a doc comment
