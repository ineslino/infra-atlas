# Phase 3 — Gap analysis

Synthesis of Phase 1 (`inventory.md`) + Phase 2 (`research/*.md`). A gap qualifies
only if it has **≥1 external user-pain citation** OR **≥1 named competitor** that
does it and Infra Atlas could do better. "Vendor surface ready?" = is the data
public, credential-free, and citable today.

| # | Gap | Evidence (link) | Vendor surface ready? |
|---|-----|-----------------|------------------------|
| G1 | **No network-cost coverage** — egress, cross-AZ, cross-region, NAT processing. The single most-complained-about cloud bill line. | r/aws "NAT gateways are too expensive" 171▲ <reddit.com/r/aws/comments/w3zrwz> · r/googlecloud "Cloud NAT pricing caught us off guard" · HN "no mention of bandwidth pricing… cross-AZ" id=31282930 | **Yes** — AWS Price List Bulk API + Azure Retail Prices API both credential-free & dated; GCP curated (key-walled). |
| G2 | **No "X vs Y / which product" decision content** | Top-voted SO question in nearly every cloud tag is a "which/difference" Q: GCE App Engine vs Compute Engine 547▲; api-gateway vs reverse proxy 80k views; r/devops reverse-proxy vs LB vs API-gateway 156▲ | **Yes** — pure editorial; vendor docs. No neutral competitor (blogs are vendor-biased). |
| G3 | **No API-gateway hard-limits / quotas reference** (the 29-sec timeout, payload caps, rate defaults) | SO "Amazon API Gateway timeout" 202k views; aws-cdk#30539; `lessons.md` L4 flags the on-site timeout claim is already stale | **Yes** — vendor docs; slots into existing APIM material. |
| G4 | **No region × SKU / GPU availability overlay** — which family/accelerator exists in which region | Azure "VM size not available in this zone" 18▲; HN spot thread "which AMD Zen types in London?"; GCE "GPUS_ALL_REGIONS quota" 93k views; competitor AWS regional-services table is single-cloud | **Partial** — GCP GPU×zone table good; AWS scattered across docs+blogs; Azure products-by-region UI. |
| G5 | **No GPU/accelerator instrument** — though the landing page already teases "GPU progression V100→…→B200" | GitHub `llm-price-compass` 223★ (price normalised to tokens/sec); Google "which region has h100"; `vendor-surface.md` C5 | **Partial** — documented free everywhere, but no clean machine file; fastest-rotting data → curated. |
| G6 | **No carbon-intensity-per-region view** | `vendor-surface.md` C1 — GCP `region-carbon-info` CSV (Apache-2.0, dated); AWS itself defers customers to Electricity Maps | **Yes (asymmetric)** — GCP CSV is the cleanest dataset in the whole scan; AWS publishes nothing → honest blank cells. |
| G7 | **No inter-region latency** — the map shows geography, not the ms | Competitor cloudping.co (AWS-only); `vendor-surface.md` C2 — Azure embeds a full 50×50 CSV in its latency doc | **Partial** — Azure (+OCI) only; AWS/GCP publish no table. |
| G8 | **Equivalent-SKU covers only raw VMs** — not Fargate / Cloud Run / Container Apps task sizes | r/aws Fargate↔EC2 "closest equivalent" 69▲; HN "is 1 CPU in Fargate the same as App Runner and Lambda?" | **Yes** — extends an instrument that already exists. |
| G9 | **No cross-cloud networking-primitives map** — Transit Gateway ⇄ Virtual WAN ⇄ NCC, PrivateLink variants, LB types | `vendor-surface.md` C6; `competitive.md` — nobody unifies the three vendors' service tables neutrally | **Yes** — pure curated matrix, the proven `equivalent-sku` shape. |
| G10 | **No managed-database catalog** (engine × version × cloud) | `vendor-surface.md` C8; GitHub `bytebase/dbcost` exists for exactly this | **Yes** — curated matrix, the `kubernetes`-atlas model. |
| G11 | **No service-mesh comparison** (Istio/Linkerd/Cilium/Consul/App Mesh) | `adjacent-verticals.md` §1 — prose comparisons saturated, but no neutral structured matrix incl. Cilium mesh-mode + App Mesh | **Yes** — first-party project docs; same matrix shape as `kubernetes`. |
| G12 | **No secrets-management comparison** (Vault/OpenBao/AWS SM/Azure KV/GCP SM/Infisical) | `adjacent-verticals.md` §4 — GCP SM + OpenBao rarely in one matrix; BSL-license angle under-tracked | **Yes** — vendor docs; pricing normalises to $/secret/mo. |
| G13 | **No streaming/messaging broker comparison** | `adjacent-verticals.md` §2 — unified OSS-plus-managed matrix genuinely missing; rivals vendor-published | **Partial** — capabilities yes; pricing axes incompatible (a known trap). |
| G14 | **No Ingress → Gateway API migration reference** — live, time-sensitive 2026 K8s pain | r/kubernetes front page: ingress-nginx retirement 345▲, EOL-in-120-days 233▲, Gateway-API hot-take 207▲ | **Yes** — editorial; vendor + project docs. |
| G15 | **No managed-K8s node-autoscaling reference** — Karpenter vs Cluster Autoscaler vs GKE NAP vs AKS | `competitive.md` — this lives only in operational CLIs + AWS best-practice docs, never a neutral static reference | **Yes** — row-set for the existing Kubernetes Atlas. |
| G16 | **`iam-matrix` is workforce-IAM only** — no workload-identity / federation rows | `adjacent-verticals.md` §3 — recommended deepening over a new CIAM instrument | **Yes** — extends an instrument that exists. |
| G17 | **The `data.json` public API is undiscoverable; no export** — CORS is already on, nothing links it; no CSV | `inventory.md` §4–5; competitors Vantage / cloudprice / gcloud-compute all ship CSV export + an API | **Yes** — capability already exists, just unexposed. |
| G18 | **"What Changed" feed is dormant; no RSS/Atom** | `inventory.md` §5 — `feed.json` is empty `{}`; no subscribable infra-change feed exists anywhere | **Yes** — built, needs activation + a feed format. |
| G19 | **`regions` + `gcp-compute` are curated with no upstream check** — freshness gap vs auto-refreshing competitors | `competitive.md` §7 — gcloud-compute & the AWS regional table refresh from vendor docs; `pipeline-findings.md` | **Partial** — Phase 0 added a `regions` drift guard; `gcp-compute` still unguarded. |
| G20 | **No per-cell provenance / visible "last verified" dates** | `competitive.md` §7 (gcloud-compute's "accuracy not guaranteed" honesty model); `lessons.md` L4; `pipeline-findings.md` | **Yes** — internal; the data already has source comments in places. |
| G21 | **No cost-normalised columns** (cost-per-vCPU, "list price ≠ invoiced" caveat) | `competitive.md` §4 (absorb from cloudprice.net); HN "1vCPU != 1vCPU" id=31282930 | **Yes** — trivially derived from data already held. |
| G22 | **No editorial "Field Notes" layer** — the site is all instruments, no investigative writing | `competitive.md` — Last Week in AWS / Pragmatic Engineer prove a paying audience for legible infra writing; the site's own "Issue 01 / periodical" framing promises it | **Yes** — pure editorial. |

## Synthesis

- **The biggest validated pain has no instrument at all: network/egress cost (G1).** It is the most-cited billing trap across every source and the site covers zero of it.
- **Three gaps are cheap extensions of things that already exist** — G8 (Equivalent-SKU → serverless), G15/G16 (row-sets for the Kubernetes/IAM atlases), G17/G18 (expose the API, wake the feed). High value-to-effort.
- **The matrix format scales cleanly** — G9, G10, G11, G12 are all the proven `equivalent-sku`/`kubernetes` shape with no new pipeline. Service mesh (G11) is the single cleanest new-instrument fit.
- **"Free + neutral + readable" is the unoccupied competitive slot** — every data competitor is paywalled, lead-gen, or single-vendor. APIM and cross-cloud are the moat.
- **Asymmetric vendor data is the recurring trap** (G6, G7): build honestly with blank cells, don't fake parity.
- **Don't chase**: a pricing calculator, live latency ping, service-quota explorer (credential-gated), CIAM — see `anti-list.md`.
