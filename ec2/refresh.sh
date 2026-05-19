#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# Infra Atlas · EC2 Observatory · data refresh
#
# CREDENTIAL-FREE. No AWS account, no IAM, no OIDC.
# Pulls the public ec2instances.info dataset (maintained by Vantage),
# which carries per-region availability for every EC2 instance type.
#
# Transfer is ~18 MB gzipped (curl --compressed). Transforms into
# Infra Atlas schema: { generated, currency, priceRef, regions[], families[] }.
# Each family carries specs[size] = { vcpu, mem, price, storage?, net?, gpu? }
# and a family-level clock — price is the on-demand Linux $/hr in the
# reference region (us-east-1); the hardware fields come from the upstream feed.
#
# Requirements: curl, python3.
# ─────────────────────────────────────────────────────────────────

set -euo pipefail
cd "$(dirname "$0")"

need() { command -v "$1" >/dev/null 2>&1 || { echo "✗ $1 not found." >&2; exit 1; }; }
need curl
need python3

SRC="https://instances.vantage.sh/instances.json"
TMP="$(mktemp -t ec2_raw.XXXXXX)"
trap 'rm -f "$TMP"' EXIT

echo "▸ Downloading EC2 dataset (ec2instances.info, gzip)…"
curl --compressed -fsSL "$SRC" -o "$TMP"
echo "  $(du -h "$TMP" | cut -f1) decompressed"

echo "▸ Transforming → data.json…"
python3 - "$TMP" <<'PYEOF'
import json, re, sys, datetime

with open(sys.argv[1], encoding='utf-8') as f:
    raw = json.load(f)

# ── Region metadata (Vantage gives codes; geography is static) ──
REGION_META = {
  "us-east-1":("N. Virginia","Americas","🇺🇸",2006), "us-east-2":("Ohio","Americas","🇺🇸",2016),
  "us-west-1":("N. California","Americas","🇺🇸",2009), "us-west-2":("Oregon","Americas","🇺🇸",2011),
  "ca-central-1":("Canada Central","Americas","🇨🇦",2016), "ca-west-1":("Calgary","Americas","🇨🇦",2023),
  "sa-east-1":("São Paulo","Americas","🇧🇷",2011), "mx-central-1":("Mexico Central","Americas","🇲🇽",2025),
  "eu-west-1":("Ireland","Europe","🇮🇪",2007), "eu-west-2":("London","Europe","🇬🇧",2016),
  "eu-west-3":("Paris","Europe","🇫🇷",2017), "eu-central-1":("Frankfurt","Europe","🇩🇪",2014),
  "eu-central-2":("Zurich","Europe","🇨🇭",2022), "eu-north-1":("Stockholm","Europe","🇸🇪",2018),
  "eu-south-1":("Milan","Europe","🇮🇹",2020), "eu-south-2":("Spain","Europe","🇪🇸",2022),
  "il-central-1":("Tel Aviv","Middle East","🇮🇱",2023), "af-south-1":("Cape Town","Africa","🇿🇦",2020),
  "me-south-1":("Bahrain","Middle East","🇧🇭",2019), "me-central-1":("UAE","Middle East","🇦🇪",2022),
  "ap-east-1":("Hong Kong","Asia Pacific","🇭🇰",2019), "ap-south-1":("Mumbai","Asia Pacific","🇮🇳",2016),
  "ap-south-2":("Hyderabad","Asia Pacific","🇮🇳",2022), "ap-northeast-1":("Tokyo","Asia Pacific","🇯🇵",2011),
  "ap-northeast-2":("Seoul","Asia Pacific","🇰🇷",2016), "ap-northeast-3":("Osaka","Asia Pacific","🇯🇵",2018),
  "ap-southeast-1":("Singapore","Asia Pacific","🇸🇬",2010), "ap-southeast-2":("Sydney","Asia Pacific","🇦🇺",2012),
  "ap-southeast-3":("Jakarta","Asia Pacific","🇮🇩",2021), "ap-southeast-4":("Melbourne","Asia Pacific","🇦🇺",2023),
  "ap-southeast-5":("Malaysia","Asia Pacific","🇲🇾",2024), "ap-southeast-6":("New Zealand","Asia Pacific","🇳🇿",2025),
  "ap-southeast-7":("Thailand","Asia Pacific","🇹🇭",2025), "ap-east-2":("Taipei","Asia Pacific","🇹🇼",2025),
}

