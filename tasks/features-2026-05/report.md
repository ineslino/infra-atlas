# Infra Atlas — Feature / Expansion Review · 2026-05

**Executive summary.** A 7-phase review of what to build next for infraatlas.dev,
grounded in repo reality, competitors, and real engineer pain. Full deliverables
indexed at the bottom; this page is the 10-minute version.

---

## Phase 0 — data-integrity check (the blocker) · ✅ RESOLVED

The brief flagged a "known AWS region regression — site shows 34, should be 39,
not corrected." **Verified against AWS's own docs: that was a misdiagnosis.**

- **34 and 39 are both real, measuring different things.** AWS's docs table
  *"Regions provided by an AWS account"* has exactly 34 rows; AWS's marketing
  headline "39 Geographic Regions" = 34 commercial + 2 GovCloud + 2 China + 1
  European Sovereign Cloud. No regression — a scope-definition gap.
- **The actual drift was small and elsewhere** — 3 issues, none in AWS: Azure
  carried a phantom `taiwannorth` (announced, not GA) and was missing
  `westcentralus`; OCI was missing `af-casablanca-1`; OVH was missing Mumbai.
  All **fixed**.
- **Root cause** (`integrity/pipeline-findings.md`): the `regions` instrument is
  hand-curated with no upstream-truth check — its daily "refresh" only
  re-serialises a human-typed list. So a miss or a phantom shipped silently.
- **Guards added**: `scripts/check_region_drift.py` + `regions/region-reference.json`
  pin the region set to a dated, vendor-verified snapshot, wired into CI
  (`verify-data.yml`). `docs/data-policy.md` now documents the inclusion policy.
- **Decision (yours, 2026-05-16):** the Region Map now shows **all partitions** —
  AWS 39, Azure 67, OCI 55, GCP 43, OVH 15 — each gated region labelled by scope.

Phase 0 is complete and committed (`90ba1ba`, `d229c48`, `f2d8752`); CI guard is
live. Gate passed.

## What Infra Atlas is today (for a fresh reviewer)

A free, static, credential-free, *editorial* reference for cloud + API-management
infrastructure — 16 instruments in 3 classes: 6 cloud-compute explorers, 5 API-
management references, 5 cross-cloud matrices. No login, no build step, €0. Full
map in `inventory.md`. Its real moat: it is the only candidate that is **free +
neutral + readable** at once — every data competitor is paywalled, lead-gen for a
FinOps SaaS, or single-vendor (`research/competitive.md`).

## The recommendation — build these three next

Scored on value + feasibility + fit + defensibility − maintenance
(`shortlist.md`). The three top-scoring candidates, each with a buildable spec in
`specs/`:

1. **"X vs Y" decision pages** (`specs/decision-pages.md`) — 8 short, neutral,
   footnoted "which one" pages. The top-voted Stack Overflow question in *every*
   cloud tag is a "which/difference" question; the only existing answers are
   vendor-biased. Effort **S**, pure editorial.
2. **Expose the `data.json` API** (`specs/data-json-api.md`) — every data
   instrument already serves a CORS-enabled `data.json`; nothing documents it.
   Documenting it turns a hidden asset into a distribution lever. Effort **S**,
   the capability already exists.
3. **Egress & Data-Transfer Cost Map** (`specs/egress-cost-map.md`) — the #1
   validated unmet pain (NAT/egress cost is the most-complained-about cloud bill
   line) and no free neutral tool covers it. Effort **M**, AWS/Azure price APIs
   are credential-free.

**Do #4 in parallel:** the Cross-Cloud Networking Primitives Matrix — lowest-risk
new instrument, a pure curated matrix.

## The rest of the shortlist (4–10)

API Gateway Limits & Quotas reference · IAM Matrix workload-identity rows ·
Service Mesh Atlas · per-cell provenance + "last verified" dates · Kubernetes
Atlas node-autoscaling rows · cost-normalised columns. The S-effort ones (IAM
rows, K8s rows, cost columns, gateway limits) are cheap wins that deepen
instruments already shipped.

## Cross-cutting findings

- **The data disagrees with itself** — every instrument stores its own region
  list and they had drifted apart (Azure 56 map vs 52 VM Atlas; OCI 44 vs 38;
  OVH 14 vs 15). Landing-page stat cards are hand-typed and stale (EC2 "32
  regions / ~700 types" vs an actual 34 / 1338). See `integrity/data-audit.md`.
- **"Refreshes daily" is misleading for `regions` and `gcp-compute`** — they are
  curated; the daily job only re-stamps them. Site copy should distinguish
  live-API instruments from curated ones.
- **Don't build** (`anti-list.md`): accounts, paid tiers, infra monitoring, an AI
  chatbot, ads, comments, a pricing calculator, a service-quota explorer
  (credential-gated), a standalone CIAM instrument.

## Deliverables

```
tasks/features-2026-05/
  todo.md                      plan + repo sanity-check
  integrity/
    region-audit.csv           223-row audit, 5 providers vs upstream
    build_region_audit.py      reproducible audit generator
    pipeline-findings.md       why the drift happened + root cause
    data-audit.md              extended audit (instance/SKU/cross-instrument)
  inventory.md                 the 16 instruments + IA + implicit gaps
  research/                    competitive · user-intent · vendor-surface · adjacent-verticals
  gaps.md                      22 gaps, evidence-cited
  ideation.md                  31 candidates, 5 categories
  anti-list.md                 10 rejected patterns
  shortlist.md                 all 31 scored; top 10 detailed
  specs/                       decision-pages · data-json-api · egress-cost-map
  report.md                    this file
docs/data-policy.md            inclusion policy, refresh cadence, guards
scripts/check_region_drift.py  the new CI drift guard
```
