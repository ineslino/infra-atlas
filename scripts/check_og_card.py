#!/usr/bin/env python3
"""
Infra Atlas — Open Graph card guard.

og.png (the social-share image) is a 1200x630 screenshot of _ogcard.html, which
hard-codes an "N instruments" chip. That number drifts when instruments are
added — the card shipped "16 instruments" long after the site had 21, so every
shared link previewed a stale figure.

This guard derives the live instrument count from index.html and fails if
_ogcard.html disagrees, so the social card can't go silently stale again.
When it fails, regenerate the card + image with:

    python3 scripts/build_og.py

Run from repo root:  python3 scripts/check_og_card.py
No third-party deps; credential-free. Mirrors scripts/check_landing_stats.py.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDEX = os.path.join(ROOT, "index.html")
CARD = os.path.join(ROOT, "_ogcard.html")


def live_instrument_count(html):
    # one <a class="instrument is-live" …> per shipped (live) instrument — the
    # same set the hero's "instruments shipping today" stat counts.
    return len(re.findall(r'class="instrument is-live"', html))


def main():
    with open(INDEX, encoding="utf-8") as f:
        live = live_instrument_count(f.read())
    with open(CARD, encoding="utf-8") as f:
        m = re.search(r"<b>(\d+)</b>&nbsp;instruments", f.read())

    if not m:
        print("::error file=_ogcard.html:: could not find the '<b>N</b> instruments' "
              "chip in the OG card — has the template changed?")
        return 1

    card = int(m.group(1))
    if card != live:
        print(f"::error file=_ogcard.html:: OG card says {card} instruments but the site "
              f"ships {live} (counted in index.html). The social preview is stale — "
              f"run: python3 scripts/build_og.py")
        return 1

    print(f"OK — OG card matches the site ({live} instruments).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
