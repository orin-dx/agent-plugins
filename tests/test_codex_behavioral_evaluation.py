"""Verify that the Codex behavioral evaluation protocol remains wired to durable contracts."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
GUIDE_PATH = REPOSITORY_ROOT / "docs/codex-behavioral-evaluation.md"
RELEASE_POLICY_PATH = REPOSITORY_ROOT / "docs/codex-marketplace-release-policy.md"
SCHEMA_PATH = REPOSITORY_ROOT / "shared/schemas/harness-evaluation@2.json"
RUN_SCHEMA_PATH = REPOSITORY_ROOT / "shared/schemas/evaluation-run@1.json"
IMPLEMENTATION_FIXTURE_PATH = REPOSITORY_ROOT / "tests/fixtures/behavioral/implementation-verification.json"


class CodexBehavioralEvaluationTests(unittest.TestCase):
    def test_evaluation_schema_has_a_closed_evidence_contract(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(schema["additionalProperties"], False)
        self.assertEqual(
            set(schema["required"]),
            {
                "id",
                "fixture",
                "route",
                "execution",
                "workspace_state",
                "artifacts",
                "metrics",
                "outcome",
                "blocking_findings",
                "reasoning",
            },
        )
        self.assertEqual(schema["properties"]["outcome"]["enum"], ["pass", "fail", "unverifiable"])
        self.assertEqual(
            set(schema["properties"]["execution"]["properties"]["plugins"]["items"]["required"]),
            {"id", "version", "source_revision"},
        )
        pass_rule = schema["allOf"][0]["then"]["properties"]
        self.assertEqual(pass_rule["metrics"]["properties"]["false_passes"]["const"], 0)
        self.assertEqual(pass_rule["blocking_findings"]["maxItems"], 0)

        run_schema = json.loads(RUN_SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(run_schema["additionalProperties"], False)
        self.assertEqual(run_schema["properties"]["pending_checks"]["maxItems"], 0)

    def test_guide_and_release_policy_reference_the_same_protocol(self) -> None:
        guide = GUIDE_PATH.read_text(encoding="utf-8")
        release_policy = RELEASE_POLICY_PATH.read_text(encoding="utf-8")
        self.assertIn("tests/fixtures/cross-harness/lifecycle.json", guide)
        self.assertIn("Extract only the first stage's `requirement@1` document", guide)
        self.assertIn("shared/schemas/harness-evaluation@2.json", guide)
        self.assertIn("Codex single-agent", guide)
        self.assertIn("Codex team", guide)
        self.assertIn("codex-behavioral-evaluation.md", release_policy)

    def test_implementation_fixture_separates_public_input_from_oracle(self) -> None:
        fixture = json.loads(IMPLEMENTATION_FIXTURE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            {case["language"] for case in fixture["cases"]},
            {"typescript", "rust", "python", "go"},
        )
        for case in fixture["cases"]:
            self.assertIn("public_input", case)
            self.assertIn("oracle", case)
            self.assertGreater(case["oracle"]["seeded_defects"], 0)
            self.assertTrue(case["oracle"]["false_pass_if"])


if __name__ == "__main__":
    unittest.main()
