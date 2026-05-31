#!/usr/bin/env python3
"""
Infra Atlas — regenerate the Open Graph card (og.png).

og.png is a 1200x630 screenshot of _ogcard.html (the social-share card). Its
"N instruments" chip is DERIVED here from index.html so it can't drift; the
companion guard scripts/check_og_card.py fails CI when it does.

Steps:
  1. count the live instruments in index.html
  2. write that count into _ogcard.html (idempotent)
  3. screenshot _ogcard.html -> og.png with headless Chrome, served from a
     throwaway localhost server (so the Google-Fonts webfonts load cleanly)

Requires a Chrome/Chromium binary. On macOS it finds Google Chrome
automatically; elsewhere it looks on PATH; set CHROME_BIN to override.
No Python third-party deps.

Run from repo root:  python3 scripts/build_og.py
"""
import contextlib
import functools
import http.server
import os
import re
import shutil
import socket
import socketserver
import subprocess
import sys
import threading

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDEX = os.path.join(ROOT, "index.html")
CARD = os.path.join(ROOT, "_ogcard.html")
OUT = os.path.join(ROOT, "og.png")


def live_instrument_count():
    with open(INDEX, encoding="utf-8") as f:
        return len(re.findall(r'class="instrument is-live"', f.read()))


def update_card_count(n):
    with open(CARD, encoding="utf-8") as f:
        html = f.read()
    new = re.sub(r"(<b>)\d+(</b>&nbsp;instruments)", r"\g<1>%d\g<2>" % n, html, count=1)
    if new == html:
        print(f"  _ogcard.html already at {n} instruments")
        return
    with open(CARD, "w", encoding="utf-8") as f:
        f.write(new)
    print(f"  _ogcard.html -> {n} instruments")


def find_chrome():
    if os.environ.get("CHROME_BIN"):
        return os.environ["CHROME_BIN"]
    mac = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if os.path.exists(mac):
        return mac
    for name in ("google-chrome", "google-chrome-stable", "chromium",
                 "chromium-browser", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    return None


def _free_port():
    with contextlib.closing(socket.socket()) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def screenshot(chrome):
    port = _free_port()
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    httpd.allow_reuse_address = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    try:
        cmd = [
            chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=1", "--window-size=1200,630",
            "--default-background-color=00000000", "--virtual-time-budget=4000",
            f"--screenshot={OUT}", f"http://127.0.0.1:{port}/_ogcard.html",
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        httpd.shutdown()
    print(f"  og.png <- screenshot ({os.path.getsize(OUT) // 1024} KB)")


def main():
    chrome = find_chrome()
    if not chrome:
        print("::error:: no Chrome/Chromium found. Install Chrome or set CHROME_BIN "
              "to its binary path.", file=sys.stderr)
        return 1
    n = live_instrument_count()
    update_card_count(n)
    screenshot(chrome)
    print(f"OK — og.png regenerated for {n} instruments. "
          f"Bump the og:image ?v= query if you want platforms to re-fetch sooner.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
