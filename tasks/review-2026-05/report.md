# Infra Atlas — Full Review · 2026-05-16

**Scope:** homepage + 11 instrument pages, 4 axes (UI/UX, functionality, data accuracy, features).
**Method:** repo as source of truth (`origin/main` == local `main` `79e9ee1` — live site reflects the repo); local server for UI; 6 parallel research agents for data accuracy, every claim cited.
**Companion files:** `accuracy-audit.csv` (39-row drift table), `feature-shortlist.md` (top-5), `../lessons.md` (recurring patterns).

## Sanity-check notes (mission assumptions vs repo)

- The mission referenced `claude.md`, `progress.md`, `session_summary.md`, `tasks/`, `lessons.md` — **none existed**; this is a flat static site. `progress.md` / `session_summary.md` / `tasks/` created per the agreed plan.
- No build/lint/typecheck (static HTML/CSS/JS). "Tests pass" reframed as a coverage finding (A2-3).
- Live site == repo, so findings apply to production.

## Summary — findings by severity

| Axis | P0 | P1 | P2 | P3 |
|---|---|---|---|---|
| 1 — UI/UX | 1 | 0 | 5 | 1 |
| 2 — Functionality | 0 | 0 | 3 | 1 |
| 3 — Data accuracy | 1 | 13 | 10 | 8 |
| **Total** | **2** | **13** | **18** | **10** |

**Headline:** Two P0s — (1) the footer "GitHub / open an issue / contributor guide" links are dead `href="#"` while the site positions itself as open and MIT-licensed (and the repo is currently private); (2) EC2 Observatory's Melbourne region over-claims instance availability ~2×, so the site's core promise — "which region offers what" — is wrong where it matters most. The data-accuracy axis is where the real risk lives: a recurring **staleness + mislabel** pattern across EC2, GCP, Azure, OCI and the APIM pages (see `lessons.md`). The APIM atlas pages additionally carry **invented** data (a fabricated Apigee pricing tier, AWS pricing numbers not in any AWS doc). UI/UX and functionality are otherwise solid — fast (LCP 120–344 ms), responsive, real permalink + refresh infrastructure.

---

## Axis 1 — UI/UX

**P0 · A1-1 · `index.html:1227`, `apim-matrix/index.html:430`, `aws-api-gateway/index.html:690`** — Five footer links are `href="#"` (GitHub, "Open an issue" ×2, "Read the contributor guide", "Spotted a stale fact?"). *Why it matters:* the site's whole positioning is "open, free, contribute" — dead links on that exact promise read as abandoned/untrustworthy on a public site. *Root cause, not band-aid:* the links have no targets because there is **no public repo to point at** (the GitHub repo is private). *Fix:* decide the actual model — either make the repo public and wire all five links to real `github.com/<org>/infraatlas` URLs (repo, `/issues/new`, `CONTRIBUTING.md`), or remove the open-source/contribution claims. Don't ship `#`.

**P2 · A1-2 · all 12 pages** — No skip-link. Keyboard users tab through the full nav (brand + Instruments/⌘K button, then page filters) on every page. *Fix:* add a visually-hidden `<a class="skip" href="#results">Skip to content</a>` as the first body child, shown on `:focus`; nav.js is the natural place since it already injects the header.

**P2 · A1-3 · `index.html`, `apim-matrix`, `aws-api-gateway`, `apigee`, `mulesoft`, `self-hosted-apim`** — No `<main>` landmark (the 5 cloud pages + regions have one). *Why:* screen-reader users lose "jump to main content." *Fix:* wrap the primary content of those 6 pages in `<main>`.

**P2 · A1-4 · CSS custom properties, all pages** — Muted text fails WCAG AA contrast. `--paper-3` = cream at 0.42 alpha over `--ink` computes to ≈ **3.7:1** (AA normal text needs 4.5:1); `--paper-4` at 0.20 alpha ≈ **1.7:1**. These are used for mono meta/label/eyebrow text site-wide. *Fix:* raise `--paper-3` to ≥ 0.55 alpha (≈ 4.6:1) for any text ≥ ~13px; reserve `--paper-4` for non-text decoration only (corner marks), never copy.

**P2 · A1-5 · `ec2/index.html` (and likely all data pages)** — EC2 Observatory **CLS 0.23** (Chrome trace; "good" is < 0.1). LCP is fine (120 ms). *Root cause:* the page renders embedded fallback data immediately, then `data.json` (≈1,338 rows vs 791 embedded) loads and re-renders a much longer list → large layout shift. *Fix:* render `data.json`-first with a fixed-height skeleton/min-height on `#results`, or reserve space so the upgrade doesn't reflow. Home & APIM Matrix CLS = 0 (no async data).

**P2 · A1-6 · whole site** — No light mode / theme toggle (dark-only). Flagged P2 per mission. *Fix (optional):* the palette is all CSS variables — a `prefers-color-scheme: light` block is feasible; or document dark-only as a deliberate editorial choice.

**P3 · A1-7 · `aws-api-gateway`, `apigee`, `mulesoft`, `self-hosted-apim`** — These 4 editorial pages define no `:focus` styles (grep: 0); interactive elements rely on the browser default ring, which is low-contrast on the dark bg. *Fix:* a shared `:focus-visible` outline rule (coral, 2px).

**Positive:** Perf is excellent — LCP home 344 ms / EC2 120 ms / APIM Matrix 126 ms; CLS 0 on home & APIM. Responsive at 375 px (regions map correctly collapses behind a toggle). Empty states (`.empty` "Nothing matches.") and error states (`loadData` falls back to embedded on fetch failure) are handled. Editorial tone is consistent.

