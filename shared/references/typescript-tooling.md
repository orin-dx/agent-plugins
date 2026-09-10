# TypeScript and JavaScript Verification Tooling

## Outcome

Choose project-native checks that can falsify the changed behavior across the runtime, type, bundle, or process boundary involved.

## Discover capabilities

Inspect `package.json` scripts, workspace configuration, lockfiles, task runners, CI, and existing tests. Prefer configured commands over guessed runner invocations.

| Changed risk | Useful capability when available | Evidence to record |
| :--- | :--- | :--- |
| Local behavior | Configured Vitest, Jest, Bun, or Node test target | Test target and observed result |
| Type boundary | Configured type-check command | Project and configuration exercised |
| Weak assertions | Stryker or a safe deliberate fault | Wrong behavior rejected by the test |
| Combinatorial or stateful input | `fast-check` or configured generator | Arbitrary, oracle, and minimized failure |
| Bundle or package boundary | Configured build/package task | Produced artifact or import path inspected |
| Process or network boundary | Integration harness | Boundary crossed and mocked segment |

## Candidate quality checks

Apply these only when the repository contract or changed risk makes them relevant:

- Dynamic values: prevent `any` from escaping an unvalidated boundary; a local, justified escape hatch is not automatically a defect.
- Promises: ensure started async work has an owner for completion and failure; framework-managed handlers may provide that owner.
- Logging: follow the application's logging contract. `console` use is not inherently wrong in CLIs, scripts, or configured runtimes.
- Mutability: use `readonly` where mutation would violate ownership, not as a universal shape requirement.
- Cloning: choose behavior that preserves the required value types and target runtime; neither JSON cloning nor `structuredClone` is universally interchangeable.
- Variant handling: require exhaustive handling when the set is closed and silent fallback would be wrong.
- Exported documentation: follow repository policy and document non-obvious contracts rather than restating signatures.

Record unsupported checks as coverage gaps. Do not add dependencies or install optional tooling without authorization.
