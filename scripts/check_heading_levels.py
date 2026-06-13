#!/usr/bin/env python3
"""
Infra Atlas — heading-level guard.

The instrument and calculator pages share a template whose colophon used
<h5> for its column headings (About / Sources / Shortcuts). With the masthead
title at <h1> and no <h2>-<h4> in the static DOM (the only h2/h4 live inside
the JS-built drawer, hidden on load), a screen-reader user browsing by heading
jumped h1 -> h5 — a skipped-level defect a UI/UX audit flagged across ~26
pages (2026-06-13). The fix promoted colophon headings to <h2>.

This guard keeps it fixed: a <footer class="colophon"> must not contain an
<h5> (its column heads belong at <h2>, one clean step below the page <h1>).
Cloning a new instrument from an old template can't silently reintroduce the
skip without failing the build.

Run from repo root:  python3 scripts/check_heading_levels.py
No third-party deps; credential-free.
"""
import glob
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)

FOOTER_RE = re.compile(r'<footer class="colophon">(.*?)</footer>', re.S)


def main():
    fails = 0
    checked = 0
    for path in sorted(glob.glob("*/index.html") + ["index.html"]):
        with open(path, encoding="utf-8") as f:
            html = f.read()
        for m in FOOTER_RE.finditer(html):
            checked += 1
            if "<h5" in m.group(1):
                print(f"::error file={path}:: colophon footer uses <h5> — its "
                      f"column headings must be <h2> (the page jumps h1→h5 for "
                      f"screen-reader heading navigation otherwise).")
                fails += 1
            else:
                print(f"  {path:34} colophon headings — h2, no skip")

    if fails:
        print(f"::error:: {fails} colophon(s) with a skipped heading level — "
              f"promote the <h5> column heads to <h2>.")
        return 1
    print(f"OK — {checked} colophon(s) keep a clean h1→h2 heading order.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
