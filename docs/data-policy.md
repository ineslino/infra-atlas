# Infra Atlas — Data Policy

What counts as "a region", what counts as "available", where the data comes
from, and how often it refreshes. This document exists so those are *decisions*,
not accidents — and so "the site says 34 AWS regions but AWS says 39" can be
answered without re-litigating it every time.

_Last reviewed: 2026-05-16._

## 1. Region inclusion

**The site counts commercial, standard-partition, generally-available (GA)
regions only.**

| Class | Included? | Why |
|-------|-----------|-----|
| Commercial / standard partition, GA | **Yes** | The default cloud every engineer can deploy to with an ordinary account. |
| GovCloud / Government partitions (AWS GovCloud, Azure Government, OCI OC2/OC3/OC4/OC10) | No | Separate partitions, eligibility-gated, separate accounts. Not comparable in a general cross-cloud reference. |
| China partitions (AWS China, Azure operated by 21Vianet) | No | Operated by separate legal entities; separate accounts and consoles. |
| Sovereign / EU-sovereign partitions (AWS European Sovereign Cloud, OCI OC19) | No | Distinct partitions with their own eligibility. |
| Announced / "coming soon" / preview regions | No | Not yet deployable. Added only when the vendor's authoritative region doc lists them as GA. |

**This is why the counts look lower than vendors' marketing headlines:**

| Provider | Site shows (commercial GA) | Vendor's "all" headline | Difference |
|----------|----------------------------|--------------------------|------------|
| AWS   | 34 | 39 | + 2 GovCloud, 2 China, 1 European Sovereign Cloud |
| Azure | 56 | 67 GA | + 5 Government, 6 China |
| GCP   | 43 | 43 | (GCP has no separate partitions) |
| OCI   | 45 | 55 | + 8 Government, 2 EU Sovereign |
| OVH   | 15 | — | OVH counts *datacenters* (46) separately; the site counts Public Cloud regions |

The site should **label region counts as "commercial regions"** in UI copy so
the difference is self-explanatory. The non-commercial regions are recorded (in
`tasks/features-2026-05/integrity/region-audit.csv`) but not displayed.

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
