# Spec — Egress & Data-Transfer Cost Map (candidate N1)

Buildable spec. Implementer should not need a second briefing.

## Goal

A new instrument: one footnoted, cross-provider table of the data-transfer costs
that quietly dominate cloud bills — internet egress (tiered), cross-AZ,
cross-region, NAT-gateway processing, and inter-cloud transfer — for AWS, Azure
and GCP. It targets the **#1 ranked unmet user pain** (`gaps.md` G1) and has no
free neutral competitor.

## Non-goals

- **Not a calculator.** No "enter your GB, get a number" — no stateful estimate
  inputs (`anti-list.md`). It is a *rate reference*, like the compute instruments.
- **Not invoiced cost.** List/published rates only; a standing "list price ≠
  invoiced price" footnote.
- **Commercial regions only** — consistent with the compute instruments'
  data-source coverage (`docs/data-policy.md` §1 scope caveat).
- Not committed-use / private-pricing deals.

## Data model & source ingestion

New instrument folder, same shape as `ec2/`:

```
egress/
  index.html      embedded EGRESS const (source of truth) + the UI
  data.json       generated artefact
  refresh.sh      regenerates data.json
```

**`data.json` schema:**
```
{ "generated": "...", "schemaVersion": 1, "currency": "USD",
  "providers": ["aws","azure","gcp"],
  "transfers": [
    { "key": "internet-egress", "label": "Internet egress (out)",
      "rates": { "aws": [ {"tierGB": 10240, "usd": 0.09}, ... ],
                 "azure": [...], "gcp": [...] },
      "notes": { "aws": "First 100 GB/mo free…", ... },
      "src":   { "aws": "https://…", ... } },
    { "key": "cross-az",        "label": "Cross-AZ, same region",      ... },
    { "key": "cross-region",    "label": "Cross-region, intra-cloud",  ... },
    { "key": "nat-processing",  "label": "NAT gateway data processing", ... },
    { "key": "inter-cloud",     "label": "To another cloud / internet", ... }
  ] }
```

**Ingestion (`refresh.sh`, credential-free):**
- **AWS** — AWS Price List Bulk API: `pricing.us-east-1.amazonaws.com/offers/v1.0/aws/index.json`
  → the `AWSDataTransfer` offer file. Verified credential-free, HTTP 200, dated.
  Python transform (same shape as `ec2/refresh.sh`) extracts the egress/transfer
  SKU dimensions.
- **Azure** — Retail Prices API `prices.azure.com/api/retail/prices` filtered to
  bandwidth/`Bandwidth` meters. Credential-free.
- **GCP** — **curated** in the embedded `EGRESS` const from
  `cloud.google.com/vpc/network-pricing` (small, stable set; GCP's billing API is
  key-walled — same constraint as `gcp-compute`). Carries a dated snapshot.
- `refresh.sh` runs in the daily `refresh.yml` for the AWS/Azure portion; the GCP
  portion is curated and only re-serialised.

## UI sketch

Masthead "Egress *Map.*" + subtitle. Then:
- **A reading note** (accent card): "Egress pricing is conditional — free tiers,
  same-region exemptions, CDN-routed discounts. Treat the table as the headline;
  the footnotes are the truth. List price, not invoiced price."
- **The matrix**: rows = the 5 transfer categories; columns = AWS · Azure · GCP;
  each cell = the headline rate + footnote markers. Tiered rates (internet
  egress) expand to show the tier breakpoints.
- **Filters**: provider (show/hide a cloud), transfer category.
- **Footnotes**: every conditional (free tier, same-region-free, Premium vs
  Standard tier for GCP) numbered and sourced.
- `generated` / verified date in the masthead status block.

## Filter / cross-reference behaviour

- URL-encoded filter state (deep-linkable), consistent with other instruments.
- Cross-links: from the Region Map (cross-region transfer), from the EC2/VM
  instruments (NAT note), and from the "NAT Gateway vs NAT instance" decision
  page (E1, #8). Registered in `nav.js` + ⌘K.

## Edge cases & empty/error states

- **Conditional pricing** — modelled as footnotes, never flattened into one
  number. Free tiers shown as a note on the cell.
- **GCP Premium vs Standard network tier** — two sub-rows (or a labelled note).
- **Refresh API failure** — `data.json` keeps the last good copy
  (`stale-while-revalidate` in `_headers`); the `generated` date shows staleness.
- **A provider with no published rate for a category** — explicit "—" / "not
  published" cell, never a guessed number (`lessons.md` L3).

## Verification strategy

- `verify-data.yml` — add `egress` to the index↔json sync check for the curated
  (GCP) portion.
- A sanity check in `refresh.sh`: assert each provider has all 5 transfer
  categories and rates are positive numbers; `::warning::` on a gap.
- `lessons.md` L4 risk (rate rot): the GCP curated rates carry a `<time
  datetime>` verified date; add `egress` to `verify-freshness.yml`.
- Manual: spot-check 3 headline rates against the vendor pricing pages.

## Docs to update on launch

- `nav.js` — register `/egress/` (Cloud Compute group, or a new "Cost" theme).
- `index.html` — new instrument card; bump the instrument count.
- `CONTRIBUTING.md` — the egress instrument's refresh model.
- `docs/data-policy.md` — note egress in the live-API instrument list.
- `_headers` — already covers `/*/data.json`; no change.

## Rollback plan

Self-contained instrument. Rollback = delete the `egress/` folder, remove the
`nav.js` entry and the landing-page card. No other instrument depends on it;
the shared AWS Price List plumbing is new code in `egress/refresh.sh` only.

## Note — sequencing with the Object Storage comparator

`ideation.md` N10 (object-storage tiers) shares the AWS Price List Bulk API
pipeline. If both are wanted, build them as **one "Cloud Cost Almanac"
instrument** (transfer + storage tiers) to avoid duplicating the ingestion code
(`vendor-surface.md`; MEMORY anti-duplication rule). This spec covers the
transfer half; the storage half is an additive second `transfers`-sibling array.
