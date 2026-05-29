#!/usr/bin/env python3
"""Infra Atlas · build /feed.xml (RSS 2.0) from feed.json.

Run after scripts/diff_feed.py in the daily refresh so the changelog's RSS
stays in lockstep with the "What Changed" feed. Static output — no server.

Usage:  python3 scripts/build_feed_rss.py [feed.xml]
"""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = "https://infraatlas.dev"

# Mirrors the INST map in /assets/feed.js (kept small + stable; different runtime).
LABELS = {
    "ec2": "AWS EC2", "azure-vm": "Azure VM", "gcp-compute": "GCP Compute",
    "oci-compute": "OCI", "ovh-instances": "OVHcloud", "regions": "Regions",
    "egress": "Egress", "atlas": "Infra Atlas",
}


def load_entries(name):
    try:
        return (json.load(open(os.path.join(ROOT, name), encoding="utf-8")).get("entries")) or []
    except Exception:
        return []


def rfc822(ts):
    try:
        return format_datetime(datetime.strptime(ts[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc))
    except Exception:
        return format_datetime(datetime.now(timezone.utc))


def main():
    out_p = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "feed.xml")
    # Merge the auto-detected feed with curated editorial dispatches, newest-first
    # (same model as the client's IA.feed.load).
    entries = load_entries("feed.json") + load_entries("dispatches.json")
    entries = [e for e in entries if e.get("ts")]
    entries.sort(key=lambda e: e.get("ts", ""), reverse=True)
    built = rfc822(entries[0]["ts"] if entries else "")

    items = []
    for e in entries:
        inst, kind = e.get("instrument", ""), e.get("kind", "")
        text, ts = e.get("text", ""), e.get("ts", "")
        title = f"{LABELS.get(inst, inst)} · {text}"
        link = f"{SITE}/{inst}/" if inst in LABELS else f"{SITE}/changelog/"
        guid = hashlib.md5(f"{ts}|{inst}|{kind}|{text}".encode("utf-8")).hexdigest()
        items.append(
            "    <item>\n"
            f"      <title>{escape(title)}</title>\n"
            f"      <link>{escape(link)}</link>\n"
            f'      <guid isPermaLink="false">{guid}</guid>\n'
            f"      <category>{escape(kind)}</category>\n"
            f"      <pubDate>{rfc822(ts)}</pubDate>\n"
            f"      <description>{escape(title)}</description>\n"
            "    </item>"
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        "    <title>Infra Atlas · What Changed</title>\n"
        f"    <link>{SITE}/changelog/</link>\n"
        f'    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>\n'
        "    <description>A neutral, sourced changelog of cloud infrastructure — "
        "new instance families, regions, withdrawals and price moves across AWS, "
        "Azure, GCP, OCI and OVHcloud.</description>\n"
        "    <language>en</language>\n"
        f"    <lastBuildDate>{built}</lastBuildDate>\n"
        + ("\n".join(items) + "\n" if items else "")
        + "  </channel>\n"
        "</rss>\n"
    )
    with open(out_p, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"feed.xml <- {len(items)} items")


if __name__ == "__main__":
    main()
