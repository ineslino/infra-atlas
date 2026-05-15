# Price Overlay & "What Changed" Feed — Implementation Plan

> **For Claude:** Companion to `2026-05-15-price-overlay-and-feed-design.md`.
> Execute task-by-task; verify each before moving on.

**Goal:** Add per-instance-type price + vCPU + memory (with sort/filter) to all
five cloud-compute pages, and an auto-updating "What Changed" feed on the
landing page.

**Architecture:** A `specs` map (`{size: {vcpu, mem, price}}`) is added to every
`FAMILIES` entry, sourced live where a credential-free API exists (EC2, Azure,
OVH, OCI) and from a dated published snapshot where it does not (GCP). A pure
`diff_feed.py` run inside the daily refresh workflow appends change entries to a
committed `feed.json` that the landing page renders.

**Tech Stack:** Static HTML/CSS/vanilla JS, bash + python3 refresh scripts,
GitHub Actions, `curl`/`jq`.

**Verification model:** No test framework exists. "Tests" = run `refresh.sh`
locally, assert the JSON schema with a python check, spot-check 3–5 prices
against the provider's public pricing page. The diff script gets a real
synthetic-fixture test.

---

## Phase 1 — EC2 (reference implementation)

### Task 1.1: Extend `ec2/refresh.sh` to emit `specs`

**Files:** Modify `ec2/refresh.sh` (python transform, the family-build loop).

- In the per-instance loop, capture `inst["vCPU"]`, `inst["memory"]`, and
  `pricing[REF].get("linux",{}).get("ondemand")` where `REF = "us-east-1"`.
- Build `fams[key]["specs"][size] = {vcpu, mem, price}`; `price` is
  `float(ondemand)` rounded to 4 dp, or `null` when absent/`"N/A"`.
- Emit `specs` in each family dict; add top-level `"currency":"USD"`,
  `"priceRef":"us-east-1"`.

**Verify:** `./ec2/refresh.sh` runs clean; then
`python3 -c "import json; d=json.load(open('ec2/data.json')); f=[x for x in d['families'] if x['key']=='m5'][0]; print(d['currency'], d['priceRef'], f['specs']['large'])"`
→ expect `USD us-east-1 {'vcpu': 2, 'mem': 8, 'price': 0.096}`.

### Task 1.2: Regenerate the EC2 embedded fallback

**Files:** Modify `ec2/index.html` (the `FAMILIES` const, ~lines 1115–1491;
`SNAPSHOT_DATE`).

- Generate a JS `FAMILIES` literal from the fresh `ec2/data.json` (python
  script, one-off) and replace the embedded const. Keep the `in:"*"` compaction
  where a family is in every region. Bump `SNAPSHOT_DATE`.

**Verify:** page loads with `data.json` blocked (rename it) → counts non-zero,
prices visible from the embedded fallback.

### Task 1.3: Instance-row price UI

**Files:** Modify `ec2/index.html` — `.instance-row` CSS + `renderInstanceView`.

- Add a `priceOf(fam,size)` helper: `fam.specs?.[size]?.price ?? null`.
- Row right-hand block becomes: price (`$0.096`, accent, `--mono`, ~15px) above
  a `2 vCPU · 8 GB · 31 regions` line (`--paper-3`, ~10px). `—` when price null.
- Add `.instance-row__price` CSS consistent with the existing type scale.

**Verify:** By Instance view shows a price on every row; null-price rows show
`—` without layout break.

### Task 1.4: Sort control

**Files:** Modify `ec2/index.html` — filters markup, `state`, `renderInstanceView`,
`init`, `applyHash`/`writeHash`.

- Add a `<select id="sort">` (Name / Price ↑ / Price ↓ / vCPU / Memory) to the
  `.filters` bar. Add `.filter-sort` CSS.
- `state.sort = "name"`; sort `entries` accordingly (price/vcpu pull from
  `specs`; null sorts last). Persist `sort` in the hash.

**Verify:** each sort option reorders rows correctly; null prices sink to the
bottom; sort survives reload via the hash.

### Task 1.5: Price-tier filter

