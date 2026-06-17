#!/usr/bin/env python3
"""Tests for diff_feed.py.  Run:  python3 scripts/test_diff_feed.py

No framework — plain asserts. Covers each change kind, the price
threshold, the null→value guard, the many-changes summary, and the
fail-safe behaviour (missing/bad input must never crash or block)."""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("diff_feed", os.path.join(HERE, "diff_feed.py"))
df = importlib.util.module_from_spec(spec)
spec.loader.exec_module(df)


def data(regions, families):
    return {"generated": "2026-05-16T06:00:00Z", "regions": regions, "families": families}


def fam(key, sizes, prices=None, in_regions=None):
    prices = prices or {}
    specs = {s: {"vcpu": 2, "mem": 8, "price": prices.get(s)} for s in sizes}
    f = {"key": key, "sizes": sizes, "specs": specs}
    if in_regions is not None:
        f["in"] = in_regions
    return f


def reg(*codes):
    return [{"code": c} for c in codes]


passed = 0


def check(name, cond):
    global passed
    assert cond, f"FAIL: {name}"
    passed += 1
    print(f"  ok · {name}")


base = data(reg("a", "b"), [fam("m5", ["large", "xlarge"], {"large": 0.1, "xlarge": 0.2})])

# 1 · identical snapshots → no entries
check("identical → 0 changes", df.diff("ec2", base, base) == [])

# 2 · region added
e = df.diff("ec2", base, data(reg("a", "b", "c"), base["families"]))
check("region added → region-added", len(e) == 1 and e[0][2] == "region-added")

# 3 · family added
e = df.diff("ec2", base, data(base["regions"], base["families"] + [fam("c7g", ["large"])]))
check("family added → family-added", len(e) == 1 and e[0][2] == "family-added")

# 4 · size added
d4 = data(base["regions"], [fam("m5", ["large", "xlarge", "2xlarge"],
                                {"large": 0.1, "xlarge": 0.2})])
e = df.diff("ec2", base, d4)
check("size added → instance-added", len(e) == 1 and e[0][2] == "instance-added")

# 5 · price move beyond ±2%
d5 = data(base["regions"], [fam("m5", ["large", "xlarge"], {"large": 0.12, "xlarge": 0.2})])
e = df.diff("ec2", base, d5)
check("price +20% → price-change", len(e) == 1 and e[0][2] == "price-change")

# 6 · price move below ±2% ignored
d6 = data(base["regions"], [fam("m5", ["large", "xlarge"], {"large": 0.1005, "xlarge": 0.2})])
check("price +0.5% → ignored", df.diff("ec2", base, d6) == [])

# 7 · null → value is not a price change (first post-launch refresh stays quiet)
b7 = data(base["regions"], [fam("m5", ["large"], {})])
n7 = data(base["regions"], [fam("m5", ["large"], {"large": 0.1})])
check("null→price → not a change", df.diff("ec2", b7, n7) == [])

# 8 · many price changes collapse to one summary entry
big_o = data(base["regions"], [fam("m5", [f"s{i}" for i in range(20)],
                                   {f"s{i}": 1.0 for i in range(20)})])
big_n = data(base["regions"], [fam("m5", [f"s{i}" for i in range(20)],
                                   {f"s{i}": 2.0 for i in range(20)})])
e = df.diff("ec2", big_o, big_n)
check("20 price changes → 1 summary", len(e) == 1 and "price changes" in e[0][3])

# 8b · availability — a family becomes available in an EXISTING region
av_base = data(reg("a", "b", "c"), [fam("m5", ["large"], in_regions=["a", "b"])])
av_new = data(reg("a", "b", "c"), [fam("m5", ["large"], in_regions=["a", "b", "c"])])
e = df.diff("ec2", av_base, av_new)
check("availability gained → availability-added",
      len(e) == 1 and e[0][2] == "availability-added" and "now in c" in e[0][3])

# 8c · availability — a family drops a region
e = df.diff("ec2", av_new, av_base)
check("availability lost → availability-removed",
      len(e) == 1 and e[0][2] == "availability-removed" and "no longer in c" in e[0][3])

