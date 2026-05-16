# Phase 6 — Scoring & shortlist

Every Phase-4 candidate scored. **Composite = value + feasibility + fit +
defensibility − maintenance** (each sub-score 1–5; maintenance lower = better;
**effort S/M/L is the tiebreaker**).

## Scoring table (all 31)

| ID | Candidate | Val | Feas | Fit | Def | Maint | **Comp** | Effort |
|----|-----------|:---:|:----:|:---:|:---:|:-----:|:--------:|:------:|
| E1 | "X vs Y" decision pages | 5 | 5 | 5 | 4 | 2 | **17** | S |
| X1 | Expose the `data.json` API | 4 | 5 | 5 | 4 | 1 | **17** | S |
| N1 | Egress & Data-Transfer Cost Map | 5 | 4 | 5 | 5 | 2 | **17** | M |
| N2 | Cross-Cloud Networking Primitives Matrix | 4 | 5 | 5 | 4 | 2 | **16** | S |
| N3 | Service Mesh Atlas | 4 | 5 | 5 | 4 | 3 | **15** | M |
| E2 | API Gateway Limits & Quotas reference | 4 | 5 | 5 | 4 | 3 | **15** | S |
| I2 | IAM Matrix → workload-identity rows | 4 | 5 | 5 | 3 | 2 | **15** | S |
| D1 | Per-cell provenance + "last verified" | 4 | 5 | 5 | 3 | 2 | **15** | M |
| I1 | Equivalent-SKU → serverless task sizes | 4 | 4 | 5 | 4 | 3 | **14** | M |
| I3 | Kubernetes Atlas → node-autoscaling rows | 3 | 5 | 5 | 3 | 2 | **14** | S |
| I4 | Cost-normalised columns | 4 | 5 | 4 | 3 | 2 | **14** | S |
| X3 | Wake "What Changed" feed + RSS | 3 | 5 | 4 | 4 | 2 | **14** | M |
| N5 | Managed Database Catalog | 4 | 4 | 4 | 4 | 3 | **13** | M |
| N6 | GPU / Accelerator Availability Matrix | 5 | 3 | 5 | 5 | 5 | **13** | L |
| N8 | Inter-Region Latency Matrix | 4 | 3 | 4 | 4 | 2 | **13** | M |
| E4 | "Field Notes" investigative series | 3 | 5 | 4 | 4 | 3 | **13** | M |
| E5 | Cross-vendor glossary | 3 | 5 | 4 | 3 | 2 | **13** | S |
| I8 | Compare/pin mode on the matrices | 3 | 5 | 4 | 3 | 2 | **13** | M |
| X2 | CSV/JSON export per instrument | 3 | 5 | 4 | 3 | 2 | **13** | S |
| N4 | Secrets Management Atlas | 3 | 4 | 5 | 3 | 3 | **12** | M |
| N7 | Carbon Intensity Atlas | 3 | 4 | 4 | 3 | 2 | **12** | M |
| E3 | Ingress → Gateway API migration ref | 4 | 5 | 4 | 2 | 3 | **12** | M |
| E6 | Node-autoscaling standalone page | 3 | 5 | 4 | 3 | 3 | **12** | S |
| N10 | Object Storage Tier comparator | 3 | 4 | 4 | 3 | 3 | **11** | M |
| E8 | ADR-style decision aids | 3 | 5 | 3 | 3 | 2 | **11** | M |
| I5 | Region × SKU/GPU availability overlay | 4 | 3 | 4 | 4 | 4 | **11** | L |
| X4 | Global content search | 3 | 4 | 4 | 3 | 3 | **11** | M |
| D2 | Public corrections changelog | 2 | 5 | 4 | 2 | 2 | **11** | S |
| D3 | Drift dashboard | 3 | 4 | 4 | 3 | 3 | **11** | M |
| X5 | Print-friendly stylesheet | 2 | 5 | 3 | 1 | 1 | **10** | S |
| D5 | Reproducibility links | 2 | 5 | 3 | 2 | 2 | **10** | S |
| N9 | Streaming & Messaging Atlas | 3 | 3 | 4 | 3 | 3 | **10** | M |
| D4 | Close `gcp-compute` freshness gap | 3 | 3 | 4 | 2 | 3 | **9** | M |
| E7 | Incident anatomy series | 2 | 4 | 3 | 3 | 3 | **9** | M |
| I7 | SAP-HANA / OS-licensing columns | 2 | 4 | 3 | 2 | 2 | **9** | S |
| X6 | Embeddable widget | 2 | 4 | 3 | 3 | 3 | **9** | M |
| I6 | Workload-benchmark footnotes | 3 | 2 | 3 | 2 | 3 | **7** | M |

