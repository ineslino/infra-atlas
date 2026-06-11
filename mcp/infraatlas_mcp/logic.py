"""Pure logic for infraatlas-mcp — no network, no MCP imports.

Everything here mirrors the site exactly and is pinned by tests/test_logic.py:
- catalogue flattening   → equivalent-sku/index.html's adapter
- equivalence scoring    → equivalent-sku/index.html (W 50/38/12, arch ×0.55)
- egress band parsing +
  tier-ladder walk       → tools/egress-cost/'s computeCost
"""

from __future__ import annotations

import math
import re
from typing import Any, Optional

# ─── Equivalence scoring constants — keep in lockstep with the site ───
W_VCPU, W_MEM, W_CAT = 50, 38, 12  # additive axis weights, sum = 100
ARCH_FACTOR = 0.55                 # multiplier when the architecture differs
CAT_ADJ = {
    "general": ["compute", "memory"],
    "compute": ["general", "hpc"],
    "memory": ["general"],
    "hpc": ["compute"],
    "storage": [],
    "accelerated": [],
    "macos": [],
    "baremetal": [],
    "confidential": ["general"],
}


# ─── Catalogue flattening ───
def _gcp_vcpu_from_name(name: str) -> Optional[int]:
    if re.match(r"^(e2-(micro|small|medium)|f1-micro|g1-small)$", name):
        return None  # shared-core: left unscored rather than guessed
    m = re.search(r"-(\d+)$", name)
    return int(m.group(1)) if m else None


def flatten_catalogue(cloud: str, data: dict) -> list[dict]:
    """families[] with sizes/specs → flat instance list with price/regions."""
    out: list[dict] = []
    total_regions = len(data.get("regions") or [])
    for fam in data.get("families") or []:
        fam_key = fam.get("key", "")
        cat = fam.get("cat") or "general"
        arch = fam.get("arch") or "x86"
        vendor = fam.get("vendor") or ""
        desc = fam.get("desc") or ""
        specs = fam.get("specs") or {}
        fam_in = fam.get("in")
        if fam_in == "*":
            regions, region_codes = total_regions, None
        elif isinstance(fam_in, list):
            regions, region_codes = len(fam_in), fam_in
        else:
            regions, region_codes = None, None
        for size in fam.get("sizes") or []:
            sp = specs.get(size) or {}
            if cloud == "aws":
                name = size if size.startswith(fam_key) else f"{fam_key}.{size}"
                vcpu = sp.get("vcpu")
            elif cloud == "gcp":
                name = size
                vcpu = _gcp_vcpu_from_name(size)
            elif cloud == "oci":
                name = f"{fam_key} · {size}" if re.search(r"OCPUs?$", size) else size
                vcpu = sp.get("vcpu")
            else:
                name = size
                vcpu = sp.get("vcpu")
            price = sp.get("price")
            out.append({
                "name": name,
                "family": fam_key,
                "category": cat,
                "arch": "arm64" if arch == "arm" else "x86_64",
                "_arch_raw": arch,
                "cpuVendor": vendor,
                "familyDescription": desc,
                "vcpu": vcpu,
                "memoryGiB": sp.get("mem"),
                "pricePerHour": price if isinstance(price, (int, float)) else None,
                "regions": regions,
                "_region_codes": region_codes,
            })
    return out


# ─── Equivalence scoring ───
def _ratio_score(src_val, cand_val) -> Optional[float]:
    """1 when identical, decays linearly in |log2(ratio)|, 0 at 2x apart."""
    if not src_val or not cand_val or src_val <= 0 or cand_val <= 0:
        return None
    return max(0.0, 1.0 - abs(math.log2(cand_val / src_val)))


def _category_score(src_cat: str, cand_cat: str) -> float:
    if src_cat == cand_cat:
        return 1.0
    if cand_cat in CAT_ADJ.get(src_cat, []):
        return 0.5
    return 0.0


