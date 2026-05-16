# Phase 4 — Ideation: the long list

31 candidates across 5 categories, each grounded in a Phase 3 gap (`gaps.md`) or
a named competitor. Format per candidate: **idea · grounding · effort (S/M/L) ·
data feasibility (1–5) · fit (1–5)**. Feasibility = is the data public,
credential-free, citable. Fit = alignment with the static/editorial/neutral DNA.
Scoring and the shortlist are Phase 6.

---

## 4a · New instruments

| ID | Idea | Grounding | Effort | Feas. | Fit |
|----|------|-----------|:------:|:-----:|:---:|
| N1 | **Egress & Data-Transfer Cost Map** — internet-out tiers, cross-AZ, cross-region, NAT processing, inter-cloud, per provider | G1 · r/aws "NAT too expensive" 171▲; HN "no mention of bandwidth pricing"; #1 ranked pain | M | 4 | 5 |
| N2 | **Cross-Cloud Networking Primitives Matrix** — Transit Gateway⇄Virtual WAN⇄NCC, PrivateLink variants, LB types, peering | G9 · `vendor-surface.md` C6; no neutral cross-cloud service map exists | S | 5 | 5 |
| N3 | **Service Mesh Atlas** — Istio/Linkerd/Cilium/Consul/App Mesh × capabilities | G11 · `adjacent-verticals.md` §1 — prose saturated, no neutral matrix incl. Cilium+App Mesh | M | 5 | 5 |
| N4 | **Secrets Management Atlas** — Vault/OpenBao/AWS SM/Azure KV/GCP SM/Infisical | G12 · `adjacent-verticals.md` §4; BSL-license angle under-tracked | M | 4 | 5 |
| N5 | **Managed Database Catalog** — engine × version × cloud (RDS/Aurora/Cloud SQL/AlloyDB/Azure SQL/OCI) | G10 · `vendor-surface.md` C8; GitHub `bytebase/dbcost` exists | M | 4 | 4 |
| N6 | **GPU / Accelerator Availability Matrix** — T4→B200/Trainium/TPU × region | G5 · landing page already teases it; `llm-price-compass` 223★; "which region has h100" | L | 3 | 5 |
| N7 | **Carbon Intensity Atlas** — gCO₂eq/kWh + CFE% per region | G6 · `vendor-surface.md` C1 — GCP `region-carbon-info` CSV (cleanest dataset found) | M | 4 | 4 |
| N8 | **Inter-Region Latency Matrix** — backbone ms, Azure-anchored | G7 · `vendor-surface.md` C2 — Azure embeds a 50×50 CSV; cloudping.co is AWS-only | M | 3 | 4 |
| N9 | **Streaming & Messaging Atlas** — Kafka/Pulsar/Kinesis/MSK/Event Hubs/Pub-Sub/RabbitMQ, capability-only | G13 · `adjacent-verticals.md` §2 — unified OSS+managed matrix missing | M | 3 | 4 |
| N10 | **Object Storage Tier comparator** — hot→archive, $/GB + retrieval + min-retention | `vendor-surface.md` C3 · merge with N1 as one "Cloud Cost Almanac" | M | 4 | 4 |

## 4b · New editorial / content sections

| ID | Idea | Grounding | Effort | Feas. | Fit |
|----|------|-----------|:------:|:-----:|:---:|
| E1 | **"X vs Y" decision pages** — App Engine vs Compute Engine, API Gateway vs reverse proxy, Fargate vs EC2… short neutral footnoted verdicts | G2 · top-voted SO question in *every* cloud tag is a "which/difference" Q (GCE 547▲) | S | 5 | 5 |
| E2 | **API Gateway Limits & Quotas reference** — timeout ceilings, payload caps, rate defaults, regional vs edge | G3 · SO "API Gateway timeout" 202k views; `lessons.md` L4 (on-site claim already stale) | S | 5 | 5 |
| E3 | **Ingress → Gateway API migration reference** — resource mapping, controller support, per-feature GA | G14 · r/kubernetes front page 345/233/207▲, live 2026 pain | M | 5 | 4 |
| E4 | **"Field Notes"** — short investigative posts on infra gotchas (the 29-sec timeout, NAT economics) | G22 · Last Week in AWS / Pragmatic Engineer prove the audience; site's "periodical" framing promises it | M | 5 | 4 |
| E5 | **Cross-vendor glossary** — every vendor's name for the same thing (AZ⇄zone, PrivateLink⇄PSC) | `competitive.md` (taxonomy confusion is endemic); SO "what does Ocp- stand for" | S | 5 | 4 |
| E6 | **Managed-K8s node-autoscaling reference** — Karpenter vs Cluster Autoscaler vs GKE NAP vs AKS | G15 · `competitive.md` — exists only in CLIs/best-practice docs | S | 5 | 4 |
| E7 | **Incident anatomy series** — annotated public post-mortems (regional outages) | HN "AWS Outage… single region" 306▲; "GCP region down — water intrusion" 289▲ | M | 4 | 3 |
| E8 | **ADR-style decision aids** — "pick your APIM in 5 questions" interactive flow | `competitive.md` (Gartner is abstract; engineers want concrete) | M | 5 | 3 |