# 8d · a brand-new region is reported once (region-added), NOT also per-family
nr_base = data(reg("a", "b"), [fam("m5", ["large"], in_regions=["a", "b"])])
nr_new = data(reg("a", "b", "c"), [fam("m5", ["large"], in_regions=["a", "b", "c"])])
e = df.diff("ec2", nr_base, nr_new)
check("new region not double-reported as availability",
      len(e) == 1 and e[0][2] == "region-added")

# 8e · many families gaining regions collapse to one summary entry
many_o = data(reg("a", "b"),
              [fam(f"f{i}", ["large"], in_regions=["a"]) for i in range(10)])
many_n = data(reg("a", "b"),
              [fam(f"f{i}", ["large"], in_regions=["a", "b"]) for i in range(10)])
e = df.diff("ec2", many_o, many_n)
check("10 availability changes → 1 summary",
      len(e) == 1 and e[0][2] == "availability-added" and "families gained regions" in e[0][3])

# 9 · fail-safe — missing old file → exit 0, no feed written
with tempfile.TemporaryDirectory() as td:
    newp, feedp = os.path.join(td, "new.json"), os.path.join(td, "feed.json")
    json.dump(base, open(newp, "w"))
    r = subprocess.run([sys.executable, os.path.join(HERE, "diff_feed.py"),
                        "ec2", os.path.join(td, "missing.json"), newp, feedp])
    check("missing old → exit 0", r.returncode == 0)
    check("missing old → no feed written", not os.path.exists(feedp))

# 10 · fail-safe — unparseable new file → exit 0
with tempfile.TemporaryDirectory() as td:
    badp, feedp = os.path.join(td, "new.json"), os.path.join(td, "feed.json")
    open(badp, "w").write("{not json")
    r = subprocess.run([sys.executable, os.path.join(HERE, "diff_feed.py"),
                        "ec2", badp, badp, feedp])
    check("bad new file → exit 0", r.returncode == 0)

# 11 · end-to-end — feed.json written, entry shape correct
with tempfile.TemporaryDirectory() as td:
    oldp, newp, feedp = (os.path.join(td, n) for n in ("old.json", "new.json", "feed.json"))
    json.dump(base, open(oldp, "w"))
    json.dump(d5, open(newp, "w"))
    r = subprocess.run([sys.executable, os.path.join(HERE, "diff_feed.py"),
                        "ec2", oldp, newp, feedp])
    feed = json.load(open(feedp))
    check("end-to-end → feed written", r.returncode == 0 and len(feed["entries"]) == 1)
    check("end-to-end → entry shape",
          feed["entries"][0]["kind"] == "price-change"
          and feed["entries"][0]["instrument"] == "ec2"
          and feed["entries"][0]["ts"] == "2026-05-16")

# 12 · per-instrument feed — written beside the new data.json, filtered, shaped
with tempfile.TemporaryDirectory() as td:
    inst_dir = os.path.join(td, "ec2")
    os.makedirs(inst_dir)
    oldp, newp = os.path.join(td, "old.json"), os.path.join(inst_dir, "data.json")
    feedp = os.path.join(td, "feed.json")
    # the aggregate already carries another instrument's entry — it must NOT
    # leak into ec2's per-instrument feed
    json.dump({"entries": [{"ts": "2026-05-01", "instrument": "regions",
                            "kind": "region-added", "text": "x"}]}, open(feedp, "w"))
    json.dump(base, open(oldp, "w"))
    json.dump(d5, open(newp, "w"))
    r = subprocess.run([sys.executable, os.path.join(HERE, "diff_feed.py"),
                        "ec2", oldp, newp, feedp])
    instp = os.path.join(inst_dir, "feed.json")
    check("per-instrument feed written", r.returncode == 0 and os.path.exists(instp))
    inst_feed = json.load(open(instp))
    check("per-instrument feed filtered",
          inst_feed["instrument"] == "ec2"
          and len(inst_feed["entries"]) == 1
          and all(e["instrument"] == "ec2" for e in inst_feed["entries"]))
    agg = json.load(open(feedp))
    check("aggregate keeps both instruments", len(agg["entries"]) == 2)

print(f"\n{passed} checks passed — OK")
