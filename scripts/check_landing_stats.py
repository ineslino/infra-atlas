#!/usr/bin/env python3
"""
Infra Atlas — landing-page stat guard.

Each data instrument's card on the landing page (index.html) hard-codes a stat
chip — "34 regions", "196 families", and so on. Those numbers were hand-typed
and drifted from the instruments' own data.json (see tasks/lessons.md L6: the
EC2 card said "32 regions / ~700 types" while the data held 34 / 1338).

This guard derives the counts from each data.json and fails if the matching
landing-card chip is missing — so the cards cannot silently go stale again.
When it fails, update the chip in index.html to the number it reports.

Run from repo root:  python3 scripts/check_landing_stats.py
No third-party deps; credential-free.
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDEX = os.path.join(ROOT, "index.html")

# instrument -> [(count key, chip-text template)]; the chip is "<span>TEXT</span>".
CHECKS = {
    "ec2":           [("regions", "{} regions"), ("families", "{} families")],
    "regions":       [("cities", "{} cities"), ("regions", "{} regions")],
    "azure-vm":      [("regions", "{} regions"), ("families", "{} series"),
                      ("sizes", "{} VM sizes")],
    "gcp-compute":   [("regions", "{} regions"), ("families", "{} families"),
                      ("sizes", "{} machine types")],
    "oci-compute":   [("regions", "{} regions"), ("families", "{} shape families")],
    "ovh-instances": [("regions", "{} regions"), ("families", "{} families"),
                      ("sizes", "{} instance types")],
}


def counts(data):
    """regions / cities / families / sizes for one instrument's data.json."""
    if "cities" in data:  # the regions instrument is city-modelled
        return {"cities": len(data["cities"]),
                "regions": sum(len(c["regions"]) for c in data["cities"])}
    fams = data.get("families", [])
    return {"regions": len(data.get("regions", [])),
            "families": len(fams),
            "sizes": sum(len(f.get("sizes", [])) for f in fams)}


def card_block(html, inst):
    """The landing card <a … href="./<inst>/"> … </a> for one instrument."""
    start = html.find(f'href="./{inst}/"')
    if start == -1:
        return None
    end = html.find("</a>", start)
    return html[start:end] if end != -1 else None


def main():
    with open(INDEX, encoding="utf-8") as f:
        html = f.read()

    fails = 0
    for inst, checks in CHECKS.items():
        with open(os.path.join(ROOT, inst, "data.json"), encoding="utf-8") as f:
            c = counts(json.load(f))
        block = card_block(html, inst)
        if block is None:
            print(f"::error file=index.html:: no landing card found for {inst}")
            fails += 1
            continue
        for key, tmpl in checks:
            text = tmpl.format(c[key])
            if f">{text}<" in block:               # the chip is <span>{text}</span>
                print(f"  {inst:14} \"{text}\" — matches data.json")
            else:
                fails += 1
                print(f"::error file=index.html:: {inst} card is stale — expected "
                      f"a \"{text}\" chip (from {inst}/data.json); not found.")

    if fails:
        print(f"::error:: {fails} landing-page stat(s) out of sync — update the "
              f"card chips in index.html to the numbers above.")
        return 1
    print("OK — every landing-page stat chip matches its instrument's data.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
