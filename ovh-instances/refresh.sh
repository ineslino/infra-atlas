#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# Infra Atlas · OVH Instance Catalogue · data refresh
#
# v1: regenerate data.json from index.html every run. v2 TODO: wire OVH API
# (https://api.ovh.com/) to fetch live flavors per region.
# ─────────────────────────────────────────────────────────────────

set -euo pipefail
cd "$(dirname "$0")"

need() { command -v "$1" >/dev/null 2>&1 || { echo "✗ $1 not found." >&2; exit 1; }; }
need jq
need python3

echo "▸ Regenerating data.json from index.html…"
python3 - <<'PYEOF'
import re, json, sys
with open('index.html', encoding='utf-8') as f: html = f.read()
def extract(name):
    m = re.search(rf'^(?:const|let|var) {name} = (\[.*?\n\]);', html, re.DOTALL | re.MULTILINE)
    if not m: sys.exit(f"✗ {name} not found")
    src = m.group(1)
    src = re.sub(r'([{,]\s*)([a-zA-Z_]\w*)\s*:', r'\1"\2":', src)
    src = re.sub(r',(\s*[}\]])', r'\1', src)
    src = re.sub(r'//[^\n]*', '', src)
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.DOTALL)
    return json.loads(src)
regions=extract("REGIONS"); families=extract("FAMILIES")
with open('data.json','w',encoding='utf-8') as f:
    json.dump({"generated":"1970-01-01T00:00:00Z","provider":"ovh","regions":regions,"families":families},
              f, indent=2, ensure_ascii=False)
print(f"  ✓ extracted {len(regions)} regions · {len(families)} families")
PYEOF

TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
jq --arg ts "$TS" '.generated = $ts' data.json > data.json.tmp && mv data.json.tmp data.json
echo "✓ data.json refreshed at $TS"
echo "  $(jq '.regions | length' data.json) regions · $(jq '.families | length' data.json) families · $(jq '[.families[].sizes[]] | length' data.json) instance types"
