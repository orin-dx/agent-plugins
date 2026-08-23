# Rust Reference Index

This file is an index. Agents must load only the file that matches their phase — do not load all three.

| File | Load when... |
|---|---|
| [`rust-hazards.md`](./rust-hazards.md) | Scanning for bugs (all taxonomies) or verifying a non-T7/T10 candidate |
| [`rust-hazards-t7-t10.md`](./rust-hazards-t7-t10.md) | Tracing field boundaries, or verifying a T7/T10 candidate — boundary-tracer's entire scope |
| [`rust-smells.md`](./rust-smells.md) | Clustering findings into architectural smells and trait designs |
| [`rust-tooling.md`](./rust-tooling.md) | Running tests, applying fixes, or running mutation analysis |
