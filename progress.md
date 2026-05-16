# Infra Atlas — Progress

A reference periodical of cloud + API-management infrastructure. Static site (HTML/CSS/JS, no build), deployed via GitHub → Cloudflare. 12 pages: landing + 11 instruments.

## State — 2026-05-16

- **Live & deployed.** `origin/main` == `main`; the live site reflects the repo.
- **Instruments (11):** EC2 Observatory, Region Map, Azure VM Atlas, GCP Compute Index, OCI Compute, OVH Instances, APIM Feature Matrix, AWS API Gateway Atlas, Apigee Atlas, Mulesoft Atlas, Self-hosted APIM.
- **Recent work:** shared ⌘K nav palette, filter permalinks, OG cards, region recommender, compare mode, EC2/Azure/OCI/OVH pricing, "What Changed" feed, region-map data corrections (186→191 regions), new contour logo.
- **Data pipeline:** daily `refresh.yml` cron (06:00 UTC, credential-free) refreshes the 6 data instruments; the 5 APIM instruments are static snapshots. `verify-data.yml` checks artifact-sync for the 2 curated instruments.

## Open — from the 2026-05 review (`tasks/review-2026-05/report.md`)

43 findings logged. Priority order:

1. **P0 — footer dead links** (`href="#"` × 5) vs the site's open-source positioning. Decide the repo-public model first.
2. **P0 — EC2 Melbourne data ~2× wrong.** Regenerate per-region `in` membership from AWS's authoritative regional doc; re-verify other new regions.
3. **P1 ×13 — data accuracy** (`tasks/review-2026-05/accuracy-audit.csv`): stale region lists (GCP C4A, OVH Paris), GPU-shape `vendor` mislabels, fabricated APIM data.
4. **P2 — systemic:** refresh pipeline validates timestamps but not correctness (`tasks/lessons.md` L1); a11y gaps (skip links, landmarks, contrast); EC2 CLS 0.23; minimal test coverage.

## Next instruments (candidates)

See `tasks/review-2026-05/feature-shortlist.md` — top pick: Equivalent-SKU finder (reuses existing in-repo data).
