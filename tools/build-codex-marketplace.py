#!/usr/bin/env python3
"""Materialize the repository's authored Codex marketplace.

Codex behavior is authored in ``harnesses/codex/plugins/<id>/``.  The builder
copies those native plugin trees into ``dist/codex`` without rewriting manifests
or skills. ``harnesses/codex/catalog.json`` controls marketplace identity, order,
and portable runtime files only. Its supported shape is::

    {
      "catalog_version": 1,
      "harness": "codex",
      "runtime_files": [],
      "plugins": [{"id": "...", "runtime_files": ["shared/schemas/example@1.json"]}]
    }

``runtime_files`` may alternatively use ``{"source": "...", "destination":
"..."}`` when preserving the repository-relative source path is not appropriate.
The output is rebuilt atomically and contains regular files only.  It is a build
artifact; do not hand-edit ``dist/codex``.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


CATALOG_VERSION = 1
PLUGIN_ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


class BuildError(Exception):
    """A catalog or source input cannot produce a safe marketplace."""


def fail(message: str) -> None:
    raise BuildError(message)


def read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"{label} does not exist: {path}")
    except json.JSONDecodeError as error:
        fail(f"{label} is invalid JSON ({path}:{error.lineno}:{error.colno}): {error.msg}")
    if not isinstance(value, dict):
        fail(f"{label} must be a JSON object: {path}")
    return value


def require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label} must be a non-empty string")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        fail(f"{label} must be an array")
    return value


def require_string_list(value: Any, label: str) -> list[str]:
    values = require_list(value, label)
    if not all(isinstance(item, str) and item.strip() for item in values):
        fail(f"{label} must contain non-empty strings")
    return values


def path_within(root: Path, raw_path: str, label: str) -> Path:
    candidate = (root / raw_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        fail(f"{label} escapes the repository root: {raw_path}")
    return candidate


def output_path(repo_root: Path, raw_path: str) -> Path:
    path = (repo_root / raw_path).resolve()
    try:
        relative = path.relative_to(repo_root)
    except ValueError:
        fail(f"output path escapes the repository root: {raw_path}")
    if not relative.parts:
        fail("output path cannot be the repository root")
    return path


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_regular_files(source: Path, destination: Path, repo_root: Path, label: str) -> None:
    """Copy a file or directory, resolving links but never emitting one."""
    resolved = source.resolve()
    try:
        resolved.relative_to(repo_root)
    except ValueError:
        fail(f"{label} resolves outside the repository root: {source}")
    if resolved.is_file():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(resolved, destination)
        return
    if not resolved.is_dir():
        fail(f"{label} is neither a regular file nor a directory: {source}")

    for child in sorted(resolved.rglob("*"), key=lambda item: item.as_posix()):
        if child.is_dir():
            continue
        child_resolved = child.resolve()
        try:
            child_resolved.relative_to(repo_root)
        except ValueError:
            fail(f"{label} contains a link outside the repository root: {child}")
        if not child_resolved.is_file():
            fail(f"{label} contains a non-regular file: {child}")
        target = destination / child.relative_to(resolved)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(child_resolved, target)


def source_plugin(repo_root: Path, plugin_id: str) -> tuple[dict[str, Any], set[str]]:
    if not PLUGIN_ID.fullmatch(plugin_id):
        fail(f"plugins[].id must be a lowercase hyphen-case identifier: {plugin_id!r}")
    manifest_path = path_within(repo_root, f"plugins/{plugin_id}/plugin.json", f"plugin {plugin_id} manifest")
    manifest = read_json(manifest_path, f"plugin {plugin_id} manifest")
    if manifest.get("id") != plugin_id:
        fail(f"plugin {plugin_id} manifest id does not match its catalog id")
    version = require_string(manifest.get("version"), f"plugin {plugin_id} manifest.version")
    del version
    if not isinstance(manifest.get("author"), dict):
        fail(f"plugin {plugin_id} manifest.author must be an object")
    skills_root = path_within(repo_root, f"plugins/{plugin_id}/skills", f"plugin {plugin_id} skills")
    if not skills_root.is_dir():
        fail(f"plugin {plugin_id} skills directory does not exist: {skills_root}")
    skills = {
        child.name
        for child in skills_root.iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    }
    if not skills:
        fail(f"plugin {plugin_id} has no source skills")
    return manifest, skills


def native_plugin(repo_root: Path, plugin_id: str) -> tuple[Path, dict[str, Any], set[str]]:
    native_root = path_within(repo_root, f"harnesses/codex/plugins/{plugin_id}", f"native Codex plugin {plugin_id}")
    if not native_root.is_dir():
        fail(f"native Codex plugin directory does not exist: {native_root}")
    manifest_path = path_within(
        repo_root,
        f"harnesses/codex/plugins/{plugin_id}/.codex-plugin/plugin.json",
        f"native Codex plugin {plugin_id} manifest",
    )
    manifest = read_json(manifest_path, f"native Codex plugin {plugin_id} manifest")
    if require_string(manifest.get("name"), f"native Codex plugin {plugin_id} manifest.name") != plugin_id:
        fail(f"native Codex plugin {plugin_id} manifest name does not match its catalog id")
    version = require_string(manifest.get("version"), f"native Codex plugin {plugin_id} manifest.version")
    if SEMVER.fullmatch(version) is None:
        fail(f"native Codex plugin {plugin_id} manifest.version must be strict semver")
    require_string(manifest.get("description"), f"native Codex plugin {plugin_id} manifest.description")
    author = manifest.get("author")
    if not isinstance(author, dict):
        fail(f"native Codex plugin {plugin_id} manifest.author must be an object")
    require_string(author.get("name"), f"native Codex plugin {plugin_id} manifest.author.name")
    if "email" in author:
        require_string(author["email"], f"native Codex plugin {plugin_id} manifest.author.email")
    if manifest.get("skills") not in {"skills", "./skills", "skills/", "./skills/"}:
        fail(f"native Codex plugin {plugin_id} manifest.skills must resolve to skills")
    skills_root = path_within(repo_root, f"harnesses/codex/plugins/{plugin_id}/skills", f"native Codex plugin {plugin_id} skills")
    if not skills_root.is_dir():
        fail(f"native Codex plugin {plugin_id} skills directory does not exist: {skills_root}")
    skills = {
        child.name
        for child in skills_root.iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    }
    if not skills:
        fail(f"native Codex plugin {plugin_id} has no skills")
    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        fail(f"native Codex plugin {plugin_id} manifest.interface must be an object")
    for field in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        require_string(interface.get(field), f"native Codex plugin {plugin_id} manifest.interface.{field}")
    require_string_list(interface.get("capabilities"), f"native Codex plugin {plugin_id} manifest.interface.capabilities")
    require_string_list(interface.get("defaultPrompt"), f"native Codex plugin {plugin_id} manifest.interface.defaultPrompt")
    return native_root, manifest, skills


def runtime_entry(entry: Any, repo_root: Path, plugin_output: Path, plugin_id: str) -> None:
    if isinstance(entry, str):
        source_relative = entry
        destination_relative = entry
    elif isinstance(entry, dict):
        source_relative = require_string(entry.get("source"), f"plugin {plugin_id} runtime_files[].source")
        destination_relative = require_string(
            entry.get("destination"), f"plugin {plugin_id} runtime_files[].destination"
        )
    else:
        fail(f"plugin {plugin_id} runtime_files entries must be strings or objects")
    source = path_within(repo_root, source_relative, f"plugin {plugin_id} runtime source")
    destination = (plugin_output / destination_relative).resolve()
    try:
        destination.relative_to(plugin_output)
    except ValueError:
        fail(f"plugin {plugin_id} runtime destination escapes plugin output: {destination_relative}")
    if destination.exists():
        fail(f"plugin {plugin_id} runtime destination conflicts with authored native source: {destination_relative}")
    copy_regular_files(source, destination, repo_root, f"plugin {plugin_id} runtime source")


def materialize_plugin(
    repo_root: Path,
    generated_plugins: Path,
    entry: dict[str, Any],
    global_runtime_files: list[Any],
) -> dict[str, Any]:
    plugin_id = require_string(entry.get("id"), "plugins[].id")
    if not PLUGIN_ID.fullmatch(plugin_id):
        fail(f"plugins[].id must be a lowercase hyphen-case identifier: {plugin_id!r}")
    source_manifest, source_skills = source_plugin(repo_root, plugin_id)
    native_root, native_manifest, native_skills = native_plugin(repo_root, plugin_id)
    if native_manifest["version"] != source_manifest["version"]:
        fail(f"native Codex plugin {plugin_id} version must match plugins/{plugin_id}/plugin.json")
    if native_manifest["author"] != source_manifest["author"]:
        fail(f"native Codex plugin {plugin_id} author must match plugins/{plugin_id}/plugin.json")
    if native_skills != source_skills:
        missing = sorted(source_skills - native_skills)
        extra = sorted(native_skills - source_skills)
        fail(f"native Codex plugin {plugin_id} skill parity mismatch (missing: {missing}; extra: {extra})")
    plugin_output = generated_plugins / plugin_id
    copy_regular_files(native_root, plugin_output, repo_root, f"native Codex plugin {plugin_id}")

    runtime_files = global_runtime_files + require_list(
        entry.get("runtime_files", []), f"plugin {plugin_id} runtime_files"
    )
    for runtime_file in runtime_files:
        runtime_entry(runtime_file, repo_root, plugin_output, plugin_id)

    category = require_string(native_manifest["interface"].get("category"), f"native Codex plugin {plugin_id} category")
    return {"name": plugin_id, "category": category}


def catalog_marketplace(catalog: dict[str, Any]) -> dict[str, Any]:
    if catalog.get("catalog_version") != CATALOG_VERSION:
        fail(f"catalog catalog_version must be {CATALOG_VERSION}")
    if catalog.get("harness") != "codex":
        fail("catalog harness must be 'codex'")
    marketplace = catalog.get("marketplace", {})
    if not isinstance(marketplace, dict):
        fail("catalog marketplace must be an object when set")
    name = marketplace.get("name", "wisp-plugins")
    display_name = marketplace.get("display_name", marketplace.get("displayName", "Wisp Plugins"))
    return {
        "name": require_string(name, "catalog marketplace.name"),
        "displayName": require_string(display_name, "catalog marketplace.display_name"),
    }


def files_match(expected: Path, actual: Path) -> bool:
    if not actual.is_dir():
        return False
    expected_paths = [path.relative_to(expected) for path in expected.rglob("*") if path.is_file()]
    if any(path.is_symlink() for path in actual.rglob("*")):
        return False
    actual_paths = [path.relative_to(actual) for path in actual.rglob("*") if path.is_file()]
    if sorted(expected_paths) != sorted(actual_paths):
        return False
    return all((expected / path).read_bytes() == (actual / path).read_bytes() for path in expected_paths)


def build(repo_root: Path, catalog_path: Path, output: Path, check: bool = False) -> None:
    catalog = read_json(catalog_path, "Codex catalog")
    marketplace = catalog_marketplace(catalog)
    entries = require_list(catalog.get("plugins"), "catalog plugins")
    if not entries:
        fail("catalog plugins must not be empty")
    if not all(isinstance(entry, dict) for entry in entries):
        fail("catalog plugins entries must be objects")
    ids = [entry.get("id") for entry in entries]
    if len(ids) != len(set(ids)):
        fail("catalog plugins must not repeat an id")
    global_runtime_files = require_list(catalog.get("runtime_files", []), "catalog runtime_files")

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{output.name}.build-", dir=output.parent))
    backup: Path | None = None
    try:
        plugins_output = temporary / "plugins"
        generated_entries = [
            materialize_plugin(repo_root, plugins_output, entry, global_runtime_files) for entry in entries
        ]
        marketplace_payload = {
            "name": marketplace["name"],
            "interface": {"displayName": marketplace["displayName"]},
            "plugins": [
                {
                    "name": entry["name"],
                    "source": {"source": "local", "path": f"./plugins/{entry['name']}"},
                    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                    "category": entry["category"],
                }
                for entry in generated_entries
            ],
        }
        write_json(temporary / ".agents" / "plugins" / "marketplace.json", marketplace_payload)

        if check:
            if not files_match(temporary, output):
                fail(f"generated marketplace is out of date: {output}")
            return

        if output.exists() and not output.is_dir():
            fail(f"output path exists but is not a directory: {output}")
        backup = output.with_name(f".{output.name}.previous-{os.getpid()}")
        if backup.exists():
            shutil.rmtree(backup)
        if output.exists():
            output.rename(backup)
        temporary.rename(output)
        if backup.exists():
            shutil.rmtree(backup)
    except Exception:
        if backup is not None and backup.exists() and not output.exists():
            backup.rename(output)
        raise
    finally:
        if temporary.exists():
            shutil.rmtree(temporary, ignore_errors=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".", help="repository root (default: current directory)")
    parser.add_argument(
        "--catalog", default="harnesses/codex/catalog.json", help="catalog path relative to --repo-root"
    )
    parser.add_argument("--output", default="dist/codex", help="output path relative to --repo-root")
    parser.add_argument("--check", action="store_true", help="fail if output differs instead of writing it")
    arguments = parser.parse_args(argv)
    repo_root = Path(arguments.repo_root).resolve()
    try:
        catalog_path = path_within(repo_root, arguments.catalog, "catalog path")
        build(repo_root, catalog_path, output_path(repo_root, arguments.output), arguments.check)
    except BuildError as error:
        print(f"build-codex-marketplace: error: {error}", file=sys.stderr)
        return 2
    except OSError as error:
        print(f"build-codex-marketplace: error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
