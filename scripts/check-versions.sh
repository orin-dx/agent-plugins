#!/usr/bin/env bash
# For each plugin, checks that plugin.json's version, the README's
# **Version:** line, the CHANGELOG's top entry, and marketplace.json's
# per-plugin version all agree. These four are updated by hand on every
# bump and have drifted before (fixed across 4 plugins in v3.1.0) —
# nothing structural stopped it from happening again.
#
# Usage: scripts/check-versions.sh

set -euo pipefail
script_dir="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=lib/report.sh
source "$script_dir/lib/report.sh"
cd "$script_dir/.."

fail=0
count=0

for plugin_json in plugins/*/plugin.json; do
  dir="$(dirname "$plugin_json")"
  id="$(basename "$dir")"
  count=$((count + 1))

  pj_version="$(jq -r '.version' "$plugin_json")"
  readme_version="$(grep -oE '\*\*Version:\*\* *[0-9]+\.[0-9]+\.[0-9]+' "$dir/README.md" | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || true)"
  changelog_version="$(grep -oE '^## \[[0-9]+\.[0-9]+\.[0-9]+' "$dir/CHANGELOG.md" | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || true)"
  marketplace_version="$(jq -r --arg id "$id" '.plugins[] | select(.id == $id) | .version' marketplace.json)"

  mismatches=()
  [[ -z "$readme_version" ]] && mismatches+=("README: no **Version:** line found")
  [[ -n "$readme_version" && "$readme_version" != "$pj_version" ]] && mismatches+=("README says $readme_version")
  [[ -z "$changelog_version" ]] && mismatches+=("CHANGELOG: no ## [x.y.z] entry found")
  [[ -n "$changelog_version" && "$changelog_version" != "$pj_version" ]] && mismatches+=("CHANGELOG says $changelog_version")
  [[ -z "$marketplace_version" ]] && mismatches+=("marketplace.json: no entry for id \"$id\"")
  [[ -n "$marketplace_version" && "$marketplace_version" != "$pj_version" ]] && mismatches+=("marketplace.json says $marketplace_version")

  if [[ ${#mismatches[@]} -gt 0 ]]; then
    fail=$((fail + 1))
    echo "FAIL: $id (plugin.json: $pj_version)"
    for m in "${mismatches[@]}"; do
      echo "    $m"
    done
  fi
done

report_check "$fail" "$count" \
  "plugin(s), all versions agree across plugin.json/README/CHANGELOG/marketplace.json." \
  "plugin(s) have version drift. Fix and re-run."
