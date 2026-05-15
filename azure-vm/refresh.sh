#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# Infra Atlas · Azure VM Atlas · data refresh
#
# CREDENTIAL-FREE. Pulls the Azure Retail Prices API
# (prices.azure.com/api/retail/prices) — no account, no token, no OIDC.
#
# Per VM size:
#  · price — live, on-demand Linux $/hr in the reference region,
#            from the Retail Prices API (Consumption, non-Spot).
#  · vCPU  — derived from the SKU name (the integer is the vCPU count;
#            constrained HB/HX sizes use the "-Nrs" segment).
#  · mem   — derived from the documented per-series GiB-per-vCPU ratio
#            for the regular D/E/L/F series; left null for the
#            irregular M / GPU (N*) / HPC (H*) / confidential (*C*)
#            series, where memory does not follow a flat ratio.
#
# Schema: { generated, provider, currency, priceRef, regions[], families[] }
# Each family: specs[size] = { vcpu, mem, price }.
#
# Requirements: python3.
# ─────────────────────────────────────────────────────────────────

set -euo pipefail
cd "$(dirname "$0")"

need() { command -v "$1" >/dev/null 2>&1 || { echo "✗ $1 not found." >&2; exit 1; }; }
need python3

echo "▸ Fetching Azure Retail Prices + regenerating data.json…"
python3 - <<'PYEOF'
import re, json, sys, datetime, urllib.request, urllib.parse

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

# ── Fetch the Azure Retail Prices API (paginated) ──
REF = "westeurope"
flt = (f"serviceName eq 'Virtual Machines' and armRegionName eq '{REF}' "
       f"and priceType eq 'Consumption'")
url = "https://prices.azure.com/api/retail/prices?$filter=" + urllib.parse.quote(flt)

prices = {}   # armSkuName -> lowest retailPrice (base Linux, non-Spot)
pages = 0
while url:
    req = urllib.request.Request(url, headers={"User-Agent": "infra-atlas-refresh"})
    with urllib.request.urlopen(req, timeout=60) as r:
        doc = json.load(r)
    for it in doc.get("Items", []):
        if "Windows" in (it.get("productName") or ""):
            continue
        sku = it.get("skuName") or ""
        if "Spot" in sku or "Low Priority" in sku:
            continue
        arm, rp = it.get("armSkuName"), it.get("retailPrice")
        if not arm or rp is None:
            continue
        if arm not in prices or rp < prices[arm]:
            prices[arm] = rp
    url = doc.get("NextPageLink")
    pages += 1
print(f"  · {len(prices)} VM SKUs priced over {pages} API page(s)")

# ── Derive vCPU / memory from the SKU name ──
def vcpu_of(name):
    m = re.match(r'^H[BX](\d+)(?:-(\d+))?', name)   # HPC: "HB120-16rs_v2" -> 16
    if m:
        return int(m.group(2)) if m.group(2) else int(m.group(1))
    m = re.match(r'^[A-Za-z]+(\d+)', name)
    return int(m.group(1)) if m else None

def mem_of(name, vcpu):
    # Documented GiB-per-vCPU ratios for the regular series; the
    # irregular series (B, M, N*, H*, *C confidential) are left null.
    if vcpu is None:
        return None
    if name.startswith(("DC", "EC")):
        return None
    if name.startswith("D"):
        return vcpu * 4
    if name.startswith("E"):
        return 672 if vcpu in (96, 104) else vcpu * 8   # E96/E104 cap at 672
    if name.startswith("L"):
        return vcpu * 8
    if name.startswith("FX"):
        return vcpu * 21
    if name.startswith("F"):
        return vcpu * 2
    return None   # B, M, NV, NC, ND, HB, HX

priced = 0
for fam in families:
    specs = {}
    for size in fam.get("sizes", []):
        v = vcpu_of(size)
        p = prices.get("Standard_" + size)
        if p is not None:
            p = round(p, 5)
            priced += 1
        specs[size] = {"vcpu": v, "mem": mem_of(size, v), "price": p}
    fam["specs"] = specs

out = {
    "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "provider": "azure",
    "source": "Azure Retail Prices API — public, no credentials",
    "currency": "USD",
    "priceRef": REF,
    "regions": regions,
    "families": families,
}
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

n_types = sum(len(f["sizes"]) for f in families)
print(f"  ✓ {len(regions)} regions · {len(families)} series · "
      f"{n_types} VM sizes · {priced} priced (REF {REF})")
PYEOF

echo "✓ data.json refreshed — Azure VM prices live from the Retail Prices API"
