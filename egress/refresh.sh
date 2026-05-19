#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# Infra Atlas · Egress & Data-Transfer Cost Map · data refresh
#
# CREDENTIAL-FREE. Data-transfer rates are curated in index.html — no
# vendor API exposes a clean, comparable multi-cloud transfer rate card,
# and the published pricing pages render their tables dynamically. This
# script regenerates ./data.json from the PROVIDERS / GROUPS / TRANSFERS
# consts in index.html (the source of truth), refreshes the timestamp,
# and sanity-checks the structure. Update rates by editing index.html,
# then re-run this script and commit data.json.
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
    # Quote unquoted object keys:  {key: …}  →  {"key": …}
    src = re.sub(r'([{,]\s*)([a-zA-Z_]\w*)\s*:', r'\1"\2":', src)
    # Drop trailing commas before } or ]
    src = re.sub(r',(\s*[}\]])', r'\1', src)
    # Strip // line comments — but NOT the // inside https:// URLs
    src = re.sub(r'(?<!:)//[^\n]*', '', src)
    # Strip /* block */ comments
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.DOTALL)
    try:
        return json.loads(src)
    except json.JSONDecodeError as e:
        print(f"✗ Failed to parse {name}: {e}", file=sys.stderr)
        lines = src.split('\n')
        for i in range(max(0, e.lineno - 3), min(len(lines), e.lineno + 3)):
            print(f"  {i+1}: {lines[i]}", file=sys.stderr)
        sys.exit(1)

providers = extract_array("PROVIDERS")
groups    = extract_array("GROUPS")
transfers = extract_array("TRANSFERS")

out = {
    "generated":     "1970-01-01T00:00:00Z",
    "schemaVersion": 1,
    "currency":      "USD",
    "providers":     providers,
    "groups":        groups,
    "transfers":     transfers,
}
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print(f"  ✓ extracted {len(providers)} providers · {len(groups)} groups · {len(transfers)} transfer types")
PYEOF

# Update timestamp every run
TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
jq --arg ts "$TS" '.generated = $ts' data.json > data.json.tmp && mv data.json.tmp data.json

# ─────────────────────────────────────────────────────────────────
# Sanity check — every transfer must price every provider, with a
# headline, a sourced footnote, and non-negative tier rates.
# ─────────────────────────────────────────────────────────────────
echo "▸ Checking structure…"
python3 - <<'PYEOF'
import json, sys

with open('data.json', encoding='utf-8') as f:
    data = json.load(f)

provider_keys = [p['key'] for p in data['providers']]
transfers = data['transfers']
problems = 0

if len(transfers) < 5:
    print(f"::warning::only {len(transfers)} transfer types — expected at least 5")

for t in transfers:
    for pk in provider_keys:
        r = t.get('rates', {}).get(pk)
        if r is None:
            print(f"::error::{t['id']} has no rate for provider '{pk}'")
            problems += 1
            continue
        for field in ('level', 'headline', 'note', 'src'):
            if not r.get(field):
                print(f"::error::{t['id']}/{pk} is missing '{field}'")
                problems += 1
        if r.get('src', '') and not r['src'].startswith('https://'):
            print(f"::error::{t['id']}/{pk} src is not an https URL")
            problems += 1
        for tier in r.get('tiers', []):
            if not isinstance(tier.get('usd'), (int, float)) or tier['usd'] < 0:
                print(f"::error::{t['id']}/{pk} tier '{tier.get('band')}' has a bad rate")
                problems += 1

if problems:
    print(f"::error::{problems} structural problem(s) in egress/data.json")
    sys.exit(1)
print(f"  ✓ {len(transfers)} transfers × {len(provider_keys)} providers — all priced and sourced")
PYEOF

T_COUNT="$(jq '.transfers | length' data.json)"
P_COUNT="$(jq '.providers | length' data.json)"
echo ""
echo "✓ data.json refreshed at $TS"
echo "  $T_COUNT transfer types · $P_COUNT providers"
echo ""
echo "  ⚠  Egress rates are hand-curated in index.html. To update,"
echo "     edit PROVIDERS / GROUPS / TRANSFERS there and re-run this script."
