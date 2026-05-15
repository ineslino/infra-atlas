#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# Infra Atlas · GCP Compute Index · data refresh
#
# v1 strategy:
#  - On every run, regenerate ./data.json from the FAMILIES/REGIONS
#    consts embedded in ./index.html (Python parses the JS literals),
#    then refresh the `generated` timestamp.
#
# v2 (TODO): wire `gcloud` via Workload Identity Federation
# (https://cloud.google.com/iam/docs/workload-identity-federation-with-other-providers).
# Then auto-fetch:
#   gcloud compute machine-types list --format=json
#   gcloud compute regions list --format=json
# And cross-check tracked FAMILIES against live offerings, flag drift.
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

echo "▸ Regenerating data.json from index.html…"
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
    "provider": "gcp",
    "regions":  regions,
    "families": families,
}
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

n_sizes = sum(len(f.get('sizes', [])) for f in families)
print(f"  ✓ extracted {len(regions)} regions · {len(families)} families · {n_sizes} unique machine types")
PYEOF

# Update timestamp every run
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
jq --arg ts "$TS" '.generated = $ts' data.json > data.json.tmp && mv data.json.tmp data.json

REGION_COUNT="$(jq '.regions  | length' data.json)"
FAMILY_COUNT="$(jq '.families | length' data.json)"
TYPES_COUNT="$( jq '[.families[].sizes[]] | length' data.json)"

echo "✓ data.json refreshed at $TS"
echo "  $REGION_COUNT regions · $FAMILY_COUNT families · $TYPES_COUNT machine types"
echo ""
echo "  ⚠  Note: GCP data is hand-curated in index.html. To update,"
echo "     edit FAMILIES/REGIONS there and re-run this script."
echo "     v2 will wire gcloud CLI via Workload Identity Federation."