**Files:** Modify `ec2/index.html` — filter-chips markup, `state`,
`renderInstanceView`, `init`, hash.

- Add a "Price" chip group: `Any / < $0.25 / $0.25–1 / $1–4 / ≥ $4`
  (`data-tier="any|0|1|2|3"`).
- `state.priceTier = "any"`; filter entries by tier in `renderInstanceView`.
  Persist in hash.

**Verify:** each tier narrows the list to the right band; `Any` restores all.

### Task 1.6: Instance drawer price

**Files:** Modify `ec2/index.html` — `openInstanceDrawer` meta row.

- Add `vCPU`, `Memory`, `Price` to `.drawer__meta` using the opened size's spec.

**Verify:** opening any instance row shows the three values in the drawer.

### Task 1.7: Commit Phase 1

`git add ec2/ docs/plans/` → commit `add price + vCPU/memory overlay to EC2`.

---

## Phase 2 — Azure, OVH, OCI (live pipelines)

For each cloud: (a) rewrite `refresh.sh` to fetch+merge, (b) add `specs` to the
embedded `FAMILIES`, (c) port the Phase 1 UI (Tasks 1.3–1.6) verbatim — the
pages are structurally identical, so the diff is mechanical.

### Task 2.1: Azure `refresh.sh`

**Files:** Rewrite `azure-vm/refresh.sh`.

- Extract `FAMILIES`/`REGIONS` from `index.html` (reuse the existing
  `extract_array` parser).
- Page `prices.azure.com/api/retail/prices` with
  `$filter=serviceName eq 'Virtual Machines' and armRegionName eq 'westeurope' and priceType eq 'Consumption'`,
  `$top=1000`, following `NextPageLink`.
- Build `armSkuName → retailPrice`, skipping items whose `productName` contains
  `Windows` or `skuName` contains `Spot`/`Low Priority`.
- For each family size, resolve its Azure SKU (`Standard_<size>`), set
  `specs[size].price`; keep curated `vcpu`/`mem` (added in Task 2.2).
- Write `data.json` with `currency:"USD"`, `priceRef:"westeurope"`.

**Verify:** spot-check `D4s_v5`, `B2s`, `E8s_v5` prices against
`azure.microsoft.com/pricing/details/virtual-machines/linux/`.

### Task 2.2: Azure embedded `specs` (curated vCPU/memory + snapshot price)

**Files:** Modify `azure-vm/index.html` `FAMILIES`.

- Add `specs` per family with curated `vcpu`/`mem` and a snapshot `price`
  (taken from the Task 2.1 run). Bump `SNAPSHOT_DATE`.

### Task 2.3: Azure UI port — apply Tasks 1.3–1.6 to `azure-vm/index.html`.

### Task 2.4: OVH `refresh.sh`

**Files:** Rewrite `ovh-instances/refresh.sh`.

- Fetch `api.ovh.com/v1/order/catalog/public/cloud?ovhSubsidiary=IE`.
- For each base flavor addon (`planCode` matching `^<flavor>\.consumption$`),
  read `pricings[0].price` (µ€ → `/1e9` € — verify the divisor against
  `formattedPrice`), `blobs.technical.cpu.cores`, `blobs.technical.memory.size`.
- Match flavor → family size; fill `specs[size] = {vcpu, mem, price}`.
- Write `data.json` with `currency:"EUR"`, `priceRef:"GRA"`.

**Verify:** spot-check `b3-8`, `c3-8`, `d2-4` against `ovhcloud.com` Public
Cloud pricing; confirm the µ€ divisor (`275000000` ⇄ `"€ 2.75"` → divide by 1e8).

### Task 2.5: OVH embedded `specs` + UI port (Tasks 1.3–1.6).

### Task 2.6: OCI `refresh.sh`

**Files:** Rewrite `oci-compute/refresh.sh`.

- Fetch `apexapps.oracle.com/pls/apex/cetools/api/v1/products/?currencyCode=USD`.
- Build per-family OCPU/hr and GB/hr rates from `displayName` matches
  (e.g. `Compute - Standard - E5 - OCPU`).