# A proper AWS region is geo-direction-number (3 segments). Local Zones
# (us-east-1-atl-1) and Wavelength Zones (us-east-1-wl1-*) have more — exclude them.
REGION_RE = re.compile(r'^[a-z]{2}-[a-z]+-\d+$')
def is_region(code):
    return bool(REGION_RE.match(code)) and not code.startswith(("us-gov", "cn-"))

# Reference region for the headline on-demand price shown on instance rows.
REF = "us-east-1"

def category(vantage_family, key):
    if key.startswith("mac"):    return "macos"
    f = (vantage_family or "").lower()
    if "compute optimized" in f: return "compute"
    if "memory" in f:            return "memory"
    if "storage" in f:           return "storage"
    if any(k in f for k in ("gpu","acceler","fpga","asic","media","machine learning")): return "accelerated"
    if "hpc" in f or "high performance" in f: return "hpc"
    return "general"

def vendor(proc):
    p = (proc or "")
    if "Graviton" in p:
        m = re.search(r"Graviton(\d)", p)
        return f"Graviton{m.group(1)}" if m else "Graviton"
    if "AMD" in p:   return "AMD"
    if "Intel" in p: return "Intel"
    if "Apple" in p: return "Apple"
    return "AWS"

SIZE_RANK = {s:i for i,s in enumerate(
  ["nano","micro","small","medium","large","xlarge","2xlarge","3xlarge","4xlarge","6xlarge",
   "8xlarge","9xlarge","10xlarge","12xlarge","16xlarge","18xlarge","24xlarge","32xlarge",
   "48xlarge","56xlarge","112xlarge","metal"])}
def size_key(s):
    return (SIZE_RANK.get(s, 999), s)

def fmt_storage(s):
    """Local instance storage → display string, or None for EBS-only."""
    if not s:
        return None
    size, dev = s.get("size"), s.get("devices") or 1
    if size is None:
        return None
    unit = s.get("size_unit") or "GB"
    kind = "NVMe SSD" if s.get("nvme_ssd") else ("SSD" if s.get("ssd") else "HDD")
    return f"{size} {unit} {kind}" if dev == 1 else f"{dev} × {size} {unit} {kind}"

def fmt_gpu(inst):
    """Attached accelerators → display string, or None when there are none."""
    n = inst.get("GPU") or 0
    if not n:
        return None
    model = (inst.get("GPU_model") or "GPU").strip()
    mem = inst.get("GPU_memory") or 0
    base = f"{n} × {model}" if n > 1 else model
    return f"{base} · {mem} GB" if mem else base

# ── Collect regions actually offered (proper regions only) ──
region_set = set()
for inst in raw:
    for code in (inst.get("pricing") or {}).keys():
        if is_region(code):
            region_set.add(code)

regions = []
for code in sorted(region_set):
    meta = REGION_META.get(code)
    name, area, flag, since = meta if meta else (code, "Other", "🌐", "—")
    regions.append({"code":code, "name":name, "area":area, "flag":flag, "since":since})

