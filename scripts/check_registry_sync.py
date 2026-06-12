#!/usr/bin/env python3
"""
Infra Atlas — registry-sync guard (nav.js vs README.md vs llms.txt).

nav.js is the canonical instrument/tool registry (it feeds the ⌘K palette,
the related strips and the constellation map). README.md and llms.txt are
hand-maintained mirrors of it — and they rot: the README sat at "Nineteen
instruments" while the site shipped 25, and llms.txt missed both the TCO
comparator and the Service Quotas matrix (lessons.md L6: headline claims rot;
this is the same failure on the repo's front door and on the file agents read).

This guard derives the registry from nav.js and fails when:
  1. an instrument path (CLOUD / APIM / XCLOUD groups) is missing from
     README.md's tables or from llms.txt;
  2. a calculator path (TOOLS group) is missing from llms.txt
     (the README does not list calculators — by design);
  3. README.md's "N instruments" headline differs from the registry count.

Run from repo root:  python3 scripts/check_registry_sync.py
No third-party deps; credential-free.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

fails = 0


def err(path, msg):
    global fails
    print(f"::error file={path}:: {msg}")
    fails += 1


def nav_group(src, name):
    """Parse one `var NAME = [...]` registry array from nav.js → list of paths."""
    m = re.search(rf"var {name} = \[(.*?)\n  \];", src, re.S)
    if m is None:
        return None
    return re.findall(r'\["(/[^"]+/)",', m.group(1))


def main():
    with open(os.path.join(ROOT, "nav.js"), encoding="utf-8") as f:
        nav = f.read()
    groups = {name: nav_group(nav, name) for name in ("CLOUD", "APIM", "XCLOUD", "TOOLS")}
    for name, paths in groups.items():
        if not paths:
            err("nav.js", f"could not parse the {name} registry array — "
                          f"update scripts/check_registry_sync.py if its shape changed.")
            return 1
    instruments = groups["CLOUD"] + groups["APIM"] + groups["XCLOUD"]
    tools = groups["TOOLS"]

    with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
        readme = f.read()
    with open(os.path.join(ROOT, "llms.txt"), encoding="utf-8") as f:
        llms = f.read()

    # 1) every instrument appears in both mirrors
    for path in instruments:
        slug = path.strip("/")
        if f"`{slug}/`" not in readme:
            err("README.md", f"instrument {path} is in nav.js but missing from "
                             f"the README tables — add its row.")
        else:
            print(f"  README   {slug:24} — listed")
        if f"https://infraatlas.dev{path}" not in llms:
            err("llms.txt", f"instrument {path} is in nav.js but missing from "
                            f"llms.txt — agents won't find it.")
        else:
            print(f"  llms.txt {slug:24} — listed")

    # 2) every calculator appears in llms.txt
    for path in tools:
        if f"https://infraatlas.dev{path}" not in llms:
            err("llms.txt", f"calculator {path} is in nav.js but missing from "
                            f"llms.txt — agents won't find it.")
        else:
            print(f"  llms.txt {path.strip('/'):24} — listed")

    # 3) the README's instrument count matches the registry
    m = re.search(r"^(\d+) instruments", readme, re.M)
    if not m:
        err("README.md", 'no "<N> instruments" headline found — keep the count '
                         "in digits so this guard can read it.")
    elif int(m.group(1)) != len(instruments):
        err("README.md", f"headline says {m.group(1)} instruments but nav.js "
                         f"registers {len(instruments)} — update the README.")
    else:
        print(f"  README   count {m.group(1):>18} — matches nav.js")

    if fails:
        print(f"::error:: {fails} registry-sync check(s) failed — see above.")
        return 1
    print("OK — README.md and llms.txt list everything nav.js registers.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
