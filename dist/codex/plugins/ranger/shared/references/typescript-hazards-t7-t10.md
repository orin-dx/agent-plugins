# TypeScript Hazard Reference — T7 / T10 (Boundary-Tracer Scope)

_Loaded by: boundary-tracer (always — this is its entire scope), adversary (only when the candidate's taxonomy is T7 or T10; otherwise load `typescript-hazards.md` instead). The other taxonomies live in `typescript-hazards.md`._

---

## Hazard Taxonomies

### T7. Intent-Capture-to-Execution Discard ← highest impact
- **Signal:** A wide options object or validated config is constructed with user-specified fields (`dryRun`, `registry`, `tag`, `access`), but the function that performs the side effect accepts a narrower interface — those fields are never read at the execution boundary.

```typescript
// ✗ BEFORE — tag and registry captured, silently dropped at the call site
interface PublishOptions {
  packageId: string
  version: string
  registry?: string  // user-specified
  tag?: string       // user-specified
}

// Narrow parameter type — extra fields structurally compatible but never read
function publish(opts: { packageId: string; version: string }) {
  execSync(`npm publish`) // registry, tag never reach the command
}

function run(opts: PublishOptions) {
  publish(opts) // TypeScript allows this; registry and tag are silently gone
}

// ✓ AFTER — execution function accepts the full options type
function publish(opts: PublishOptions) {
  const args = ['npm', 'publish']
  if (opts.registry) args.push('--registry', opts.registry)
  if (opts.tag)      args.push('--tag', opts.tag)
  execSync(args.join(' '))
}
```
- **Search:**
  1. Find options/config types — interfaces or types matching `*Options`, `*Config`, `*Params`, `*Payload`, `*Args`.
  2. Find construction sites where the wide type is built with user-provided values.
  3. Find the execution function — check its parameter type and what it actually reads.
  4. Flag any field present in the constructed object but absent from the execution function's parameter type or body.
- **Risk:** User intent (dry-run, private registry, access level) is silently overridden by a hardcoded default.
- **False positive check:** Is the field explicitly documented as unused at the call site?
- **Verdict signal:** Confirmable when the field is absent from the execution function's parameter type, or present in the type but not read in the body. Dismissible only when the field is explicitly read and forwarded to the subprocess or external call.

### T10. Error Suppression & Downgrade ← distinct from T2
- **Signal:** A catch block or rejection handler that swallows the error without signaling failure to the caller. The outer call resolves or returns successfully even though the operation failed.
  - `.catch(() => {})` or `.catch((_) => undefined)` — empty or null-returning handler
  - `try { ... } catch { }` — catch with no body (TS 4.0+ allows omitting the binding entirely)
  - `try { ... } catch (e) { console.log(e) }` — only logging, not re-throwing or returning a failure signal
- **Grep patterns:**
  - `\.catch\(\s*[(_)]\s*=>\s*\{?\s*\}?\s*\)` — empty or trivially-returning catch handler
  - `catch\s*\([^)]*\)\s*\{\s*\}` — empty catch body
  - `catch\s*\([^)]*\)\s*\{\s*console\.\w+` — logging-only catch
- **Risk:** Callers receive a resolved promise or a non-throwing return believing the operation succeeded. The failure is invisible to monitoring, retry logic, and the caller's control flow.
- **False positive check:** Is the no-op explicitly documented as intentional? Is the error logged AND the caller notified via a return value or status field? If neither, it is suppression.
- **Distinguisher from T2 (Unhandled Promise Rejection):** T2 has no catch at all — the rejection propagates unhandled. T10 has a catch that actively hides the error from the caller.
- **Verdict signal:** Confirmable when the catch handler resolves or returns without signaling failure and the caller has no recovery path. Dismissible when the handler logs the error AND signals failure via a return value, status field, or re-throw.