`N10` is folded into `N1` (shared AWS Price List pipeline). `E6`≈`I3` (same
content, row-set chosen over standalone page).

---

## Shortlist — top 10

### 1 · E1 — "X vs Y" decision pages  ·  composite 17 · effort S

**Value prop.** Short, neutral, footnoted "which one / what's the difference"
pages for the comparisons engineers ask constantly — App Engine vs Compute
Engine, API Gateway vs reverse proxy, Fargate vs EC2, REST vs HTTP API. The
top-voted Stack Overflow question in nearly every cloud tag is one of these; the
only existing answers are vendor-biased blogs or community re-derivations. Cheap
to produce, evergreen search traffic, and a perfect fit for the editorial format.
**Primary user.** The engineer/architect mid-decision, often arriving from search.
**Data source.** Vendor product docs (free, credential-free); no pipeline — pure
editorial. Cadence: review per page ~2×/yr.
**Biggest risk.** Scope creep into an infinite listicle / opinions rotting.
*Mitigation:* fixed small set (8–12 pages), each a tight verdict with a dated
"reviewed" stamp; only pairs with a top-voted SO question qualify.
**Effort.** S — a shared page template + 8–12 short pages. ~1 template day + ~0.5 day/page.
**Shipped when.** ≥8 decision pages live, each footnoted, in the nav + ⌘K, with a "reviewed" date.

### 2 · X1 — Expose the public `data.json` API  ·  composite 17 · effort S

**Value prop.** Every data instrument *already* serves a CORS-enabled `data.json`
(`_headers` sets `Access-Control-Allow-Origin: *`) — an unadvertised public API.
Documenting it (a `/api` page + per-instrument link + a stability note) turns a
hidden asset into a distribution and defensibility lever: people who build on the
data come back. Near-zero build cost because the capability exists.
**Primary user.** Tool-builders, scripters, the "I'll just scrape it" engineer.
**Data source.** The existing `*/data.json` files; no new data. Cadence: n/a.
**Biggest risk.** Implying a stability guarantee, then breaking a schema.
*Mitigation:* publish an explicit "best-effort, may change, no SLA" note and a
schema version field; it is a reference, not a product.
**Effort.** S — one `/api` page, per-instrument links, a schema note. ~1–2 days.
**Shipped when.** `/api` page lists every `data.json` with its schema + the
caveat; each instrument links its own; landing page references it.

### 3 · N1 — Egress & Data-Transfer Cost Map  ·  composite 17 · effort M

**Value prop.** The single most-complained-about, least-transparent line on a
cloud bill — internet-out tiers, cross-AZ, cross-region, NAT-gateway processing,
inter-cloud — in one footnoted table per provider. It is the **#1 ranked unmet
pain** in the user research and **no neutral free tool covers it**. A genuine new
instrument that lands on raw, validated demand.
**Primary user.** Anyone who has opened an AWS bill, seen "EC2-Other", and not
known why; architects sizing a multi-region/multi-cloud design.
**Data source.** AWS Price List Bulk API (`pricing.us-east-1.amazonaws.com` —
credential-free, dated, verified HTTP 200) + Azure Retail Prices API
(`prices.azure.com`, credential-free); GCP `cloud.google.com/vpc/network-pricing`
curated (small, stable set). Cadence: AWS/Azure daily via `refresh.sh`; GCP
curated with a dated snapshot.
**Biggest risk.** Egress pricing is heavily conditional (free tiers, same-region,
CloudFront-routed discounts) — a flat $/GB table oversimplifies and misleads.
*Mitigation:* footnotes are on-brand ("asterisks intact"); model the common
*conditions* as columns, not a single rate; "list price ≠ invoiced" disclaimer.
**Effort.** M — a `refresh.sh` transform of the AWS/Azure price JSON (the
`ec2/refresh.sh` shape), a curated GCP layer, the matrix UI. ~1–1.5 weeks.
**Shipped when.** Internet-egress, cross-AZ, cross-region and NAT rates for AWS +
Azure + GCP render in one filterable table; every conditional is footnoted; data
auto-refreshes for AWS/Azure and is dated for GCP.

