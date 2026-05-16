# Phase 0b — Pipeline forensics: why the region data drifts

**Date:** 2026-05-16 · **Scope:** the refresh pipeline behind the region data, and the root cause of the drifts found in Phase 0a.

## TL;DR

The mission's premise — *"AWS shows 34, should be 39, a regression that wasn't corrected"* — **is not what the evidence shows.**

- **AWS 34 is correct.** All 34 are AWS *commercial* regions and every code matches AWS's own docs exactly. AWS's public **"39"** = 34 commercial + 2 GovCloud + 2 China + 1 European Sovereign Cloud. **34 vs 39 is a scope-definition difference, not stale data.** The prior fix (`63b8eba`, 32→34) brought AWS to the correct commercial count.
- The **real** drift is small and elsewhere — 3 issues, none in AWS:
  - **Azure**: phantom `taiwannorth` (announced, *not* GA) + missing `westcentralus` (real GA region, Wyoming).
  - **OCI**: missing `af-casablanca-1` (GA).
  - **OVH**: missing Mumbai (GA Public Cloud region).
- The deeper problem is **structural and process**, not a broken job (see below).

## How the refresh pipeline actually works

`refresh.yml` runs daily 06:00 UTC. It **does run** — `gh run list` shows one scheduled run on 2026-05-16 08:13 UTC, status *success*, 1m48s; it produced 6 `chore(<instrument>): refresh data` commits. It is **not** silently failing and the data **is** propagating.

But "refresh" means different things per instrument:

| Instrument | `refresh.sh` does | Genuinely tracks upstream? |
|------------|-------------------|----------------------------|
| `ec2` | Downloads the Vantage `instances.json` public dataset; derives the region list from regions that appear in the pricing map | **Indirect** — only as current as Vantage's dataset |
| `azure-vm` | Azure Retail Prices API (public) | Yes |
| `oci-compute` | Oracle public price list | Yes |
| `ovh-instances` | OVHcloud public order catalogue | Yes |
| `regions` | **Re-serialises a hand-curated `CITIES` const from `index.html`** | **No** |
| `gcp-compute` | **Re-serialises a hand-curated `FAMILIES`/`REGIONS` const** | **No** |

`regions/refresh.sh`'s own header says it: *"Region geography is curated in index.html… Update region data by editing index.html, then re-run."* A daily run of `regions/refresh.sh` re-extracts whatever a human last typed and bumps a timestamp. **It cannot discover a new region, a renamed region, or a phantom region.**

## Root cause of the Phase 0a drifts

**The `regions` instrument has no upstream-truth check. Its only data source is human transcription from vendor pages.** Both the original undercount *and* the incomplete corrections share this single cause:

1. A human reads vendor region pages and types entries into the `CITIES` const.
2. `refresh.sh` + `verify-data.yml` only guarantee `data.json` stays in sync with `index.html` — i.e. they verify the transcription was *copied* faithfully, never that it was *correct*.
3. So a missed region (OCI Casablanca, OVH Mumbai), a stale region (Azure `westcentralus` dropped), or a premature add (Azure `taiwannorth`, announced-not-GA) sails straight through CI.

Commit `63b8eba` ("Fix region-map undercounts… 32/51/42/36 → 34/56/43/44") is exactly this failure mode in action: a manual correction pass that fixed *most* of the gap but, being eyeball-driven, re-introduced/left a phantom and three misses. The fix was real; it was just unverifiable, so it was incomplete and nobody could tell.

This is the mission's fourth hypothesis — *"no automated refresh… the claim is aspirational"* — and it is **correct for the `regions` and `gcp-compute` instruments specifically.** For those two, "refreshes daily from public datasets" is misleading: they refresh from themselves.

## Secondary finding — the homepage claim

The landing page says the cloud-compute instruments "refresh daily from public datasets and price APIs." True for `ec2`/`azure-vm`/`oci-compute`/`ovh-instances`; **not true for `regions` and `gcp-compute`**, which are curated. The copy should distinguish "live-API" instruments from "curated, dated-snapshot" instruments (the APIM/cross-cloud pages are already correctly described as curated).

## Process observations

- The project is ~1 day old (v1 = 2026-05-15); the scheduled refresh has run **once**. "Daily" is correct mechanically but barely exercised — there is no monitoring/alerting on a failed or skipped run yet.
- `verify-data.yml` covers only `regions` + `gcp-compute` for index↔json sync. There is **no check of any kind that site data matches upstream reality.** That is the guard Phase 0d adds.
- Process note (out of scope but worth recording): commit `63b8eba` carries a `Co-Authored-By: Claude` trailer, which violates the project's no-AI-attribution rule. Unrelated to data integrity, flagged for a separate history cleanup.

## What Phase 0 should therefore deliver

Not "fix a big AWS bug" (there isn't one) but:
1. **0d** — correct the 3 real drifts (Azure swap, OCI Casablanca, OVH Mumbai) and add a **drift guard** that compares site region counts/codes to a reference and fails loudly.
2. **0e** — a written **inclusion policy** (`docs/data-policy.md`) so "commercial only" is a documented decision and "34 vs 39" can't be re-litigated.
3. On-site: a scope label ("34 commercial regions") and honest per-instrument refresh wording.
