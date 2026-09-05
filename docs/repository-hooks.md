# Repository Hooks

These hooks apply only while working in `orin-dx/agent-plugins`. They are project configuration, not distributable plugin behavior.

## Commit-time integrity guard

Claude and Codex run `scripts/authoring-integrity-hook.py` before a shell command that invokes `git commit`. The hook is silent unless it blocks a commit for one of two hard invariants:

- A tracked `shared/schemas/<name>@<version>.json` file is modified, deleted, renamed, or copied instead of adding a new version.
- `dist/codex` does not exactly match the authored Codex sources and catalog.

The hook does not run tests, rewrite files, add context, inspect ordinary edits, or act outside this repository. It permits new schema files and reports the one corrective action when it blocks.

## Configuration

| Harness | Configuration | Hook command |
| :--- | :--- | :--- |
| Claude Code | `.claude/settings.json` | `PreToolUse` for `Bash` |
| Codex | `.codex/hooks.json` | `PreToolUse` for `Bash` |

Both harness adapters invoke the same standard-library Python check and accept its shared `{"decision":"block","reason":"..."}` output. The adapters remain separate because each harness resolves project-root paths and hook configuration independently.

## Verification

Run the hook test with:

```bash
python3 -m unittest tests/test_authoring_integrity_hook.py -v
```

To inspect or trust the Codex hook, use `/hooks`. Claude Code exposes its configured hooks through its `/hooks` view.
