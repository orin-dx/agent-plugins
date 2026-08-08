# Rust Smell Reference

_Loaded by: architect. Contains code-level and architectural smell sweeps, and the shared trait centralization framework. Do not load for scanning or fix work._

---

## Code-Level Smell Sweeps

Quick checks any agent can run during a pass. These indicate local correctness problems.

### Domain Method vs PartialEq Confusion
- `entry.name == pkg.id.to_string()` — bare string comparison on a newtype.
- `id == &pkg.id` where `PackageId::matches()` has broader semantics.
- `version == req.version` where `VersionReq::matches()` is the correct predicate.
- **Search:** `==` on types that have a named domain method (`matches`, `satisfies`, `equivalent`, `covers`). `PartialEq` tests structural identity; the domain method tests semantic equivalence.

### UTF-8 Boundary Issues
- Never use `&s[..n]` — use `s.floor_char_boundary(n)` or `s.chars().take(n)`.
- **Search:** `&\w+\[\.\.[\w\d]+\]`

### Missing `BTreeMap`/`BTreeSet` for Output
- Maps and sets in agent-visible output, error payloads, or user-facing responses must be deterministically ordered.
- `HashMap`/`HashSet` is fine for internal state only.
- **Search:** `HashMap<` or `HashSet<` in response/render/error code.
- `HashSet.into_iter().collect::<Vec>()` in error messages or logs produces non-deterministic ordering — collect into `BTreeSet` first.

### String Pre-allocation
- Strings built with repeated `push_str` or `format!` in a loop must use `String::with_capacity`.
- **Search:** `String::new()` followed by `.push_str` in loops.

### Float Rendering
- `f64` values in agent output must handle `NaN` and `Inf` explicitly.
- **Search:** `f64` in render/display code; check for a guard before formatting.

---

## Architectural Pattern Smells

Higher-level patterns that indicate systemic design problems, not just local correctness issues. The architect clusters these across findings.

### 1. Domain Method vs PartialEq Confusion (systemic)
- See code-level smell above. When this appears more than once, it signals that identity resolution is not centralized — there is no single `PackageIdentityResolver` trait enforcing the correct comparison.
- **Resolving trait:** `PackageIdentityResolver`.

### 2. Un-Transactional Disk Mutation
- Step-by-step file edits or Git state changes in non-dry-run paths without atomic batch rollback.
- **Search:** `fs::write` or `fs::remove_file` in version plan resolution.
- **Resolving trait:** `ChangesetStorage` with rollback transaction support.
- **Sub-pattern — Multi-writer last-wins:** A loop iterates over a collection (packages, plan entries) and each iteration writes to the same target file. Last writer wins silently; earlier writes are discarded without error. Different from un-transactional single writes — the bug is in the orchestration, not the individual write call.
  - **Search:** `for.*in.*packages|for.*in.*plan` followed within the same block by a write call (`fs::write`, `atomic_write`, `File::create`) targeting the same path variable.

### 3. Lossy Serde / CST Mutation
- Replacing `toml_edit::Value` or `serde_json::Value` nodes without preserving `.decor()` or line endings.
- **Search:** `Value::from(` or `insert("version"`.
- **Resolving trait:** `CstManifestEditor`.

### 4. Un-Fsynced Directory Metadata
- `create_dir_all` or atomic file writes missing `.sync_all()` on the parent directory handle post-rename.
- **Search:** `atomic_write` or `fs::create_dir_all`.
- **Resolving trait:** `ChangesetStorage`.

### 5. Scopeless Fallback and Unbounded Traversal
- `unwrap_or_else` defaults hiding invalid state, or `revwalk` traversing entire Git history without a bound.
- **Search:** `rev_walk` or `unwrap_or_else`.
- **Resolving trait:** `GitVcsProvider` with bounded revwalk; `CascadeSolver` with explicit fixpoint termination.

### 6. Hardcoded Dummy Constant
- Inserting placeholder strings (`"Release update"`, `"changeset.md"`) instead of preserving user-provided metadata.
- **Search:** `"Release update"` or `"changeset.md"`.
- **Resolving trait:** `ReportPresenter`.

### 7. Test Fixture Drift
- Hardcoded JSON/TOML/YAML string literals in test files whose field names no longer match the production serde struct.
- After any schema change (new field, rename, `Vec` → `HashMap`), search test files for string literals embedding the old shape and confirm keys match current `#[serde(rename = "...")]` or field names.
- **Search:** string literals containing `{` in test files — cross-reference against current struct definition.

### 8. Invisible Invariants
- Architectural constraints stated in project constitution files (`CLAUDE.md`, `AGENTS.md`, doc comments) — workspace-member visibility rules, layer dependency boundaries, error code uniqueness, crate ownership rules — that have no corresponding `#[test]`, `cargo-deny` ban, clippy lint, or CI assertion.
- The constraint is known and documented. It is simply not machine-enforced, so it breaks silently as the codebase evolves.
- **Sweep:** Read the project's constitution file if present. For each stated architectural invariant, check for an enforcing mechanism: a test whose name is the invariant statement, a `cargo-deny` `[bans]` rule, a workspace-level `clippy.toml` lint, or a CI step. Report any invariant with no enforcer.
- **Resolution:** Write the enforcement first — a `#[test]` that fails when the invariant is violated — then verify it currently passes. The test name should be the invariant statement verbatim.

---

## Shared Trait Centralization Framework

When multiple smells resolve to the same abstraction boundary, propose a centralized Rust trait. The goal is eliminating entire defect classes, not patching individual instances.

| Trait | Eliminates |
|---|---|
| `PackageIdentityResolver` | PartialEq confusion, bare name comparisons |
| `VersionSpecRenderer` | Format/precision-preserving version rendering |
| `ChangesetStorage` | Un-transactional writes, un-fsynced metadata |
| `CstManifestEditor` | Lossy serde / CST mutations |
| `GitVcsProvider` | Unbounded revwalk, shallow checkout hazards |
| `CascadeSolver` | Fixpoint staleness, graph cascade bugs |
| `ReportPresenter` | Hardcoded dummies, non-deterministic output |