### 4 · N2 — Cross-Cloud Networking Primitives Matrix  ·  composite 16 · effort S

**Value prop.** A Rosetta-stone matrix mapping equivalent networking constructs —
Transit Gateway ⇄ Virtual WAN ⇄ Network Connectivity Center; PrivateLink ⇄
Private Link ⇄ Private Service Connect; peering, NAT, LB types — with per-cell
asterisks (VPC is global on GCP, regional on AWS/Azure). The networking analogue
of Equivalent-SKU; nobody does it neutrally. Lowest-risk new instrument — pure
curated matrix, the proven format, zero pipeline.
**Primary user.** The architect porting a design between clouds, or learning a
second cloud.
**Data source.** Vendor networking docs (AWS/Azure/GCP), free + credential-free.
Cadence: curated; review ~2×/yr.
**Biggest risk.** "Equivalent" is rarely 1:1 — false equivalence misleads.
*Mitigation:* the matrix's `note`/`src` per cell exists for exactly this; mark
partial equivalences explicitly.
**Effort.** S — one curated matrix page, the `kubernetes`/`iam-matrix` shape. ~3–5 days.
**Shipped when.** ≥4 vendors × the core networking primitives, every cell sourced, in nav + ⌘K.

### 5 · E2 — API Gateway Limits & Quotas reference  ·  composite 15 · effort S

**Value prop.** The hard ceilings that bite in production — the AWS API Gateway
29-second timeout (202k SO views), payload caps, rate-limit defaults, regional vs
edge behaviour — per gateway, in one place. `lessons.md` L4 notes the on-site
timeout claim is *already* stale, so this also fixes a known rot.
**Primary user.** The engineer debugging a 504 or designing around a limit.
**Data source.** Vendor gateway docs; free. Cadence: curated, dated — limits rot
(L4), so an aggressive "verified" date.
**Biggest risk.** "Hard limit" claims rot silently (the exact L4 trap).
*Mitigation:* every limit carries a dated last-verified marker; feeds the D1 work.
**Effort.** S — a section/page extending the existing APIM material. ~3–4 days.
**Shipped when.** Timeout, payload, rate, and quota limits for ≥5 gateways, each dated + sourced.

### 6 · I2 — IAM Matrix → workload-identity / federation rows  ·  composite 15 · effort S

**Value prop.** The existing IAM Matrix is workforce-IAM only. Adding a
workload-identity row-set — OIDC federation, workload identity federation,
short-lived credentials, the "how does my CI authenticate to the cloud" question
— deepens an instrument that already exists, stays inside the infrastructure DNA,
and is the research-recommended move *over* a new CIAM instrument.
**Primary user.** The platform engineer wiring CI/CD or cross-cloud workloads.
**Data source.** AWS/Azure/GCP/OCI identity docs; free, credential-free.
**Biggest risk.** Low — additive row-set on a proven instrument.
*Mitigation:* n/a beyond normal sourcing discipline.
**Effort.** S — a row-set + footnotes on an existing matrix. ~2–3 days.
**Shipped when.** Workload-identity rows render for all 4 providers, sourced.

### 7 · N3 — Service Mesh Atlas  ·  composite 15 · effort M

