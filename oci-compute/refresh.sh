#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# Infra Atlas · OCI Compute Observatory · data refresh
#
# CREDENTIAL-FREE. Pulls Oracle's PUBLIC price list
# (apexapps.oracle.com/.../cetools/api/v1/products) — no account, no token.
#
# OCI prices flexible compute per OCPU/hour + per GiB/hour. For each
# Flex VM shape this script computes the hourly price of a shape at
# the OCI console default of 16 GiB per OCPU:
#     price = OCPUs · OCPU-rate  +  memory · GiB-rate
#  · vCPU — 2 × OCPU on x86, 1 × OCPU on Ampere (arm).
#  · mem  — OCPUs × 16 GiB (the default Flex ratio; stated per row).
# Bare-metal (BM.*) shapes have fixed, non-ratio memory and are left
# without a computed hourly price.
#
# Schema: { generated, provider, currency, priceRef, regions[], families[] }
# Each family: specs[size] = { vcpu, mem, price }.
#
# Requirements: curl, python3.
# ─────────────────────────────────────────────────────────────────

set -euo pipefail
cd "$(dirname "$0")"

need() { command -v "$1" >/dev/null 2>&1 || { echo "✗ $1 not found." >&2; exit 1; }; }
need curl
need python3

PRODUCTS="https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/?currencyCode=USD"
TMP="$(mktemp -t oci_prod.XXXXXX)"
trap 'rm -f "$TMP"' EXIT

echo "▸ Downloading OCI price list (apexapps.oracle.com)…"
curl --compressed -fsSL "$PRODUCTS" -o "$TMP"

echo "▸ Computing shape prices → data.json…"
python3 - "$TMP" <<'PYEOF'
import re, json, sys, datetime

GB_PER_OCPU = 16   # OCI console default memory ratio for Flex shapes

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

# ── Parse the OCI price list into per-(kind, series) OCPU + GiB rates ──
with open(sys.argv[1], encoding='utf-8') as f:
    products = json.load(f)

rates = {}   # (kind, series) -> {"ocpu": rate, "mem": rate}
for it in products.get("items", []):
    dn = it.get("displayName", "")
    if "Compute" not in dn:
        continue
    low = dn.lower()
    if "dense" in low:        kind = "denseio"
    elif "optimized" in low:  kind = "optimized"
    elif "standard" in low:   kind = "standard"
    else:                     continue
    sm = re.search(r'\b([EA]\d|X\d+)\b', dn)
    if not sm:
        continue
    series = sm.group(1)
    try:
        val = it["currencyCodeLocalizations"][0]["prices"][0]["value"]
    except (KeyError, IndexError):
        continue
    metric = (it.get("metricName") or "").lower()
    slot = rates.setdefault((kind, series), {})
    if "ocpu" in metric:
        slot["ocpu"] = max(slot.get("ocpu", 0), val)   # paid rate beats $0 free-tier line
    elif "gigabyte" in metric or "memory" in low:
        slot["mem"] = max(slot.get("mem", 0), val)

# The public price list reports the Ampere A1 shape at the free-tier $0.
# Its paid rate is published on oracle.com/cloud/compute/pricing — used
# only as a fallback when the API carries no non-zero rate.
FALLBACK = {("standard", "A1"): {"ocpu": 0.01, "mem": 0.0015}}
for k, fb in FALLBACK.items():
    if not (rates.get(k) or {}).get("ocpu"):
        rates[k] = fb

# ── Map a family key to its (kind, series) rate bucket ──
def rate_key(key):
    if not key.startswith("VM."):
        return None                       # bare metal — no computed hourly price
    if "DenseIO" in key:     kind = "denseio"
    elif "Optimized" in key: kind = "optimized"
    elif "Standard" in key:  kind = "standard"
    else:                    return None
    m = re.search(r'\.(E\d|A\d)\.', key)
    if m:
        return (kind, m.group(1))
    if "Standard3" in key or "Optimized3" in key:
        return (kind, "X9")               # Intel Ice Lake generation
    return None

priced = 0
for fam in families:
    arch = fam.get("arch", "x86")
    rk = rate_key(fam.get("key", ""))
    r = rates.get(rk) if rk else None
    specs = {}
    for size in fam.get("sizes", []):
        m = re.match(r'(\d+)\s*OCPU', size)
        if r and m and r.get("ocpu"):
            ocpu = int(m.group(1))
            mem = ocpu * GB_PER_OCPU
            price = round(ocpu * r["ocpu"] + mem * r.get("mem", 0), 4)
            specs[size] = {"vcpu": ocpu * (1 if arch == "arm" else 2),
                           "mem": mem, "price": price}
            priced += 1
        else:
            specs[size] = {"vcpu": None, "mem": None, "price": None}
    fam["specs"] = specs

out = {
    "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "provider": "oci",
    "source": "Oracle Cloud public price list — no credentials",
    "currency": "USD",
    "priceRef": "us-ashburn-1",
    "regions": regions,
    "families": families,
}
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

n_types = sum(len(f["sizes"]) for f in families)
print(f"  ✓ {len(regions)} regions · {len(families)} shape families · "
      f"{n_types} configurations · {priced} priced (Flex shapes, @ {GB_PER_OCPU} GiB/OCPU)")
PYEOF

echo "✓ data.json refreshed — OCI Flex shape prices computed from the public price list"
