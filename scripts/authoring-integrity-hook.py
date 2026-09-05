#!/usr/bin/env python3
"""Block commits that violate generated-output or schema-version invariants."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


COMMIT_COMMAND = re.compile(r"(?:^|[;&|]\s*)git(?:\s+-[A-Za-z]\s+[^\s;&|]+)*\s+commit(?:\s|$)")
REPOSITORY_MARKERS = ("marketplace.json", "shared/constitution.md", "tools/build-codex-marketplace.py")


def emit_block(reason: str) -> None:
    print(json.dumps({"decision": "block", "reason": reason}))


def repository_root(cwd: str) -> Path | None:
    try:
        result = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    root = Path(result.stdout.strip())
    if all((root / marker).is_file() for marker in REPOSITORY_MARKERS):
        return root
    return None


def is_commit_command(command: str) -> bool:
    return bool(COMMIT_COMMAND.search(command))


def staged_schema_mutations(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), "diff", "--cached", "--name-status", "--", "shared/schemas"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line and not line.startswith("A\t")]


def generated_bundle_is_current(root: Path) -> bool:
    result = subprocess.run(
        [sys.executable, "tools/build-codex-marketplace.py", "--check"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def evaluate(payload: dict[str, Any]) -> str | None:
    tool_name = payload.get("tool_name")
    tool_input = payload.get("tool_input")
    if tool_name != "Bash" or not isinstance(tool_input, dict):
        return None
    command = tool_input.get("command")
    cwd = payload.get("cwd")
    if not isinstance(command, str) or not is_commit_command(command) or not isinstance(cwd, str):
        return None
    root = repository_root(cwd)
    if root is None:
        return None
    mutations = staged_schema_mutations(root)
    if mutations:
        changed = ", ".join(mutations)
        return f"Tracked schema versions are immutable. Add a new shared/schemas/<name>@<N+1>.json instead of committing: {changed}"
    if not generated_bundle_is_current(root):
        return "The generated Codex marketplace is stale. Run python3 tools/build-codex-marketplace.py, review dist/codex, then commit."
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    if not isinstance(payload, dict):
        return 0
    reason = evaluate(payload)
    if reason:
        emit_block(reason)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
