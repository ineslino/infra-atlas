#!/usr/bin/env python3
"""
Infra Atlas — sovereignty freshness guard.

The European Sovereignty instrument tracks a fast-moving topic — EUCS adoption,
the Data Privacy Framework's fate, new sovereign-cloud regions, provider
ownership/jurisdiction changes. Its "Verified · <date>" stamp must not silently
rot. This fails when that date is older than the threshold, forcing a
re-verification pass against the primary sources.

When it fails: re-check the volatile cells/briefing against their cited primary
sources, update them, and bump the <time datetime> stamp in
sovereignty/index.html (then re-run this).

Run from repo root:  python3 scripts/check_sovereignty_freshness.py
No third-party deps; credential-free. Sibling of check_landing_stats.py.
"""
import datetime
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PAGE = os.path.join(ROOT, "sovereignty", "index.html")
MAX_AGE_DAYS = 183  # ~6 months — the topic moves fast enough to warrant a half-yearly pass


def main():
    with open(PAGE, encoding="utf-8") as f:
        # the masthead "Verified · <time datetime="YYYY-MM-DD">" is the only <time> stamp
        m = re.search(r'<time datetime="(\d{4}-\d{2}-\d{2})"', f.read())
    if not m:
        print("::error file=sovereignty/index.html:: could not find the 'Verified' <time datetime> stamp")
        return 1

    verified = datetime.date.fromisoformat(m.group(1))
    age = (datetime.date.today() - verified).days

    if age > MAX_AGE_DAYS:
        print(f"::error file=sovereignty/index.html:: European Sovereignty was last verified {age} days "
              f"ago ({verified}) — over the {MAX_AGE_DAYS}-day window. The topic moves fast (EUCS, DPF, "
              f"sovereign regions, provider ownership). Re-verify the cells + briefing against their "
              f"primary sources and bump the <time datetime> stamp.")
        return 1

    print(f"OK — European Sovereignty verified {age} days ago ({verified}); within the {MAX_AGE_DAYS}-day window.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
