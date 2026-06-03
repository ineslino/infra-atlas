#!/usr/bin/env python3
"""
Infra Atlas — matrix-instrument chrome guard.

/assets/matrix.css ships ONLY the table (+ tokens + drawer). The page chrome —
masthead, counts, the read-this callout, filters, crosslinks, colophon — lives in
a per-page inline <style> block. Every matrix instrument carries its own.

The Data Layer Equivalence page shipped (#23) with NO inline <style> block at all,
so its entire chrome rendered unstyled: the title fell back to Times, the
"Providers / Features / Footnotes" counts ran together, the callout's "*" floated
loose, and the cloud filter silently did nothing (no .matrix.hide-* rules). The
expert panel (2026-06) flagged it.

This fails when a page that uses the chrome (class="masthead") and links matrix.css
does not also define `.masthead` in an inline <style> block — i.e. it would render
its chrome unstyled. Cheap structural guard; catches the whole-page-unstyled bug.

Run from repo root:  python3 scripts/check_matrix_chrome.py
No third-party deps; credential-free. Sibling of check_html_attrs.py.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".github"}


def html_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn == "index.html":
                yield os.path.join(dirpath, fn)


def style_blocks(html):
    return "\n".join(re.findall(r"<style\b[^>]*>(.*?)</style>", html, re.S | re.I))


def main():
    fails = 0
    checked = 0
    for path in sorted(html_files()):
        rel = os.path.relpath(path, ROOT)
        html = open(path, encoding="utf-8").read()

        links_matrix = "assets/matrix.css" in html
        uses_masthead = 'class="masthead"' in html
        if not (links_matrix and uses_masthead):
            continue  # not a matrix instrument page
        checked += 1

        css = style_blocks(html)
        # the chrome anchor: matrix.css never defines .masthead, so the page must
        defines_masthead = re.search(r"\.masthead\b", css) is not None
        if not defines_masthead:
            fails += 1
            print(f"::error file={rel}:: matrix page links matrix.css and uses "
                  f'class="masthead" but no inline <style> defines `.masthead` — its '
                  f"chrome (title/counts/callout/filters) will render unstyled. Add the "
                  f"page-chrome <style> block (see any sibling matrix page).")

        # Drawer structure: matrix.js drawer.open() writes into .drawer__head and
        # .drawer__body. data-layer shipped a single .drawer__inner instead, so
        # every cell click opened an EMPTY drawer (no note, no source link).
        if 'id="drawer"' in html:
            has_body = 'class="drawer__body"' in html
            has_head = 'class="drawer__head"' in html
            if not (has_body and has_head):
                fails += 1
                print(f"::error file={rel}:: page has a #drawer but is missing "
                      f"`.drawer__head`/`.drawer__body` — matrix.js writes the note + "
                      f"source link into those, so cells open an empty drawer. Use the "
                      f"two-div drawer markup (see any sibling matrix page).")

        if defines_masthead and ('id="drawer"' not in html or ('class="drawer__body"' in html and 'class="drawer__head"' in html)):
            print(f"  OK  {rel}")

    if not checked:
        print("::warning:: no matrix instrument pages found to check.")
    if fails:
        print(f"::error:: {fails} matrix page(s) missing their chrome <style> block.")
        return 1
    print(f"OK — all {checked} matrix instrument page(s) ship their chrome.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
