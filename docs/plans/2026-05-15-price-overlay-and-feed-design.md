# Wave 3 — Price Overlay & "What Changed" Feed — Design

Date: 2026-05-15
Status: validated, ready for implementation

## Context

Two features remain from the 7-feature plan. Both need data-pipeline work, not
just frontend. Waves 1–2 shipped at commit `575f74f`.

The 5 cloud-compute pages (`ec2`, `azure-vm`, `gcp-compute`, `oci-compute`,
`ovh-instances`) are structurally identical: a `FAMILIES` const where each entry
is `{ key, cat, arch, vendor, desc, sizes[], in }`. There is **no vCPU, memory,
or price field** anywhere. Only `ec2` has a live data pipeline (Vantage's
`instances.json`); the other four `refresh.sh` scripts bootstrap `data.json`
once from the embedded `FAMILIES` and then only bump a timestamp.

## Source verification (done up front)

All four candidate sources were hit live and confirmed credential-free:

| Cloud | Endpoint | Result |
|---|---|---|
| EC2 | `instances.vantage.sh/instances.json` | 1340 types; `vCPU`, `memory`, `pricing[region].linux.ondemand` all present (1302/1340 have us-east-1 price) |
| Azure | `prices.azure.com/api/retail/prices` | no-auth; `$top=1000`; `retailPrice` + `armSkuName` per region; filter to `Consumption`, drop Windows/Spot |
| OVH | `api.ovh.com/v1/order/catalog/public/cloud?ovhSubsidiary=IE` | 75 base hourly flavors; `pricings[].price` (µ€) + `blobs.technical.cpu/memory` |
| OCI | `apexapps.oracle.com/pls/apex/cetools/api/v1/products` | OCPU/hr + GB/hr unit rates per family (e.g. E5 = $0.03/OCPU, $0.002/GB) |
| GCP | — | needs an API key; **no free source** |

## Feature 1 — Price + spec overlay

### Decision: all five pages, all-or-nothing on *feature presence*

Every cloud page gains price + vCPU + memory per instance type, plus sort and
filter by price. Sourcing is heterogeneous (the spec prescribes a different
source per cloud, and EC2-live / others-curated heterogeneity already exists),
but the *feature* is uniform — no sibling page diverges on what the user sees.
A cloud whose live pipeline cannot be made correct falls back to a dated
snapshot for that cloud only; the feature still ships on all five.

### Data model

Add a `specs` object to each `FAMILIES` entry, keyed by size name:

```js
specs: { "<size>": { vcpu: <int>, mem: <number GB>, price: <number|null> } }
```

- `sizes` (string array) is left untouched — non-invasive, preserves order, no
  change to existing region/filter/drawer code. New code reads `f.specs?.[size]`.
- `price` is hourly on-demand in the cloud's native currency.
- `price: null` renders as "—" (graceful), but the target is full coverage.
- `data.json` gains, per file: `currency` ("USD" | "EUR") and `priceRef` (the
  reference region the price is quoted for).

### Sourcing per cloud (reference region in parens)

- **EC2** (us-east-1) — live. Extend the Vantage transform to also emit
  `specs` from `vCPU`, `memory`, `pricing[ref].linux.ondemand`.
- **Azure** (westeurope) — live, new. `refresh.sh` fetches the Retail Prices
  API, builds `armSkuName → retailPrice`, merges price into curated `specs`.
  vCPU/memory are curated (the API has no spec data).
- **OVH** (GRA) — live, new. `refresh.sh` parses the public catalog `addons`;
  each base flavor carries cpu, memory and hourly price. Currency: EUR.
- **OCI** (us-ashburn-1) — live, new. `refresh.sh` fetches OCPU/hr + GB/hr unit
  rates; per-shape price is *computed* `ocpu×r_ocpu + mem×r_mem` — this is how
  OCI actually bills flexible shapes. OCPU/memory curated (1 OCPU = 2 vCPU on
  x86, 1 vCPU on Ampere). Memory assumes the documented per-OCPU default.
- **GCP** (us-central1) — dated snapshot. No free API. Predefined machine
  types are priced by published per-vCPU/hr + per-GB/hr family rates; vCPU is
  in the type name, memory follows the standard/highmem/highcpu ratio — so
  `specs` is *derived* from real published rates, curated into the embedded
  data with a source URL and date. Not fake; just not auto-refreshing.