def score_candidate(src: dict, cand: dict) -> dict:
    """Same math as the site: additive vCPU/memory/category axes renormalised
    over the axes that were actually scorable, then an architecture gate."""
    why: list[str] = []
    earned = available = 0.0

    v = _ratio_score(src["vcpu"], cand["vcpu"])
    if v is not None:
        earned += v * W_VCPU
        available += W_VCPU
        dv = (cand["vcpu"] or 0) - (src["vcpu"] or 0)
        why.append(f"vCPU {cand['vcpu']}" + (" (exact)" if dv == 0 else f" ({dv:+d})"))
    else:
        why.append("vCPU not scored")

    mem_scored = src["memoryGiB"] is not None and cand["memoryGiB"] is not None
    if mem_scored:
        m = _ratio_score(src["memoryGiB"], cand["memoryGiB"])
        if m is not None:
            earned += m * W_MEM
            available += W_MEM
        dm = cand["memoryGiB"] - src["memoryGiB"]
        why.append(f"memory {cand['memoryGiB']} GiB" + (" (exact)" if abs(dm) < 0.01 else f" ({dm:+g})"))
    else:
        why.append("memory not scored")  # axis dropped; weight renormalised away

    c = _category_score(src["category"], cand["category"])
    earned += c * W_CAT
    available += W_CAT
    why.append(
        f"category {cand['category']}"
        + ("" if c == 1.0 else " (adjacent)" if c == 0.5 else " (off)")
    )

    base = (earned / available) * 100 if available > 0 else 0.0
    arch_ok = src["_arch_raw"] == cand["_arch_raw"]
    if not arch_ok:
        why.append(f"arch differs → {cand['arch']} (×{ARCH_FACTOR})")
    return {
        "score": round(base * (1.0 if arch_ok else ARCH_FACTOR), 1),
        "memScored": mem_scored,
        "archMatch": arch_ok,
        "why": why,
    }


# ─── Egress band parsing + tier walk ───
_TB = 1024.0


_UNIT = r"(gb|tb|gib|tib)"


def _to_gb(value: float, unit: str) -> float:
    return value * (_TB if unit in ("tb", "tib") else 1)


def _band_upper_gb(band: str):
    """Cumulative upper bound in GB for one textual band, None for open-ended,
    or the string 'unparseable' when the wording is unknown.

    Wordings seen in egress/data.json: "First 100 GB / month",
    "Up to 10 TB / month", "0 – 1 TB / month", "0 to 1 TB / month",
    "Next 40 TB", "Beyond 150 TB", "10 TB and above".
    """
    b = band.strip().lower()
    m = re.match(rf"first\s+([\d.]+)\s*{_UNIT}", b)
    if m:
        return _to_gb(float(m.group(1)), m.group(2))
    m = re.match(rf"up to\s+([\d.]+)\s*{_UNIT}", b)
    if m:
        return _to_gb(float(m.group(1)), m.group(2))
    m = re.match(rf"[\d.]+\s*(?:[–-]|to)\s*([\d.]+)\s*{_UNIT}", b)
    if m:
        return _to_gb(float(m.group(1)), m.group(2))
    if re.match(rf"next\s+[\d.]+\s*{_UNIT}", b):
        return "relative"  # resolved against the previous bound by the caller
    if "beyond" in b or "and above" in b:
        return None
    return "unparseable"


def parse_tiers(tiers: list[dict]) -> Optional[list[dict]]:
    """[{band, usd}] → [{band, usd, upToGB}] cumulative, or None if unparseable."""
    out: list[dict] = []
    prev = 0.0
    for t in tiers:
        upper = _band_upper_gb(t.get("band", ""))
        if upper == "unparseable":
            return None
        if upper == "relative":
            m = re.match(rf"next\s+([\d.]+)\s*{_UNIT}", t["band"].strip().lower())
            width = _to_gb(float(m.group(1)), m.group(2))
            upper = prev + width
        out.append({"band": t["band"], "usd": t["usd"], "upToGB": upper})
        prev = upper if upper is not None else prev
    return out


def walk_ladder(ladder: list[dict], volume_gb: float) -> dict:
    """Same walk as /tools/egress-cost/: fill each tier in order."""
    remaining, prev, total = volume_gb, 0.0, 0.0
    breakdown = []
    for t in ladder:
        upper = t["upToGB"] if t["upToGB"] is not None else math.inf
        in_tier = min(remaining, upper - prev)
        if in_tier <= 0:
            break
        cost = in_tier * t["usd"]
        breakdown.append({
            "band": t["band"],
            "volumeGB": round(in_tier, 2),
            "usdPerGB": t["usd"],
            "cost": round(cost, 2),
        })
        total += cost
        remaining -= in_tier
        prev = upper
        if remaining <= 0:
            break
    return {"totalUSD": round(total, 2), "breakdown": breakdown}


def public_view(inst: dict) -> dict:
    """Strip private (underscore) keys from a flattened instance."""
    return {k: v for k, v in inst.items() if not k.startswith("_")}
