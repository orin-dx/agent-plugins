# Rust Verification Tooling

## Outcome

Choose the smallest project-native checks that can falsify the changed behavior. Tool names alone are not evidence.

## Discover capabilities

Inspect `Cargo.toml`, workspace configuration, task runners, CI, and existing tests before choosing commands. Prefer configured tasks; otherwise use targeted Cargo commands and then consider the applicable workspace suite.

| Changed risk | Useful capability when available | Evidence to record |
| :--- | :--- | :--- |
| Local behavior | `cargo test` or configured `cargo nextest` target | Test target and observed result |
| Type, feature, or crate boundary | `cargo check` under relevant features or targets | Configuration exercised |
| Weak assertions | `cargo-mutants` or a safe deliberate fault | Wrong behavior rejected by the test |
| Combinatorial or stateful input | `proptest` or an existing fuzz target | Generator, oracle, and minimized failure |
| FFI or NAPI boundary | Project integration test or boundary harness | Boundary crossed and mocked segment |
| Packaging or generated files | Project build/package task | Produced artifact inspected |

## Candidate quality checks

Apply these only when the repository contract or changed risk makes them relevant:

- Panic paths: determine whether `unwrap`, `expect`, or `panic!` is reachable from recoverable input before treating it as a defect.
- Unsafe code: verify the safety contract and boundary ownership; location alone is not proof of unsoundness.
- Output ordering: require deterministic maps or sets only when output is user-visible, serialized, snapshot-tested, or contractually ordered.
- String construction: investigate allocation only when measurement or a hot path makes it material.
- UTF-8 slicing: reject byte indexing when the index can split a character boundary.
- Public documentation: follow the repository's lint and public API policy rather than inventing one.
- Plan or config fields: trace values to the execution boundary when changed behavior depends on them.

Record unsupported checks as coverage gaps. Do not install optional tooling without authorization.
