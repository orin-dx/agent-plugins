#!/usr/bin/env bash
# For each plugin, extracts every `plugin/skill-name` mention from a README
# table row (the "| `plugin/skill` | ... |" Skills table every split plugin
# uses) and checks a matching skills/<skill-name>/SKILL.md exists. Scoped to
# table rows, not free prose, so a README that explicitly says "there is no
# `plugin/skill` to invoke" (the fix applied in v3.1.0) doesn't false-positive.
# Catches skills documented as real but never built or renamed without
# updating the docs — five plugins had this fixed in v3.1.0.
#
# Usage: scripts/check-skills-doc.sh

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

  mentions="$(grep -E "^\| \`${id}/[a-z0-9-]+\`" "$dir/README.md" 2>/dev/null \
              | grep -oE "\`${id}/[a-z0-9-]+\`" | tr -d '`' | sort -u || true)"

  missing=()
  while IFS= read -r mention; do
    [[ -z "$mention" ]] && continue
    skill="${mention#"${id}"/}"
    [[ -f "$dir/skills/$skill/SKILL.md" ]] || missing+=("$mention")
  done <<< "$mentions"

  if [[ ${#missing[@]} -gt 0 ]]; then
    fail=$((fail + 1))
    echo "FAIL: $id"
    for m in "${missing[@]}"; do
      echo "    documented but no skills/${m#"${id}"/}/SKILL.md: $m"
    done
  fi
done

report_check "$fail" "$count" \
  "plugin(s), every documented skill has a matching skills/ directory." \
  "plugin(s) document skills with no matching directory. Fix and re-run."