- For each size (`"N OCPU"`): `ocpu=N`; `vcpu = N*2` (x86) or `N` (arm, by
  `family.arch`); `mem` from a curated per-family GB-per-OCPU ratio;
  `price = N*r_ocpu + mem*r_mem`, 4 dp.
- Write `data.json` with `currency:"USD"`, `priceRef:"us-ashburn-1"`.

**Verify:** spot-check `VM.Standard.E5.Flex` @ 8 OCPU and `VM.Standard.A1.Flex`
against `oracle.com/cloud/compute/pricing/`.

### Task 2.7: OCI embedded `specs` + UI port (Tasks 1.3–1.6).

### Task 2.8: Commit Phase 2

`git add azure-vm/ ovh-instances/ oci-compute/` → commit
`add price + vCPU/memory overlay to Azure, OVH, OCI`.

---

## Phase 3 — GCP (curated snapshot)

### Task 3.1: GCP snapshot specs

**Files:** Modify `gcp-compute/index.html` `FAMILIES`; `gcp-compute/refresh.sh`.

- For each family, take published per-vCPU/hr and per-GB/hr rates from
  `cloud.google.com/compute/all-pricing` (us-central1); derive each size's
  vCPU from its name, memory from the standard/highmem/highcpu ratio, and
  `price = vcpu*r_vcpu + mem*r_mem` (shared-core types e2-micro/small/medium
  get their flat published price). Record the snapshot date + source URL in a
  comment.
- `refresh.sh`: emit `currency:"USD"`, `priceRef:"us-central1"` (still curated;
  no live fetch).

**Verify:** spot-check `n2-standard-4`, `e2-medium`, `c3-highcpu-8` against the
GCP pricing page.

### Task 3.2: GCP UI port (Tasks 1.3–1.6).

### Task 3.3: Commit Phase 3

`git add gcp-compute/` → commit `add price + vCPU/memory overlay to GCP`.

---

## Phase 4 — "What Changed" feed

### Task 4.1: `diff_feed.py`

**Files:** Create `scripts/diff_feed.py`.

- CLI: `diff_feed.py <instrument> <old.json> <new.json> <feed.json>`.
- Compare families/sizes/regions sets and per-size `price`; emit entries for
  added/removed families, added/removed sizes, added/removed regions, and
  price moves > ±2 %.
- Append to `feed.json` (`{generated, entries[]}`), newest-first, cap 200.
- Missing/empty old file → exit 0, append nothing.

### Task 4.2: Test `diff_feed.py`

**Files:** Create `scripts/test_diff_feed.py`.

- Fixtures: identical (→ 0 entries), a size added, a region added, a price
  +10 % move, missing old file. Assert entry count + `kind` for each.

**Verify:** `python3 scripts/test_diff_feed.py` prints `OK`.

### Task 4.3: Wire into `refresh.yml`

**Files:** Modify `.github/workflows/refresh.yml`.

- Before the commit step: `git show HEAD:<inst>/data.json > /tmp/old.json` (tolerate
  failure), `python3 scripts/diff_feed.py <inst> /tmp/old.json <inst>/data.json feed.json`.
- `git add <inst>/data.json feed.json` in the commit step.

### Task 4.4: Seed `feed.json` + landing section

**Files:** Create `feed.json` (`{generated, entries:[]}`); modify `index.html`
(new section + CSS + fetch/render JS).

- A "What Changed" `<section>` after the instruments section; fetch `feed.json`,
  render newest ~15 entries grouped by date with instrument + kind tags; hide
  the section gracefully if the fetch fails or `entries` is empty.

**Verify:** locally serve the site; with a hand-seeded `feed.json` the section
renders; with `entries:[]` it is hidden.

### Task 4.5: Commit Phase 4

`git add scripts/ feed.json index.html .github/` → commit
`add "What Changed" feed — diff pipeline + landing section`.

---

## Final verification

- All 5 `refresh.sh` run clean and produce schema-valid `data.json`.
- All 5 pages: price on rows, sort, price filter, drawer — verified in a browser.
- `diff_feed.py` test passes.
- `git diff --stat` touches only the 5 cloud dirs, `scripts/`, `index.html`,
  `.github/`, `feed.json`, `docs/` — **not** `regions/`.
