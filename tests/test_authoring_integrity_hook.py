"""Verify the repository-local commit guard remains narrowly scoped."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import patch


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "scripts/authoring-integrity-hook.py"


def load_hook_module() -> object:
    specification = importlib.util.spec_from_file_location("authoring_integrity_hook", SCRIPT_PATH)
    if specification is None or specification.loader is None:
        raise AssertionError("could not load authoring integrity hook")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


HOOK = load_hook_module()


class AuthoringIntegrityHookTests(unittest.TestCase):
    def test_only_git_commit_commands_trigger_the_guard(self) -> None:
        self.assertTrue(HOOK.is_commit_command("git commit -m 'release'"))
        self.assertTrue(HOOK.is_commit_command("git add -A && git commit -m release"))
        self.assertFalse(HOOK.is_commit_command("git status"))
        self.assertFalse(HOOK.is_commit_command("python3 tools/build-codex-marketplace.py"))

    def test_non_bash_and_non_commit_events_are_ignored(self) -> None:
        with patch.object(HOOK, "repository_root") as root:
            self.assertIsNone(HOOK.evaluate({"tool_name": "apply_patch", "tool_input": {"command": "patch"}, "cwd": "/tmp"}))
            self.assertIsNone(HOOK.evaluate({"tool_name": "Bash", "tool_input": {"command": "git status"}, "cwd": "/tmp"}))
        root.assert_not_called()

    def test_tracked_schema_mutation_blocks_before_generated_bundle_check(self) -> None:
        payload = {"tool_name": "Bash", "tool_input": {"command": "git commit -m release"}, "cwd": "/tmp"}
        with patch.object(HOOK, "repository_root", return_value=Path("/repo")), patch.object(HOOK, "staged_schema_mutations", return_value=["M\tshared/schemas/spec@1.json"]), patch.object(HOOK, "generated_bundle_is_current") as bundle:
            reason = HOOK.evaluate(payload)
        self.assertIn("immutable", reason)
        self.assertIn("spec@1.json", reason)
        bundle.assert_not_called()

    def test_stale_generated_bundle_blocks_the_commit(self) -> None:
        payload = {"tool_name": "Bash", "tool_input": {"command": "git commit -m release"}, "cwd": "/tmp"}
        with patch.object(HOOK, "repository_root", return_value=Path("/repo")), patch.object(HOOK, "staged_schema_mutations", return_value=[]), patch.object(HOOK, "generated_bundle_is_current", return_value=False):
            reason = HOOK.evaluate(payload)
        self.assertEqual(reason, "The generated Codex marketplace is stale. Run python3 tools/build-codex-marketplace.py, review dist/codex, then commit.")

    def test_current_bundle_and_new_schema_addition_are_allowed(self) -> None:
        payload = {"tool_name": "Bash", "tool_input": {"command": "git commit -m release"}, "cwd": "/tmp"}
        with patch.object(HOOK, "repository_root", return_value=Path("/repo")), patch.object(HOOK, "staged_schema_mutations", return_value=[]), patch.object(HOOK, "generated_bundle_is_current", return_value=True):
            self.assertIsNone(HOOK.evaluate(payload))

    def test_both_harnesses_register_the_same_guard(self) -> None:
        for path in (REPOSITORY_ROOT / ".claude/settings.json", REPOSITORY_ROOT / ".codex/hooks.json"):
            configuration = json.loads(path.read_text(encoding="utf-8"))
            commands = [
                hook["command"]
                for group in configuration["hooks"]["PreToolUse"]
                if group.get("matcher") == "Bash"
                for hook in group["hooks"]
            ]
            self.assertTrue(any("authoring-integrity-hook.py" in command for command in commands), path)


if __name__ == "__main__":
    unittest.main()
