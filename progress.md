# Infra Atlas — Progress

A reference periodical of cloud + API-management infrastructure. Static site
(HTML/CSS/JS, no build), deployed via GitHub → Cloudflare. 17 pages: landing + 16
instruments.

## State — 2026-05-16

- **Live & deployed.** `origin/main` == `main`; the live site reflects the repo.
- **Instruments (16):**
  - *Cloud compute (6):* EC2 Observatory, Region Map, Azure VM Atlas, GCP Compute
    Index, OCI Compute Observatory, OVH Instance Catalogue.
  - *API management (5):* APIM Feature Matrix, AWS API Gateway Atlas, Apigee
    Atlas, Mulesoft Atlas, Kong · Gravitee · IBM (self-hosted).
  - *Cross-cloud matrices (5):* Equivalent-SKU Finder, Kubernetes Atlas,
    Compliance Footprint, Confidential Computing, IAM Matrix.
- **Data pipeline:** daily `refresh.yml` (06:00 UTC, credential-free) refreshes
  the 4 live-API data instruments (ec2, azure-vm, oci-compute, ovh-instances);
  `regions` + `gcp-compute` are curated; APIM + cross-cloud instruments are
  static dated snapshots. Guards: `verify-data.yml` (artifact sync **+ region
  drift**), `verify-freshness.yml` (curated-snapshot staleness).
- **Region Map shows all partitions** — AWS 39, Azure 67, GCP 43, OCI 55, OVH 15
  (219 regions). Inclusion policy: `docs/data-policy.md`.

## Open — feature roadmap (`tasks/features-2026-05/`)

The 2026-05 feature/expansion review. **Build next:** (1) "X vs Y" decision
pages, (2) expose the `data.json` API, (3) Egress & Data-Transfer Cost Map; then
the Cross-Cloud Networking Primitives Matrix. Scored shortlist of 10 in
`shortlist.md`; buildable specs for the top 3 in `specs/`; one-page summary in
`report.md`.

## Open — from the 2026-05 four-axis review (`tasks/review-2026-05/report.md`)

The earlier UI/UX + functionality + data-accuracy review. Its P0s (footer links,
EC2 Melbourne data) and accuracy corrections were addressed; the 5 cross-cloud
instruments were built from its feature shortlist. Residual P2/P3 polish items
remain logged there.
