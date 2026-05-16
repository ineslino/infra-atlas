# Session summary — 2026-05-16 · Feature / expansion review

A 7-phase feature/expansion review of infraatlas.dev, gated on a Phase-0
data-integrity audit. Repo treated as source of truth. Deliverables under
`tasks/features-2026-05/`.

## What was done

- **Phase 0 — region integrity (blocker).** Audited all 5 providers' region
  lists against vendor docs. The briefed "AWS 34-vs-39 regression" was a
  **misdiagnosis** — 34 = a standard AWS account's regions, 39 = all partitions
  (the marketing headline). Found and fixed **3 real drifts**, none in AWS:
  Azure had a phantom `taiwannorth` (announced, not GA) and was missing
  `westcentralus`; OCI was missing `af-casablanca-1`; OVH was missing Mumbai.
  Added a CI drift guard (`scripts/check_region_drift.py` + `region-reference.json`)
  and a written inclusion policy (`docs/data-policy.md`). Per the user's
  decision, the Region Map now shows **all partitions** — AWS 39, Azure 67,
  OCI 55, GCP 43, OVH 15 (219 regions).
- **Phase 1 — inventory.** 16 instruments mapped (data source, refresh, filters,
  cross-refs) + the IA + the implicit layer (the `data.json` files are already a
  public CORS API; the "What Changed" feed is built but dormant).
- **Phase 2 — research.** 4 parallel agents — competitive landscape, user-intent
  mining, vendor surface scan, adjacent verticals — every claim URL-cited.
- **Phases 3–7.** 22 evidence-cited gaps → 31 scored candidates → a top-10
  shortlist → buildable specs for the top 3.

## Outcome

**Build next:** "X vs Y" decision pages · expose the `data.json` API · Egress &
Data-Transfer Cost Map (then the Cross-Cloud Networking Primitives Matrix). The
single biggest validated unmet pain is network/egress cost — no instrument
covers it. Full roadmap: `tasks/features-2026-05/report.md`.

## Honest limitations

- Cloud CLIs (`aws`/`az`/`gcloud`) are installed but unauthenticated — the region
  audit used the authoritative vendor doc pages, not the CLIs.
- Per-region instance/SKU counts and GPU GA status were **not** independently
  audited (credential-free constraint) — stated in `integrity/data-audit.md`.
- Gated-region launch years (`since`) added to the Region Map are best-effort
  estimates; the region **codes** are vendor-verified (`integrity/region-audit.csv`).
- `cloudinfrastructuremap.com` could not be fetched (JS SPA) — flagged unverified
  in `research/competitive.md`.
