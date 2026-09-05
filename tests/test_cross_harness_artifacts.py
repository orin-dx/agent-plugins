"""Verify the portable lifecycle fixture against Claude source and Codex output."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = REPOSITORY_ROOT / "tests/fixtures/cross-harness/lifecycle.json"


def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON object from a repository-controlled file."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain a JSON object")
    return value


def validate_subset(instance: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    """Validate the JSON-Schema features used by the lifecycle fixture."""
    errors: list[str] = []
    expected_type = schema.get("type")
    type_matches = {
        "object": lambda value: isinstance(value, dict),
        "array": lambda value: isinstance(value, list),
        "string": lambda value: isinstance(value, str),
        "boolean": lambda value: isinstance(value, bool),
    }
    if expected_type in type_matches and not type_matches[expected_type](instance):
        return [f"{path}: expected {expected_type}"]

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: expected one of {schema['enum']!r}")

    if isinstance(instance, dict):
        properties = schema.get("properties", {})
        for name in schema.get("required", []):
            if name not in instance:
                errors.append(f"{path}: missing required property {name!r}")
        if schema.get("additionalProperties") is False:
            for name in instance:
                if name not in properties:
                    errors.append(f"{path}: unexpected property {name!r}")
        for name, value in instance.items():
            child_schema = properties.get(name)
            if isinstance(child_schema, dict):
                errors.extend(validate_subset(value, child_schema, f"{path}.{name}"))

    if isinstance(instance, list):
        minimum = schema.get("minItems")
        if isinstance(minimum, int) and len(instance) < minimum:
            errors.append(f"{path}: expected at least {minimum} items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, value in enumerate(instance):
                errors.extend(validate_subset(value, item_schema, f"{path}[{index}]"))
    return errors


class CrossHarnessArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixture = read_json(FIXTURE_PATH)
        cls.stages = fixture["stages"]

    def test_fixture_documents_validate_against_portable_contracts(self) -> None:
        for stage in self.stages:
            artifact = stage["artifact"]
            source_schema = read_json(REPOSITORY_ROOT / "shared/schemas" / f"{artifact}.json")
            errors = validate_subset(stage["document"], source_schema)
            self.assertEqual(errors, [], f"{artifact} fixture is invalid: {errors}")

    def test_codex_materializes_the_same_contract_bytes_for_each_handoff(self) -> None:
        for stage in self.stages:
            artifact = stage["artifact"]
            source = REPOSITORY_ROOT / "shared/schemas" / f"{artifact}.json"
            for role in ("producer", "consumer"):
                plugin = stage[role]["plugin"]
                materialized = REPOSITORY_ROOT / "dist/codex/plugins" / plugin / "shared/schemas" / f"{artifact}.json"
                self.assertTrue(materialized.is_file(), f"{plugin} is missing {artifact}")
                self.assertFalse(materialized.is_symlink(), f"{plugin} ships {artifact} as a symlink")
                self.assertEqual(materialized.read_bytes(), source.read_bytes(), f"{plugin} changed {artifact}")

    def test_each_fixture_handoff_is_declared_by_both_harnesses(self) -> None:
        for stage in self.stages:
            artifact = stage["artifact"]
            producer = stage["producer"]
            consumer = stage["consumer"]
            producer_manifest = read_json(REPOSITORY_ROOT / "plugins" / producer["plugin"] / "plugin.json")
            consumer_manifest = read_json(REPOSITORY_ROOT / "plugins" / consumer["plugin"] / "plugin.json")
            self.assertIn(artifact, producer_manifest["produces"])
            self.assertIn(artifact, consumer_manifest["consumes"])

            codex_producer = REPOSITORY_ROOT / "dist/codex/plugins" / producer["plugin"] / "skills" / producer["skill"] / "SKILL.md"
            codex_consumer = REPOSITORY_ROOT / "dist/codex/plugins" / consumer["plugin"] / "skills" / consumer["skill"] / "SKILL.md"
            self.assertIn(artifact, codex_producer.read_text(encoding="utf-8"))
            self.assertIn(artifact, codex_consumer.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
