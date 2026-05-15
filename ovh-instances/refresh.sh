#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# Infra Atlas · OVH Instance Catalogue · data refresh
#
# CREDENTIAL-FREE. Pulls OVHcloud's PUBLIC order catalogue
# (api.ovh.com/v1/order/catalog/public/cloud) — no account, no token.
#
# Public Cloud families (d2, b3, c3, r3, i1, t1, t2, h100) are sourced
# live: the catalogue is authoritative for which flavours exist, and
# carries vCPU / memory / hourly price → merged into specs[size].
# Bare-metal families are dedicated servers, billed monthly — not part
# of the hourly cloud-instance catalogue; their curated sizes are kept
# and carry no hourly price.
#
# Schema: { generated, provider, currency, priceRef, regions[], families[] }
# Each family: specs[size] = { vcpu, mem, price }  ·  price = EUR/hour.
#
# Requirements: curl, python3.
# ─────────────────────────────────────────────────────────────────

set -euo pipefail
cd "$(dirname "$0")"

need() { command -v "$1" >/dev/null 2>&1 || { echo "✗ $1 not found." >&2; exit 1; }; }
need curl
need python3

CATALOG="https://api.ovh.com/v1/order/catalog/public/cloud?ovhSubsidiary=IE"
TMP="$(mktemp -t ovh_cat.XXXXXX)"
trap 'rm -f "$TMP"' EXIT

echo "▸ Downloading OVH Public Cloud catalogue (api.ovh.com)…"
curl --compressed -fsSL "$CATALOG" -o "$TMP"

echo "▸ Merging live prices → data.json…"
python3 - "$TMP" <<'PYEOF'
import re, json, sys, datetime

with open('index.html', encoding='utf-8') as f:
    html = f.read()

def extract(name):
    m = re.search(rf'^(?:const|let|var) {name} = (\[.*?\n\]);', html, re.DOTALL | re.MULTILINE)
    if not m:
        sys.exit(f"✗ {name} not found in index.html")
    src = m.group(1)
    src = re.sub(r'([{,]\s*)([a-zA-Z_]\w*)\s*:', r'\1"\2":', src)
    src = re.sub(r',(\s*[}\]])', r'\1', src)
    src = re.sub(r'//[^\n]*', '', src)
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.DOTALL)
    return json.loads(src)

regions  = extract("REGIONS")
families = extract("FAMILIES")

# ── Parse the OVH catalogue: base hourly flavour addons ──
with open(sys.argv[1], encoding='utf-8') as f:
    cat = json.load(f)

flavors = {}   # flavour name -> {vcpu, mem, price}
for addon in cat.get("addons", []):
    pc = addon.get("planCode", "")
    m = re.match(r'^([a-z].*)\.consumption$', pc)   # base hourly flavour only
    if not m or addon.get("product") != "publiccloud-instance":
        continue
    tech = (addon.get("blobs") or {}).get("technical") or {}
    price = None
    for pr in addon.get("pricings", []):
        if pr.get("intervalUnit") == "hour" and pr.get("price") is not None:
            price = round(pr["price"] / 1e8, 5)   # catalogue scale is 1e8
            break
    flavors[m.group(1)] = {
        "vcpu":  (tech.get("cpu") or {}).get("cores"),
        "mem":   (tech.get("memory") or {}).get("size"),
        "price": price,
    }

# Group flavours by family prefix ("b3-8" -> "b3", "t2-le-45" -> "t2").
def fam_prefix(flavour):
    m = re.match(r'^([a-z]+\d*)-', flavour)
    return m.group(1) if m else flavour

catalog_fams = {}
for fl in flavors:
    catalog_fams.setdefault(fam_prefix(fl), []).append(fl)

def natural(s):
    return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', s)]

# ── Merge into families: Public Cloud sourced live, bare-metal kept curated ──
priced = 0
for fam in families:
    key = fam.get("key", "")
    if key in catalog_fams:
        # Public Cloud — the catalogue is authoritative for the flavour list
        fam["sizes"] = sorted(catalog_fams[key], key=natural)
        specs = {}
        for size in fam["sizes"]:
            fl = flavors[size]
            specs[size] = {"vcpu": fl["vcpu"], "mem": fl["mem"], "price": fl["price"]}
            if fl["price"] is not None:
                priced += 1
        fam["specs"] = specs
    else:
        # Bare-metal — dedicated servers, no hourly catalogue entry
        fam["specs"] = {s: {"vcpu": None, "mem": None, "price": None}
                        for s in fam.get("sizes", [])}

out = {
    "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "provider": "ovh",
    "source": "OVHcloud public order catalogue — no credentials",
    "currency": "EUR",
    "priceRef": "GRA",
    "regions": regions,
    "families": families,
}
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

n_types = sum(len(f["sizes"]) for f in families)
print(f"  ✓ {len(regions)} regions · {len(families)} families · "
      f"{n_types} instance types · {priced} priced (Public Cloud, EUR/hr)")
PYEOF

echo "✓ data.json refreshed — OVH Public Cloud priced live from the public catalogue"
