#!/usr/bin/env python3
"""Infra Atlas · search-index builder.

Builds a small static `search-index.json` consumed by the ⌘K palette in
`nav.js`. It is loaded lazily on first palette open, so visitors who never
hit ⌘K do not pay its cost. Every entry is `{href, term}` — the palette
already knows each instrument's display name from `nav.js`'s ITEMS list, so
we keep entries tiny.

What gets indexed (kept compact on purpose — names and short labels, NOT
the long per-cell `note` strings which would blow up the bundle):
  · Matrix instruments — VENDORS / PROVIDERS / CATEGORIES / GROUPS /
    FEATURES / TRANSFERS — `name`, `short`, `label`, `desc`, `sub` fields.
  · Compute instruments — region codes/names + family keys/names +
    full instance-type names (family.size, e.g. "m5.xlarge") from data.json.
  · The Region Map — city names + per-city region codes/names.
  · Decision pages — the per-page `<h1>` title and `<p class="subtitle">`.
  · Toolbox pages — tool names scraped from .tbx-row__name spans.

Re-run after editing matrix data or after a data refresh:
    python3 scripts/build_search_index.py

No third-party deps; credential-free.
"""
import glob
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)

MATRIX = [
    "kubernetes", "iam-matrix", "apim-matrix", "compliance",
    "confidential-computing", "ai-atlas", "networking-matrix", "egress",
]
COMPUTE = ["ec2", "azure-vm", "gcp-compute", "oci-compute", "ovh-instances"]
TOOLBOX = [
    ("toolbox/kubernetes",    "/toolbox/kubernetes/"),
    ("toolbox/networking",    "/toolbox/networking/"),
    ("toolbox/shell",         "/toolbox/shell/"),
    ("toolbox/auth",          "/toolbox/auth/"),
    ("toolbox/iac",           "/toolbox/iac/"),
    ("toolbox/security",      "/toolbox/security/"),
    ("toolbox/observability", "/toolbox/observability/"),
    ("toolbox/finops",        "/toolbox/finops/"),
    ("toolbox/cicd",          "/toolbox/cicd/"),
    ("toolbox/database",      "/toolbox/database/"),
    ("toolbox/api",           "/toolbox/api/"),
    ("toolbox/containers",    "/toolbox/containers/"),
    ("toolbox/localdev",      "/toolbox/localdev/"),
    ("toolbox/git",           "/toolbox/git/"),
]

# Keys whose string values get indexed. `value` catches the per-cell vendor
# terms ("VPC peering", "Direct Connect", "Cloud NAT") that people actually
# search for. `note` is excluded — it would balloon the index for marginal
# gain.
KEYS = ("name", "short", "label", "desc", "sub", "value", "headline")

# Top-level matrix-engine consts that hold rows / categories / vendors.
CONSTS = ("VENDORS", "PROVIDERS", "CATEGORIES", "GROUPS", "FEATURES", "TRANSFERS")

entries = []


def extract_const(html, name):
    """Return the bracketed body of `const NAME = [ ... ];`, or None."""
    m = re.search(
        rf"^(?:const|let|var) {name} = (\[.*?\n\]);",
        html, re.DOTALL | re.MULTILINE,
    )
    return m.group(1) if m else None


def strings_for_key(block, key):
    """Yield every double-quoted string value bound to `key:` in the block."""
    pattern = rf'\b{key}\s*:\s*"((?:[^"\\]|\\.)*)"'
    for raw in re.findall(pattern, block):
        # Unescape a couple of common sequences for cleaner display.
        s = raw.replace(r"\"", '"').replace(r"\\", "\\").strip()
        if s:
            yield s


def push(href, term):
    entries.append({"href": href, "term": term})


# ── Matrix instruments ────────────────────────────────────────────────
for slug in MATRIX:
    path = f"{slug}/index.html"
    if not os.path.exists(path):
        continue
    html = open(path, encoding="utf-8").read()
    for cn in CONSTS:
        block = extract_const(html, cn)
        if not block:
            continue
        for key in KEYS:
            for s in strings_for_key(block, key):
                push(f"/{slug}/", s)

# ── Compute instruments — top-level regions[] + families[] from data.json
for slug in COMPUTE:
    p = f"{slug}/data.json"
    if not os.path.exists(p):
        continue
    data = json.load(open(p, encoding="utf-8"))
    for r in data.get("regions", []):
        for k in ("code", "name"):
            v = r.get(k)
            if v:
                push(f"/{slug}/", str(v))
    for f in data.get("families", []):
        for k in ("key", "name"):
            v = f.get(k)
            if v:
                push(f"/{slug}/", str(v))
        # Full instance-type names (e.g. "m5.xlarge") so palette matches
        # specific SKUs like "c7g.16xlarge" or "Standard_D4s_v5".
        fkey = f.get("key", "")
        if fkey:
            for size in f.get("sizes", []):
                push(f"/{slug}/", f"{fkey}.{size}")

# ── Regions instrument — city-modelled
data = json.load(open("regions/data.json", encoding="utf-8"))
for city in data.get("cities", []):
    if city.get("city"):
        push("/regions/", city["city"])
    for r in city.get("regions", []):
        for k in ("code", "name"):
            v = r.get(k)
            if v:
                push("/regions/", str(v))

# ── Decision pages — title + subtitle from each generated page
for path in sorted(glob.glob("decisions/*/index.html")):
    html = open(path, encoding="utf-8").read()
    href = "/" + path.rsplit("/", 1)[0] + "/"
    for pattern in (
        r'<h1 class="title">(.*?)</h1>',
        r'<p class="subtitle">(.*?)</p>',
    ):
        m = re.search(pattern, html, re.DOTALL)
        if not m:
            continue
        txt = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        # Decode the few HTML entities the generator can emit.
        txt = txt.replace("&amp;", "&").replace("&rsquo;", "’").replace("&ldquo;", "“").replace("&rdquo;", "”")
        if txt:
            push(href, txt)

# ── Toolbox pages — tool names from .tbx-row__name spans
for slug, href in TOOLBOX:
    path = f"{slug}/index.html"
    if not os.path.exists(path):
        continue
    html = open(path, encoding="utf-8").read()
    for m in re.finditer(r'class="tbx-row__name"[^>]*>([^<]+)<', html):
        name = m.group(1).strip()
        if name:
            push(href, name)

# ── Dedupe (same href + same lower-cased term)
seen = set()
out = []
for e in entries:
    k = (e["href"], e["term"].lower())
    if k in seen:
        continue
    seen.add(k)
    out.append(e)

# Deliberately no `generated` field — Cloudflare's Last-Modified header
# handles freshness, and a timestamp here would create spurious diffs every
# refresh-run when the entries themselves are unchanged.
doc = {"entries": out}
with open("search-index.json", "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, separators=(",", ":"))

# Tiny summary, broken down by source — helps spot drift on re-run.
by_href = {}
for e in out:
    by_href[e["href"]] = by_href.get(e["href"], 0) + 1
print(f"✓ search-index.json — {len(out)} unique terms across {len(by_href)} pages")
for href, n in sorted(by_href.items()):
    print(f"  {n:4}  {href}")
