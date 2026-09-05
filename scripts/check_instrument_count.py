#!/usr/bin/env python3
"""
Infra Atlas — instrument-count guard.

The homepage reports how many instruments the site ships in three places: the
hero stat, the section header ("N Live"), and the filter chips (All / Tools /
Matrices / Guides). The hero stat + section header are ALSO recomputed by JS at
runtime, but crawlers, social scrapers and no-JS clients only ever see the
STATIC values — so the static numbers must match the real cards.

A drift here is the "21 vs 22" credibility bug the expert panel flagged (2026-06):
the site's own headline self-report contradicting the cards on the same page, on
a site whose whole pitch is "accurate, sourced". This derives the truth from the
`class="instrument is-live"` cards + their `.instrument__type` badges and fails
if any static count diverges.

Run from repo root:  python3 scripts/check_instrument_count.py
No third-party deps; credential-free. Sibling of check_landing_stats.py.
"""
import os
import re
import sys
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDEX = os.path.join(ROOT, "index.html")


def main():
    html = open(INDEX, encoding="utf-8").read()
    n = len(re.findall(r'class="instrument is-live"', html))
    badges = Counter(re.findall(r'class="instrument__type" data-type="([a-z]+)"', html))

    checks = []  # (label, found, expected)

    def grab(label, pattern, expected):
        m = re.search(pattern, html, re.S)
        checks.append((label, int(m.group(1)) if m else None, expected))

    grab("hero #stat-instruments", r'id="stat-instruments">(\d+)<', n)
    grab('section header "N Live"', r"<strong>(\d+)</strong> Live", n)
    grab("filter chip All", r'data-type="all"[^>]*>All <span class="ia-filter__count">(\d+)</span>', n)
    grab("filter chip Tools", r'data-type="tool"[^>]*>Tools <span class="ia-filter__count">(\d+)</span>', badges["tool"])
    grab("filter chip Matrices", r'data-type="matrix"[^>]*>Matrices <span class="ia-filter__count">(\d+)</span>', badges["matrix"])
    grab("filter chip Guides", r'data-type="guide"[^>]*>Guides <span class="ia-filter__count">(\d+)</span>', badges["guide"])

    # Page-index department counts — both the visible chip and the aria-label must
    # match the real cards in each department. The Cross-Cloud chip shipped "11"
    # while 12 cards lived under it (aria said 12, the chip said 11); the chip is
    # the STATIC value crawlers / no-JS clients see before any filter click.
    order = re.findall(r'class="department" id="([^"\s]+)"', html)
    assert order, "Homepage must expose subject groups"
    starts = [html.index('class="department" id="%s"' % d) for d in order]
    ends = starts[1:] + [html.index("</section>", starts[-1])]
    for d, a, b in zip(order, starts, ends):
        real = html[a:b].count('class="instrument is-live"')
        item = re.search(r'href="#%s".*?</a>' % re.escape(d), html, re.S)
        block = item.group(0) if item else ""
        m_chip = re.search(r'ia-pageindex__count[^>]*>(\d+)<', block)
        m_aria = re.search(r'aria-label="[^"]*?(\d+)\s+instruments?"', block)
        checks.append((f'page-index chip [{d}]', int(m_chip.group(1)) if m_chip else None, real))
        checks.append((f'page-index aria [{d}]', int(m_aria.group(1)) if m_aria else None, real))

    fails = 0
    print(f"is-live cards: {n}  (tool={badges['tool']}, matrix={badges['matrix']}, "
          f"guide={badges['guide']}; sum={sum(badges.values())})")
    for label, found, expected in checks:
        if found == expected:
            print(f"  OK  {label}: {found}")
        else:
            fails += 1
            print(f"::error file=index.html:: {label} is {found}, expected {expected} "
                  f"(from the live cards / type badges).")

    if sum(badges.values()) != n:
        fails += 1
        print(f"::error file=index.html:: type badges sum to {sum(badges.values())} "
              f"but there are {n} is-live cards.")

    if fails:
        print(f"::error:: {fails} instrument-count literal(s) out of sync — update "
              f"index.html to match the live cards (the '21 vs 22' drift).")
        return 1
    print("OK — every static instrument count matches the live cards.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
