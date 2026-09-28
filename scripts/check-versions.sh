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

# The ecosystem-level version has the same drift risk as a plugin's, and the
# same nothing structural stopped it: marketplace.json's top-level .version
# sat two releases ahead of the root CHANGELOG.md and README badge before
# this check existed.
root_version="$(jq -r '.version' marketplace.json)"
root_changelog_version="$(grep -oE '^## \[[0-9]+\.[0-9]+\.[0-9]+' CHANGELOG.md | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || true)"
root_badge_version="$(grep -oE 'Marketplace-v[0-9]+\.[0-9]+\.[0-9]+' README.md | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || true)"

root_mismatches=()
[[ -z "$root_changelog_version" ]] && root_mismatches+=("CHANGELOG.md: no ## [x.y.z] entry found")
[[ -n "$root_changelog_version" && "$root_changelog_version" != "$root_version" ]] && root_mismatches+=("CHANGELOG.md says $root_changelog_version")
[[ -z "$root_badge_version" ]] && root_mismatches+=("README.md: no Marketplace badge found")
[[ -n "$root_badge_version" && "$root_badge_version" != "$root_version" ]] && root_mismatches+=("README.md badge says $root_badge_version")

root_fail=0
if [[ ${#root_mismatches[@]} -gt 0 ]]; then
  root_fail=1
  echo "FAIL: ecosystem version (marketplace.json: $root_version)"
  for m in "${root_mismatches[@]}"; do
    echo "    $m"
  done
fi

report_check "$root_fail" 1 \
  "ecosystem version agrees across marketplace.json/CHANGELOG.md/README.md." \
  "ecosystem version has drift. Fix and re-run."
