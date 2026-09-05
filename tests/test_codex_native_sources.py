"""Verify that the release bundle copies every authored native Codex source unchanged."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPOSITORY_ROOT / "harnesses/codex/catalog.json"
NATIVE_ROOT = REPOSITORY_ROOT / "harnesses/codex/plugins"
ROLE_ROOT = REPOSITORY_ROOT / "harnesses/codex/agent-roles"
OUTPUT_ROOT = REPOSITORY_ROOT / "dist/codex/plugins"
SOURCE_ROOT = REPOSITORY_ROOT / "plugins"
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
SCHEMA_REFERENCE = re.compile(r"shared/schemas/([A-Za-z0-9@._-]+\.json)")


def read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain a JSON object")
    return value


class CodexNativeSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        catalog = read_json(CATALOG_PATH)
        entries = catalog["plugins"]
        if not isinstance(entries, list):
            raise AssertionError("Codex catalog plugins must be an array")
        cls.plugin_ids = [entry["id"] for entry in entries if isinstance(entry, dict) and isinstance(entry.get("id"), str)]

    def test_catalog_and_native_source_trees_have_exact_plugin_parity(self) -> None:
        native_ids = {path.name for path in NATIVE_ROOT.iterdir() if path.is_dir()}
        self.assertEqual(native_ids, set(self.plugin_ids))

    def test_native_skill_sets_match_claude_source_skill_sets(self) -> None:
        for plugin_id in self.plugin_ids:
            source_skills = {path.name for path in (SOURCE_ROOT / plugin_id / "skills").iterdir() if (path / "SKILL.md").is_file()}
            native_skills = {path.name for path in (NATIVE_ROOT / plugin_id / "skills").iterdir() if (path / "SKILL.md").is_file()}
            self.assertEqual(native_skills, source_skills, plugin_id)

    def test_native_manifests_and_skill_frontmatter_meet_the_release_contract(self) -> None:
        for plugin_id in self.plugin_ids:
            manifest = read_json(NATIVE_ROOT / plugin_id / ".codex-plugin" / "plugin.json")
            self.assertEqual(manifest.get("name"), plugin_id)
            self.assertRegex(str(manifest.get("version", "")), SEMVER)
            self.assertTrue(isinstance(manifest.get("description"), str) and manifest["description"].strip())
            self.assertEqual(manifest.get("skills"), "./skills/")
            author = manifest.get("author")
            self.assertTrue(isinstance(author, dict) and isinstance(author.get("name"), str) and author["name"].strip(), plugin_id)
            interface = manifest.get("interface")
            self.assertIsInstance(interface, dict, plugin_id)
            for field in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
                self.assertTrue(isinstance(interface.get(field), str) and interface[field].strip(), f"{plugin_id}.{field}")
            for field in ("capabilities", "defaultPrompt"):
                self.assertTrue(isinstance(interface.get(field), list) and all(isinstance(item, str) and item.strip() for item in interface[field]), f"{plugin_id}.{field}")
            for skill in (NATIVE_ROOT / plugin_id / "skills").iterdir():
                contents = (skill / "SKILL.md").read_text(encoding="utf-8")
                self.assertTrue(contents.startswith("---\n"), f"{plugin_id}/{skill.name}")
                frontmatter, _, _ = contents[4:].partition("\n---\n")
                self.assertRegex(frontmatter, rf"(?m)^name: {re.escape(skill.name)}$")
                self.assertRegex(frontmatter, r"(?m)^description: .+\S$")

    def test_each_native_schema_reference_is_declared_for_materialization(self) -> None:
        catalog = read_json(CATALOG_PATH)
        global_runtime = catalog.get("runtime_files")
        self.assertIsInstance(global_runtime, list)
        entries = {entry["id"]: entry for entry in catalog["plugins"] if isinstance(entry, dict) and isinstance(entry.get("id"), str)}
        for plugin_id in self.plugin_ids:
            entry = entries[plugin_id]
            runtime = [*global_runtime, *entry.get("runtime_files", [])]
            declared_sources = {
                item if isinstance(item, str) else item.get("source")
                for item in runtime
                if isinstance(item, str) or isinstance(item, dict)
            }
            expected = {
                match
                for skill in (NATIVE_ROOT / plugin_id / "skills").iterdir()
                for match in SCHEMA_REFERENCE.findall((skill / "SKILL.md").read_text(encoding="utf-8"))
            }
            if "shared/schemas" in declared_sources:
                continue
            actual = {Path(source).name for source in declared_sources if isinstance(source, str) and source.startswith("shared/schemas/")}
            self.assertTrue(expected <= actual, f"{plugin_id} does not materialize {sorted(expected - actual)}")

    def test_delegating_skills_select_packaged_role_cards(self) -> None:
        role_files = {path.name: path.read_bytes() for path in ROLE_ROOT.glob("*.md")}
        self.assertIn("README.md", role_files)
        role_guide = role_files["README.md"].decode("utf-8")
        for field in ("Role", "Objective", "Inputs", "Owned paths", "Exclusions", "Output", "Evidence", "Completion"):
            self.assertIn(f"| {field} |", role_guide)
        for plugin_id in self.plugin_ids:
            for name, contents in role_files.items():
                output = OUTPUT_ROOT / plugin_id / "agent-roles" / name
                self.assertTrue(output.is_file(), f"{plugin_id} is missing agent role {name}")
                self.assertEqual(output.read_bytes(), contents, f"{plugin_id} rewrote agent role {name}")
            for skill in (NATIVE_ROOT / plugin_id / "skills").iterdir():
                contents = (skill / "SKILL.md").read_text(encoding="utf-8")
                can_delegate = any(
                    phrase in contents
                    for phrase in ("teams are available", "teams are enabled", "teams may", "teammates may")
                )
                if can_delegate:
                    self.assertIn("agent-roles/README.md", contents, f"{plugin_id}/{skill.name} can delegate without a role card")

    def test_mason_materializes_the_cross_harness_authoring_guide(self) -> None:
        source = REPOSITORY_ROOT / "shared/harness-authoring.md"
        output = OUTPUT_ROOT / "mason/shared/harness-authoring.md"
        self.assertTrue(output.is_file())
        self.assertEqual(output.read_bytes(), source.read_bytes())

    def test_every_authored_native_file_is_identical_in_the_release_bundle(self) -> None:
        for plugin_id in self.plugin_ids:
            source_root = NATIVE_ROOT / plugin_id
            output_root = OUTPUT_ROOT / plugin_id
            for source in source_root.rglob("*"):
                if not source.is_file():
                    continue
                output = output_root / source.relative_to(source_root)
                self.assertTrue(output.is_file(), f"{plugin_id} is missing {source.relative_to(source_root)}")
                self.assertFalse(output.is_symlink(), f"{plugin_id} ships {source.relative_to(source_root)} as a symlink")
                self.assertEqual(output.read_bytes(), source.read_bytes(), f"{plugin_id} rewrote {source.relative_to(source_root)}")


if __name__ == "__main__":
    unittest.main()
