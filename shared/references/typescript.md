# TypeScript Reference Index

This file is an index. Agents must load only the file that matches their phase — do not load all three.

| File | Load when... |
|---|---|
| [`typescript-hazards.md`](./typescript-hazards.md) | Scanning for bugs (all taxonomies) or verifying a non-T7/T10 candidate |
| [`typescript-hazards-t7-t10.md`](./typescript-hazards-t7-t10.md) | Tracing field boundaries, or verifying a T7/T10 candidate — boundary-tracer's entire scope |
| [`typescript-smells.md`](./typescript-smells.md) | Clustering findings into architectural smells and interface designs |
| [`typescript-tooling.md`](./typescript-tooling.md) | Running tests, applying fixes, or running mutation analysis |
