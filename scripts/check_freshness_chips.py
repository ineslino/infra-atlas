#!/usr/bin/env python3
"""
Infra Atlas — landing-page freshness-chip guard.

Every instrument card on the landing page carries a freshness chip
(<span class="instrument__fresh" data-fresh="…">…</span>) so readers can see
the data-hygiene guarantee per instrument without opening it:

  - live-refreshed instruments      → data-fresh="daily"   · "Refreshed daily"
  - equivalent-sku (live data.json) → data-fresh="live"    · "Live data"
  - hand-curated datasets           → data-fresh="curated" · "Curated"
  - dated snapshots                 → data-fresh="<date>"  · "Verified <date>"
    where <date> is the FIRST <time datetime="…"> in the instrument's own
    index.html — re-verifying a snapshot (bumping its <time>) must also bump
    the landing chip, or this guard fails the build.

This is the same anti-drift pattern as check_landing_stats.py (lessons.md L6:
headline claims rot): the chip is hand-typed, so a guard derives the truth and
fails loudly when they diverge.

Run from repo root:  python3 scripts/check_freshness_chips.py
No third-party deps; credential-free.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDEX = os.path.join(ROOT, "index.html")

DAILY = ["ec2", "azure-vm", "oci-compute", "ovh-instances"]
LIVE = ["equivalent-sku"]
CURATED = ["regions", "gcp-compute"]
SNAPSHOT = [
    "apim-matrix", "aws-api-gateway", "apigee", "mulesoft", "self-hosted-apim",
    "kubernetes", "compliance", "sovereignty", "confidential-computing",
    "iam-matrix", "ai-atlas", "egress", "networking-matrix", "observability",
    "observability-stacks", "idp-matrix", "data-layer", "service-quotas",
]

CHIP_RE = re.compile(
    r'<span class="instrument__fresh" data-fresh="([^"]*)">([^<]*)</span>')
TIME_RE = re.compile(r'<time datetime="([0-9-]+)"')


def card_block(html, inst):
    """The landing instrument card — same matching rule as check_landing_stats."""
    needle = f'href="./{inst}/"'
    pos = 0
    while True:
        i = html.find(needle, pos)
        if i == -1:
            return None
        if 'class="instrument' in html[max(0, i - 80):i]:
            end = html.find("</a>", i)
            return html[i:end] if end != -1 else None
        pos = i + len(needle)


def page_date(inst):
    path = os.path.join(ROOT, inst, "index.html")
    with open(path, encoding="utf-8") as f:
        m = TIME_RE.search(f.read())
    return m.group(1) if m else None


def expected(inst):
    if inst in DAILY:
        return ("daily", "Refreshed daily")
    if inst in LIVE:
        return ("live", "Live data")
    if inst in CURATED:
        return ("curated", "Curated")
    d = page_date(inst)
    if d is None:
        return (None, None)
    return (d, f"Verified {d}")


def main():
    with open(INDEX, encoding="utf-8") as f:
        html = f.read()

    fails = 0
    for inst in DAILY + LIVE + CURATED + SNAPSHOT:
        block = card_block(html, inst)
        if block is None:
            print(f"::error file=index.html:: no landing card found for {inst}")
            fails += 1
            continue
        key, text = expected(inst)
        if key is None:
            print(f"::error file={inst}/index.html:: snapshot page has no "
                  f"<time datetime=…> stamp — add one (it feeds the landing chip).")
            fails += 1
            continue
        m = CHIP_RE.search(block)
        if not m:
            print(f"::error file=index.html:: {inst} card has no freshness chip "
                  f"— expected data-fresh=\"{key}\" · \"{text}\".")
            fails += 1
        elif m.group(1) != key or m.group(2) != text:
            print(f"::error file=index.html:: {inst} freshness chip is stale — "
                  f"has \"{m.group(2)}\" (data-fresh=\"{m.group(1)}\"), expected "
                  f"\"{text}\" (data-fresh=\"{key}\").")
            fails += 1
        else:
            print(f"  {inst:24} \"{text}\" — matches")

    if fails:
        print(f"::error:: {fails} freshness chip(s) out of sync — update the "
              f"instrument__fresh spans in index.html to the values above.")
        return 1
    print("OK — every landing-page freshness chip matches its instrument.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
