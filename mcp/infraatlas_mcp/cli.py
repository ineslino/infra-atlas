#!/usr/bin/env python3
"""
infraatlas — the Infra Atlas terminal client.

The ICP lives in a terminal; this is the site's public data.json API without
the browser. Same package as the MCP server, same logic.py (the scoring and
egress math pinned to the site by tests), plus a small on-disk cache so
repeat queries answer instantly.

    infraatlas ec2 --region eu-west-1 --arch arm64 --min-memory 16
    infraatlas equivalent m5.xlarge
    infraatlas egress aws azure --gb 500
    infraatlas regions gcp --area Europe
    infraatlas changes --days 7 --instrument ec2

Prices are hourly on-demand LIST prices (Linux; USD except OVHcloud in EUR)
— never spot, reserved, savings-plan or invoiced prices.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

import httpx

from .logic import flatten_catalogue, parse_tiers, score_candidate, walk_ladder

BASE_URL = "https://infraatlas.dev"
CACHE_DIR = Path.home() / ".cache" / "infraatlas"
CACHE_TTL = 3600  # the data refreshes daily; an hour is plenty

CLOUD_SLUGS = {
    "aws": "ec2", "azure": "azure-vm", "gcp": "gcp-compute",
    "oci": "oci-compute", "ovh": "ovh-instances",
}
CLOUD_ORDER = ["aws", "azure", "gcp", "oci", "ovh"]
PRICE_NOTE = ("list prices: hourly on-demand, Linux; USD (OVHcloud in EUR) — "
              "no spot/reserved/savings plans")


# ─── fetch layer — httpx + a TTL file cache ───
def fetch_json(path: str, fresh: bool = False):
    name = path.strip("/").replace("/", "_") or "root"
    cache = CACHE_DIR / f"{name}"
    if not fresh and cache.exists() and time.time() - cache.stat().st_mtime < CACHE_TTL:
        try:
            return json.loads(cache.read_text(encoding="utf-8"))
        except Exception:
            pass  # corrupt cache — fall through to the network
    resp = httpx.get(f"{BASE_URL}{path}", timeout=30.0, follow_redirects=True)
    resp.raise_for_status()
    data = resp.json()
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(data), encoding="utf-8")
    except Exception:
        pass  # read-only home etc. — cache is best-effort
    return data


def load_cloud(cloud: str, fresh: bool = False):
    data = fetch_json(f"/{CLOUD_SLUGS[cloud]}/data.json", fresh)
    return flatten_catalogue(cloud, data), data


# ─── output helpers ───
def table(rows, headers):
    """Plain mono table — no third-party deps, pipe-friendly."""
    cols = [headers] + [[("" if c is None else str(c)) for c in r] for r in rows]
    widths = [max(len(r[i]) for r in cols) for i in range(len(headers))]
    out = ["  ".join(h.ljust(widths[i]) for i, h in enumerate(headers))]
    out.append("  ".join("─" * w for w in widths))
    for r in cols[1:]:
        out.append("  ".join(c.ljust(widths[i]) for i, c in enumerate(r)))
    return "\n".join(out)


def money(p, currency="USD"):
    if p is None:
        return "—"
    s = f"{p:.4f}".rstrip("0").rstrip(".")
    return ("€" if currency == "EUR" else "$") + (s if "." in s else s + ".00")


def emit(args, payload, text):
    print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else text)


# ─── compute ───
def cmd_compute(args):
    flat, data = load_cloud(args.cloud, args.fresh)
    currency = data.get("currency", "USD")
    rows = flat
    if args.region:
        rows = [r for r in rows if r["_region_codes"] is None or args.region in r["_region_codes"]]
    if args.arch:
        want = {"arm": "arm64", "arm64": "arm64", "x86": "x86_64", "x86_64": "x86_64"}.get(args.arch.lower(), args.arch)
        rows = [r for r in rows if r["arch"] == want]
    if args.min_vcpu:
        rows = [r for r in rows if (r["vcpu"] or 0) >= args.min_vcpu]
    if args.min_memory:
        rows = [r for r in rows if (r["memoryGiB"] or 0) >= args.min_memory]
    if args.max_price is not None:
        rows = [r for r in rows if r["pricePerHour"] is not None and r["pricePerHour"] <= args.max_price]
    if args.name_contains:
        needle = args.name_contains.lower()
        rows = [r for r in rows if needle in r["name"].lower()]
    key = {
        "price": lambda r: (r["pricePerHour"] is None, r["pricePerHour"] or 0),
        "vcpu": lambda r: -(r["vcpu"] or 0),
        "memory": lambda r: -(r["memoryGiB"] or 0),
        "name": lambda r: r["name"],
    }[args.sort]
    rows = sorted(rows, key=key)
    total = len(rows)
    rows = rows[: args.limit]
    payload = {
        "source": f"{BASE_URL}/{CLOUD_SLUGS[args.cloud]}/data.json",
        "generated": data.get("generated"), "currency": currency,
        "total": total, "shown": len(rows), "note": PRICE_NOTE,
        "instances": [{k: v for k, v in r.items() if not k.startswith("_")} for r in rows],
    }
    text = table(
        [[r["name"], r["category"], r["arch"], r["vcpu"], r["memoryGiB"],
          money(r["pricePerHour"], currency), r["regions"]] for r in rows],
        ["INSTANCE", "CLASS", "ARCH", "VCPU", "MEM GiB", f"{currency}/HR", "REGIONS"],
    ) + f"\n\n{len(rows)} of {total} · data {str(payload['generated'])[:10]} · {PRICE_NOTE}"
    emit(args, payload, text)


# ─── equivalent ───
def cmd_equivalent(args):
    src_flat, src_data = load_cloud(args.cloud, args.fresh)
    src = next((r for r in src_flat if r["name"] == args.sku), None)
    if src is None:
        near = [r["name"] for r in src_flat if args.sku.lower() in r["name"].lower()][:8]
        hint = f" Closest names: {', '.join(near)}" if near else ""
        sys.exit(f"infraatlas: '{args.sku}' not found in the {args.cloud} catalogue.{hint}")
    if not src.get("vcpu"):
        sys.exit(f"infraatlas: '{args.sku}' has no published vCPU count — it cannot be scored.")

    blocks, payload_eq = [], {}
    for cloud in CLOUD_ORDER:
        if cloud == args.cloud:
            continue
        try:
            flat, data = load_cloud(cloud, args.fresh)
        except Exception:
            continue
        currency = data.get("currency", "USD")
        scored = sorted(
            ((score_candidate(src, c), c) for c in flat if c.get("vcpu")),
            key=lambda t: (-t[0]["score"], not t[0]["memScored"],
                           abs((t[1]["vcpu"] or 0) - src["vcpu"]), t[1]["name"]),
        )[: args.top]
        payload_eq[cloud] = [
            {"name": c["name"], "score": s["score"], "vcpu": c["vcpu"],
             "memoryGiB": c["memoryGiB"], "pricePerHour": c["pricePerHour"],
             "currency": currency, "regions": c["regions"], "why": s["why"]}
            for s, c in scored
        ]
        for s, c in scored:
            blocks.append([cloud, c["name"], f"{s['score']:g}",
                           c["vcpu"], c["memoryGiB"],
                           money(c["pricePerHour"], currency), c["regions"]])
    src_cur = src_data.get("currency", "USD")
    head = (f"{src['name']} ({args.cloud}) — {src['vcpu']} vCPU · "
            f"{src['memoryGiB']} GiB · {money(src['pricePerHour'], src_cur)}/hr")
    text = head + "\n\n" + table(
        blocks, ["CLOUD", "MATCH", "SCORE", "VCPU", "MEM GiB", "PRICE/HR", "REGIONS"]
    ) + f"\n\nsame scoring as {BASE_URL}/equivalent-sku/ · {PRICE_NOTE}"
    emit(args, {"source": {"name": src["name"], "cloud": args.cloud,
                           "vcpu": src["vcpu"], "memoryGiB": src["memoryGiB"],
                           "pricePerHour": src["pricePerHour"], "currency": src_cur},
                "note": PRICE_NOTE, "equivalents": payload_eq}, text)


# ─── egress ───
def cmd_egress(args):
    data = fetch_json("/egress/data.json", args.fresh)
    transfer = next((t for t in data.get("transfers", []) if t.get("id") == args.transfer), None)
    if transfer is None:
        ids = ", ".join(t.get("id", "?") for t in data.get("transfers", []))
        sys.exit(f"infraatlas: unknown transfer '{args.transfer}'. Available: {ids}.")
    providers = args.providers or ["aws", "azure", "gcp"]
    rows, payload = [], {}
    for prov in providers:
        rate = (transfer.get("rates") or {}).get(prov)
        if not rate:
            rows.append([prov, "—", "no rate published", ""])
            continue
        ladder = parse_tiers(rate["tiers"]) if rate.get("tiers") else None
        if ladder:
            res = walk_ladder(ladder, args.gb)
        else:
            m = re.match(r"\$([\d.]+)\s*/\s*(GB|GiB)", rate.get("headline", ""))
            if m:
                usd = float(m.group(1))
                res = {"totalUSD": round(usd * args.gb, 2),
                       "breakdown": [{"band": "Flat rate", "volumeGB": args.gb,
                                      "usdPerGB": usd, "cost": round(usd * args.gb, 2)}]}
            elif rate.get("headline", "").strip().lower() == "free":
                res = {"totalUSD": 0.0, "breakdown": []}
            else:
                rows.append([prov, "—", rate.get("headline", "—"), ""])
                continue
        eff = round(res["totalUSD"] / args.gb, 4) if args.gb else 0
        payload[prov] = {**res, "effectiveUsdPerGB": eff, "source": rate.get("src", "")}
        rows.append([prov, f"${res['totalUSD']:,.2f}", f"${eff}/GB effective",
                     rate.get("note", "")[:60]])
    text = (f"{transfer.get('label', args.transfer)} · {args.gb:,.0f} GB/month\n\n"
            + table(rows, ["PROVIDER", "TOTAL", "EFFECTIVE", "NOTE"])
            + f"\n\nheadline list prices from {BASE_URL}/egress/ — free tiers applied, "
              "CDN/committed-use deals not modelled")
    emit(args, {"transfer": args.transfer, "volumeGB": args.gb,
                "generated": data.get("generated"), "results": payload}, text)


# ─── regions ───
def cmd_regions(args):
    data = fetch_json("/regions/data.json", args.fresh)
    rows = []
    needle = args.query.lower() if args.query else None
    for city in data.get("cities", []):
        if args.area and city.get("area", "").lower() != args.area.lower():
            continue
        for region in city.get("regions", []):
            if args.cloud and region.get("p") != args.cloud:
                continue
            if needle and not any(
                needle in str(v).lower()
                for v in (city.get("city"), city.get("country"),
                          region.get("code"), region.get("name"))
            ):
                continue
            rows.append({
                "provider": region.get("p"), "code": region.get("code"),
                "name": region.get("name"), "city": city.get("city"),
                "country": city.get("country"), "area": city.get("area"),
                "lat": city.get("lat"), "lng": city.get("lng"),
                "since": region.get("since"),
            })
    rows.sort(key=lambda r: (r["provider"] or "", r["code"] or ""))
    text = table(
        [[r["provider"], r["code"], r["city"], r["country"], r["area"], r["since"]] for r in rows],
        ["CLOUD", "CODE", "CITY", "COUNTRY", "AREA", "SINCE"],
    ) + f"\n\n{len(rows)} regions · curated, vendor-verified · {BASE_URL}/regions/"
    emit(args, {"source": f"{BASE_URL}/regions/data.json",
                "total": len(rows), "regions": rows}, text)


# ─── changes ───
def cmd_changes(args):
    import datetime
    path = f"/{CLOUD_SLUGS.get(args.instrument, args.instrument)}/feed.json" if args.instrument else "/feed.json"
    try:
        data = fetch_json(path, args.fresh)
    except httpx.HTTPStatusError:
        data = fetch_json("/feed.json", args.fresh)  # pre-split fallback
    cutoff = (datetime.date.today() - datetime.timedelta(days=args.days)).isoformat()
    entries = [e for e in data.get("entries", [])
               if e.get("ts", "") >= cutoff
               and (args.instrument is None
                    or e.get("instrument") in (args.instrument, CLOUD_SLUGS.get(args.instrument)))]
    text = table(
        [[e["ts"], e["instrument"], e["kind"], e["text"]] for e in entries],
        ["DATE", "INSTRUMENT", "KIND", "CHANGE"],
    ) + f"\n\n{len(entries)} change(s) in the last {args.days} day(s) · {BASE_URL}/changelog/"
    emit(args, {"windowDays": args.days, "count": len(entries), "entries": entries}, text)


# ─── argparse wiring ───
def build_parser():
    p = argparse.ArgumentParser(
        prog="infraatlas",
        description="Query infraatlas.dev's multi-cloud reference data from the terminal.",
        epilog="Data: CC BY 4.0 · cached ~1h in ~/.cache/infraatlas (--fresh bypasses).",
    )
    sub = p.add_subparsers(dest="command", required=True)

    def common(sp):
        sp.add_argument("--json", action="store_true", help="raw JSON output")
        sp.add_argument("--fresh", action="store_true", help="bypass the local cache")

    def compute_args(sp):
        sp.add_argument("--region", help="region code the family must be available in")
        sp.add_argument("--arch", help="x86_64 or arm64")
        sp.add_argument("--min-vcpu", type=int)
        sp.add_argument("--min-memory", type=float, metavar="GIB")
        sp.add_argument("--max-price", type=float, metavar="PER_HR")
        sp.add_argument("--name-contains", metavar="SUBSTR")
        sp.add_argument("--sort", choices=["price", "vcpu", "memory", "name"], default="price")
        sp.add_argument("--limit", type=int, default=20)
        common(sp)

    sp = sub.add_parser("compute", help="search one cloud's compute catalogue")
    sp.add_argument("cloud", choices=CLOUD_ORDER)
    compute_args(sp)
    sp.set_defaults(func=cmd_compute)

    for alias in CLOUD_ORDER:
        spa = sub.add_parser(alias if alias != "aws" else "ec2",
                             help=f"shorthand for `compute {alias}`")
        compute_args(spa)
        spa.set_defaults(func=cmd_compute, cloud=alias)

    sp = sub.add_parser("equivalent", help="closest SKUs on every other cloud")
    sp.add_argument("sku", help="instance name as the vendor writes it (e.g. m5.xlarge)")
    sp.add_argument("--cloud", choices=CLOUD_ORDER, default="aws", help="cloud the SKU belongs to")
    sp.add_argument("--top", type=int, default=3)
    common(sp)
    sp.set_defaults(func=cmd_equivalent)

    sp = sub.add_parser("egress", help="price N GB through the egress tier ladders")
    sp.add_argument("providers", nargs="*", choices=["aws", "azure", "gcp"],
                    help="providers to compare (default: all three)")
    sp.add_argument("--gb", type=float, required=True, help="monthly volume in GB")
    sp.add_argument("--transfer", default="internet-egress",
                    help="internet-egress | cross-az | cross-region | nat-processing | interconnect")
    common(sp)
    sp.set_defaults(func=cmd_egress)

    sp = sub.add_parser("regions", help="list GA cloud regions")
    sp.add_argument("cloud", nargs="?", choices=CLOUD_ORDER)
    sp.add_argument("--area", help="Americas, Europe, Asia Pacific, Middle East, Africa")
    sp.add_argument("--query", help="substring match on city/country/code")
    common(sp)
    sp.set_defaults(func=cmd_regions)

    sp = sub.add_parser("changes", help="what changed in the catalogues lately")
    sp.add_argument("--days", type=int, default=30)
    sp.add_argument("--instrument", help="one cloud only (aws/azure/gcp/oci/ovh or a slug)")
    common(sp)
    sp.set_defaults(func=cmd_changes)

    return p


def main():
    args = build_parser().parse_args()
    try:
        args.func(args)
    except httpx.TransportError:
        sys.exit("infraatlas: could not reach infraatlas.dev — check the network and retry.")
    except httpx.HTTPStatusError as e:
        sys.exit(f"infraatlas: infraatlas.dev returned HTTP {e.response.status_code} "
                 f"for {e.request.url.path} — the endpoint list lives at {BASE_URL}/api/.")
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
