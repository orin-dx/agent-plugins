"""Enforce concern-first shared references, valid paths, and runtime callers."""

from __future__ import annotations

import re
import unittest
from pathlib import Path
from urllib.parse import unquote


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
REFERENCE_ROOT = REPOSITORY_ROOT / "shared/references"
REFERENCE_PATH = re.compile(r"shared/references/[A-Za-z0-9@._/-]+\.md")
SCHEMA_PATH = re.compile(r"shared/schemas/[A-Za-z0-9@._/-]+\.json")
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_LINK = re.compile(r"^\s*\[[^\]]+\]:\s+(\S+)", re.MULTILINE)
HTML_LINK = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']")
RETIRED_REFERENCE_NAME = re.compile(
    r"(?:\*|rust|typescript|python|go)-hazards(?:-t7-t10)?\.md|(?<!/)changesets\.md"
)
TEXT_SUFFIXES = {".json", ".md", ".py", ".sh", ".yaml", ".yml"}
EXCLUDED_PARTS = {".git", ".agents", "dist"}
AUTHORING_ONLY = {
    "shared/references/README.md",
    "shared/references/authoring/diagrams.md",
    "shared/references/tooling/cli.md",
}
CONCERN_DIRECTORIES = {
    "architecture",
    "authoring",
    "delivery",
    "evaluation",
    "hazards",
    "tooling",
    "verification",
    "workspace",
}
# Published schemas are byte-immutable. Keep narrow exceptions for exact paths
# embedded before a reference move; live skill and agent routes must still use
# current paths and pass the checks below.
IMMUTABLE_PATH_EXCEPTIONS = {
    (
        "shared/schemas/changeset@2.json",
        "shared/references/" "changesets" ".md",
    ): "shared/references/delivery/changesets.md",
}


def authored_text_files() -> list[Path]:
    return [
        path
        for path in REPOSITORY_ROOT.rglob("*")
        if path.is_file()
        and path.suffix in TEXT_SUFFIXES
        and path.name != "CHANGELOG.md"
        and not EXCLUDED_PARTS.intersection(path.relative_to(REPOSITORY_ROOT).parts)
    ]


def is_runtime_caller(path: Path) -> bool:
    relative = path.relative_to(REPOSITORY_ROOT)
    parts = relative.parts
    if parts[:2] == ("shared", "references"):
        return path != REFERENCE_ROOT / "README.md"
    if parts[:2] == ("shared", "hooks"):
        return True
    if parts and parts[0] == "plugins":
        return "agents" in parts or "skills" in parts
    return parts[:3] == ("harnesses", "codex", "plugins") and "skills" in parts


def local_markdown_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = target.split(maxsplit=1)[0]
    if not target or target.startswith("#") or "://" in target or target.startswith("mailto:"):
        return None
    return unquote(target.split("#", 1)[0].split("?", 1)[0])


class ReferenceIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sources = {
            path: path.read_text(encoding="utf-8")
            for path in authored_text_files()
        }

    def test_exact_reference_paths_exist(self) -> None:
        broken: list[str] = []
        for source, contents in self.sources.items():
            for reference in REFERENCE_PATH.findall(contents):
                source_name = source.relative_to(REPOSITORY_ROOT).as_posix()
                if (source_name, reference) in IMMUTABLE_PATH_EXCEPTIONS:
                    continue
                if not (REPOSITORY_ROOT / reference).is_file():
                    broken.append(f"{source_name} -> {reference}")
        self.assertEqual(broken, [])

    def test_exact_schema_paths_exist(self) -> None:
        broken = [
            f"{source.relative_to(REPOSITORY_ROOT).as_posix()} -> {schema}"
            for source, contents in self.sources.items()
            if source.suffix in {".json", ".md", ".yaml", ".yml"}
            for schema in SCHEMA_PATH.findall(contents)
            if not (REPOSITORY_ROOT / schema).is_file()
        ]
        self.assertEqual(broken, [])

    def test_immutable_path_exceptions_have_live_replacements(self) -> None:
        invalid: list[str] = []
        for (source_name, historical), replacement in IMMUTABLE_PATH_EXCEPTIONS.items():
            source = REPOSITORY_ROOT / source_name
            if historical not in source.read_text(encoding="utf-8"):
                invalid.append(f"{source_name} no longer contains {historical}")
            if not (REPOSITORY_ROOT / replacement).is_file():
                invalid.append(f"replacement missing: {replacement}")
            live_callers = [
                path.relative_to(REPOSITORY_ROOT).as_posix()
                for path, contents in self.sources.items()
                if path != source and is_runtime_caller(path) and historical in contents
            ]
            if live_callers:
                invalid.append(f"live callers still use {historical}: {live_callers}")
        self.assertEqual(invalid, [])

    def test_local_markdown_links_resolve(self) -> None:
        broken: list[str] = []
        for source, contents in self.sources.items():
            if source.suffix != ".md":
                continue
            raw_targets = (
                MARKDOWN_LINK.findall(contents)
                + REFERENCE_LINK.findall(contents)
                + HTML_LINK.findall(contents)
            )
            for raw_target in raw_targets:
                target = local_markdown_target(raw_target)
                if target is None:
                    continue
                resolved = (source.parent / target).resolve()
                if not resolved.exists():
                    source_name = source.relative_to(REPOSITORY_ROOT).as_posix()
                    broken.append(f"{source_name} -> {target}")
        self.assertEqual(broken, [])

    def test_retired_or_ambiguous_reference_names_are_absent(self) -> None:
        stale = [
            f"{source.relative_to(REPOSITORY_ROOT).as_posix()} -> {match.group(0)}"
            for source, contents in self.sources.items()
            for match in RETIRED_REFERENCE_NAME.finditer(contents)
        ]
        self.assertEqual(stale, [])

    def test_reference_paths_are_concern_first(self) -> None:
        misplaced = [
            path.relative_to(REFERENCE_ROOT).as_posix()
            for path in REFERENCE_ROOT.rglob("*.md")
            if path != REFERENCE_ROOT / "README.md"
            and path.relative_to(REFERENCE_ROOT).parts[0] not in CONCERN_DIRECTORIES
        ]
        self.assertEqual(misplaced, [])

    def test_each_runtime_reference_has_a_runtime_caller(self) -> None:
        missing: list[str] = []
        for reference_file in REFERENCE_ROOT.rglob("*.md"):
            reference = reference_file.relative_to(REPOSITORY_ROOT).as_posix()
            if reference in AUTHORING_ONLY:
                continue
            callers = [
                source
                for source, contents in self.sources.items()
                if source != reference_file and is_runtime_caller(source) and reference in contents
            ]
            if not callers:
                missing.append(reference)
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
