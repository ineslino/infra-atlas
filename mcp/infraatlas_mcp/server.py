#!/usr/bin/env python3
"""
MCP server for Infra Atlas (infraatlas.dev).

Exposes the site's public, CORS-enabled data.json endpoints as MCP tools:
multi-cloud compute catalogues (AWS / Azure / GCP / OCI / OVHcloud),
cross-cloud SKU equivalence (the same scoring the Equivalent-SKU Finder
uses), region geography, internet-egress cost math and the change feed.

No API key anywhere: the data is public (CC BY 4.0) and the server runs
locally over stdio. Compute prices are hourly on-demand *list* prices
(Linux; USD except OVHcloud which publishes EUR) — never spot, reserved,
savings-plan or invoiced prices.
"""

from __future__ import annotations

import datetime
import json
import re
import time
from enum import Enum
from typing import Any, Optional

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field

mcp = FastMCP("infraatlas_mcp")

BASE_URL = "https://infraatlas.dev"
CACHE_TTL_SECONDS = 3600  # data refreshes daily; 1h is plenty
PRICE_NOTE = (
    "Hourly on-demand list prices (Linux; USD except OVHcloud in EUR) — "
    "spot, reserved, savings-plan and negotiated rates are out of scope."
)

CLOUD_SLUGS = {
    "aws": "ec2",
    "azure": "azure-vm",
    "gcp": "gcp-compute",
    "oci": "oci-compute",
    "ovh": "ovh-instances",
}
CLOUD_ORDER = ["aws", "azure", "gcp", "oci", "ovh"]

from .logic import (
    flatten_catalogue,
    parse_tiers,
    public_view,
    score_candidate,
    walk_ladder,
)


class Cloud(str, Enum):
    aws = "aws"
    azure = "azure"
    gcp = "gcp"
    oci = "oci"
    ovh = "ovh"


# ─── Fetch layer — small in-process TTL cache over the public endpoints ───
_cache: dict[str, tuple[float, Any]] = {}


async def _fetch_json(path: str) -> Any:
    """GET {BASE_URL}{path} with a TTL cache. Raises httpx errors upward."""
    now = time.monotonic()
    hit = _cache.get(path)
    if hit and now - hit[0] < CACHE_TTL_SECONDS:
        return hit[1]
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}{path}", timeout=30.0, follow_redirects=True)
        resp.raise_for_status()
        data = resp.json()
    _cache[path] = (now, data)
    return data


def _error(e: Exception) -> str:
    if isinstance(e, httpx.HTTPStatusError):
        return (
            f"Error: infraatlas.dev returned HTTP {e.response.status_code} for "
            f"{e.request.url.path}. The endpoint list lives at {BASE_URL}/api/."
        )
    if isinstance(e, httpx.TransportError):
        return "Error: could not reach infraatlas.dev — check network access and retry."
    return f"Error: {type(e).__name__}: {e}"


def _dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2)


async def _load_cloud(cloud: str) -> tuple[list[dict], dict]:
    data = await _fetch_json(f"/{CLOUD_SLUGS[cloud]}/data.json")
    return flatten_catalogue(cloud, data), data


# ─── Input models ───
class ComputeQuery(BaseModel):
    """Filters for one cloud's compute catalogue."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    cloud: Cloud = Field(..., description="Cloud catalogue to query: aws, azure, gcp, oci or ovh")
    region: Optional[str] = Field(default=None, description="Region code the instance family must be available in (e.g. 'eu-west-1', 'westeurope', 'GRA'). Codes come from infraatlas_get_regions.")
    arch: Optional[str] = Field(default=None, description="CPU architecture: 'x86_64' or 'arm64'")
    category: Optional[str] = Field(default=None, description="Workload class: general, compute, memory, storage, accelerated, hpc, baremetal, confidential, macos")
    min_vcpu: Optional[int] = Field(default=None, ge=1, description="Minimum vCPU count")
    min_memory_gb: Optional[float] = Field(default=None, ge=0.5, description="Minimum memory in GiB")
    max_price_per_hour: Optional[float] = Field(default=None, gt=0, description="Maximum hourly list price (catalogue currency: USD, or EUR for OVH)")
    name_contains: Optional[str] = Field(default=None, description="Substring match on the instance name (e.g. 'm7g', 'D4s')")
    sort: str = Field(default="price", description="Sort key: price, vcpu, memory or name (price sorts unknown prices last)")
    limit: int = Field(default=25, ge=1, le=200, description="Maximum results to return")
    offset: int = Field(default=0, ge=0, description="Results to skip, for pagination")


class EquivalentQuery(BaseModel):
    """A source SKU to translate to every other cloud."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    source_cloud: Cloud = Field(..., description="Cloud the source SKU belongs to")
    sku_name: str = Field(..., min_length=2, description="Exact instance name as the vendor writes it (e.g. 'm5.xlarge', 'D4s_v5', 'n2-standard-4')")
    top_n: int = Field(default=3, ge=1, le=10, description="Matches to return per target cloud")


