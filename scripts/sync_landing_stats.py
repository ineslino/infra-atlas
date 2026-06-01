#!/usr/bin/env python3
"""
Infra Atlas — landing-stat auto-sync (the inverse of check_landing_stats.py).

The daily refresh changes an instrument's counts (a new region, a new instance
family), but the hand-typed homepage card chips don't follow. Because the bot's
refresh push doesn't trigger CI, that drift only surfaces — confusingly — on the
next *human* push, as a check_landing_stats failure on an unrelated commit.

This rewrites each chip in index.html from the instrument's data.json, so the
chips stay in lockstep with the data and the guard never trips on a stale chip
again. The daily refresh runs it right after pulling new data — same
self-healing pattern as build_og.py for the OG card.

It reuses CHECKS / counts / card_block from check_landing_stats, so the numbers
it writes are exactly the ones the guard validates — one source of truth.

Usage (from repo root):
    python3 scripts/sync_landing_stats.py            # sync every instrument
    python3 scripts/sync_landing_stats.py ec2        # sync just one
No third-party deps; credential-free.
"""
import json
import os
import re
import sys

from check_landing_stats import CHECKS, counts, card_block, INDEX, ROOT


def main(argv):
    only = argv[1] if len(argv) > 1 else None
    if only and only not in CHECKS:
        print(f"::error:: unknown instrument '{only}' — known: {', '.join(CHECKS)}")
        return 2

    with open(INDEX, encoding="utf-8") as f:
        html = f.read()

    changes, warnings = [], []
    for inst, checks in CHECKS.items():
        if only and inst != only:
            continue
        with open(os.path.join(ROOT, inst, "data.json"), encoding="utf-8") as f:
            c = counts(json.load(f))
        block = card_block(html, inst)
        if block is None:
            warnings.append(f"{inst}: no landing card found — skipped")
            continue
        new_block = block
        for key, tmpl in checks:
            prefix, suffix = tmpl.split("{}")          # all chips are "{} <unit>"
            want = tmpl.format(c[key])
            # the chip is <span>{prefix}{N}{suffix}</span> -> ">{prefix}N{suffix}<"
            pat = re.compile(">" + re.escape(prefix) + r"(\d+)" + re.escape(suffix) + "<")
            m = pat.search(new_block)
            if not m:
                warnings.append(f"{inst}: no \"{prefix}N{suffix}\" chip found — left as-is")
                continue
            if m.group(1) != str(c[key]):
                changes.append(f"{inst:14} \"{m.group(0)[1:-1]}\" -> \"{want}\"")
                new_block = new_block[:m.start()] + f">{want}<" + new_block[m.end():]
        if new_block != block:
            html = html.replace(block, new_block, 1)

    if changes:
        with open(INDEX, "w", encoding="utf-8") as f:
            f.write(html)
        print("Synced landing-page chips to data.json:")
        for ch in changes:
            print("  " + ch)
    else:
        print("OK — landing-page chips already match data.json; nothing to sync.")
    for w in warnings:
        print("  ! " + w)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