## 4c · Improvements to existing instruments

| ID | Idea | Grounding | Effort | Feas. | Fit |
|----|------|-----------|:------:|:-----:|:---:|
| I1 | **Equivalent-SKU → serverless/container task sizes** — Fargate/Cloud Run/Container Apps ⇄ raw VM | G8 · r/aws Fargate↔EC2 "closest equivalent" 69▲; HN "1 CPU Fargate vs Lambda?" | M | 4 | 5 |
| I2 | **IAM Matrix → workload-identity / federation rows** — OIDC federation, short-lived creds | G16 · `adjacent-verticals.md` §3 (preferred over a new CIAM instrument) | S | 5 | 5 |
| I3 | **Kubernetes Atlas → node-autoscaling row-set** | G15 · same source as E6; row-set vs standalone page | S | 5 | 5 |
| I4 | **Cost-normalised columns** — cost-per-vCPU, cost-per-GB; "list price ≠ invoiced" footnote | G21 · `competitive.md` §4 (absorb from cloudprice); HN "1vCPU != 1vCPU" | S | 5 | 4 |
| I5 | **Region × SKU / GPU availability overlay** on the Region Map / compute instruments | G4 · Azure "VM size not available in zone"; "which AMD Zen in London?" | L | 3 | 4 |
| I6 | **Workload-level benchmark footnotes** on compute instruments (LLM/db/compression, not synthetic) | `competitive.md` §4 — absorb from Spare Cores | M | 2 | 3 |
| I7 | **SAP-HANA-certified / OS-licensing-cost columns** on compute instruments | `competitive.md` — absorb from gcloud-compute | S | 4 | 3 |
| I8 | **Side-by-side compare / pin mode** extended to the matrices | `inventory.md` §4 (compute instruments have it; matrices don't) | M | 5 | 4 |

## 4d · Cross-cutting features

| ID | Idea | Grounding | Effort | Feas. | Fit |
|----|------|-----------|:------:|:-----:|:---:|
| X1 | **Document & expose the public `data.json` API** — landing-page section + per-instrument link | G17 · `inventory.md` §5 (CORS already on, undiscoverable); competitors all ship an API | S | 5 | 5 |
| X2 | **CSV / JSON export button** per instrument | G17 · Vantage, cloudprice, gcloud-compute all have it | S | 5 | 4 |
| X3 | **Wake the "What Changed" feed + add RSS/Atom** | G18 · `inventory.md` §5 (`feed.json` empty); no subscribable infra-change feed exists | M | 5 | 4 |
| X4 | **Global content search** across all instrument data (not just the ⌘K instrument list) | `competitive.md`; `user-intent.md` (engineers want fast lookup) | M | 4 | 4 |
| X5 | **Print-friendly stylesheet** — engineers print reference pages | mission 4d; low-cost polish | S | 5 | 3 |
| X6 | **Embeddable single-row/matrix widget** (`<iframe>` a comparison into a blog post) | mission 4d; distribution lever | M | 4 | 3 |

## 4e · Data & trust layer

| ID | Idea | Grounding | Effort | Feas. | Fit |
|----|------|-----------|:------:|:-----:|:---:|
| D1 | **Per-cell provenance + visible "last verified" date** per instrument | G20 · `competitive.md` §7 (gcloud-compute's honesty model); `lessons.md` L4 | M | 5 | 5 |
| D2 | **Public data-corrections changelog** | G20 · `pipeline-findings.md`; builds trust | S | 5 | 4 |
| D3 | **Drift dashboard** — last successful sync + open drift per instrument | G19 · Phase 0 confirmed silent staleness; extends `check_region_drift.py` | M | 4 | 4 |
| D4 | **Close the `gcp-compute` freshness gap** — upstream guard like `regions` now has | G19 · `competitive.md` §7 (gcloud-compute auto-refreshes; Infra Atlas curated) | M | 3 | 4 |
| D5 | **Reproducibility links** — each table links the script + commit that produced it | mission 4e · `competitive.md` §7 (open-source honesty) | S | 5 | 3 |

## Notes

- **N1 + N10 should ship as one instrument** ("Cloud Cost Almanac" — storage tiers + transfer) — they share the AWS Price List Bulk API pipeline; building separately duplicates plumbing (`vendor-surface.md`).
- **E6 vs I3** are the same content as either a standalone page or a Kubernetes-Atlas row-set — Phase 6 picks one.
- Rejected outright (see `anti-list.md`): pricing calculator, live latency ping, service-quota explorer (credential-gated), standalone CIAM instrument, diagram builder.
