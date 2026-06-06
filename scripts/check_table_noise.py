#!/usr/bin/env python3
"""
Infra Atlas — table-noise guard (readability pass, 2026-06).

Two table-readability invariants the readability audit hardened so they cannot
silently regress:

1. Level glyph must not be baked into a matrix cell's `value` text.
   The matrix engine already encodes the support level from the `level` field
   (matrix.js renders the ✓/◐/✗/≈ fallback, and matrix.css colours --part/--no).
   A few pages also prefixed the glyph into the value string, e.g.
   `value:"✓ EU parent"` — so the same bit was carried twice (glyph + colour /
   engine fallback) and ✓ was repeated down whole columns as visual noise. The
   canonical pages (networking, data-layer) never do this. This fails if any
   `value:` literal starts with a level glyph, so the level has ONE source.

2. Compute display names must dedupe the family-key prefix.
   The observatory builds an instance name from `fam.key` + `size`. When the
   size string already starts with the key (Azure `B`/`B1ls`, OVH `d2`/`d2-2`,
   OCI fixed shapes), a naive `${fam.key}.${size}` doubles the prefix and ships
   names like `B.B1ls` or `VM.Standard.x9.VM.Standard.x9.4`. OCI and OVH already
   guard against this with `size.indexOf(fam.key) === 0 ? size : ...`. This
   fails if a page uses the `${fam.key}.${size}` name expression WITHOUT that
   guard, so all observatory pages share one naming rule.

Run from repo root:  python3 scripts/check_table_noise.py
No third-party deps; credential-free. Sibling of check_matrix_chrome.py.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".github"}

LEVEL_GLYPHS = "✓◐✗≈"
# `value:` (optional spaces) then an opening quote then a level glyph.
GLYPH_IN_VALUE = re.compile(r"""value\s*:\s*["'][""" + LEVEL_GLYPHS + r"]")
# the `${fam.key}.${size}` name/id expression, and the dedupe guard.
KEYSIZE_EXPR = re.compile(r"\$\{fam\.key\}\.\$\{size\}")
DEDUPE_GUARD = re.compile(r"indexOf\(fam\.key\)")


def html_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


def check_glyph_in_value(path, lines):
    """Yield (line_no, text) for every `value:` that starts with a level glyph."""
    for i, line in enumerate(lines, 1):
        if GLYPH_IN_VALUE.search(line):
            yield i, line.strip()


def check_keysize_without_guard(path, text, lines):
    """Yield (line_no, text) for `${fam.key}.${size}` names lacking the guard."""
    if not KEYSIZE_EXPR.search(text):
        return
    if DEDUPE_GUARD.search(text):
        return  # page builds key.size but guards the prefix — fine
    for i, line in enumerate(lines, 1):
        if KEYSIZE_EXPR.search(line):
            yield i, line.strip()


def main():
    glyph_hits = 0
    name_hits = 0
    for path in sorted(html_files()):
        rel = os.path.relpath(path, ROOT)
        text = open(path, encoding="utf-8").read()
        lines = text.splitlines()
        for line_no, snippet in check_glyph_in_value(path, lines):
            glyph_hits += 1
            print(f"::error file={rel},line={line_no}:: level glyph baked into a "
                  f"matrix `value`: drop the glyph, let the`level` field carry "
                  f"it (avoids the doubled ✓/◐/✗ noise). [{snippet[:80]}]")
        for line_no, snippet in check_keysize_without_guard(path, text, lines):
            name_hits += 1
            print(f"::error file={rel},line={line_no}:: `${{fam.key}}.${{size}}` "
                  f"name without the dedupe guard, add"
                  f"`size.indexOf(fam.key) === 0 ? size : ...` like oci/ovh "
                  f"(else names double the prefix, e.g. B.B1ls). [{snippet[:80]}]")

    total = glyph_hits + name_hits
    if total:
        print(f"::error:: {glyph_hits} glyph-in-value + {name_hits} "
              f"unguarded-name issue(s) — see the table-readability pass.")
        return 1
    print("OK — no level glyphs baked into values, all compute names dedupe the "
          "family prefix.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