---

## Axis 2 — Functionality

**P2 · A2-1 · `index.html` colophon ("Data" section)** — Claims "Every instrument refreshes daily from public APIs." `.github/workflows/refresh.yml` refreshes **6** instruments (ec2, regions, azure-vm, gcp-compute, oci-compute, ovh-instances); the **5 APIM instruments are static** — the workflow's own comment says so, and their colophons say "Snapshot May 2026." *Why:* "every instrument" is false, and the APIM pages are exactly the ones the accuracy audit found most stale. *Fix:* reword to "Cloud-compute instruments refresh daily; APIM references are dated snapshots."

**P2 · A2-2 · `gcp-compute/refresh.sh` + `refresh.yml`** — `gcp-compute` is in the daily-refresh matrix but has **no live data source** ("curated — no credential-free price source"); its `refresh.sh` only re-extracts `data.json` from `index.html`. So "daily refresh" is a no-op for GCP — the C4A region list being 21 regions stale (A3) is the direct symptom. *Fix:* either wire a real GCP source or move gcp-compute out of the "refreshes daily" framing and treat it like the curated `regions` instrument.

**P2 · A2-3 · `scripts/`, `.github/workflows/`** — Test coverage is minimal. One unit test (`test_diff_feed.py`, feed-diff only) + `verify-data.yml` (checks `data.json` matches `index.html` for 2 instruments — an artifact-sync check, not correctness). The interactive JS — filtering, rendering, drawers, Cmd-K, compare mode, the region recommender, permalinks — is **entirely untested**. *Fix:* add a small Playwright/Vitest pass over the core render + filter paths; even smoke tests would have caught the EC2 CLS regression.

**P3 · A2-4 · repo root** — No `404.html`; unknown URLs fall to Cloudflare's unbranded default 404. *Fix:* add a branded `404.html` (the editorial tone makes this cheap and on-brand).

**Positive:** Filter state **is** URL-encoded (hash permalinks on all 7 data pages) — shareable. Filters, drawers, cross-references, the ⌘K palette, compare mode and the region recommender all function with **zero console errors** across all 12 pages. The daily-refresh cron is real, scheduled, and genuinely credential-free (`permissions: contents: write` only) — the "updated daily" claim is true for the 6 data instruments. The `data.json` `generated` timestamp is honest.

---

## Axis 3 — Data accuracy

Full 39-row drift table: **`accuracy-audit.csv`**. Every row cites an upstream URL, verified 2026-05-16. Headlines:

- **P0 — EC2 ap-southeast-4 (Melbourne):** `data.json` claims 59 instance families; AWS lists 31. ~30 false positives (t3a, m5n, c5n, r5n and most a/n/d/zn variants) **and** 2 false negatives (trn1/trn2 — Melbourne's only accelerated instances, missing). Root cause: per-region `in` membership isn't derived from AWS's authoritative regional doc. Other newer regions (ap-east-2, ap-southeast-6/7, mx-central-1) should be re-verified the same way.
- **P1 ×13** — concentrated in two patterns: (a) **stale region lists / catalogues** — GCP C4A 6 regions vs 27, OVH Instance Catalogue missing Paris, Azure confidential one generation behind; (b) **`vendor` field = host-CPU mislabels** — Azure NDv4 (Intel→AMD), OCI BM.GPU.B200.8 & H100.8 (AMD→Intel) — these break the Intel/AMD filter facet. Plus the APIM pages: a **fabricated** Apigee "Enterprise Plus Plus" tier and calls/day pricing model; Apigee FedRAMP understated (Moderate→High); the AWS REST "29-second hard timeout" gotcha stale since June 2024 (now an adjustable soft quota); AWS REST pricing numbers ("$1.51 above 20B") that exist in no AWS doc; Kong `oauth-ac` mislabels the free OSS `oauth2` plugin as Enterprise (and contradicts the adjacent cell); MuleSoft's pervasive "Flex Replica" — a SKU that does not exist.
- **Verified correct** (worth stating): Azure's SGX-vs-SEV-SNP confidential split; OCI B200 is genuinely GA; OVH's Local-Zone exclusion policy; us-east-1 / eu-west-1 EC2 availability; most Kong/Azure matrix cells.

The APIM atlas pages (`apigee`, `mulesoft`, `aws-api-gateway`) carry the highest concentration of *invented* (not merely stale) data — they are static and have drifted/were never sourced.

---

## Axis 4 — Feature ideation

12 candidates generated and ranked — see **`feature-shortlist.md`**. Top 5: (1) Equivalent-SKU finder, (2) Kubernetes flavor atlas, (3) Compliance footprint per region, (4) Confidential-computing atlas, (5) IAM/identity matrix. All fit the "cross-referenced reference periodical" concept and reuse data the site already curates or that is publicly documented.

---

## Cross-cutting

See **`../lessons.md`**. The dominant pattern: **data staleness/error is systemic, not incidental** — it appears in every data instrument and undermines the headline "updated daily, free, open" promise. The refresh pipeline keeps *timestamps* fresh but not *correctness* (it has no upstream-accuracy validation), and the static APIM pages have no refresh at all.

## Verification gate

- [x] Every P0 has a proposed fix + referenced file (A1-1, A3 EC2 Melbourne).
- [x] Every accuracy finding has an upstream URL (`accuracy-audit.csv`, 39 rows).
- [x] Report is severity-sorted and scannable in < 30 min; detail offloaded to the CSV.
- [!] Breakpoint coverage: verified 375 px + desktop; tablet/4K assessed via responsive CSS, not screenshotted — stated honestly, not padded.
