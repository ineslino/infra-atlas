#!/usr/bin/env python3
"""Infra Atlas · backfill the "What Changed" feed from git history.

Replays scripts/diff_feed.py's diff() across the full commit history of every
instrument's data.json, so the feed launches with real, dated, sourced change
entries instead of empty. Re-running is safe and idempotent: it rebuilds
feed.json from history rather than appending.

The daily refresh (.github/workflows/refresh.yml) continues to prepend new
entries on top going forward — there is no overlap, because backfill's newest
entry comes from the latest existing refresh commit and the next live diff is
against a future commit.

Usage:  python3 scripts/backfill_feed.py [feed.json]
"""
import glob
import importlib.util
import json
import os
import subprocess
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CAP = 200          # mirror diff_feed.CAP — keep only the newest N entries
BURST = 4          # collapse same-day/instrument/kind bursts beyond this many

# Plural nouns for collapsed-burst summaries (initial dataset build-outs show up
# as big same-day bursts; one honest summary reads like news, 57 lines read like
# an import log).
NOUN = {
    "region-added": "new regions", "region-removed": "regions withdrawn",
    "family-added": "new families", "family-removed": "families withdrawn",
    "instance-added": "size groups expanded", "instance-removed": "size groups reduced",
    "price-change": "price changes",
}

# Reuse the tested diff engine verbatim (scripts/ is not a package).
spec = importlib.util.spec_from_file_location("diff_feed", os.path.join(HERE, "diff_feed.py"))
df = importlib.util.module_from_spec(spec)
spec.loader.exec_module(df)


def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args],
                          capture_output=True, text=True, check=True).stdout


def history(rel):
    """Commit SHAs that touched <rel>, oldest first."""
    out = git("log", "--reverse", "--format=%H", "--", rel).strip()
    return out.split("\n") if out else []


def blob(sha, rel):
    """Parse <rel> as it existed at <sha>, or None if missing/unparseable."""
    try:
        return json.loads(git("show", f"{sha}:{rel}"))
    except Exception:
        return None


def collapse_bursts(entries):
    """Fold same-(date, instrument, kind) bursts beyond BURST into one summary."""
    groups, order = defaultdict(list), []
    for e in entries:
        k = (e["ts"], e["instrument"], e["kind"])
        if k not in groups:
            order.append(k)
        groups[k].append(e)
    out = []
    for k in order:
        ts, inst, kind = k
        g = groups[k]
        if len(g) > BURST:
            # identifier = family key (before ":") for size events, else the last word
            def ident(t):
                return t.split(":")[0].strip() if ":" in t else t.split()[-1]
            samples = ", ".join(ident(e["text"]) for e in g[:3])
            noun = NOUN.get(kind, kind.replace("-", " "))
            out.append({"ts": ts, "instrument": inst, "kind": kind,
                        "text": f"{len(g)} {noun} ({samples}…)"})
        else:
            out.extend(g)
    return out


def main():
    feed_p = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "feed.json")
    entries = []

    for path in sorted(glob.glob(os.path.join(ROOT, "*", "data.json"))):
        inst = os.path.basename(os.path.dirname(path))
        rel = f"{inst}/data.json"
        shas = history(rel)
        if len(shas) < 2:
            print(f"  {inst}: {len(shas)} snapshot(s) — nothing to diff")
            continue

        prev = blob(shas[0], rel)
        added = 0
        for sha in shas[1:]:
            cur = blob(sha, rel)
            if cur is None:
                continue
            if prev is not None:
                try:
                    for (ts, i, kind, text) in df.diff(inst, prev, cur):
                        entries.append({"ts": ts, "instrument": i, "kind": kind, "text": text})
                        added += 1
                except Exception as e:
                    print(f"  !! {inst} @ {sha[:8]}: diff error ({e}) — skipped")
            prev = cur
        print(f"  {inst}: {len(shas)} snapshots -> {added} entries")

    entries = collapse_bursts(entries)
    # Newest first (stable within a date), capped.
    entries.sort(key=lambda e: e["ts"], reverse=True)
    entries = entries[:CAP]
    generated = entries[0]["ts"] if entries else ""

    with open(feed_p, "w", encoding="utf-8") as f:
        json.dump({"generated": generated, "entries": entries}, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"\nfeed.json <- {len(entries)} entries (generated {generated or '-'})")


if __name__ == "__main__":
    main()
