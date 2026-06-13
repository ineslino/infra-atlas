#!/usr/bin/env python3
"""
Infra Atlas — source-link integrity checker.

The site's whole promise is "sourced": every matrix cell, decision row and
calculator figure cites an official vendor doc URL. Those URLs rot — vendors
restructure docs and move domains (Google → docs.cloud.google.com, Oracle's
servicelimits → service-limits during this project alone). This harvests every
external URL cited across the site and reports which are genuinely dead.

It is network-heavy and vendor docs frequently block bots (403/429) or rate-
limit, so this is NOT wired into verify-data.yml (it would flake the build).
Run it manually, or on a schedule, and triage the DEAD list:

    python3 scripts/check_source_links.py            # check everything
    python3 scripts/check_source_links.py --json out.json

Categories:
  OK       2xx
  REDIR    3xx → reports the final location (not dead, but worth a look)
  BLOCKED  401/403/405/429 — almost always alive but bot-walled; low priority
  DEAD     404/410, DNS failure, connection error, persistent 5xx — fix these

No third-party deps (stdlib urllib + threads); credential-free.
"""
import concurrent.futures as cf
import glob
import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
TIMEOUT = 20
WORKERS = 12

# Own infra + boilerplate that never rots / isn't a "source" claim, plus the
# placeholder URLs that appear as examples in calculator/API copy (not sources).
SKIP = ("infraatlas.dev", "fonts.googleapis", "fonts.gstatic", "schema.org",
        "creativecommons.org", "www.w3.org", "github.com/ineslino",
        "localhost", "127.0.0.1", "example.com", ".local", ".dev.local")

URL_RE = re.compile(r'https?://[^\s"\'<>)]+')


def harvest():
    urls = set()
    files = glob.glob("**/index.html", recursive=True)
    files += glob.glob("*/data.json")
    files += ["scripts/build_decisions.py", "llms.txt", "README.md"]
    for p in files:
        if "node_modules" in p or not os.path.exists(p):
            continue
        with open(p, encoding="utf-8") as f:
            text = f.read()
        for m in URL_RE.findall(text):
            u = m.rstrip(".,;)")
            if not any(s in u for s in SKIP):
                urls.add(u)
    return sorted(urls)


def probe(url):
    """Return (category, detail). Try HEAD, fall back to GET on 403/405."""
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers={
                "User-Agent": UA,
                "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            })
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                final = r.geturl()
                if final.rstrip("/") != url.rstrip("/"):
                    return ("REDIR", f"{r.status} → {final}")
                return ("OK", str(r.status))
        except urllib.error.HTTPError as e:
            if e.code in (403, 405) and method == "HEAD":
                continue  # retry with GET — many servers reject HEAD
            if e.code in (401, 403, 405, 429):
                return ("BLOCKED", str(e.code))
            return ("DEAD", str(e.code))
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if method == "HEAD":
                continue  # a connection wobble on HEAD — let GET have a turn
            reason = getattr(e, "reason", e)
            return ("DEAD", f"{type(e).__name__}: {reason}")
        except Exception as e:  # noqa: BLE001
            return ("DEAD", f"{type(e).__name__}: {e}")
    return ("BLOCKED", "403/405 on HEAD+GET")


def main():
    urls = harvest()
    print(f"Harvested {len(urls)} unique external source URLs. Checking…\n", flush=True)
    results = {}
    with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for url, (cat, detail) in zip(urls, ex.map(probe, urls)):
            results[url] = (cat, detail)

    buckets = {"OK": [], "REDIR": [], "BLOCKED": [], "DEAD": []}
    for url, (cat, detail) in results.items():
        buckets[cat].append((url, detail))

    for cat in ("DEAD", "REDIR", "BLOCKED"):
        rows = sorted(buckets[cat])
        if not rows:
            continue
        print(f"\n=== {cat} ({len(rows)}) ===")
        for url, detail in rows:
            print(f"  {detail:42}  {url}")

    print(f"\nSummary: {len(buckets['OK'])} OK · {len(buckets['REDIR'])} redirect "
          f"· {len(buckets['BLOCKED'])} bot-blocked · {len(buckets['DEAD'])} DEAD")

    if len(sys.argv) > 2 and sys.argv[1] == "--json":
        with open(sys.argv[2], "w", encoding="utf-8") as f:
            json.dump({k: dict(v) for k, v in buckets.items()}, f, indent=2)
        print(f"Wrote {sys.argv[2]}")

    # DEAD is the actionable bucket; exit non-zero so a scheduled run can alert.
    return 1 if buckets["DEAD"] else 0


if __name__ == "__main__":
    sys.exit(main())
