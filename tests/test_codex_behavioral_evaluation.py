"""Verify that the Codex behavioral evaluation protocol remains wired to durable contracts."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
GUIDE_PATH = REPOSITORY_ROOT / "docs/codex-behavioral-evaluation.md"
RELEASE_POLICY_PATH = REPOSITORY_ROOT / "docs/codex-marketplace-release-policy.md"
SCHEMA_PATH = REPOSITORY_ROOT / "shared/schemas/harness-evaluation@1.json"


class CodexBehavioralEvaluationTests(unittest.TestCase):
    def test_evaluation_schema_has_a_closed_evidence_contract(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(schema["additionalProperties"], False)
        self.assertEqual(
            set(schema["required"]),
            {"id", "fixture", "route", "execution", "artifacts", "outcome", "blocking_findings", "reasoning"},
        )
        self.assertEqual(schema["properties"]["outcome"]["enum"], ["pass", "fail", "unverifiable"])

    def test_guide_and_release_policy_reference_the_same_protocol(self) -> None:
        guide = GUIDE_PATH.read_text(encoding="utf-8")
        release_policy = RELEASE_POLICY_PATH.read_text(encoding="utf-8")
        self.assertIn("tests/fixtures/cross-harness/lifecycle.json", guide)
        self.assertIn("Extract only the first stage's `requirement@1` document", guide)
        self.assertIn("shared/schemas/harness-evaluation@1.json", guide)
        self.assertIn("Codex single-agent", guide)
        self.assertIn("Codex team", guide)
        self.assertIn("codex-behavioral-evaluation.md", release_policy)


if __name__ == "__main__":
    unittest.main()
