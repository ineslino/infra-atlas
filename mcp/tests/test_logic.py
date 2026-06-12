#!/usr/bin/env python3
"""Offline tests for infraatlas-mcp — no network, plain python3, no pytest.

Pins the scoring math to the site's Equivalent-SKU Finder and the egress walk
to the Egress Cost Calculator, so a drift between the MCP server and the site
fails loudly here.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from infraatlas_mcp.logic import (  # noqa: E402
    flatten_catalogue,
    parse_tiers,
    score_candidate,
    walk_ladder,
)

FAILURES = []


def check(label, got, want):
    if got != want:
        FAILURES.append(f"{label}: got {got!r}, want {want!r}")
    else:
        print(f"  ok  {label}")


def inst(name="x", vcpu=4, mem=16.0, cat="general", arch="x86"):
    return {
        "name": name, "vcpu": vcpu, "memoryGiB": mem,
        "category": cat, "_arch_raw": arch, "arch": "arm64" if arch == "arm" else "x86_64",
    }


# ── scoring: identical specs → 100 ──
s = score_candidate(inst(), inst())
check("identical specs score 100", s["score"], 100.0)
check("identical specs arch match", s["archMatch"], True)

# ── scoring: cross-architecture perfect size match caps at 55 ──
s = score_candidate(inst(arch="x86"), inst(arch="arm"))
check("cross-arch perfect match caps at 55", s["score"], 55.0)

# ── scoring: memory axis dropped renormalises, does not punish ──
s = score_candidate(inst(), inst(mem=None))
check("memory dropped → renormalised 100", s["score"], 100.0)
check("memory dropped flagged", s["memScored"], False)

# ── scoring: a 2x vCPU gap zeroes the vCPU axis (one octave) ──
s = score_candidate(inst(vcpu=4), inst(vcpu=8, mem=16.0))
# vcpu axis 0/50, mem 38/38, cat 12/12 → 50/100
check("2x vCPU gap → 50", s["score"], 50.0)

# ── scoring: adjacent category earns half of the 12 points ──
s = score_candidate(inst(cat="general"), inst(cat="compute"))
check("adjacent category → 94", s["score"], 94.0)

# ── egress: the calculator's own vector — 10,240 GB internet egress on AWS ──
AWS_BANDS = [
    {"band": "First 100 GB / month", "usd": 0},
    {"band": "Up to 10 TB / month", "usd": 0.09},
    {"band": "Next 40 TB", "usd": 0.085},
    {"band": "Next 100 TB", "usd": 0.07},
    {"band": "Beyond 150 TB", "usd": 0.05},
]
ladder = parse_tiers(AWS_BANDS)
check("ladder bound 1 (100 GB)", ladder[0]["upToGB"], 100.0)
check("ladder bound 2 (10 TB)", ladder[1]["upToGB"], 10240.0)
check("ladder bound 3 (next 40 TB → 50 TB)", ladder[2]["upToGB"], 51200.0)
check("ladder open end", ladder[4]["upToGB"], None)

walk = walk_ladder(ladder, 10240)
# 100 GB free + 10,140 GB × $0.09 = $912.60 — the number the calculator shows
check("10,240 GB on AWS = $912.60", walk["totalUSD"], 912.60)

GCP_BANDS = [
    {"band": "0 – 1 TB / month", "usd": 0.12},
    {"band": "1 – 10 TB / month", "usd": 0.11},
    {"band": "10 TB and above", "usd": 0.08},
]
gl = parse_tiers(GCP_BANDS)
gw = walk_ladder(gl, 10240)
# 1,024×0.12 + 9,216×0.11 = 122.88 + 1013.76 = 1,136.64 — matches the page
check("10,240 GiB on GCP = $1,136.64", gw["totalUSD"], 1136.64)

# ── egress: the LIVE wording uses "0 to 1 TB", not a dash — same ladder.
#    (This regressed once: unparsed bands fell back to the $0.12 flat headline
#    and overcharged 10 TB by $92. Pin the wording the site actually ships.) ──
GCP_LIVE_BANDS = [
    {"band": "0 to 1 TB / month", "usd": 0.12},
    {"band": "1 to 10 TB / month", "usd": 0.11},
    {"band": "10 TB and above", "usd": 0.08},
]
glive = parse_tiers(GCP_LIVE_BANDS)
check("'0 to 1 TB' wording parses", glive is not None, True)
check("'to' ladder = dash ladder", walk_ladder(glive, 10240)["totalUSD"], 1136.64)

# ── egress: GiB/TiB unit variants parse as their 1024 multiples ──
gib = parse_tiers([{"band": "First 100 GiB / month", "usd": 0},
                   {"band": "Up to 10 TiB / month", "usd": 0.09}])
check("GiB band bound", gib[0]["upToGB"], 100.0)
check("TiB band bound", gib[1]["upToGB"], 10240.0)

check("unknown band wording → None", parse_tiers([{"band": "ask sales", "usd": 1}]), None)

# ── flattening: aws prefixing, gcp vcpu-from-name, region counts ──
aws_flat = flatten_catalogue("aws", {
    "regions": [{"code": "a"}, {"code": "b"}],
    "families": [{
        "key": "m5", "cat": "general", "arch": "x86", "vendor": "Intel",
        "desc": "", "sizes": ["large"], "specs": {"large": {"vcpu": 2, "mem": 8, "price": 0.096}},
        "in": ["a"],
    }],
})
check("aws name prefixed", aws_flat[0]["name"], "m5.large")
check("aws region count from list", aws_flat[0]["regions"], 1)
check("aws price carried", aws_flat[0]["pricePerHour"], 0.096)

gcp_flat = flatten_catalogue("gcp", {
    "regions": [{"code": "a"}],
    "families": [{
        "key": "n2", "cat": "general", "arch": "x86", "vendor": "Intel",
        "desc": "", "sizes": ["n2-standard-8", "e2-micro"], "in": "*",
    }],
})
check("gcp vcpu from name", gcp_flat[0]["vcpu"], 8)
check("gcp shared-core unscored", gcp_flat[1]["vcpu"], None)
check("gcp '*' region count", gcp_flat[0]["regions"], 1)

print()
if FAILURES:
    print(f"FAILED ({len(FAILURES)}):")
    for f in FAILURES:
        print("  ✗", f)
    sys.exit(1)
print("All offline tests passed.")
