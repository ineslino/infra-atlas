# Phase 1 — Inventory: what Infra Atlas is today

**Date:** 2026-05-16. Source: the repo + rendered site. Purpose — so Phase 4
ideation never proposes something that already exists.

## 1. The 16 instruments

Three classes. "Update" = how the data changes; see `docs/data-policy.md`.

### Cloud-compute data instruments (6)

| Instrument | Folder | Data source | Update | Filters / interaction |
|------------|--------|-------------|--------|------------------------|
| EC2 Observatory | `ec2` | ec2instances.info dataset (Vantage), public | `refresh.sh` daily 06:00 UTC | family, arch (x86/arm), vendor (Intel/AMD/Graviton), category, region; on-demand price; sort; region↔type cross-filter |
| Multi-Cloud Region Map | `regions` | **Curated** `CITIES` const in `index.html` | daily *re-serialise only* | world map; filter by provider + area; region recommender; compare. The one genuinely multi-provider instrument. |
| Azure VM Atlas | `azure-vm` | Azure Retail Prices API, public | daily | series, arch (Intel/AMD/Ampere/Cobalt), GPU class, confidential-compute; price; sort |
| GCP Compute Index | `gcp-compute` | **Curated** `FAMILIES`/`REGIONS` const | daily *re-serialise only* | family, arch, vendor |
| OCI Compute Observatory | `oci-compute` | Oracle public price list | daily | shape family, arch, VM/bare-metal |
| OVH Instance Catalogue | `ovh-instances` | OVHcloud public order catalogue | daily | range, family, VM/bare-metal |

### API-management instruments (5) — all curated, static

| Instrument | Folder | Form | In-body cross-links |
|------------|--------|------|---------------------|
| APIM Feature Matrix | `apim-matrix` | 7-vendor × ~28-capability matrix; filter category + vendor | — |
| AWS API Gateway Atlas | `aws-api-gateway` | editorial guide (REST/HTTP/WS) | → apim-matrix, regions |
| Apigee Atlas | `apigee` | editorial guide | → apim-matrix, aws-api-gateway |
| Mulesoft Atlas | `mulesoft` | editorial guide | → apigee, apim-matrix, aws-api-gateway |
| Kong · Gravitee · IBM | `self-hosted-apim` | self-hosted comparison guide | → apigee, apim-matrix, aws-api-gateway, mulesoft |

### Cross-cloud matrices (5) — curated; carry a visible snapshot date

| Instrument | Folder | Form | Data |
|------------|--------|------|------|
| Equivalent-SKU Finder | `equivalent-sku` | tool — pick an instance, get scored cross-cloud matches | **reuses the 5 compute instruments' `data.json` live, client-side** |
| Kubernetes Atlas | `kubernetes` | 5-service × 14-capability matrix | curated; `verify-freshness.yml` nags at 180 d |
| Compliance Footprint | `compliance` | 5-cloud × 11-program matrix | curated; verify-freshness |
| Confidential Computing | `confidential-computing` | 5-cloud × 5-technology matrix | curated; verify-freshness |
| IAM Matrix | `iam-matrix` | 4-provider × 21-capability matrix | curated; verify-freshness |

## 2. Information architecture

- **Landing page** (`index.html`): top rule (Issue No. + sync line) · hero (title, lead, 4 stat cards) · **Instruments** section in 3 "Departments" (Cloud Compute / API Management / Cross-Cloud) · a hidden **"What Changed"** feed section · tracked-providers strip · manifesto ("editor's letter") · colophon footer · signature line.
- **Shared nav** (`nav.js`, injected on every page): sticky bar with the contour-logo brand, a "here" breadcrumb, and an **Instruments ⌘K command palette** — fuzzy search over all 16 instruments in 3 groups + Home. Also injects a **skip-to-content** link.
- **Footer / colophon**: 3 columns — The Atlas / Data / Contribute. Contribute links → GitHub repo, new-issue, `CONTRIBUTING.md`.
- **404** (`404.html`): branded "off the map" page, includes `nav.js`.
- **Design system**: `:root` CSS tokens (ink/paper/accent palette), fonts Instrument Serif / JetBrains Mono / Manrope; dark, editorial. Replicated per page (no shared CSS file).

## 3. Global / shared mechanics

- `refresh.yml` — daily cron, refreshes the 4 live-API instruments; commits `data.json` + appends to `feed.json` via `scripts/diff_feed.py`.
- `verify-data.yml` — per-push: `data.json`↔`index.html` sync (regions, gcp-compute) + the new **region-drift guard**.
- `verify-freshness.yml` — monthly: curated-matrix snapshot-date staleness.
- `_headers` — Cloudflare: HTML cached 300 s; **`/*/data.json` served with `Access-Control-Allow-Origin: *`**; security headers (nosniff, X-Frame-Options DENY).
- `_ogcard.html`, `og.png` — social-card assets.

## 4. Implicit capabilities (the user may not realise these exist)

- **Every data instrument's `data.json` is a public, CORS-enabled JSON endpoint** (`/ec2/data.json`, etc.) — an unadvertised read-only API already exists.
- **Deep-linkable filter state** — all 12 interactive instruments use `URLSearchParams`/`history` state, so a filtered view is shareable by URL (permalinks).
- **Compare / pin mode** in the compute instruments and the region map.
- **⌘K command palette** — fast cross-instrument navigation, keyword-searchable.
- **Region recommender** in the Region Map.
- Per-page **OG/social cards**.

## 5. Implicit gaps (built-but-dormant, or claimed-but-missing)

- **"What Changed" feed is dormant** — `feed.json` is `{"generated":"","entries":[]}`. The landing section stays hidden until the daily diff populates it; it has produced nothing yet.
- **No RSS/Atom** — change data exists only as `feed.json` consumed by the landing page; not subscribable.
- **`data.json` API is undiscoverable** — CORS is on, but nothing links to or documents it. No CSV export anywhere.
- **Cloud-compute instruments are not cross-linked in-body** — only the APIM pages link to siblings. EC2 Observatory doesn't link to the Region Map or Equivalent-SKU Finder; the cross-cloud matrices don't link to each other.
- **No per-instrument "last verified" date that reflects ingestion** — pages show a `generated` timestamp (the *re-serialisation* time, misleading for curated instruments). `docs/data-policy.md` and `region-reference.json` now carry real `verified` dates, but they aren't surfaced on-page.
- **Repo-public dependency** — colophon "Open an issue" / "contributor guide" links and the manifesto's correction invite all point at `github.com/ineslino/infraatlas`; they only work once the repo is public.
- **Landing-page stat cards are hand-typed and stale** — see `integrity/data-audit.md` (EC2 "32 regions / ~700 types" vs 34 / 1338, etc.).