class EgressQuery(BaseModel):
    """Volume to price through the egress tier ladder."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    gb: float = Field(..., gt=0, le=10_000_000, description="Monthly transfer volume in GB")
    provider: Optional[str] = Field(default=None, description="aws, azure or gcp; omit for all three side by side")
    transfer: str = Field(default="internet-egress", description="Transfer type id from the Egress Cost Map: internet-egress, cross-az, cross-region, nat-processing or interconnect")


class RegionsQuery(BaseModel):
    """Filters over the multi-cloud region map."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    cloud: Optional[Cloud] = Field(default=None, description="Only regions of this cloud")
    area: Optional[str] = Field(default=None, description="Geography filter: Americas, Europe, Asia Pacific, Middle East, Africa")
    query: Optional[str] = Field(default=None, description="Substring match on city, country or region code")


class ChangesQuery(BaseModel):
    """Window over the data change feed."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    days: int = Field(default=30, ge=1, le=365, description="Look-back window in days")
    instrument: Optional[str] = Field(default=None, description="Limit to one instrument slug: ec2, regions, azure-vm, gcp-compute, oci-compute, ovh-instances")


# ─── Tools ───
@mcp.tool(
    name="infraatlas_get_compute_instances",
    annotations={
        "title": "Search cloud compute instances",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def infraatlas_get_compute_instances(params: ComputeQuery) -> str:
    """Search one cloud's compute catalogue (instance types with vCPU, memory,
    hourly list price and regional availability), refreshed daily from public
    sources by infraatlas.dev.

    Returns a JSON object:
    {
      "source": str,        # the data.json endpoint used
      "generated": str,     # upstream refresh timestamp
      "currency": str,      # USD, or EUR for OVHcloud
      "priceNote": str,     # what the price is (and is not)
      "total": int,         # matches before pagination
      "count": int, "offset": int, "has_more": bool,
      "instances": [{name, family, category, arch, cpuVendor, vcpu,
                     memoryGiB, pricePerHour, regions}]
    }
    Notes: GCP publishes no per-size specs, so its vcpu derives from the name
    and prices are null. `regions` is the count of regions offering the
    family; pass `region` to filter by a specific region code.

    Examples: cheapest arm64 with 16 GiB on AWS → cloud=aws, arch=arm64,
    min_memory_gb=16, sort=price. What 8-vCPU boxes exist in westeurope →
    cloud=azure, region=westeurope, min_vcpu=8.
    """
    try:
        flat, data = await _load_cloud(params.cloud.value)
    except Exception as e:  # noqa: BLE001 — every failure becomes an actionable message
        return _error(e)

    rows = flat
    if params.region:
        region = params.region.strip()
        rows = [r for r in rows if r["_region_codes"] is None or region in r["_region_codes"]]
    if params.arch:
        rows = [r for r in rows if r["arch"].lower() == params.arch.lower()]
    if params.category:
        rows = [r for r in rows if r["category"].lower() == params.category.lower()]
    if params.min_vcpu is not None:
        rows = [r for r in rows if (r["vcpu"] or 0) >= params.min_vcpu]
    if params.min_memory_gb is not None:
        rows = [r for r in rows if (r["memoryGiB"] or 0) >= params.min_memory_gb]
    if params.max_price_per_hour is not None:
        rows = [r for r in rows if r["pricePerHour"] is not None and r["pricePerHour"] <= params.max_price_per_hour]
    if params.name_contains:
        needle = params.name_contains.lower()
        rows = [r for r in rows if needle in r["name"].lower()]

    sort_key = {
        "price": lambda r: (r["pricePerHour"] is None, r["pricePerHour"] or 0),
        "vcpu": lambda r: -(r["vcpu"] or 0),
        "memory": lambda r: -(r["memoryGiB"] or 0),
        "name": lambda r: r["name"],
    }.get(params.sort, lambda r: (r["pricePerHour"] is None, r["pricePerHour"] or 0))
    rows = sorted(rows, key=sort_key)

    page = rows[params.offset:params.offset + params.limit]
    return _dumps({
        "source": f"{BASE_URL}/{CLOUD_SLUGS[params.cloud.value]}/data.json",
        "generated": data.get("generated"),
        "currency": data.get("currency", "USD"),
        "priceNote": PRICE_NOTE,
        "total": len(rows),
        "count": len(page),
        "offset": params.offset,
        "has_more": params.offset + len(page) < len(rows),
        "instances": [public_view(r) for r in page],
    })


@mcp.tool(
    name="infraatlas_find_equivalent_sku",
    annotations={
        "title": "Find equivalent SKUs on other clouds",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def infraatlas_find_equivalent_sku(params: EquivalentQuery) -> str:
    """Translate an instance type to its closest equivalents on every other
    cloud, using the exact scoring of infraatlas.dev/equivalent-sku/: vCPU
    (50) + memory (38) + workload category (12) renormalised over scorable
    axes, then ×0.55 when the CPU architecture differs (an x86 image will not
    boot on Arm, so cross-architecture matches cap at 55/100).

    Returns JSON:
    {
      "source": {name, cloud, vcpu, memoryGiB, arch, category,
                 pricePerHour, currency, regions},
      "priceNote": str,
      "equivalents": { "<cloud>": [ {name, score, vcpu, memoryGiB, arch,
                        category, pricePerHour, currency, regions, why[]} ] }
    }
    `why` spells out the deltas behind each score. If the SKU is not found,
    the error lists near-miss names to retry with.
    """
    try:
        src_flat, src_data = await _load_cloud(params.source_cloud.value)
    except Exception as e:  # noqa: BLE001
        return _error(e)

    src = next((r for r in src_flat if r["name"] == params.sku_name), None)
    if src is None:
        near = [r["name"] for r in src_flat if params.sku_name.lower() in r["name"].lower()][:8]
        hint = f" Closest names: {', '.join(near)}." if near else ""
        return (
            f"Error: '{params.sku_name}' not found in the {params.source_cloud.value} catalogue."
            f"{hint} Use infraatlas_get_compute_instances(cloud={params.source_cloud.value}, "
            f"name_contains=...) to browse names."
        )
    if not src.get("vcpu"):
        return (
            f"Error: '{params.sku_name}' has no published vCPU count, so it cannot be scored "
            f"(the dominant axis would be missing). Pick a sized variant instead."
        )

    currencies: dict[str, str] = {}
    equivalents: dict[str, list[dict]] = {}
    for cloud in CLOUD_ORDER:
        if cloud == params.source_cloud.value:
            continue
        try:
            flat, data = await _load_cloud(cloud)
        except Exception:  # noqa: BLE001 — one unreachable catalogue should not kill the rest
            equivalents[cloud] = []
            continue
        currencies[cloud] = data.get("currency", "USD")
        scored = []
        for cand in flat:
            if not cand.get("vcpu"):
                continue
            s = score_candidate(src, cand)
            scored.append((s, cand))
        scored.sort(key=lambda t: (
            -t[0]["score"],
            not t[0]["memScored"],
            abs((t[1]["vcpu"] or 0) - src["vcpu"]),
            t[1]["name"],
        ))
        equivalents[cloud] = [
            {
                "name": cand["name"],
                "score": s["score"],
                "vcpu": cand["vcpu"],
                "memoryGiB": cand["memoryGiB"],
                "arch": cand["arch"],
                "category": cand["category"],
                "pricePerHour": cand["pricePerHour"],
                "currency": currencies[cloud],
                "regions": cand["regions"],
                "why": s["why"],
            }
            for s, cand in scored[:params.top_n]
        ]

    src_currency = src_data.get("currency", "USD")
    return _dumps({
        "source": {
            "name": src["name"], "cloud": params.source_cloud.value,
            "vcpu": src["vcpu"], "memoryGiB": src["memoryGiB"],
            "arch": src["arch"], "category": src["category"],
            "pricePerHour": src["pricePerHour"], "currency": src_currency,
            "regions": src["regions"],
        },
        "priceNote": PRICE_NOTE,
        "equivalents": equivalents,
    })


@mcp.tool(
    name="infraatlas_get_egress_cost",
    annotations={
        "title": "Estimate data-transfer cost",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def infraatlas_get_egress_cost(params: EgressQuery) -> str:
    """Estimate the monthly cost of moving N GB on AWS, Azure and GCP, by
    walking the tier ladder curated in infraatlas.dev/egress/ (internet
    egress by default; also cross-az, cross-region, nat-processing,
    interconnect).

    Returns JSON per provider:
    { "transfer": str, "volumeGB": float, "results": { "<provider>": {
        "totalUSD": float, "effectiveUsdPerGB": float,
        "breakdown": [{band, volumeGB, usdPerGB, cost}],
        "note": str, "source": str } }, "disclaimer": str }

    These are headline list prices: free same-region paths, CDN routing,
    committed-use deals and private pricing all move the real number.
    """
    try:
        data = await _fetch_json("/egress/data.json")
    except Exception as e:  # noqa: BLE001
        return _error(e)

    transfer = next((t for t in data.get("transfers", []) if t.get("id") == params.transfer), None)
    if transfer is None:
        ids = ", ".join(t.get("id", "?") for t in data.get("transfers", []))
        return f"Error: unknown transfer '{params.transfer}'. Available: {ids}."

    wanted = [params.provider.lower()] if params.provider else ["aws", "azure", "gcp"]
    results: dict[str, Any] = {}
    for prov in wanted:
        rate = (transfer.get("rates") or {}).get(prov)
        if not rate:
            results[prov] = {"error": f"No {prov} rate published for '{params.transfer}'."}
            continue
        entry: dict[str, Any] = {"note": rate.get("note", ""), "source": rate.get("src", "")}
        ladder = parse_tiers(rate["tiers"]) if rate.get("tiers") else None
        if ladder:
            entry.update(walk_ladder(ladder, params.gb))
        else:
            # headline like "$0.01 /GB" → flat rate; otherwise report verbatim
            m = re.match(r"\$([\d.]+)\s*/\s*(GB|GiB)", rate.get("headline", ""))
            if m:
                usd = float(m.group(1))
                entry.update({
                    "totalUSD": round(usd * params.gb, 2),
                    "breakdown": [{"band": "Flat rate", "volumeGB": params.gb, "usdPerGB": usd, "cost": round(usd * params.gb, 2)}],
                })
            else:
                entry["unpricedHeadline"] = rate.get("headline", "—")
        if "totalUSD" in entry and params.gb:
            entry["effectiveUsdPerGB"] = round(entry["totalUSD"] / params.gb, 4)
        results[prov] = entry

    return _dumps({
        "transfer": params.transfer,
        "transferLabel": transfer.get("label"),
        "volumeGB": params.gb,
        "generated": data.get("generated"),
        "results": results,
        "disclaimer": (
            "Headline list prices from the Egress Cost Map "
            f"({BASE_URL}/egress/). Free tiers and same-region exemptions are "
            "applied where the ladder encodes them, but CDN routing, "
            "committed-use deals and enterprise discounts are not."
        ),
    })


@mcp.tool(
    name="infraatlas_get_regions",
    annotations={
        "title": "List cloud regions",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def infraatlas_get_regions(params: RegionsQuery) -> str:
    """List GA cloud regions across AWS, Azure, GCP, OCI and OVHcloud with
    city, country, geography and coordinates (curated, vendor-verified).

    Returns JSON:
    { "source": str, "generated": str, "total": int,
      "regions": [{provider, code, name, city, country, area,
                   lat, lng, availabilityZones, since}] }
    """
    try:
        data = await _fetch_json("/regions/data.json")
    except Exception as e:  # noqa: BLE001
        return _error(e)

    rows = []
    needle = params.query.lower() if params.query else None
    for city in data.get("cities", []):
        if params.area and city.get("area", "").lower() != params.area.lower():
            continue
        for region in city.get("regions", []):
            if params.cloud and region.get("p") != params.cloud.value:
                continue
            if needle and not any(
                needle in str(v).lower()
                for v in (city.get("city"), city.get("country"), region.get("code"), region.get("name"))
            ):
                continue
            rows.append({
                "provider": region.get("p"),
                "code": region.get("code"),
                "name": region.get("name"),
                "city": city.get("city"),
                "country": city.get("country"),
                "area": city.get("area"),
                "lat": city.get("lat"),
                "lng": city.get("lng"),
                "availabilityZones": region.get("az"),
                "since": region.get("since"),
            })

    rows.sort(key=lambda r: (r["provider"] or "", r["code"] or ""))
    return _dumps({
        "source": f"{BASE_URL}/regions/data.json",
        "generated": data.get("generated"),
        "total": len(rows),
        "regions": rows,
    })


@mcp.tool(
    name="infraatlas_whats_changed",
    annotations={
        "title": "Cloud catalogue change feed",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def infraatlas_whats_changed(params: ChangesQuery) -> str:
    """What changed in the cloud compute catalogues lately — regions and
    instance families added or removed, as detected by the daily refresh.

    Returns JSON:
    { "source": str, "windowDays": int, "count": int,
      "entries": [{ts, instrument, kind, text}] }
    """
    try:
        data = await _fetch_json("/feed.json")
    except Exception as e:  # noqa: BLE001
        return _error(e)

    cutoff = (datetime.date.today() - datetime.timedelta(days=params.days)).isoformat()
    entries = [
        e for e in data.get("entries", [])
        if e.get("ts", "") >= cutoff
        and (params.instrument is None or e.get("instrument") == params.instrument)
    ]
    return _dumps({
        "source": f"{BASE_URL}/feed.json",
        "windowDays": params.days,
        "count": len(entries),
        "entries": entries,
    })


def main() -> None:
    """Entry point for the `infraatlas-mcp` console script (stdio transport)."""
    mcp.run()


if __name__ == "__main__":
    main()
