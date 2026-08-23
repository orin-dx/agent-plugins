# Interface Implementers

_Loaded by: vector:challenger, when a plan@1 task modifies a file that implements a shared trait, interface, or protocol — to enumerate every other known implementer before judging interface-incompleteness. This is a deterministic pre-scan: run the search, read the matches, then reason — do not reason first and try to recall siblings from memory._

---

## Language detection

`plan@1` carries no `language` field. Infer it from the extensions of the files named in the task under review: `.rs` → Rust, `.ts`/`.tsx` → TypeScript, `.js`/`.jsx` → treat as TypeScript's patterns minus type annotations. A task touching multiple languages runs the relevant scan for each.

## Rust

1. Identify the trait: if the task's target file contains `impl` blocks, read the trait name(s) from `impl TraitName for TypeName`. If the task instead defines the trait itself, use that trait's name directly.
2. Enumerate implementers workspace-wide: grep `impl\s+TraitName\s+for\s+(\w+)` across every `.rs` file in the workspace — not just files the task touches. Each match's captured type name is one implementer.
3. Cross-reference: for every implementer found, check whether the plan has at least one task whose `files.modify` or `files.create` list includes that implementer's defining file, or whose description explicitly addresses it.
4. Anything found in step 2 but absent from step 3 is an uncovered implementer.

- **Grep pattern:** `impl\s+TraitName\s+for\s+(\w+)` (substitute the trait name found in step 1).
- **False positive check:** Is the trait sealed to a single known implementer by design (a marker trait, a newtype pattern)? If the trait's own doc comment or a `sealed` marker states this, the plan should still say so explicitly rather than silently omitting siblings — that satisfies the `interface-incompleteness` dimension's "or state why not" clause.

## TypeScript / JavaScript

1. Identify the interface or protocol: `interface InterfaceName`, or a discriminated union's member type, in the task's target file.
2. Enumerate implementers workspace-wide:
   - Explicit: grep `implements\s+(?:[\w,\s]*\b)InterfaceName\b`.
   - Structural (no `implements` keyword — common for plain interfaces): grep object literals or factory functions annotated `:\s*InterfaceName\b`, or files under the same directory pattern as the task's target (e.g. `adapters/*.ts` when the task touches one file under `adapters/`) that export a same-shaped object.
3. Cross-reference and flag exactly as in the Rust case.

- **Grep pattern:** `implements\s+InterfaceName\b` for explicit implementers; `:\s*InterfaceName\b` for structural ones — the structural case has a higher false-positive rate and needs a read of surrounding code, not just the grep hit.
- **False positive check:** Does the type's own comment mark it closed or exhaustive? Structural typing means a grep match may satisfy the interface's shape by coincidence, not intent — confirm by reading the matched file, not the grep hit alone.

---

Once the implementer list and its covered/uncovered split are built, that list — not the raw grep output or the files read to disambiguate matches — is what enters the agent's reasoning about `interface-incompleteness`.
