# Code Comment Reference

Operational subset of the Reader-Scoped Writing rule (`constitution.md`) for doc comments (`///`, `/**`, docstrings) and inline comments, in any language. Companion to `docs-voice.md`, which covers commit messages, PR bodies, changesets, and prose docs — this file covers comments written inside code.

## Name the reader before writing

- **Doc comment** (`///`, `/**`, docstring) → the caller of this function/type. Needs the contract: non-obvious behavior, invariants, error conditions. Not the signature restated in prose.
- **Inline comment** → a future maintainer reading this exact line. Needs why the line exists when it looks wrong or non-obvious. Not what it does, if the code already shows that.

If neither reader would gain anything actionable from the comment, don't write it.

## Cut

- Restated signature or type ("This function takes a `String` and returns...")
- A narrated alternative not taken ("Instead of X, we use Y because...") — belongs in the PR body, not the code
- Process narration ("After investigating, we found...") — same
- Hedge and filler: "essentially," "basically," "in order to," "it's worth noting that"

## Keep, at whatever length it takes

- A non-obvious invariant the caller must not violate
- Why a workaround exists instead of the obvious approach
- A subtle failure mode the type system doesn't capture

Length follows the reader's need, not a target in either direction — a genuinely non-obvious invariant earns a multi-line comment.

## Example

```rust
// Before — restates the signature, narrates the alternative, justifies at length
/// This function determines the ordering of packages for publish sequencing.
/// Rather than using a generic DependencyResolverExt::toposort() call, which
/// would not correctly account for dev-dependency edges being optional
/// participants in a cycle, we build a specialized ordering that...

// After — states the contract and the one non-obvious fact the caller needs
/// Publish-specific ordering (see `plan_publish`, its only caller).
///
/// Prefers `Dev`-inclusive ordering; falls back to cascade's kinds on a
/// cycle, since mutual dev-only deps between packages are legitimate and
/// must not hard-fail the whole plan.
```

## Self-check

Delete a sentence. Did the reader lose anything they'd act on? If not, leave it deleted.
