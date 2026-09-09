# Python Tooling Reference

Inspect `pyproject.toml`, lockfiles, task runners, and CI before choosing commands. Prefer configured project commands.

## Common capabilities

- Tests: `pytest <path>` or the configured `tox`, `nox`, `uv`, Poetry, or task-runner command.
- Type checks: the configured `mypy`, Pyright, or project script.
- Property tests: Hypothesis when already configured or when the task authorizes adding it. Use structured strategies and a domain invariant.
- Mutation: the configured mutation runner, such as `mutmut`; scope it to changed behavior when supported.
- Packaging: build and inspect the wheel or source distribution when metadata, entry points, imports, or bundled files change.

Do not infer environment parity from a local virtual environment. Record relevant interpreter, dependency, working-directory, and packaging differences.
