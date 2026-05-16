# Spec — Expose the public `data.json` API (candidate X1)

Buildable spec. Implementer should not need a second briefing.

## Goal

Turn an asset the site *already has* into a documented, discoverable feature.
Every data instrument already serves `data.json` with
`Access-Control-Allow-Origin: *` (set in `_headers`). Document those endpoints,
make them discoverable, and state their stability contract — so tool-builders
can consume Infra Atlas data instead of re-scraping vendor docs.

## Non-goals

- **No backend, no new runtime** — the site stays static; these are flat files.
- **No auth, no API keys, no rate limiting, no SLA** — it is a reference, not a
  product (`anti-list.md`).
- No new endpoints or query parameters — the existing `data.json` files only.
- No GraphQL / no versioned URL routes.

## Data model & source ingestion

No new data. Two small additions to existing artefacts:

1. **`schemaVersion` field** — add a top-level `"schemaVersion": 1` to each
   instrument's `data.json`. Implement in each `refresh.sh` (one line in the
   output dict) so it survives the daily refresh. For curated instruments, add
   it to the generator. This lets a consumer detect a breaking change.
2. **No other data change.** The `_headers` CORS rule is already correct.

The 6 data endpoints (already live):
`/ec2/data.json`, `/regions/data.json`, `/azure-vm/data.json`,
`/gcp-compute/data.json`, `/oci-compute/data.json`, `/ovh-instances/data.json`.
(`feed.json` is also public and worth listing.)

## UI sketch

**New page `api/index.html`** — masthead "The *Data*." (or "API"). Body:
- Intro: "Every data instrument publishes its dataset as JSON. CORS-enabled,
  free, no key. Build on it."
- **Endpoint table** — one row per instrument: name · URL (clickable) ·
  one-line description · `generated` cadence (daily / curated).
- **Stability contract box** — explicit: "Best-effort. The schema *can* change;
  watch `schemaVersion`. No uptime guarantee, no SLA, no rate limit — be kind.
  Cached ~1 h at the edge."
- **Example** — a 4-line `fetch()` snippet and a `curl | jq` snippet.
- **Schema** — for one representative instrument, the top-level shape
  (`generated`, `schemaVersion`, the data arrays) with field notes.

**Per-instrument link** — each instrument's masthead status block (or footer)
gets a small monospace `↗ data.json` link to its own endpoint.

## Filter / cross-reference behaviour

No filters. The `/api` page is registered in `nav.js` (in the colophon/utility
group, or its own ⌘K entry "Data & API"). The landing-page colophon "Data"
column links to `/api`. Each instrument cross-links to its endpoint.

## Edge cases & empty/error states

- **Schema change**: bump `schemaVersion`; note it in the corrections changelog
  (candidate D2) if built, else in the `/api` page's "changes" line.
- **An instrument with no `data.json`** (APIM / cross-cloud pages are static):
  simply not listed — the page is explicit that only data instruments expose JSON.
- **Stale data behind a failed refresh**: already handled by `_headers`
  (`stale-while-revalidate`); the `generated` timestamp tells the consumer.

## Verification strategy

- A CI check (extend `verify-data.yml`): for each listed endpoint, assert the
  file exists, parses as JSON, and carries `schemaVersion`.
- Assert the `/api` page lists exactly the instruments that have a `data.json`
  (no drift between the doc and reality).
- Manual: CORS works from a different origin (`fetch` from a scratch page).

## Docs to update on launch

- `nav.js` — register `/api/`.
- `index.html` — colophon "Data" column links to `/api`; optionally a hero stat.
- `CONTRIBUTING.md` — note that `data.json` is a public contract; schema changes
  must bump `schemaVersion`.
- Each `refresh.sh` / generator — emit `schemaVersion`.
- `README.md` — mention the API.

## Rollback plan

Lowest-risk candidate on the list. Rollback = delete `api/index.html`, remove
the `nav.js` entry and per-instrument links. The `data.json` files and CORS
header stay (instruments depend on them). `schemaVersion` is additive and
harmless if left.
