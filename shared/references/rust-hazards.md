# Rust Hazard Reference

_Loaded by: scanner, adversary, boundary-tracer. Contains workspace discovery and all hazard taxonomies. Do not load for smell analysis or fix work — use `rust-smells.md` and `rust-tooling.md` instead._

---

## Workspace Discovery

```bash
# Find crate root
find . -name "Cargo.toml" -not -path "*/target/*"

# List workspace members
cargo metadata --no-deps --format-version 1 | jq '.workspace_members'

# Check live code only (files reachable via mod declarations)
grep -r "^mod " src/ --include="*.rs"
```

**Dead code rule:** files in `src/` not reachable from `lib.rs` or `main.rs` via `mod` declarations are dead. Do not report findings in dead code.

---

## Hazard Taxonomies

Ordered by impact — start here when triaging.

### 7. Write-Only Fields ← highest impact
- **Signal:** A struct field is set at the construction site but the function that executes the action receives a stripped signature — `(id, version)` or similar. The field never reaches the subprocess or execution call.

```rust
// ✗ BEFORE — registry and tag set, never reach the subprocess
struct PublishPlan {
    id: PackageId,
    version: Version,
    registry: Option<String>,  // user-specified
    tag: Option<String>,        // user-specified
}

fn publish(id: &PackageId, version: &Version) -> Result<(), Error> {
    Command::new("npm").arg("publish").spawn()?; // registry, tag silently absent
    Ok(())
}

fn execute(plan: &PublishPlan) -> Result<(), Error> {
    publish(&plan.id, &plan.version) // plan.registry, plan.tag dropped here
}

// ✓ AFTER — plan passed whole; fields extracted at the execution site
fn execute(plan: &PublishPlan) -> Result<(), Error> {
    let mut cmd = Command::new("npm");
    cmd.arg("publish");
    if let Some(r) = &plan.registry { cmd.args(["--registry", r]); }
    if let Some(t) = &plan.tag      { cmd.args(["--tag", t]); }
    cmd.spawn()?;
    Ok(())
}
```
- **Search:**
  1. Find plan/config structs — types matching `*Plan`, `*Config`, `*Options`, `*Publish*`, `*Pre*`.
  2. Grep for construction sites: `Struct { field: value, .. }`.
  3. Find the execution function downstream. Check its parameter list and subprocess argument list.
  4. Flag any field that is set but absent at the execution boundary.
- **Grep pattern:** fields named `tag`, `index`, `registry`, `access`, `dist_tag`, `repository`, `token`, or any `Option<String>` in plan/config structs.
- **Risk:** User-specified routing (private registry, dist-tag, access level) is silently overridden by a hardcoded default.
- **False positive check:** Is the field intentionally unused with a documented reason?
- **Verdict signal:** Confirmable when the field is absent from the execution function's parameter list and absent from any subprocess argument list. Dismissible when the field appears as a named argument to the execution call or subprocess command before build or spawn.

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

### 10. Error Downgrade & Source Erasure ← distinct from T4
- **Signal:** `map_err(|_err|` or `map_err(|_|` — the underscore on the closure parameter is the tell: the original error was received and deliberately discarded. Also: `.to_string()` called on an error inside `map_err` or an `Err(...)` constructor, converting structured error context (diagnostic codes, spans, help text) to a plain string.
- **Grep patterns:**
  - `map_err\(\|_` — underscore-ignoring closure = source erasure
  - `\.to_string\(\)` inside `map_err\(` or adjacent to `Err(`
- **Risk:** Callers and diagnostic tooling lose the original error's structured context. Diagnostic codes, help text, and source spans that would identify the root cause are silently dropped. Error messages become shallow strings that obscure the cause.
- **False positive check:** Is this at a genuine FFI/ABI boundary where the foreign error type cannot cross? Is `.to_string()` required for a serialization format that mandates strings (JSON response body, structured log sink)? If neither, it is a downgrade.
- **Distinguisher from T4:** T4 is accidental — `let _ = result` with no closure. T10 is intentional-but-lossy — the programmer chose a mapping that discards the source. Different fix: T4 needs `?`; T10 needs the error type to preserve the chain.
- **Verdict signal:** Confirmable when `map_err(|_|` discards the closure parameter and the resulting error type loses source chain (no `.source()` or inner error field). Dismissible when the conversion crosses a genuine FFI/ABI boundary or the destination format mandates a string type.
