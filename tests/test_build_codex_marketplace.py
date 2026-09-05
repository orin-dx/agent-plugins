"""Black-box tests for the stdlib-only Codex marketplace generator."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BUILDER = REPOSITORY_ROOT / "tools" / "build-codex-marketplace.py"


class BuildCodexMarketplaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.write_plugin("alpha", ["inspect", "plan"])
        self.write_plugin("bravo", ["review"])
        self.write_native_plugin("alpha", ["inspect", "plan"])
        self.write_native_plugin("bravo", ["review"])
        self.write("shared/schemas/spec@1.json", '{"$id":"spec@1"}\n')

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def write_json(self, relative: str, value: object) -> None:
        self.write(relative, json.dumps(value, indent=2) + "\n")

    def write_plugin(self, plugin_id: str, skills: list[str]) -> None:
        self.write_json(
            f"plugins/{plugin_id}/plugin.json",
            {
                "id": plugin_id,
                "version": "1.2.3",
                "description": f"{plugin_id} source description",
                "author": {"name": "Orin DX", "email": "dev@example.test"},
            },
        )
        for skill in skills:
            self.write(
                f"plugins/{plugin_id}/skills/{skill}/SKILL.md",
                "---\n"
                f"name: {skill}\n"
                "description: >-\n"
                f"  {skill} source description\n"
                "---\n\n"
                "# Source skill\n",
            )

    def write_native_plugin(self, plugin_id: str, skills: list[str]) -> None:
        category = "Developer tools" if plugin_id == "alpha" else "Productivity"
        self.write_json(
            f"harnesses/codex/plugins/{plugin_id}/.codex-plugin/plugin.json",
            {
                "name": plugin_id,
                "version": "1.2.3",
                "description": f"{plugin_id} Codex description",
                "author": {"name": "Orin DX", "email": "dev@example.test"},
                "skills": "./skills/",
                "interface": {
                    "displayName": plugin_id.title(),
                    "shortDescription": f"{plugin_id} Codex description",
                    "longDescription": f"{plugin_id} Codex description",
                    "developerName": "Orin DX",
                    "category": category,
                    "capabilities": ["Read", "Write"],
                    "defaultPrompt": [f"Use {plugin_id}"],
                },
            },
        )
        for skill in skills:
            self.write(
                f"harnesses/codex/plugins/{plugin_id}/skills/{skill}/SKILL.md",
                "---\n"
                f"name: {skill}\n"
                f"description: {skill} native Codex workflow\n"
                "---\n\n"
                f"# {skill}\n\n"
                f"Native {plugin_id}/{skill} content.\n",
            )

    def catalog(self) -> dict[str, object]:
        return {
            "catalog_version": 1,
            "harness": "codex",
            "runtime_files": [],
            "plugins": [
                {
                    "id": "bravo",
                    "runtime_files": [{"source": "shared/schemas/spec@1.json", "destination": "shared/spec@1.json"}],
                },
                {
                    "id": "alpha",
                    "runtime_files": ["shared/schemas/spec@1.json"],
                },
            ],
        }

    def build(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(BUILDER), "--repo-root", str(self.root)],
            check=False,
            text=True,
            capture_output=True,
        )

    def files(self, directory: Path) -> dict[str, bytes]:
        return {
            path.relative_to(directory).as_posix(): path.read_bytes()
            for path in sorted(directory.rglob("*"))
            if path.is_file()
        }

    def test_materializes_authored_native_manifests_skills_and_runtime_files(self) -> None:
        self.write_json("harnesses/codex/catalog.json", self.catalog())

        result = self.build()

        self.assertEqual(result.returncode, 0, result.stderr)
        output = self.root / "dist/codex"
        marketplace = json.loads((output / ".agents/plugins/marketplace.json").read_text())
        self.assertEqual([item["name"] for item in marketplace["plugins"]], ["bravo", "alpha"])
        self.assertEqual(marketplace["plugins"][0]["source"]["path"], "./plugins/bravo")
        native_alpha = self.root / "harnesses/codex/plugins/alpha"
        for relative, contents in self.files(native_alpha).items():
            self.assertEqual((output / "plugins/alpha" / relative).read_bytes(), contents)
        manifest = json.loads((output / "plugins/alpha/.codex-plugin/plugin.json").read_text())
        self.assertEqual(manifest["name"], "alpha")
        self.assertEqual(manifest["version"], "1.2.3")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(manifest["interface"]["capabilities"], ["Read", "Write"])
        self.assertEqual(manifest["interface"]["defaultPrompt"], ["Use alpha"])
        skill = (output / "plugins/alpha/skills/inspect/SKILL.md").read_text()
        self.assertEqual(skill, (self.root / "harnesses/codex/plugins/alpha/skills/inspect/SKILL.md").read_text())
        self.assertEqual((output / "plugins/alpha/shared/schemas/spec@1.json").read_text(), '{"$id":"spec@1"}\n')
        self.assertEqual((output / "plugins/bravo/shared/spec@1.json").read_text(), '{"$id":"spec@1"}\n')
        self.assertFalse(any(path.is_symlink() for path in output.rglob("*")))

    def test_uses_wisp_plugins_as_the_default_marketplace_identity(self) -> None:
        self.write_json("harnesses/codex/catalog.json", self.catalog())

        result = self.build()

        self.assertEqual(result.returncode, 0, result.stderr)
        marketplace = json.loads((self.root / "dist/codex/.agents/plugins/marketplace.json").read_text())
        self.assertEqual(marketplace["name"], "wisp-plugins")
        self.assertEqual(marketplace["interface"]["displayName"], "Wisp Plugins")

    def test_rebuild_is_deterministic_and_removes_stale_output(self) -> None:
        self.write_json("harnesses/codex/catalog.json", self.catalog())
        self.assertEqual(self.build().returncode, 0)
        output = self.root / "dist/codex"
        first = self.files(output)
        self.write("dist/codex/plugins/alpha/stale.txt", "stale\n")

        result = self.build()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.files(output), first)
        self.assertFalse((output / "plugins/alpha/stale.txt").exists())

    def test_materializes_runtime_symlinks_as_regular_files(self) -> None:
        source = self.root / "shared/schemas/spec@1.json"
        linked = self.root / "shared/schemas/linked-spec@1.json"
        linked.symlink_to(source)
        catalog = self.catalog()
        catalog["runtime_files"] = ["shared/schemas/linked-spec@1.json"]
        self.write_json("harnesses/codex/catalog.json", catalog)

        result = self.build()

        self.assertEqual(result.returncode, 0, result.stderr)
        generated = self.root / "dist/codex/plugins/alpha/shared/schemas/linked-spec@1.json"
        self.assertFalse(generated.is_symlink())
        self.assertEqual(generated.read_bytes(), source.read_bytes())

    def test_native_skill_parity_failure_does_not_replace_previous_output(self) -> None:
        self.write_json("harnesses/codex/catalog.json", self.catalog())
        self.assertEqual(self.build().returncode, 0)
        output = self.root / "dist/codex"
        before = self.files(output)
        (self.root / "harnesses/codex/plugins/alpha/skills/inspect/SKILL.md").unlink()

        result = self.build()

        self.assertEqual(result.returncode, 2)
        self.assertIn("skill parity mismatch", result.stderr)
        self.assertEqual(self.files(output), before)

    def test_rejects_native_version_drift_without_replacing_output(self) -> None:
        self.write_json("harnesses/codex/catalog.json", self.catalog())
        self.assertEqual(self.build().returncode, 0)
        output = self.root / "dist/codex"
        before = self.files(output)
        manifest_path = self.root / "harnesses/codex/plugins/bravo/.codex-plugin/plugin.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["version"] = "9.9.9"
        self.write_json("harnesses/codex/plugins/bravo/.codex-plugin/plugin.json", manifest)

        result = self.build()

        self.assertEqual(result.returncode, 2)
        self.assertIn("version must match", result.stderr)
        self.assertEqual(self.files(output), before)

    def test_rejects_native_author_drift_without_replacing_output(self) -> None:
        self.write_json("harnesses/codex/catalog.json", self.catalog())
        self.assertEqual(self.build().returncode, 0)
        output = self.root / "dist/codex"
        before = self.files(output)
        manifest_path = self.root / "harnesses/codex/plugins/bravo/.codex-plugin/plugin.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["author"] = {"name": "Different maintainer", "email": "other@example.test"}
        self.write_json("harnesses/codex/plugins/bravo/.codex-plugin/plugin.json", manifest)

        result = self.build()

        self.assertEqual(result.returncode, 2)
        self.assertIn("author must match", result.stderr)
        self.assertEqual(self.files(output), before)

    def test_rejects_invalid_native_manifest_without_replacing_output(self) -> None:
        self.write_json("harnesses/codex/catalog.json", self.catalog())
        self.assertEqual(self.build().returncode, 0)
        output = self.root / "dist/codex"
        before = self.files(output)
        manifest_path = self.root / "harnesses/codex/plugins/bravo/.codex-plugin/plugin.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["interface"]["capabilities"] = "Read"  # type: ignore[index]
        self.write_json("harnesses/codex/plugins/bravo/.codex-plugin/plugin.json", manifest)

        result = self.build()

        self.assertEqual(result.returncode, 2)
        self.assertIn("interface.capabilities", result.stderr)
        self.assertEqual(self.files(output), before)

    def test_rejects_runtime_file_collision_without_replacing_output(self) -> None:
        self.write_json("harnesses/codex/catalog.json", self.catalog())
        self.assertEqual(self.build().returncode, 0)
        output = self.root / "dist/codex"
        before = self.files(output)
        catalog = self.catalog()
        catalog["plugins"][0]["runtime_files"] = [  # type: ignore[index]
            {"source": "shared/schemas/spec@1.json", "destination": ".codex-plugin/plugin.json"}
        ]
        self.write_json("harnesses/codex/catalog.json", catalog)

        result = self.build()

        self.assertEqual(result.returncode, 2)
        self.assertIn("conflicts with authored native source", result.stderr)
        self.assertEqual(self.files(output), before)

    def test_check_fails_for_missing_or_stale_output(self) -> None:
        self.write_json("harnesses/codex/catalog.json", self.catalog())
        check = subprocess.run(
            [sys.executable, str(BUILDER), "--repo-root", str(self.root), "--check"],
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(check.returncode, 2)
        self.assertIn("out of date", check.stderr)
        self.assertEqual(self.build().returncode, 0)
        checked = subprocess.run(
            [sys.executable, str(BUILDER), "--repo-root", str(self.root), "--check"],
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(checked.returncode, 0, checked.stderr)


if __name__ == "__main__":
    unittest.main()
