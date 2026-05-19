#!/usr/bin/env python3
"""Infra Atlas · sitemap generator.

Walks the repo for every page (an index.html in the root, an instrument
folder, or a decisions sub-folder) and writes sitemap.xml. Run after adding
or removing a page:  python3 scripts/build_sitemap.py

No third-party deps; credential-free.
"""
import datetime
import glob
import os

BASE = "https://infraatlas.dev"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)

# Root page + one folder deep (instruments, decisions hub, api, support)
# + two folders deep (the individual decision pages).
paths = ["index.html"]
paths += sorted(glob.glob("*/index.html"))
paths += sorted(glob.glob("*/*/index.html"))

rows = []
for p in paths:
    folder = os.path.dirname(p)
    loc = BASE + "/" + (folder + "/" if folder else "")
    lastmod = datetime.date.fromtimestamp(os.path.getmtime(p)).isoformat()
    rows.append(f"  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod></url>")

doc = ('<?xml version="1.0" encoding="UTF-8"?>\n'
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
       + "\n".join(rows) + "\n</urlset>\n")

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(doc)

print(f"✓ sitemap.xml — {len(rows)} URLs")
for r in rows:
    print("  " + r.strip())
