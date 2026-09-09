# Rust Hazard Reference — T7 / T10 (Boundary-Tracer Scope)

_Loaded by: boundary-tracer (always — this is its entire scope), adversary (only when the candidate's taxonomy is T7 or T10; otherwise load `rust-hazards.md` instead). The other eight taxonomies live in `rust-hazards.md`._

---

## Hazard Taxonomies

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

### 10. Error Downgrade & Source Erasure ← distinct from T4
- **Signal:** `map_err(|_err|` or `map_err(|_|` — the underscore on the closure parameter is the tell: the original error was received and deliberately discarded. Also: `.to_string()` called on an error inside `map_err` or an `Err(...)` constructor, converting structured error context (diagnostic codes, spans, help text) to a plain string.
- **Grep patterns:**
  - `map_err\(\|_` — underscore-ignoring closure = source erasure
  - `\.to_string\(\)` inside `map_err\(` or adjacent to `Err(`
- **Risk:** Callers and diagnostic tooling lose the original error's structured context. Diagnostic codes, help text, and source spans that would identify the root cause are silently dropped. Error messages become shallow strings that obscure the cause.
- **False positive check:** Is this at a genuine FFI/ABI boundary where the foreign error type cannot cross? Is `.to_string()` required for a serialization format that mandates strings (JSON response body, structured log sink)? If neither, it is a downgrade.
- **Distinguisher from T4:** T4 is accidental — `let _ = result` with no closure. T10 is intentional-but-lossy — the programmer chose a mapping that discards the source. Different fix: T4 needs `?`; T10 needs the error type to preserve the chain.
- **Verdict signal:** Confirmable when `map_err(|_|` discards the closure parameter and the resulting error type loses source chain (no `.source()` or inner error field). Dismissible when the conversion crosses a genuine FFI/ABI boundary or the destination format mandates a string type.
