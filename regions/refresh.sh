#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# Infra Atlas · Multi-Cloud Region Map · data refresh
#
# CREDENTIAL-FREE. Region geography is curated in index.html (no
# vendor API exposes a clean multi-cloud region atlas). This script
# bootstraps ./data.json from the CITIES const and refreshes the
# timestamp. Update region data by editing index.html, then re-run.
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

# Extract the CITIES array literal (accept const | let | var)
m = re.search(r'^(?:const|let|var) CITIES = (\[.*?\n\]);\s*$', html, re.DOTALL | re.MULTILINE)
if not m:
    print("✗ CITIES declaration not found in index.html", file=sys.stderr)
    sys.exit(1)

src = m.group(1)

# Convert JS object literal → JSON
# 1) Quote unquoted keys:   {city: ...}  →  {"city": ...}
src = re.sub(r'([{,]\s*)([a-zA-Z_]\w*)\s*:', r'\1"\2":', src)
# 2) Remove trailing commas before } or ]
src = re.sub(r',(\s*[}\]])', r'\1', src)
# 3) Comments — strip // line comments and /* block */ comments
src = re.sub(r'//[^\n]*', '', src)
src = re.sub(r'/\*.*?\*/', '', src, flags=re.DOTALL)

try:
    cities = json.loads(src)
except json.JSONDecodeError as e:
    print(f"✗ Failed to parse CITIES: {e}", file=sys.stderr)
    print("--- offending region ---", file=sys.stderr)
    lines = src.split('\n')
    start = max(0, e.lineno - 3)
    end   = min(len(lines), e.lineno + 3)
    for i in range(start, end):
        print(f"  {i+1}: {lines[i]}", file=sys.stderr)
    sys.exit(1)

out = { "generated": "1970-01-01T00:00:00Z", "cities": cities }
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print(f"  ✓ extracted {len(cities)} cities ({sum(len(c['regions']) for c in cities)} regions)")
PYEOF
fi

# ─────────────────────────────────────────────────────────────────
# Update timestamp
# ─────────────────────────────────────────────────────────────────
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
jq --arg ts "$TS" '.generated = $ts' data.json > data.json.tmp && mv data.json.tmp data.json

CITY_COUNT="$(jq '.cities | length' data.json)"
REGION_COUNT="$(jq '[.cities[].regions[]] | length' data.json)"
echo ""
echo "✓ data.json refreshed at $TS"
echo "  $CITY_COUNT cities · $REGION_COUNT regions across 5 providers"
