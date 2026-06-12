#!/usr/bin/env python3
"""
Infra Atlas — calculator-mirror guard.

The Egress Cost Calculator and the Cross-Cloud TCO Comparator carry inline
copies of the egress tier ladders ("mirrors") so they work offline and render
instantly. Mirrors rot (lessons.md L5: shared data duplicated across files
diverged silently) — a "keep in sync" comment is a wish, not a guarantee.

This guard makes it a guarantee:

  1. It re-derives every ladder and flat rate from the canonical
     egress/data.json (parsing the same band wordings the site uses:
     "First 100 GB", "Up to 10 TB", "0 – 1 TB", "0 to 1 TB", "Next 40 TB",
     "Beyond 150 TB", "10 TB and above", GiB/TiB variants) and fails if a
     calculator's inline copy differs by a single tier bound or rate.
  2. It pins the "Verified" dates: the calculators' provenance blocks and
     colophons must carry the SAME date as the Egress Cost Map's own <time>
     stamp — re-verifying the map forces the mirrors to be re-checked too.
  3. It checks each calculator's provenance block agrees with its own
     colophon stamp (subnet, apim-limits), so the visible date can't drift
     from the page's source of truth.

Run from repo root:  python3 scripts/check_calculator_rates.py
No third-party deps; credential-free.
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TB = 1024.0

fails = 0


def err(path, msg):
    global fails
    print(f"::error file={path}:: {msg}")
    fails += 1


# ─── canonical: egress/data.json → ladders / flats ───
def band_upper_gb(band):
    """Cumulative upper bound in GB, None for open-ended, 'rel' for Next-N,
    or 'unparseable'."""
    b = band.strip().lower()
    unit = r"(gb|tb|gib|tib)"
    to_gb = lambda v, u: float(v) * (TB if u in ("tb", "tib") else 1)
    m = re.match(rf"first\s+([\d.]+)\s*{unit}", b)
    if m:
        return to_gb(m.group(1), m.group(2))
    m = re.match(rf"up to\s+([\d.]+)\s*{unit}", b)
    if m:
        return to_gb(m.group(1), m.group(2))
    m = re.match(rf"[\d.]+\s*(?:[–-]|to)\s*([\d.]+)\s*{unit}", b)
    if m:
        return to_gb(m.group(1), m.group(2))
    m = re.match(rf"next\s+([\d.]+)\s*{unit}", b)
    if m:
        return ("rel", to_gb(m.group(1), m.group(2)))
    if "beyond" in b or "and above" in b:
        return None
    return "unparseable"


def canonical_ladder(tiers):
    out, prev = [], 0.0
    for t in tiers:
        upper = band_upper_gb(t.get("band", ""))
        if upper == "unparseable":
            return None
        if isinstance(upper, tuple):  # ("rel", width)
            upper = prev + upper[1]
        out.append((upper, float(t["usd"])))
        prev = upper if upper is not None else prev
    return out


def canonical_flat(rate):
    h = rate.get("headline", "").strip()
    if h.lower() == "free":
        return 0.0
    m = re.match(r"\$([\d.]+)\s*/\s*(GB|GiB)", h)
    return float(m.group(1)) if m else None


# ─── inline mirrors: brace-balanced const extraction + entry scraping ───
def extract_const(src, name):
    i = src.find(f"const {name} = {{")
    if i == -1:
        return None
    start = src.find("{", i)
    depth, j = 0, start
    while j < len(src):
        if src[j] == "{":
            depth += 1
        elif src[j] == "}":
            depth -= 1
            if depth == 0:
                return src[start:j + 1]
        j += 1
    return None


def split_provider_chunks(section):
    """aws: {...}, azure: {...}, gcp: {...} → dict of provider → chunk text."""
    out = {}
    for m in re.finditer(r"\b(aws|azure|gcp)\s*:\s*\{", section):
        prov, start = m.group(1), m.end() - 1
        depth, j = 0, start
        while j < len(section):
            if section[j] == "{":
                depth += 1
            elif section[j] == "}":
                depth -= 1
                if depth == 0:
                    out[prov] = section[start:j + 1]
                    break
            j += 1
    return out


def mirror_entries(chunk):
    """A provider chunk → ('ladder', [(upToGB|None, usd)]) or ('flat', x)."""
    tiers = re.findall(r"upToGB:\s*(null|[\d.]+)\s*,\s*usd:\s*([\d.]+)", chunk)
    if tiers:
        return ("ladder", [(None if u == "null" else float(u), float(r)) for u, r in tiers])
    m = re.search(r"\bflat:\s*([\d.]+)", chunk)
    if m:
        return ("flat", float(m.group(1)))
    return (None, None)


def ladders_equal(a, b):
    if a is None or b is None or len(a) != len(b):
        return False
    for (ua, ra), (ub, rb) in zip(a, b):
        if (ua is None) != (ub is None):
            return False
        if ua is not None and abs(ua - ub) > 1e-6:
            return False
        if abs(ra - rb) > 1e-9:
            return False
    return True


def fmt_ladder(l):
    return "—" if l is None else " · ".join(
        f"≤{'∞' if u is None else int(u)}GB@{r}" for u, r in l)


def first_time(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        m = re.search(r'<time datetime="([0-9-]+)"', f.read())
    return m.group(1) if m else None


def prov_date(src):
    m = re.search(r'verified <span class="prov__fresh">([0-9-]+)</span>', src)
    return m.group(1) if m else None


def main():
    with open(os.path.join(ROOT, "egress", "data.json"), encoding="utf-8") as f:
        data = json.load(f)
    canon = {}
    for t in data.get("transfers", []):
        for prov, rate in (t.get("rates") or {}).items():
            if rate.get("tiers"):
                canon[(t["id"], prov)] = ("ladder", canonical_ladder(rate["tiers"]))
            else:
                flat = canonical_flat(rate)
                if flat is not None:
                    canon[(t["id"], prov)] = ("flat", flat)

    # 1) egress-cost — every transfer × provider in the inline RATES
    path = "tools/egress-cost/index.html"
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        src = f.read()
    rates_block = extract_const(src, "RATES")
    if rates_block is None:
        err(path, "could not find the inline `const RATES = {…}` block.")
    else:
        for m in re.finditer(r'"([a-z-]+)":\s*\{', rates_block):
            tid, start = m.group(1), m.end() - 1
            depth, j = 0, start
            while j < len(rates_block):
                if rates_block[j] == "{":
                    depth += 1
                elif rates_block[j] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            section = rates_block[start:j + 1]
            for prov, chunk in split_provider_chunks(section).items():
                kind, val = mirror_entries(chunk)
                ck = canon.get((tid, prov))
                if ck is None:
                    err(path, f"{tid}/{prov}: present in the calculator but not in egress/data.json.")
                    continue
                ckind, cval = ck
                if kind == "ladder" and ckind == "ladder":
                    if not ladders_equal(val, cval):
                        err(path, f"{tid}/{prov} ladder drifted — calculator [{fmt_ladder(val)}] vs canonical [{fmt_ladder(cval)}]. Update the inline RATES.")
                    else:
                        print(f"  egress-cost  {tid}/{prov:6} ladder — matches")
                elif kind == "flat" and ckind == "flat":
                    if abs(val - cval) > 1e-9:
                        err(path, f"{tid}/{prov} flat rate drifted — calculator {val} vs canonical {cval}.")
                    else:
                        print(f"  egress-cost  {tid}/{prov:6} flat   — matches")
                else:
                    err(path, f"{tid}/{prov}: shape mismatch — calculator has {kind}, canonical has {ckind}.")

    # 2) tco — internet-egress mirror
    path = "tools/tco/index.html"
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        tco = f.read()
    egress_block = extract_const(tco, "EGRESS")
    if egress_block is None:
        err(path, "could not find the inline `const EGRESS = {…}` block.")
    else:
        # EGRESS uses `aws: [ … ]` arrays (no band labels), not objects
        for m in re.finditer(r"\b(aws|azure|gcp)\s*:\s*\[(.*?)\]", egress_block, re.S):
            prov, chunk = m.group(1), m.group(2)
            kind, val = mirror_entries(chunk)
            ckind, cval = canon.get(("internet-egress", prov), (None, None))
            if kind != "ladder" or ckind != "ladder":
                err(path, f"internet-egress/{prov}: expected ladders on both sides (got {kind} vs {ckind}).")
            elif not ladders_equal(val, cval):
                err(path, f"internet-egress/{prov} ladder drifted — calculator [{fmt_ladder(val)}] vs canonical [{fmt_ladder(cval)}]. Update the inline EGRESS.")
            else:
                print(f"  tco          internet-egress/{prov:6} — matches")

    # 3) verified-date pins
    map_date = first_time("egress/index.html")
    if not map_date:
        err("egress/index.html", "no <time datetime> stamp found on the Egress Cost Map.")
    else:
        ec_colophon = first_time("tools/egress-cost/index.html")
        if ec_colophon != map_date:
            err("tools/egress-cost/index.html",
                f"colophon Verified stamp {ec_colophon} ≠ Egress Cost Map {map_date} — re-check the mirror and bump the stamp.")
        ec_prov = prov_date(src)
        if ec_prov != map_date:
            err("tools/egress-cost/index.html",
                f"provenance block says verified {ec_prov} ≠ Egress Cost Map {map_date}.")
        m = re.search(r'EGRESS_VERIFIED = "([0-9-]+)"', tco)
        if not m or m.group(1) != map_date:
            err("tools/tco/index.html",
                f"EGRESS_VERIFIED {(m.group(1) if m else 'missing')} ≠ Egress Cost Map {map_date} — re-check the mirror and bump the constant.")
        if fails == 0:
            print(f"  verified stamps — all match the Egress Cost Map ({map_date})")

    # 4) each calculator's provenance date agrees with its own colophon
    for page in ("tools/subnet/index.html", "tools/apim-limits/index.html"):
        with open(os.path.join(ROOT, page), encoding="utf-8") as f:
            psrc = f.read()
        pd, cd = prov_date(psrc), first_time(page)
        if pd and cd and pd != cd:
            err(page, f"provenance block says verified {pd} but the colophon stamp is {cd}.")
        else:
            print(f"  {page.split('/')[1]:12} provenance date — agrees with colophon")

    if fails:
        print(f"::error:: {fails} calculator provenance/rate check(s) failed — see above.")
        return 1
    print("OK — every calculator mirror matches the canonical data and every visible date is pinned.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
