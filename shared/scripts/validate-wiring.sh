#!/usr/bin/env bash
# Wiring validator for agent-plugins.
# Checks that all schema references in plugin.json resolve to files in
# shared/schemas/, and that consumes/produces arrays are internally consistent.
#
# Exit codes: 0 = pass, 1 = validation failure, 2 = script error.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCHEMAS_DIR="$REPO_ROOT/shared/schemas"
PLUGINS_DIR="$REPO_ROOT/plugins"

ERRORS=0
WARNINGS=0

pass() { printf '  \033[32m✓\033[0m %s\n' "$1"; }
fail() { printf '  \033[31m✗\033[0m %s\n' "$1"; ERRORS=$((ERRORS + 1)); }
warn() { printf '  \033[33m!\033[0m %s\n' "$1"; WARNINGS=$((WARNINGS + 1)); }

schema_exists() {
  local name="$1"
  [[ -f "$SCHEMAS_DIR/$name.json" ]]
}

echo
echo "=== Wiring Validation ==="
echo

# ── Step 1: List all schema files in shared/schemas/ ──────────────────────────
echo "Step 1: Schema inventory"
SCHEMA_LIST=""
for schema_file in "$SCHEMAS_DIR"/*.json; do
  [[ -f "$schema_file" ]] || continue
  name="$(basename "$schema_file" .json)"
  SCHEMA_LIST="$SCHEMA_LIST $name"
  pass "Found schema: $name"
done

echo

# ── Step 2: Collect all produced schemas across all plugins ───────────────────
echo "Step 2: Plugin produces/consumes declarations"
ALL_PRODUCED=""
for plugin_json in "$PLUGINS_DIR"/*/plugin.json; do
  plugin_id="$(jq -r '.id' "$plugin_json")"
  produces="$(jq -r '.produces[]? // empty' "$plugin_json" 2>/dev/null | tr '\n' ' ')"
  consumes="$(jq -r '.consumes[]? // empty' "$plugin_json" 2>/dev/null | tr '\n' ' ')"
  ALL_PRODUCED="$ALL_PRODUCED $produces"
  pass "Read plugin: $plugin_id (produces: ${produces:-none}, consumes: ${consumes:-none})"
done

echo

# ── Step 3: Validate schema file references ───────────────────────────────────
echo "Step 3: Schema file resolution"
for plugin_json in "$PLUGINS_DIR"/*/plugin.json; do
  plugin_id="$(jq -r '.id' "$plugin_json")"

  while IFS= read -r schema; do
    [[ -z "$schema" ]] && continue
    if schema_exists "$schema"; then
      pass "$plugin_id produces $schema — file exists"
    else
      fail "$plugin_id produces '$schema' but $SCHEMAS_DIR/$schema.json does not exist"
    fi
  done < <(jq -r '.produces[]? // empty' "$plugin_json")

  while IFS= read -r schema; do
    [[ -z "$schema" ]] && continue
    if schema_exists "$schema"; then
      pass "$plugin_id consumes $schema — file exists"
    else
      fail "$plugin_id consumes '$schema' but $SCHEMAS_DIR/$schema.json does not exist"
    fi
  done < <(jq -r '.consumes[]? // empty' "$plugin_json")
done

echo

# ── Step 4: Validate each consumed schema is produced by at least one plugin ──
echo "Step 4: Produces satisfies consumes"
for plugin_json in "$PLUGINS_DIR"/*/plugin.json; do
  plugin_id="$(jq -r '.id' "$plugin_json")"
  while IFS= read -r schema; do
    [[ -z "$schema" ]] && continue
    if echo "$ALL_PRODUCED" | grep -qw "$schema"; then
      pass "$plugin_id consumes $schema — produced by at least one plugin"
    else
      warn "$plugin_id consumes '$schema' but no plugin declares it as produced (optional schema or external source)"
    fi
  done < <(jq -r '.consumes[]? // empty' "$plugin_json")
done

echo

# ── Step 5: Validate agent files exist ────────────────────────────────────────
echo "Step 5: Agent file existence"
for plugin_json in "$PLUGINS_DIR"/*/plugin.json; do
  plugin_dir="$(dirname "$plugin_json")"
  plugin_id="$(jq -r '.id' "$plugin_json")"
  while IFS= read -r agent_path; do
    [[ -z "$agent_path" ]] && continue
    full_path="$plugin_dir/$agent_path"
    if [[ -f "$full_path" ]]; then
      pass "$plugin_id agent exists: $agent_path"
    else
      fail "$plugin_id agent not found: $full_path"
    fi
  done < <(jq -r '.agents[]? // empty' "$plugin_json")
done

echo

# ── Summary ───────────────────────────────────────────────────────────────────
echo "=== Summary ==="
printf '  Errors:   %d\n' "$ERRORS"
printf '  Warnings: %d\n' "$WARNINGS"
echo

if (( ERRORS > 0 )); then
  echo "FAIL — $ERRORS error(s) found. Fix before running agents."
  exit 1
else
  echo "PASS — wiring is valid."
  exit 0
fi
