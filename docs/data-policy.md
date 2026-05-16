# Infra Atlas — Data Policy

What counts as "a region", what counts as "available", where the data comes
from, and how often it refreshes. This document exists so those are *decisions*,
not accidents — and so "how many regions, counting which partitions" has one
settled answer instead of being re-litigated every time.

_Last reviewed: 2026-05-16._

## 1. Region inclusion

**The Region Map shows every generally-available (GA) region across all
partitions — commercial, GovCloud/Government, China, and sovereign.** Each
region carries its partition in its code and name, so a reader sees the full
footprint, not just the slice their own account happens to reach.

| Class | On the Region Map? | Notes |
|-------|--------------------|-------|
| Commercial / standard partition, GA | **Yes** | The default cloud, reachable with an ordinary account. |
| GovCloud / Government (AWS GovCloud, Azure Government & DoD, OCI OC2/OC3/OC4/OC10) | **Yes** | Eligibility-gated, separate account types — labelled as such. |
| China (AWS China, Azure operated by 21Vianet) | **Yes** | Operated by separate legal entities — labelled as such. |
| Sovereign (AWS European Sovereign Cloud, OCI OC19 EU Sovereign) | **Yes** | Distinct partitions — labelled as such. |
| Announced / "coming soon" / preview | No | Not yet deployable. Added only when the vendor's authoritative doc lists it GA. |

**This reconciles with vendors' headline counts:**

| Provider | Region Map total | = commercial + gated partitions |
|----------|------------------|---------------------------------|
| AWS   | **39** | 34 commercial + 2 GovCloud + 2 China + 1 European Sovereign Cloud |
| Azure | **67** | 56 commercial + 5 Government + 6 China |
| GCP   | **43** | 43 commercial — GCP has no separate partitions |
| OCI   | **55** | 45 commercial + 8 Government + 2 EU Sovereign |
| OVH   | **15** | 15 Public Cloud regions (OVH's 46 *datacenters* are a separate physical count) |

> Decision (2026-05-16): show all partitions. AWS's public "39 Geographic
> Regions" headline includes GovCloud + China + the European Sovereign Cloud;
> the Region Map matches that and applies the same all-partitions basis to every
> provider. Gated regions are labelled (GovCloud / China / Sovereign) so a
> reader can tell what needs a separate account type.

**Scope caveat — the compute instruments are commercial-only.** The Region Map
covers all partitions, but the `ec2`, `azure-vm` and `oci-compute` instruments
cover **commercial regions only**: their public data sources (the Vantage
dataset, the Azure Retail Prices API, the Oracle price list) carry no
GovCloud/China/sovereign pricing. This asymmetry is data-driven, not an
oversight, and is footnoted on those instruments.

OVH note: OVHcloud uses "region" and "datacenter" inconsistently. The site
counts **OVH Public Cloud regions** (the deployment locations the Public Cloud
product exposes), not physical datacenters. Local Zones are a separate edge tier
and are excluded.

## 2. Definition of "available"

A region or feature is **GA** when it is listed as generally available in the
vendor's **authoritative documentation** — not a press release, not a blog
announcement, not a "coming soon" marker. Authoritative sources:

| Provider | Authoritative region source |
|----------|------------------------------|
| AWS   | https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html |
| Azure | https://learn.microsoft.com/en-us/azure/reliability/regions-list |
| GCP   | https://cloud.google.com/about/locations · https://cloud.google.com/compute/docs/regions-zones |
| OCI   | https://docs.oracle.com/en-us/iaas/Content/General/Concepts/regions.htm |
| OVH   | https://www.ovhcloud.com/en-ie/public-cloud/regions-availability/ |

Marketing/press pages may be used for *context* (e.g. launch dates) but never as
the sole basis for listing a region.

## 3. Instance / SKU availability

Per-instrument compute data comes from each instrument's documented source:

| Instrument | Source | Notes |
|------------|--------|-------|
| `ec2` | ec2instances.info dataset (Vantage), public, no credentials | Per-region family membership is best-effort from the dataset; `ec2/refresh.sh` carries a `REGION_FAMILY_OVERRIDES` table for regions the dataset is known to over-claim. |
| `azure-vm` | Azure Retail Prices API (public) | Lists regions with VM pricing — a subset of all regions. |
| `oci-compute` | Oracle public price list | Lists regions with priced compute shapes — a subset. |
| `ovh-instances` | OVHcloud public order catalogue | |
| `gcp-compute` | **Curated** — hand-maintained in `index.html` | No credential-free GCP price/SKU API. |

Per-region instance availability is **not** independently audited against each
vendor's offerings API (`describe-instance-type-offerings` and equivalents
require credentials; the project is credential-free by design). Treat per-region
family lists as best-effort. SKU-level availability claims (e.g. confidential-VM
SKUs, specific GPU shapes) are curated and dated, not live-verified.

## 4. Refresh cadence and monitoring

| Instrument(s) | Mechanism | Cadence |
|---------------|-----------|---------|
| `ec2`, `azure-vm`, `oci-compute`, `ovh-instances` | `refresh.sh` pulls a public API/dataset | Daily 06:00 UTC (`refresh.yml`) |
| `regions`, `gcp-compute` | **Curated** — `refresh.sh` only re-serialises the hand-maintained const in `index.html` and re-stamps the timestamp | Data changes only when a human edits `index.html` |
| APIM + cross-cloud instruments (`apim-matrix`, `apigee`, `mulesoft`, `aws-api-gateway`, `self-hosted-apim`, `equivalent-sku`, `kubernetes`, `compliance`, `confidential-computing`, `iam-matrix`) | Static, hand-curated, dated snapshots | Updated by hand; carry a visible snapshot date |

**Do not describe `regions` or `gcp-compute` as "refreshed daily from public
datasets"** — they are curated. Site copy must distinguish *live-API* instruments
from *curated* ones (the APIM/cross-cloud pages already do this correctly).

### Guards

| Guard | What it checks | When |
|-------|----------------|------|
| `verify-data.yml` → `verify` job | `data.json` matches `index.html` for `regions`, `gcp-compute` (faithful re-serialisation) | every push / PR |
| `verify-data.yml` → `region-drift` job | `regions/data.json` region set matches the dated, vendor-verified `regions/region-reference.json` | every push / PR |
| `verify-freshness.yml` | Curated cross-cloud matrices' snapshot dates are within 180 days | monthly + manual |

### Re-verification duty

The hand-curated region set has no live upstream feed, so it is pinned to
`regions/region-reference.json` — a snapshot verified against the Section 2
sources, carrying a `verified` date. **Periodically** (the guard warns past 180
days) a maintainer must re-check the region lists against the vendor docs and,
if anything changed, edit `regions/index.html`, run `./regions/refresh.sh`, then
`python3 scripts/check_region_drift.py --update`, and commit. The `verified`
date is an assertion that this happened.

A future enhancement (tracked in the feature roadmap) is a public drift
dashboard showing each instrument's last-verified date and any open drift.

## 5. Corrections

Wrong data is a bug. Spotted something off? Open an issue with the upstream
source that contradicts the site. See `CONTRIBUTING.md`.
