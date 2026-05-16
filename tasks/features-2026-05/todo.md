# Infra Atlas — Feature / Expansion Review · 2026-05

**Mission:** a ranked, opinionated roadmap of what to build next — grounded in
(a) repo reality, (b) competitors, (c) real engineer pain, (d) editorial fit.
Deliverable set lives under `tasks/features-2026-05/`.

## Repo sanity-check (done 2026-05-16, before research)

- **16 instruments live**, 3 classes:
  - *Data* (6): `ec2`, `regions`, `azure-vm`, `gcp-compute`, `oci-compute`, `ovh-instances`
  - *APIM* (5): `apim-matrix`, `aws-api-gateway`, `apigee`, `mulesoft`, `self-hosted-apim`
  - *Cross-cloud* (5): `equivalent-sku`, `kubernetes`, `compliance`, `confidential-computing`, `iam-matrix`
- **Refresh reality is mixed** — `refresh.yml` runs daily 06:00 UTC:
  - `ec2`, `azure-vm`, `oci-compute`, `ovh-instances` → genuinely pull public APIs/datasets.
  - `regions`, `gcp-compute` → **CURATED**: `refresh.sh` only re-extracts a
    hand-maintained `const` from `index.html`. A daily run cannot discover a
    new region — a human must edit `index.html` first.
  - APIM + cross-cloud instruments → fully static, no refresh.
- `regions/data.json` is **city-modelled**: `{cities:[{city,…,regions:[{p,code,name,az,since}]}]}`.
- CLIs (`aws`/`az`/`gcloud`) installed but **unauthenticated** — Phase 0 audit
  uses authoritative vendor doc pages, not the CLI.
- No `CLAUDE.md` in repo. Governing docs: `CONTRIBUTING.md` + user `MEMORY.md`.
- `docs/` exists (`docs/plans/`). Workflows: `refresh.yml`, `verify-data.yml`, `verify-freshness.yml`.

## Site region counts today (from `regions/data.json`)

| Provider | Site count | Mission claim | Verified upstream | Verdict |
|----------|-----------|---------------|-------------------|---------|
| AWS   | 34 | "should be 39 commercial" | TBD Phase 0a | TBD |
| Azure | 56 | — | TBD | TBD |
| GCP   | 43 | — | TBD | TBD |
| OCI   | 44 | — | TBD | TBD |
| OVH   | 14 | — | TBD | TBD |

---

## Phase 0 — Region/data integrity (BLOCKER)

- [ ] **0a** Region audit, 5 providers vs upstream docs → `integrity/region-audit.csv`
- [ ] **0b** Pipeline forensics — why AWS=34 is stale → `integrity/pipeline-findings.md`
- [ ] **0c** Extended data audit (instance/SKU/GPU drift) → `integrity/data-audit.md`
- [ ] **0d** Fix trivially-fixable drift + commit; add a CI drift guard
- [ ] **0e** Inclusion policy → `docs/data-policy.md`
- **GATE:** Phase 1 does not start until AWS region count is correct on the
  site (or a merged PR is pending) and 0a–0e deliverables exist.

## Phase 1 — Inventory → `inventory.md`
- [ ] Every instrument: data sources, filters, cross-refs, update mechanism
- [ ] Information architecture: nav, footer, editorial framing, global features
- [ ] Implicit capabilities (deep-link state, export, RSS) + implicit gaps

## Phase 2 — External research (4 parallel subagents) → `research/*.md`
- [ ] 2a Competitive references → `research/competitive.md`
- [ ] 2b User-intent mining → `research/user-intent.md`
- [ ] 2c Vendor surface-area scan → `research/vendor-surface.md`
- [ ] 2d Adjacent verticals (APIM-side) → `research/adjacent-verticals.md`

## Phase 3 — Gap analysis → `gaps.md`
- [ ] Synthesise P1+P2; gap qualifies only with a user-pain cite OR named competitor

## Phase 4 — Ideation → `ideation.md`
- [ ] 20–30 candidates across 4a new instruments / 4b editorial / 4c improvements
      / 4d cross-cutting / 4e data-trust

## Phase 5 — Anti-pattern list → `anti-list.md`
- [ ] ≥6 explicitly-rejected ideas with one-line reasons

## Phase 6 — Scoring + shortlist → `shortlist.md`
- [ ] Score all candidates; top 8–10 with value prop / persona / source / risk / effort / acceptance

## Phase 7 — Deep-dive specs → `specs/<feature>.md` ×3
- [ ] Buildable specs for the top 3

## Wrap
- [ ] `report.md` — 1-page exec summary, Phase 0 status at top
- [ ] Update `progress.md`, `session_summary.md`
- [ ] `tasks/lessons.md` entry for the AWS region regression
