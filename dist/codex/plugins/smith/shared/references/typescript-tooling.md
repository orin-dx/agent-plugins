# TypeScript Tooling Reference

_Loaded by: mutator, remediator. Contains test runner detection, test commands, and the non-negotiables every fix must satisfy. Do not load for scanning or smell analysis._

---

## Workspace Test Discovery & Execution

Before running tests, check `package.json` scripts and workspace task runners:

```bash
# Check package scripts and task runner configs
jq '.scripts' package.json 2>/dev/null
ls vitest.config.* jest.config.* bun.test.* moonrepo.yml turbo.json 2>/dev/null
```

- Prefer configured package scripts or task runners.
- Otherwise target the relevant Vitest, Jest, Bun, or Node test file.
- Use the configured type-check command for changed type boundaries.
- Use Stryker when available and relevant to changed behavior.
- Use `fast-check` or another configured generator for combinatorial inputs when a structured arbitrary and meaningful invariant are available.
- Exercise compiled, bundled, or process boundaries when the change depends on them.
- Run the applicable workspace suite before completion.

---

## Non-Negotiables

Every fix must satisfy these before the green pass is claimed:

- No `any` in new code without an inline comment explaining why.
- No unhandled promise rejections — every `async` call is either `await`ed, `.catch()`ed, or explicitly `void`-ed with a comment.
- All exported functions have JSDoc or TSDoc.
- No `console.log` in library code — use a structured logger or remove.
- Config and options interfaces must be `readonly`.
- No `JSON.parse(JSON.stringify(x))` — use `structuredClone`.
- Discriminated union switches must have an `assertNever` default.
