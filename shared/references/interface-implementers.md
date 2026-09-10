# Interface Implementer Coverage

## Outcome

When a plan changes a shared trait, interface, protocol, or expected method set, enumerate affected implementations before judging the plan complete. The result is a verified covered, uncovered, and uncertain inventory—not raw search matches.

## Apply when

Use this check when a task changes a shared contract, one implementation of that contract, or behavior expected across sibling adapters, providers, handlers, or backends.

## Candidate discovery

| Language | Candidate evidence |
| :--- | :--- |
| Rust | `impl Trait for Type`, trait bounds, constructors returning `dyn Trait` or `impl Trait` |
| TypeScript / JavaScript | `implements`, annotated factories or objects, registry entries, same-shaped adapters in sibling directories |
| Python | subclasses of an ABC, `Protocol` annotations, registered plugins, factories, or sibling objects with the required methods |
| Go | compile-time interface assertions, constructor returns, assignments to the interface, registrations, and concrete types with the required method set |

Search syntax first, then derive semantic candidates from the responsibility and architecture. Structural typing and implicit interfaces make text search incomplete by design.

## Evidence

1. Read the live contract and identify the behavior being changed.
2. Enumerate syntactic and semantic candidate implementations workspace-wide.
3. Read each candidate to confirm it intentionally participates in the contract.
4. Map confirmed implementations to plan tasks or an explicit reason they are unaffected.

Record:

- `covered`: a task or shared implementation addresses the changed behavior.
- `uncovered`: the implementation is affected but absent from the plan.
- `unaffected`: evidence shows the contract change cannot reach it.
- `uncertain`: dynamic registration, external packages, generated code, or missing access prevents a complete decision.

An empty search result is not completeness evidence until architecture-derived candidate sites have also been considered. Treat inaccessible or open-world implementations as a coverage gap, not a pass.
