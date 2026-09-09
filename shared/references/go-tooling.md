# Go Tooling Reference

Inspect `go.mod`, `go.work`, task runners, and CI before choosing commands. Prefer configured project commands.

## Common capabilities

- Tests: `go test ./...` or a targeted package with `-run`.
- Race-sensitive changes: `go test -race` for the relevant packages when supported by the environment.
- Fuzzing: run an existing target with `go test -fuzz=FuzzName -fuzztime=<bounded duration>`. Preserve minimized failures under `testdata/fuzz`.
- Static checks: configured linters plus `go vet ./...` when the project uses the standard toolchain directly.
- Mutation: use only a repository-configured mutation tool; the Go ecosystem has no single standard runner.

Fuzz targets need a meaningful invariant or oracle. A bounded run is evidence for the explored interval, not proof over all inputs.
