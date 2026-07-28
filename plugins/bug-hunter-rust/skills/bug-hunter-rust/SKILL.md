---
name: bug-hunter-rust
description: >-
  Rust bug hunting framework. Finds silent failures, spec-vs-code drift, ordering/staleness bugs, crash-safety violations, and edge cases across any Rust codebase using 6 Rust Hazard Taxonomies.
---

# Universal Rust Bug-Hunter Skill

## Core Laws & Verification Framework
Before auditing, review the shared debugging laws and evaluation standards:
- [General Debugging Laws](../../../shared/debugging-laws.md)
- [Evaluation Report Template](../../../shared/report-template.md)

---

## The 6 Universal Rust Hazard Taxonomies & Regex Heuristics

When auditing any Rust repository, scan all code paths using ripgrep against these 6 hazard categories:

### 1. Discarded Data & Unused CLI / Struct Parameters
- **Search Pattern**: `fn\s+\w+.*\b_[a-zA-Z0-9_]+:\s*` or `let _ =`
- Function parameters or struct fields prefixed with leading underscores (e.g. `_opts`, `_config`, `_loaded`) where user inputs or configuration flags are silently ignored.
- CLI flags parsed into argument structs (e.g., Clap `#[derive(Args)]`) but never read or evaluated before executing the gated operation.

### 2. Ordering, Mutability & Fixpoint Staleness Bugs
- **Search Pattern**: `\.or_insert\(|\.entry\(.*?\)\.or_default\(`
- First-write-wins patterns used where max-value-wins, latest-write-wins, or fixpoint convergence is required.
- Graph traversals or solver loops that modify target state without re-enqueuing dependents into a worklist, leaving downstream dependencies stale.

### 3. Spec-vs-Code Compliance Drift
- **Search Pattern**: `TODO|FIXME|unimplemented!|todo!`
- Trace stated requirements from design docs, specs, READMEs, or docstrings to the underlying Rust functions. Ensure invariants are enforced by logic, not just represented in types.

### 4. Silent Fallbacks & Falsified Defaults
- **Search Pattern**: `\.unwrap_or_else\(|\.unwrap_or_default\(|\.unwrap_or\(`
- Catch-all fallbacks that hide missing or malformed data instead of returning an explicit `Result::Err`.
- Swallowed I/O or subprocess errors (`if cmd.is_ok() { ... }`, `let _ = atomic_write(...)`) returning success reports when disk operations fail.

### 5. Boundary Inputs & Format Edge Cases
- **Search Pattern**: `split\(|lines\(|from_utf8`
- Text/Format handling: UTF-8 BOM (`\u{FEFF}`) prefixes, CRLF line endings, missing trailing newlines, non-ASCII Unicode strings.

### 6. Crash-Safety & Subprocess Security
- **Search Pattern**: `Command::new\(|runner\.run\(|NamedTempFile|persist\(`
- File I/O: Missing `.flush()` or `.sync_all()` calls prior to atomic file rename/persists.
- Subprocess invocations (e.g., `git`, `cargo`, `npm`): Misplaced `--` end-of-options delimiters or bad option ordering (`fatal: too many arguments`).

---

## Subagent Dispatch Matrix

| Agent Role | Target Taxonomies | Objective |
| :--- | :--- | :--- |
| **`bug-hunter-scanner-rust`** | Taxonomies 1 & 4 | Audit all crates for unused CLI flags, discarded parameters, and `unwrap_or` fallback defaults. |
| **`bug-hunter-adversary-rust`** | Taxonomies 2 & 3 | Audit fixpoint loops, graph solvers, ordering staleness, and spec compliance drift. |
| **`bug-hunter-remediator-rust`** | Taxonomies 5 & 6 | Audit UTF-8 BOM, CRLF, atomic file write `.flush()`/`.sync_all()`, and subprocess argument ordering. |
