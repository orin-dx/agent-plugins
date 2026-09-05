"""Regression tests for the Wisp Plugins public and marketplace identity."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def read_json(relative: str) -> dict[str, object]:
    return json.loads((REPOSITORY_ROOT / relative).read_text(encoding="utf-8"))


class BrandIdentityTests(unittest.TestCase):
    def test_marketplaces_use_wisp_plugins_identity(self) -> None:
        agy = read_json("marketplace.json")
        claude = read_json(".claude-plugin/marketplace.json")
        catalog = read_json("harnesses/codex/catalog.json")

        self.assertEqual(agy["name"], "wisp-plugins")
        self.assertEqual(claude["name"], "wisp-plugins")
        self.assertEqual(catalog["marketplace"], {"name": "wisp-plugins", "display_name": "Wisp Plugins"})

    def test_harness_docs_use_wisp_plugins_selectors(self) -> None:
        root_readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("/plugin marketplace remove orin-dx-agent-plugins", root_readme)
        self.assertIn("codex plugin add weaver@wisp-plugins", root_readme)
        self.assertIn("codex plugin marketplace upgrade wisp-plugins", root_readme)
        self.assertIn("codex plugin marketplace remove orin-dx-agent-plugins", root_readme)
        for plugin in ("courier", "mason", "muse", "navigator", "ranger", "scribe", "sentinel", "smith", "vanguard", "weaver"):
            readme = (REPOSITORY_ROOT / "plugins" / plugin / "README.md").read_text(encoding="utf-8")
            self.assertIn(f"codex plugin add {plugin}@wisp-plugins", readme)
            self.assertNotIn(f"codex plugin add {plugin}@orin-dx-agent-plugins", readme)
            self.assertIn(f"agy-plugin add {plugin}@wisp-plugins", root_readme)
            self.assertNotIn(f"agy-plugin add {plugin}@orin-dx", root_readme)

    def test_public_brand_and_publisher_source_remain_distinct(self) -> None:
        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        logo = (REPOSITORY_ROOT / "assets/logo.svg").read_text(encoding="utf-8")
        claude = read_json(".claude-plugin/marketplace.json")

        self.assertIn('alt="Wisp Plugins"', readme)
        self.assertIn(">WISP</text>", logo)
        self.assertIn(">PLUGINS</text>", logo)
        self.assertEqual(claude["plugins"][0]["source"]["url"], "https://github.com/orin-dx/agent-plugins.git")


if __name__ == "__main__":
    unittest.main()
