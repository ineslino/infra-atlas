#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# Infra Atlas · Azure VM Atlas · data refresh
#
# v1 strategy:
#  - On first run, bootstrap ./data.json from the FAMILIES/REGIONS
#    consts embedded in ./index.html (Python parses the JS literals).
#  - On every run, refresh the `generated` timestamp.
#
# v2 (TODO): wire `az` CLI via federated identity (Azure OIDC for
# GitHub Actions — see https://learn.microsoft.com/azure/active-directory/workload-identities).
# Then auto-fetch:
#   az account list-locations                          → regions
#   az vm list-skus --resource-type virtualMachines    → VM SKUs by region
# And cross-check tracked SERIES against live SKU list, flag mismatches.
#
# Requirements: jq, python3.
# ─────────────────────────────────────────────────────────────────

set -euo pipefail
cd "$(dirname "$0")"

need() {
  command -v "$1" >/dev/null 2>&1 || { echo "✗ $1 not found." >&2; exit 1; }
}
need jq
need python3

# ─────────────────────────────────────────────────────────────────
# Bootstrap data.json from index.html (one-time, on first run)
# ─────────────────────────────────────────────────────────────────
if [[ ! -f data.json ]]; then
  echo "▸ Bootstrapping data.json from index.html…"
  python3 - <<'PYEOF'
import re, json, sys

with open('index.html', encoding='utf-8') as f:
    html = f.read()

def extract_array(name):
    m = re.search(rf'^(?:const|let|var) {name} = (\[.*?\n\]);', html, re.DOTALL | re.MULTILINE)
    if not m:
        print(f"✗ {name} declaration not found in index.html", file=sys.stderr)
        sys.exit(1)
    src = m.group(1)
    # JS → JSON: quote unquoted keys, strip trailing commas, strip comments
    src = re.sub(r'([{,]\s*)([a-zA-Z_]\w*)\s*:', r'\1"\2":', src)
    src = re.sub(r',(\s*[}\]])', r'\1', src)
    src = re.sub(r'//[^\n]*', '', src)
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.DOTALL)
    try:
        return json.loads(src)
    except json.JSONDecodeError as e:
        print(f"✗ Failed to parse {name}: {e}", file=sys.stderr)
        sys.exit(1)

regions  = extract_array("REGIONS")
families = extract_array("FAMILIES")

out = {
    "generated": "1970-01-01T00:00:00Z",
    "provider": "azure",
    "regions":  regions,
    "families": families,    # consistent with EC2 instrument's loadData() shape
}
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

n_sizes = sum(len(f.get('sizes', [])) for f in families)
print(f"  ✓ extracted {len(regions)} regions · {len(families)} series · {n_sizes} unique VM sizes")
PYEOF
fi

# ─────────────────────────────────────────────────────────────────
# Update timestamp (every run)
# ─────────────────────────────────────────────────────────────────
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
jq --arg ts "$TS" '.generated = $ts' data.json > data.json.tmp && mv data.json.tmp data.json

REGION_COUNT="$(jq '.regions  | length' data.json)"
SERIES_COUNT="$(jq '.families | length' data.json)"
SIZES_COUNT="$( jq '[.families[].sizes[]] | length' data.json)"

echo "✓ data.json refreshed at $TS"
echo "  $REGION_COUNT regions · $SERIES_COUNT series · $SIZES_COUNT VM sizes"
echo ""
echo "  ⚠  Note: Azure data is hand-curated in index.html. To update,"
echo "     edit FAMILIES/REGIONS there, delete data.json, re-run this script."
echo "     v2 will wire az CLI via OIDC for auto-refresh."