### refresh.sh changes

- `ec2/refresh.sh` — extend transform; add `currency`, `priceRef`.
- `azure-vm`, `oci-compute`, `ovh-instances` — rewrite: (1) extract curated
  `FAMILIES`/`REGIONS` from `index.html`, (2) fetch the public price API,
  (3) merge price into `specs`, (4) write `data.json`. Drop the
  `if [[ ! -f data.json ]]` bootstrap gate so edits to `index.html` propagate.
- `gcp-compute/refresh.sh` — stays curated; re-extracts `FAMILIES` (now
  carrying `specs`) and bumps the timestamp.

### Embedded fallback

Every page's embedded `FAMILIES` const gains `specs`. EC2's block is
regenerated from a live refresh run. Azure/OCI/OVH/GCP get curated
vCPU/memory + a snapshot price hand-added; the live refresh overwrites price
for the three API-backed clouds.

### UI (identical across all five pages)

- **Instance row** — right block stacks the price (prominent, accent colour)
  over a small `N vCPU · M GB · X regions` line. Grid stays `1fr auto`.
- **Sort** — a `<select>` in the filters bar: Name, Price ↑, Price ↓, vCPU,
  Memory. Default Name. Affects the instance view only.
- **Filter by price** — a "Price" chip group with native-currency tiers
  (`Any`, `< 0.25`, `0.25–1`, `1–4`, `≥ 4`), tuned per cloud.
- **Drawer** — instance drawer meta row gains vCPU / memory / price.
- `state` gains `sort` and `priceTier`; both persist in the permalink hash.

## Feature 2 — "What Changed" feed (option a)

### Diff pipeline

New `scripts/diff_feed.py`. The refresh workflow, after `refresh.sh`
regenerates `data.json` and before committing, runs the diff of the previous
committed `data.json` (`git show HEAD:<inst>/data.json`) against the new
working-tree file. It detects, per instrument:

- families added / removed
- instance types (sizes) added / removed
- regions added / removed
- price changes beyond a ±2 % threshold (enabled by Feature 1)
- availability changes (family in/out of a region) — summarised, not per-pair

Detected changes are appended to a root `feed.json`:

```json
{ "generated": "...", "entries": [
  { "ts": "2026-05-15", "instrument": "ec2", "kind": "instance-added",
    "text": "4 new c8g sizes" } ] }
```

Entries are capped to the newest ~200. Missing/first-run previous data → no
entries (handled gracefully, never crashes the workflow).

### Workflow change

`refresh.yml`: after the refresh step, run `scripts/diff_feed.py`, then
`git add <inst>/data.json feed.json` and commit both. The matrix is already
`max-parallel: 1` with `git pull --rebase --autostash`, so concurrent
`feed.json` appends serialise safely.

### Frontend

A new "What Changed" section on the landing `index.html`, after the
instruments section. Fetches `feed.json`, renders the newest ~15 entries
grouped by date, each tagged with instrument + kind, styled to the landing
page's editorial aesthetic. Hidden gracefully when `feed.json` is absent.

### Testing (addresses the flagged CI risk)

`diff_feed.py` is exercised locally against two synthetic `data.json` versions
before being wired into CI, covering: first run (no previous), no-change run,
and each change kind. The diff is pure (stdin/args in, `feed.json` out) so it
is trivially testable outside Actions.

## Build sequence

1. **EC2** — data model + `refresh.sh` + UI. Reference implementation.
2. **Azure / OVH / OCI** — live `refresh.sh` rewrites + curated specs + UI port.
3. **GCP** — curated snapshot + UI port.
4. **Feed** — `diff_feed.py` + workflow + landing section.

Each cloud is verified by running its `refresh.sh` locally and spot-checking
3–5 prices against the provider's public pricing page.

## Out of scope / non-goals

- Per-region price tables (one reference price per type only).
- Currency conversion (each cloud shown in its native currency).
- Reserved / spot / savings-plan pricing (on-demand only).
- Touching the `regions` instrument (has unrelated uncommitted local changes).