# ── Group instance types into families ──
fams = {}
for inst in raw:
    it = inst.get("instance_type", "")
    if "." not in it:
        continue
    key, size = it.split(".", 1)
    pricing_regions = {c for c in (inst.get("pricing") or {}).keys() if is_region(c)}
    if not pricing_regions:
        continue
    arch_list = inst.get("arch") or []
    arch = "arm" if any("arm" in a for a in arch_list) else "x86"
    if key not in fams:
        fams[key] = {
            "key": key,
            "cat": category(inst.get("family"), key),
            "arch": arch,
            "vendor": vendor(inst.get("physical_processor")),
            "desc": " · ".join(x for x in [
                (inst.get("family") or "").strip(),
                (inst.get("physical_processor") or "").strip(),
            ] if x) or "EC2 instance family",
            "clock": (inst.get("clock_speed_ghz") or "").strip() or None,
            "sizes": set(),
            "specs": {},
            "in": set(),
        }
    fams[key]["sizes"].add(size)
    fams[key]["in"] |= pricing_regions

    # Per-instance-type spec: vCPU, memory (GiB), on-demand Linux $/hr at REF,
    # plus local storage, network performance and attached GPUs where present.
    od = (((inst.get("pricing") or {}).get(REF) or {}).get("linux") or {}).get("ondemand")
    try:
        price = round(float(od), 4)
    except (TypeError, ValueError):
        price = None
    spec = {"vcpu": inst.get("vCPU"), "mem": inst.get("memory"), "price": price}
    storage = fmt_storage(inst.get("storage"))
    if storage:
        spec["storage"] = storage
    net = (inst.get("network_performance") or "").strip()
    if net:
        spec["net"] = net
    gpu = fmt_gpu(inst)
    if gpu:
        spec["gpu"] = gpu
    fams[key]["specs"][size] = spec

# ── Authoritative per-region availability overrides ──
# The upstream dataset's per-region data (both its `pricing` and `regions`
# maps) is inaccurate for some newer/smaller regions — it over-claims
# availability and omits Trainium. ap-southeast-4 (Melbourne) is the worst
# case: ~59 families claimed vs AWS's 31, with trn1/trn2 missing entirely.
# The dataset is third-party (Vantage) and cannot be fixed here, so the
# membership for affected regions is pinned to the AWS regional doc:
#   https://docs.aws.amazon.com/ec2/latest/instancetypes/ec2-instance-regions.html
# Any family key listed here is set to exactly the named regions for that
# region; family keys absent from a region's set have it removed.
REGION_FAMILY_OVERRIDES = {
  # Asia Pacific (Melbourne) — verified against the AWS regional doc.
  "ap-southeast-4": {
    "m5","m5d","m6g","m6gd","m7g","m7i","m7i-flex","m8g","t3","t4g",
    "c5","c5d","c6g","c6in","c7i","c8g","c8gn",
    "r5","r5d","r6g","r7g","r7i","r8g","x2idn",
    "i3","i3en","i4i","i7i","i7ie",
    "trn1","trn2",
  },
}
for region_code, true_keys in REGION_FAMILY_OVERRIDES.items():
    for key, f in fams.items():
        if key in true_keys:
            f["in"].add(region_code)
        else:
            f["in"].discard(region_code)
    # Families AWS lists for the region but the upstream dataset omits
    # entirely (e.g. trn1/trn2 for Melbourne) cannot be added — they have
    # no spec/pricing rows. Surface them so the gap is visible.
    missing = sorted(true_keys - set(fams.keys()))
    if missing:
        print(f"  ::warning:: {region_code}: AWS lists families absent from "
              f"the upstream dataset (not added): {', '.join(missing)}")

families = []
for key in sorted(fams.keys()):
    f = fams[key]
    ordered_sizes = sorted(f["sizes"], key=size_key)
    families.append({
        "key": f["key"],
        "cat": f["cat"],
        "arch": f["arch"],
        "vendor": f["vendor"],
        "desc": f["desc"],
        "clock": f.get("clock"),
        "sizes": ordered_sizes,
        "specs": {s: f["specs"][s] for s in ordered_sizes if s in f["specs"]},
        "in": sorted(f["in"]),
    })

out = {
    "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "source": "ec2instances.info (Vantage) — public dataset, no credentials",
    "currency": "USD",
    "priceRef": REF,
    "regions": regions,
    "families": families,
}
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

unmapped = [r["code"] for r in regions if r["area"] == "Other"]
n_types = sum(len(f["sizes"]) for f in families)
priced = sum(1 for f in families for s in f["sizes"]
             if (f["specs"].get(s) or {}).get("price") is not None)
print(f"  ✓ {len(regions)} regions · {len(families)} families · "
      f"{n_types} instance types · {priced} priced (REF {REF})")
if unmapped:
    print(f"  ::warning:: regions without geo metadata (add to REGION_META): {', '.join(unmapped)}")
PYEOF

echo "✓ data.json refreshed — credential-free, from public dataset"
