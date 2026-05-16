#!/usr/bin/env python3
"""Infra Atlas · "What Changed" feed builder.

Diffs two data.json snapshots of one instrument and appends human-readable
change entries to a shared feed.json. Detects: regions added/removed,
families added/removed, instance sizes added/removed, and on-demand price
moves beyond ±2%.

FAIL-SAFE: any runtime error is swallowed and the script exits 0, so a bug
in the diff logic can never block the daily data-refresh commit. Only a
usage error (wrong arguments) exits non-zero.

Usage:  diff_feed.py <instrument> <old.json> <new.json> <feed.json>
"""
import json
import sys

CAP = 200            # keep only the newest N feed entries
PRICE_EPS = 0.02     # ignore on-demand price moves smaller than ±2%
PRICE_LIST_MAX = 6   # list price changes individually up to this many, else summarise


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def diff(inst, old, new):
    """Return a list of (ts, instrument, kind, text) change tuples."""
    ts = (new.get("generated") or "")[:10] or "—"
    entries = []

    # ── Regions ──
    def codes(d):
        return {r.get("code") for r in d.get("regions", []) if r.get("code")}
    o_reg, n_reg = codes(old), codes(new)
    for c in sorted(n_reg - o_reg):
        entries.append((ts, inst, "region-added", f"new region {c}"))
    for c in sorted(o_reg - n_reg):
        entries.append((ts, inst, "region-removed", f"region {c} withdrawn"))

    # ── Families ──
    def fams(d):
        return {f.get("key"): f for f in d.get("families", []) if f.get("key")}
    o_fam, n_fam = fams(old), fams(new)
    for k in sorted(n_fam.keys() - o_fam.keys()):
        entries.append((ts, inst, "family-added", f"new family {k}"))
    for k in sorted(o_fam.keys() - n_fam.keys()):
        entries.append((ts, inst, "family-removed", f"family {k} withdrawn"))

    # ── Sizes + prices, for families present in both snapshots ──
    price_changes = []
    for k in sorted(n_fam.keys() & o_fam.keys()):
        of, nf = o_fam[k], n_fam[k]
        o_sz, n_sz = set(of.get("sizes", [])), set(nf.get("sizes", []))
        added, removed = sorted(n_sz - o_sz), sorted(o_sz - n_sz)
        if added:
            shown = ", ".join(added[:4]) + ("…" if len(added) > 4 else "")
            entries.append((ts, inst, "instance-added",
                            f"{k}: {len(added)} new size{'' if len(added) == 1 else 's'} ({shown})"))
        if removed:
            entries.append((ts, inst, "instance-removed",
                            f"{k}: {len(removed)} size{'' if len(removed) == 1 else 's'} withdrawn"))
        o_specs = of.get("specs") or {}
        n_specs = nf.get("specs") or {}
        for s in sorted(o_sz & n_sz):
            op = (o_specs.get(s) or {}).get("price")
            npr = (n_specs.get(s) or {}).get("price")
            if isinstance(op, (int, float)) and isinstance(npr, (int, float)) and op > 0:
                if abs(npr - op) / op >= PRICE_EPS:
                    price_changes.append((k, s, op, npr))

    if len(price_changes) <= PRICE_LIST_MAX:
        for k, s, op, npr in price_changes:
            pct = round((npr - op) / op * 100)
            entries.append((ts, inst, "price-change",
                            f"{k}.{s}  {op:g} → {npr:g}  ({pct:+d}%)"))
    elif price_changes:
        ups = sum(1 for _, _, o, n in price_changes if n > o)
        entries.append((ts, inst, "price-change",
                        f"{len(price_changes)} price changes ({ups} up, "
                        f"{len(price_changes) - ups} down)"))
    return entries


def main():
    if len(sys.argv) != 5:
        sys.exit("usage: diff_feed.py <instrument> <old.json> <new.json> <feed.json>")
    inst, old_p, new_p, feed_p = sys.argv[1:]

    try:
        new = load(new_p)
    except Exception as e:
        print(f"::notice::diff_feed {inst}: new data unreadable ({e}) — skipped")
        return
    try:
        old = load(old_p)
    except Exception:
        print(f"::notice::diff_feed {inst}: no previous snapshot — nothing to diff")
        return

    changes = diff(inst, old, new)
    if not changes:
        print(f"::notice::diff_feed {inst}: no changes")
        return

    try:
        feed = load(feed_p)
        if not isinstance(feed.get("entries"), list):
            raise ValueError
    except Exception:
        feed = {"entries": []}

    fresh = [{"ts": t, "instrument": i, "kind": k, "text": x} for (t, i, k, x) in changes]
    feed["entries"] = (fresh + feed["entries"])[:CAP]
    feed["generated"] = new.get("generated", "")

    with open(feed_p, "w", encoding="utf-8") as f:
        json.dump(feed, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"::notice::diff_feed {inst}: +{len(fresh)} entr{'y' if len(fresh) == 1 else 'ies'}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:   # never block the data refresh on a diff bug
        print(f"::warning::diff_feed crashed ({e}) — feed left unchanged")
