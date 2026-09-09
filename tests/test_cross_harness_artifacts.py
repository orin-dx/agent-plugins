"""Verify the portable lifecycle fixture against Claude source and Codex output."""

from __future__ import annotations

import copy
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
        "integer": lambda value: isinstance(value, int) and not isinstance(value, bool),
    }
    if expected_type in type_matches and not type_matches[expected_type](instance):
        return [f"{path}: expected {expected_type}"]

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: expected one of {schema['enum']!r}")
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected {schema['const']!r}")
    forbidden = schema.get("not")
    if isinstance(forbidden, dict) and not validate_subset(instance, forbidden, path):
        errors.append(f"{path}: matched a forbidden shape")
    if isinstance(instance, str):
        minimum_length = schema.get("minLength")
        if isinstance(minimum_length, int) and len(instance) < minimum_length:
            errors.append(f"{path}: expected at least {minimum_length} characters")
    if isinstance(instance, int) and not isinstance(instance, bool):
        minimum = schema.get("minimum")
        if isinstance(minimum, int) and instance < minimum:
            errors.append(f"{path}: expected at least {minimum}")

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
        contains = schema.get("contains")
        if isinstance(contains, dict) and not any(
            not validate_subset(value, contains, f"{path}[{index}]") for index, value in enumerate(instance)
        ):
            errors.append(f"{path}: no item matched the required shape")

    for constraint in schema.get("allOf", []):
        errors.extend(validate_subset(instance, constraint, path))

    condition = schema.get("if")
    if isinstance(condition, dict):
        branch = schema.get("then") if not validate_subset(instance, condition, path) else schema.get("else")
        if isinstance(branch, dict):
            errors.extend(validate_subset(instance, branch, path))
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

    def test_implementation_review_requires_structural_assessments(self) -> None:
        stage = next(stage for stage in self.stages if stage["artifact"] == "implementation-review@1")
        schema = read_json(REPOSITORY_ROOT / "shared/schemas/implementation-review@1.json")

        missing_assessment = copy.deepcopy(stage["document"])
        del missing_assessment["defect_families"][0]["architecture"]
        self.assertTrue(any("missing required property 'architecture'" in error for error in validate_subset(missing_assessment, schema)))

        unknown_field = copy.deepcopy(stage["document"])
        unknown_field["defect_families"][0]["confidence"] = "high"
        self.assertTrue(any("unexpected property 'confidence'" in error for error in validate_subset(unknown_field, schema)))

        missing_deferral_reason = copy.deepcopy(stage["document"])
        missing_deferral_reason["defect_families"][0]["disposition"] = "explicit_deferral"
        self.assertTrue(any("missing required property 'deferral_reason'" in error for error in validate_subset(missing_deferral_reason, schema)))

        mismatched_deferral = copy.deepcopy(stage["document"])
        mismatched_deferral["defect_families"][0]["instances"][1]["status"] = "deferred"
        self.assertTrue(any("forbidden shape" in error for error in validate_subset(mismatched_deferral, schema)))

        missing_search = copy.deepcopy(stage["document"])
        del missing_search["sibling_search"]
        self.assertTrue(any("missing required property 'sibling_search'" in error for error in validate_subset(missing_search, schema)))

        missing_lineage = copy.deepcopy(stage["document"])
        del missing_lineage["workspace"]
        self.assertTrue(any("missing required property 'workspace'" in error for error in validate_subset(missing_lineage, schema)))

        unsupported_language = copy.deepcopy(stage["document"])
        unsupported_language["language"] = "python"
        self.assertTrue(any("expected one of" in error for error in validate_subset(unsupported_language, schema)))

        missing_escalation = copy.deepcopy(stage["document"])
        missing_escalation["defect_families"][0]["disposition"] = "fix_instances"
        self.assertTrue(any("no item matched" in error for error in validate_subset(missing_escalation, schema)))

        invalid_approval = copy.deepcopy(stage["document"])
        invalid_approval["status"] = "approved"
        invalid_approval["defect_families"][0]["disposition"] = "fix_instances"
        self.assertTrue(any("forbidden shape" in error for error in validate_subset(invalid_approval, schema)))

        invalid_repair = copy.deepcopy(stage["document"])
        invalid_repair["status"] = "changes_requested"
        invalid_repair["issues"] = [{
            "file": "src/consumer.ts",
            "line": 14,
            "description": "Repair the unresolved sibling.",
            "severity": "must_fix",
            "family_id": "FAMILY-001",
        }]
        self.assertTrue(any("forbidden shape" in error for error in validate_subset(invalid_repair, schema)))


if __name__ == "__main__":
    unittest.main()