**Value prop.** Istio / Linkerd / Cilium / Consul / AWS App Mesh × capabilities
(mTLS model, proxy architecture, ambient/sidecarless, multi-cluster, Gateway API
conformance, VM support). Prose comparisons are saturated but **no neutral
structured matrix includes Cilium's mesh mode and App Mesh**. Same shape as the
Kubernetes Atlas; a natural cross-link from it.
**Primary user.** The platform engineer choosing or comparing a mesh.
**Data source.** First-party project docs + CNCF landscape; free, credential-free.
Cadence: curated, dated — ambient mode moves every release.
**Biggest risk.** Performance numbers can't be cited honestly; ambient churn.
*Mitigation:* exclude latency/throughput (or quarantine behind "vendor-reported");
date-stamp the snapshot.
**Effort.** M — a new matrix instrument. ~1 week.
**Shipped when.** 5 services × the capability set, sourced, latency excluded, cross-linked from Kubernetes Atlas.

### 8 · D1 — Per-cell provenance + visible "last verified" dates  ·  composite 15 · effort M

**Value prop.** The site's whole pitch is "asterisks intact" / sourced data — but
provenance is uneven and the on-page timestamp is the *re-serialisation* time,
not a verification date. Surfacing a real per-instrument (ideally per-cell)
"verified on" date with a source link makes the trust claim *visible* — the
honesty model competitors like gcloud-compute already use.
**Primary user.** Every reader deciding whether to trust a number — and contributors.
**Data source.** Internal; the data already carries source comments in places.
**Biggest risk.** Retrofitting provenance across 16 instruments is broad.
*Mitigation:* ship the per-instrument "verified" date first (cheap, high-trust),
per-cell provenance as a follow-up; reuse the `region-reference.json` pattern.
**Effort.** M — a shared convention + rollout across instruments. ~1 week for v1.
**Shipped when.** Every instrument shows a real "verified" date distinct from the build timestamp.

### 9 · I3 — Kubernetes Atlas → node-autoscaling row-set  ·  composite 14 · effort S

**Value prop.** How each managed-K8s service does node autoscaling — Karpenter vs
Cluster Autoscaler vs GKE node auto-provisioning vs AKS — what each supports, spot
integration, instance-family breadth. Today this lives only in operational CLIs
and AWS best-practice docs, never as a neutral reference. A row-set on an
instrument that already exists.
**Primary user.** The platform engineer tuning cluster cost/scaling.
**Data source.** Vendor + project docs; free. Cadence: curated, dated.
**Biggest risk.** Low — additive row-set.
**Effort.** S — ~2–3 days.
**Shipped when.** Node-autoscaling rows render for all managed-K8s services, sourced.

### 10 · I4 — Cost-normalised columns  ·  composite 14 · effort S

**Value prop.** Add derived cost-per-vCPU and cost-per-GB columns to the compute
instruments, plus a standing "list price ≠ invoiced price" footnote. Trivially
computed from data already held; directly answers the research's "1 vCPU ≠ 1
vCPU, raw price misleads" complaint. Absorbed from cloudprice.net's best idea.
**Primary user.** Anyone price-comparing instances across clouds.
**Data source.** Existing instrument `data.json` (derived). Cadence: auto.
**Biggest risk.** Implying the normalised figure is the whole story.
*Mitigation:* the footnote; keep it a column, not a ranking.
**Effort.** S — a derived column + footnote per compute instrument. ~2 days.
**Shipped when.** cost-per-vCPU + cost-per-GB columns on all 4 priced compute instruments, with the caveat footnote.

---

## Recommendation

**Build E1, X1, N1 next** (the three 17-point candidates) — full specs in
`specs/`. Together they are an editorial quick-win, a near-free platform/
distribution win, and the flagship instrument for the #1 validated user pain.
**N2 is the immediate #4** — the lowest-risk new instrument, do it in parallel.
The cluster of S-effort 14–15 candidates (I2, I3, I4, E2) are cheap, high-fit
follow-ons that deepen instruments already shipped.
