#!/usr/bin/env python3
"""
Infra Atlas — typographic-quote guard for HTML tags.

A smart quote (" " ' ') pasted into an attribute turns `class="x"` into
`class="x"` — a class the browser silently can't match. That is exactly how the
European Sovereignty card shipped with its metadata run together and its CTA
floating loose (the expert panel, 2026-06): three `class=”…”` typos that broke
.instrument__tags / __side / __cta with no error anywhere.

Straight quotes are mandatory as attribute delimiters; curly quotes are perfectly
fine in *text* (the site uses them deliberately in prose). So this only flags
typographic quotes that appear INSIDE a tag — between `<tag` and its closing `>`.

Run from repo root:  python3 scripts/check_html_attrs.py
No third-party deps; credential-free. Sibling of check_instrument_count.py.
"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SMART = {"“": '"', "”": '"', "‘": "'", "’": "'"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".github"}


def html_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


def scan(path):
    """Yield (line, col, char) for every smart quote found inside a tag."""
    text = open(path, encoding="utf-8").read()
    in_tag = False
    line = 1
    col = 0
    n = len(text)
    for i, ch in enumerate(text):
        col += 1
        if ch == "\n":
            line += 1
            col = 0
            continue
        if not in_tag:
            # a tag opens on '<' immediately followed by a name / close / decl
            if ch == "<" and i + 1 < n and (text[i + 1].isalpha() or text[i + 1] in "/!?"):
                in_tag = True
        else:
            if ch == ">":
                in_tag = False
            elif ch in SMART:
                yield line, col, ch


def main():
    total = 0
    for path in sorted(html_files()):
        rel = os.path.relpath(path, ROOT)
        for line, col, ch in scan(path):
            total += 1
            print(f"::error file={rel},line={line},col={col}:: typographic quote "
                  f"{ch!r} inside a tag — use a straight {SMART[ch]!r} "
                  f"(curly quotes silently break attributes like class/href).")
    if total:
        print(f"::error:: {total} typographic quote(s) inside HTML tags — replace "
              f"with straight quotes (the 'broken class' bug).")
        return 1
    print("OK — no typographic quotes inside any HTML tag.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
