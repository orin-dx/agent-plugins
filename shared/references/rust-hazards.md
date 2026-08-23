# Rust Hazard Reference

_Loaded by: scanner (all taxonomies), adversary (when the candidate's taxonomy is not T7 or T10). T7 and T10 live in `rust-hazards-t7-t10.md` — boundary-tracer's exact scope, loaded directly instead of this file. Do not load for smell analysis or fix work — use `rust-smells.md` and `rust-tooling.md` instead._

---

## Hazard Taxonomies

Ordered by impact — start here when triaging. T7 and T10 are documented in `rust-hazards-t7-t10.md`.

### 8. False-Success Mutation ← highest impact
- **Signal:** A function named `update_*`, `write_*`, `set_*`, or `bump_*` returns `Result<(), E>` and has a `return Ok(());` path that was reached without performing any visible mutation.

```rust
// ✗ BEFORE — caller receives Ok(()) with no way to know nothing was written
fn update_version(manifest: &mut Manifest, new: &Version) -> Result<(), Error> {
    if manifest.version == *new {
        return Ok(()); // silent no-op; caller assumes disk was updated
    }
    manifest.version = new.clone();
    manifest.write_to_disk()
}

// ✓ AFTER — outcome is explicit; caller can act on it
fn update_version(manifest: &mut Manifest, new: &Version) -> Result<bool, Error> {
    if manifest.version == *new {
        return Ok(false); // no-op, signaled
    }
    manifest.version = new.clone();
    manifest.write_to_disk()?;
    Ok(true) // mutation confirmed
}
```
- **Grep pattern:** `fn (update|write|set|bump)_\w+` — then check the body for `return Ok\(\(\)\);` before any write operation.
- **Risk:** Caller believes the write succeeded; state is silently wrong going forward.
- **False positive check:** Does the function document an "already-correct → Ok(())" contract with a caller-side check after? If neither, the silent Ok is a bug.

### 1. Discarded Parameters
- **Signal:** `fn foo(_param: T)` — leading underscore on a parameter.
- **Grep pattern:** `fn\s+\w+[^{]*\b_[a-zA-Z][a-zA-Z0-9_]*:\s*`
- **Risk:** User-provided value is silently ignored.
- **False positive check:** Trait requirement? (`trait Foo { fn bar(&self, _: T) }` is intentional.)

### 4. Missing Error Propagation
- **Signal:** `let _ = result;`, `drop(result)`.
- **Grep pattern:** `let _\s*=|drop\(\w*result\w*\)`
- **Risk:** Error is discarded; subsequent code runs on invalid state.

### 9. Duplicate Diagnostic Codes
- **Signal:** Two or more error variants share the same `#[diagnostic(code(...))]` annotation.
- **Grep pattern:** `diagnostic\(code\(` — collect all values, check for duplicates across the file and module.
- **Risk:** Tooling dispatching on codes can't distinguish the two errors.
- **False positive check:** None. Duplicate codes are always wrong.

### Incomplete Conversion Coverage
- **Signal:** `from_path`, `from_str`, or `try_from` whose match arms cover fewer variants than the source enum — indicated by `_ => Err(Unknown...)`.
- **Grep pattern:** `_ => Err(` inside `impl From` / `impl TryFrom` / `from_path` / `from_str` bodies.
- **Risk:** Unknown variants silently become errors instead of being handled.

### 2. Silent Unwrap Fallbacks
- **Signal:** `.unwrap_or(default)`, `.unwrap_or_default()`, `.unwrap_or_else(|| ...)`.
- **Grep pattern:** `\.unwrap_or\b|\.unwrap_or_default\b|\.unwrap_or_else\b`
- **Risk:** Error is swallowed; wrong behavior proceeds silently.
- **False positive check:** Is the default semantically correct for all callers? Is the error logged?

### 3. Panic in Lib Code
- **Signal:** `.unwrap()`, `.expect("...")`, `panic!(...)`.
- **Grep pattern:** `\.unwrap\(\)|\.expect\(|panic!\(`
- **Risk:** Unrecoverable crash propagates to caller.
- **False positive check:** Test code and `fn main` are acceptable.

### 5. Integer Overflow in Release
- **Signal:** Arithmetic on user-controlled integers without checked ops.
- **Grep pattern:** `\b(usize|u32|u64|i32|i64)\b.*[+\-\*]`
- **Risk:** Wraps in release mode; panics in debug.
- **False positive check:** Is overflow impossible or separately handled?

### 6. Unsafe Boundary Violations
- **Signal:** `unsafe` blocks outside an explicit FFI/NAPI boundary.
- **Grep pattern:** `unsafe\s*\{`
- **Risk:** Memory unsafety, UB.
- **False positive check:** Is this in an `#[napi]` context or FFI shim?
