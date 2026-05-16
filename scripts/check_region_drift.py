#!/usr/bin/env python3
"""
Infra Atlas — region drift guard.

The `regions` instrument is hand-curated: no credential-free API exposes a clean
multi-cloud region atlas (see docs/data-policy.md and regions/refresh.sh). So its
`refresh.sh` and verify-data only confirm data.json was *copied* faithfully from
index.html — never that the region set is *correct*. That gap let a phantom
region (azure taiwannorth) and three misses (azure westcentralus, oci
af-casablanca-1, ovh Mumbai) ship silently — see tasks/features-2026-05/integrity.

This guard closes it: the region code set is pinned to a checked-in, dated
reference (regions/region-reference.json) verified against vendor docs. Any
accidental add / drop / rename now fails CI instead of shipping.

  check  (default):  python3 scripts/check_region_drift.py
      Compares regions/data.json against regions/region-reference.json.
      Exits 1 on any per-provider code-set mismatch.

  update:            python3 scripts/check_region_drift.py --update
      Rewrites region-reference.json from the current data.json. Run this ONLY
      after re-verifying the region data against the vendor source URLs — the
      new `verified` date asserts that verification happened.

A warning is emitted once the reference is older than STALE_DAYS so a periodic
re-verification gets prompted. No third-party deps; credential-free.
"""
import json
import os
import sys
import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "regions", "data.json")
REF = os.path.join(ROOT, "regions", "region-reference.json")
STALE_DAYS = 180

SOURCES = {
    "aws":   "https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html",
    "azure": "https://learn.microsoft.com/en-us/azure/reliability/regions-list",
    "gcp":   "https://cloud.google.com/about/locations",
    "oci":   "https://docs.oracle.com/en-us/iaas/Content/General/Concepts/regions.htm",
    "ovh":   "https://www.ovhcloud.com/en-ie/public-cloud/regions-availability/",
}


def site_codes():
    """Region code set per provider, read from the generated regions/data.json."""
    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)
    out = {}
    for city in data["cities"]:
        for r in city["regions"]:
            out.setdefault(r["p"], set()).add(r["code"])
    return {p: sorted(v) for p, v in out.items()}


def update():
    ref = {
        "_comment": ("Verified region code set per provider. Commercial / "
                     "standard-partition GA regions only — see docs/data-policy.md. "
                     "Regenerate with `python3 scripts/check_region_drift.py --update` "
                     "ONLY after re-verifying against the source URLs below."),
        "verified": datetime.date.today().isoformat(),
        "sources": SOURCES,
        "expected": site_codes(),
    }
    with open(REF, "w", encoding="utf-8") as f:
        json.dump(ref, f, indent=2, ensure_ascii=False)
        f.write("\n")
    total = sum(len(v) for v in ref["expected"].values())
    print(f"region-reference.json updated — verified {ref['verified']}, {total} regions")


def check():
    if not os.path.exists(REF):
        print("::error:: regions/region-reference.json missing — run with --update", file=sys.stderr)
        return 1
    with open(REF, encoding="utf-8") as f:
        ref = json.load(f)
    expected = {p: set(v) for p, v in ref["expected"].items()}
    actual = {p: set(v) for p, v in site_codes().items()}

    drift = False
    for p in sorted(set(expected) | set(actual)):
        dropped = sorted(expected.get(p, set()) - actual.get(p, set()))
        added = sorted(actual.get(p, set()) - expected.get(p, set()))
        if dropped or added:
            drift = True
            print(f"::error:: {p}: region set drifted from the verified reference")
            if dropped:
                print(f"   in reference but missing from data.json: {', '.join(dropped)}")
            if added:
                print(f"   in data.json but not in reference: {', '.join(added)}")
        else:
            print(f"  {p}: {len(actual.get(p, set()))} regions — matches reference")

    try:
        age = (datetime.date.today() - datetime.date.fromisoformat(ref["verified"])).days
        if age > STALE_DAYS:
            print(f"::warning:: region-reference.json last verified {age} days ago "
                  f"({ref['verified']}) — re-verify against vendor docs, then --update.")
        else:
            print(f"  reference last verified {age} days ago ({ref['verified']})")
    except (KeyError, ValueError):
        print("::warning:: region-reference.json has no valid 'verified' date")

    if drift:
        print("::error:: Region data drifted from the verified reference. If the change "
              "is intentional AND verified against the vendor docs, run "
              "`python3 scripts/check_region_drift.py --update` and commit the reference.")
        return 1
    print("OK — region data matches the verified reference.")
    return 0


if __name__ == "__main__":
    if "--update" in sys.argv:
        update()
    else:
        sys.exit(check())
