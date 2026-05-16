# Vendor surface-area scan — reference data Infra Atlas does not yet expose

Phase 2c · 2026-05-16 · for `tasks/features-2026-05`

**Brief:** scan the public cloud-vendor surface for cross-vendor reference data
that Infra Atlas has *no instrument for today*, and that could become one. The
16 live instruments (6 compute explorers, the region map, 5 APIM guides, and 5
cross-cloud matrices: equivalent-SKU, Kubernetes, compliance, confidential
computing, IAM) are out of scope — only gaps below.

**Editorial fit test applied to each candidate** (from `README.md` /
`CONTRIBUTING.md` / the data-policy): is the source (a) free, (b) credential-free,
(c) stable enough to cite, (d) refreshable by a `refresh.sh` in the daily
`refresh.yml` cron — or at least curatable with a stated staleness budget like
`gcp-compute`/`regions`. Lessons L1 (silent staleness) and L4 ("hard limit" rot)
are the main risks flagged per-candidate.

Every data-source claim below carries a URL. Sources reached via WebFetch/curl
on 2026-05-16 are marked **[reached]**; anything not directly fetched is marked.

---

## Candidate 1 — Carbon Intensity Atlas (region × gCO2eq/kWh × CFE%)

**Value proposition:** the only cross-vendor view of how dirty each cloud region's
electricity is — pick `europe-north1` over `asia-south1` and cut workload carbon
~7×, a decision every region-map user implicitly makes blind today.

**Public data sources:**

- GCP — `GoogleCloudPlatform/region-carbon-info`, machine-readable CSV per year,
  Apache-2.0. **[reached]** `https://github.com/GoogleCloudPlatform/region-carbon-info`
  — repo last pushed 2025-12-03, six yearly files `data/yearly/2019.csv` …
  `2024.csv`. Schema is exactly 4 columns:
  `Google Cloud Region, Location, Google CFE, Grid carbon intensity (gCO2eq / kWh)`.
  Raw: `https://raw.githubusercontent.com/GoogleCloudPlatform/region-carbon-info/main/data/yearly/2024.csv` **[reached]** — e.g. `asia-south1,Mumbai,0.09,678.76` vs `europe-north2,Stockholm,1.00,~3`.
  Human page: `https://cloud.google.com/sustainability/region-carbon` **[reached]**.
- Azure — community-extracted PUE/WUE/renewable JSON from Microsoft's regional
  fact-sheet PDFs: `https://raw.githubusercontent.com/autosysops/azure_sustainability_data/main/regiondata.json`
  **[reached]** — 28 regions, fields PUE / WUE / renewable %. Source PDFs:
  `https://datacenters.microsoft.com/globe/fact-sheets/`. No timestamp in the JSON
  (obstacle — see below). Azure publishes *no* per-region grid-carbon number.
- AWS — **does not publish per-region carbon intensity at all.** AWS's own
  sustainability guidance tells customers to use Electricity Maps instead:
  `https://aws.amazon.com/blogs/architecture/how-to-select-a-region-for-your-workload-based-on-sustainability-goals/`.
  AWS publishes only a binary "19 regions 100%-renewable-attributed since Jan 2022"
  claim (market-based): `https://sustainability.aboutamazon.com/products-services/aws-cloud`.
- Electricity Maps — the upstream both GCP and AWS defer to. A free zone-level
  API exists but is **key-gated** (`https://api.electricitymap.org`); the free
  public artifact is the yearly carbon-intensity CSV at
  `https://www.electricitymaps.com/data-portal` (zone, not cloud-region, granularity).

**Free / stable / refreshable without credentials?**
GCP: yes on all three — a `refresh.sh` can `curl` the raw CSV; it is the cleanest
credential-free dataset found in this whole scan. Azure: free + credential-free
but the community JSON is a third-party scrape with no update guarantee and no
timestamp. AWS: no usable per-region data exists.

**Obstacle:** asymmetric coverage. Only GCP gives a real per-region number; AWS
gives nothing comparable. A true cross-vendor *grid-carbon* matrix would need
Electricity Maps' zone CSV mapped onto AWS/Azure region→city→grid-zone — a
curation layer (publishable, but a maintained mapping like `regions/`). Honest
v1: a **GCP-first carbon instrument** (clean auto-refresh) with an Azure
PUE/renewable column and an explicit "AWS publishes nothing" cell — consistent
with the site's "with the asterisks intact" tone. L1 risk is low for the GCP CSV
(it carries its own year); high for the Azure scrape.

---

## Candidate 2 — Inter-Region Latency Matrix

**Value proposition:** "how many ms from Frankfurt to Singapore on this cloud's
backbone" — the number behind every multi-region / DR-pair decision, and the
region map shows geography but not the latency that geography implies.

**Public data sources:**

- Azure — `https://learn.microsoft.com/en-us/azure/networking/azure-network-latency`
  **[reached]**. P50 round-trip ms between ~50 Azure regions. Critically, the page
  **embeds a complete single CSV block** (`Source,<region>,…` 50×50 matrix) in
  addition to the per-tab HTML tables — directly parseable. Dataset dated
  2025-07-07, page metadata `updated_at: 2025-08-18`.
- OCI — inter-region latency doc + live dashboard:
  `https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/inter_region_latency.htm`
  and the dashboard announced at
  `https://blogs.oracle.com/cloud-infrastructure/post/announcing-the-inter-region-latency-dashboard-for-oracle-cloud-infrastructure`.
- GCP — no first-party inter-region latency table published; only an in-console
  Network Intelligence Center and the per-VM test docs.
- AWS — no public table; AWS Network Manager Infrastructure Performance is
  account-scoped (`https://docs.aws.amazon.com/vpc/latest/userguide/working-with-up.html`).
- Cross-cloud third-party: Kentik Cloud Latency Map
  (`https://www.kentik.com/blog/announcing-the-cloud-latency-map/`) — not a
  citable raw dataset.

**Free / stable / refreshable without credentials?**
Azure: yes — free, credential-free, and the embedded CSV makes a `refresh.sh`
trivial (`curl` the page, slice the fenced ```csv block). Stability caveat:
Microsoft states the numbers refresh only **every 6–9 months** — so a *daily*
cron is pointless; this is a curated/slow-refresh instrument with a stated
staleness budget, like `gcp-compute`. OCI: free, credential-free, but the
dashboard is JS-rendered (harder to scrape). GCP/AWS: nothing.

**Obstacle:** same asymmetry as carbon — only Azure (and partially OCI) expose
the data, so a genuine *cross-cloud* matrix is not possible from first-party
sources. Defensible scopes: (a) an **Azure-only latency matrix** (the CSV is
a gift), or (b) an Azure+OCI "backbone latency" instrument with AWS/GCP marked
"not published". Either way it complements `regions/` well — same region
vocabulary, adds the dimension the map can't show.

---

## Candidate 3 — Object Storage Tier & Egress Matrix

**Value proposition:** one table of every object-storage tier (hot → deep
archive) and its true cost stack — $/GB-month **plus** retrieval $/GB, minimum
retention days, and per-1k-request fees — the line items that make "archive"
quietly cost 5× the sticker.

**Public data sources:**

- AWS — the **AWS Price List Bulk API is fully credential-free.** Verified by
  `curl`: `https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/index.json`
  returned **HTTP 200, no auth**, `publicationDate: 2026-05-15` **[reached]**,
  listing 267 offer files including `AmazonS3` and `AWSDataTransfer`. Per-service
  offer JSON is linked from that index. Human page: `https://aws.amazon.com/s3/pricing/`.
- Azure — Retail Prices REST API, also **no credentials**:
  `https://prices.azure.com/api/retail/prices` (filterable by `serviceName eq
  'Storage'`). Tier doc: `https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview`.
- GCP — storage pricing is documented on
  `https://cloud.google.com/storage/pricing`, but the *programmatic* Cloud
  Billing Catalog API **requires an API key** — the same blocker that keeps
  `gcp-compute` curated today.
- Cloudflare R2 — flat published pricing, `https://developers.cloudflare.com/r2/pricing/`
  (notable as the "$0 egress" outlier).

**Free / stable / refreshable without credentials?**
AWS + Azure: yes — both bulk pricing APIs are genuinely open and date-stamped,
so a `refresh.sh` is feasible. GCP: no credential-free machine source; the
numbers would have to be curated from the pricing page (small, stable set —
4 tiers — so a curated column is low-burden).

**Obstacle:** the AWS S3 offer file is large and its JSON is verbose
("dimension" rows keyed by SKU) — non-trivial but tractable transform, same
shape as `ec2/refresh.sh` already does for the Vantage dataset. The editorial
risk is L4: retrieval-fee and minimum-retention values are exactly the
"gotcha" numbers that rot — each needs a dated last-verified marker.

---

## Candidate 4 — Data-Transfer / Egress Cost Map

**Value proposition:** the egress-pricing decision in one screen — internet-out
tiered $/GB, cross-region, cross-AZ, and the easily-missed NAT-gateway and
inter-cloud rates — the single most-complained-about and least-transparent line
on a cloud bill.

**Public data sources:**

- AWS — same credential-free `AWSDataTransfer` offer in the Price List Bulk API
  index verified above **[reached]**
  (`https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/index.json`).
  Human reference: `https://aws.amazon.com/blogs/architecture/overview-of-data-transfer-costs-for-common-architectures/`.
- Azure — bandwidth pricing on `https://azure.microsoft.com/en-us/pricing/details/bandwidth/`;
  Retail Prices API (`serviceName` bandwidth filters), credential-free.
- GCP — network pricing `https://cloud.google.com/vpc/network-pricing`
  (Premium vs Standard tier); Billing Catalog API again key-gated.
- Cloudflare R2 zero-egress: `https://developers.cloudflare.com/r2/pricing/`.

**Free / stable / refreshable without credentials?**
AWS + Azure: machine-readable and credential-free. GCP: pricing-page curation
only. Egress matrices are *small* (a dozen rows per vendor) and change rarely,
so even a fully-curated version is cheap to maintain — arguably this is better
as a curated editorial instrument than an auto-refresh one.

**Obstacle:** egress pricing is heavily *conditional* (free tier, same-region
free, CloudFront-routed discounts, committed-use deals) — a flat $/GB table
risks oversimplifying. Mitigation = footnotes, which is on-brand. **Strong
overlap with Candidate 3** — egress is one section of the storage-cost story.
Recommendation: treat C3 + C4 as **one "Cloud Cost Almanac" instrument**
(storage tiers + transfer), not two; splitting them duplicates the AWS Price
List plumbing (a Lesson-L5 / MEMORY duplication flag).

---

## Candidate 5 — GPU / Accelerator Availability Matrix

**Value proposition:** which accelerator (T4 · L4 · A10 · A100 · H100 · H200 ·
B200 · Trainium · TPU) you can actually get in which region — the #1 friction
point for AI workloads, and the landing page *already teases* "GPU progression
V100 → A10 → A100 → H100 → …" without an instrument behind it.

**Public data sources:**

- GCP — `https://docs.cloud.google.com/compute/docs/regions-zones/gpu-regions-zones`
  **[reached]**: an official GPU-model × zone availability table covering T4, L4,
  P4, P100, V100, A100 40/80GB, H100, H200, B200. Free, credential-free, but
  rendered as an interactive filterable table (no raw download).
- AWS — `https://docs.aws.amazon.com/ec2/latest/instancetypes/ac.html` **[reached]**:
  authoritative accelerated-instance list (G4/G5/G6/G7e, P4/P5/P5e/P5en,
  **P6-B200, P6-B300, P6e-GB200**, Trn1/Trn2, Inf1/Inf2) with host-CPU vendor —
  but **no per-region availability**. Region availability for GPUs is scattered
  across "what's new" posts (e.g.
  `https://aws.amazon.com/about-aws/whats-new/2025/08/amazon-p5-single-gpu-instances-now-available/`)
  and the regional instance-type doc
  `https://docs.aws.amazon.com/ec2/latest/instancetypes/ec2-instance-regions.html`.
- Azure — N-series (NC/ND/NG/NV) docs at
  `https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/overview` with
  per-region availability via `https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/`.
- The Vantage `instances.json` that `ec2/refresh.sh` *already pulls* carries
  per-region pricing for accelerated families — so AWS GPU-by-region is partly
  derivable from a dataset the repo already ingests.

**Free / stable / refreshable without credentials?**
All three vendors document it free and credential-free, but **none offers a
clean machine-readable GPU×region file** — GCP's is an interactive table,
AWS's is split across docs + blog posts, Azure's is a products-by-region
filter UI. So this is a **curated cross-vendor instrument** (staleness-budget
model), not an auto-refresh one — unless scoped to AWS-only, where the Vantage
dataset already in-repo could drive it.

**Obstacle:** GPU availability is the **fastest-rotting data in the whole
scan** — capacity, Capacity Blocks vs On-Demand, and "account-team approval
only" zones shift monthly (L4 risk at maximum). A curated matrix needs an
aggressive last-verified date and probably a "this is a snapshot" disclaimer.
Note also MEMORY-L2: host-CPU vendor on GPU shapes is mislabel-prone — the AWS
`ac.html` table is the authoritative cross-check (e.g. P5en = Intel, P6-B200 =
Intel, P6e-GB200 = NVIDIA Grace/arm64).

---

## Candidate 6 — Cross-Cloud Networking Primitives Matrix

**Value proposition:** a Rosetta-stone table mapping equivalent networking
constructs across clouds — Transit Gateway ⇄ Virtual WAN ⇄ Network Connectivity
Center; PrivateLink ⇄ Private Link/Endpoint ⇄ Private Service Connect; plus
peering, NAT, and load-balancer types — the networking analogue of the existing
`equivalent-sku` instrument.

**Public data sources (vendor docs, all free + credential-free):**

- AWS: Transit Gateway `https://docs.aws.amazon.com/vpc/latest/tgw/`,
  PrivateLink `https://docs.aws.amazon.com/vpc/latest/privatelink/`,
  ELB types `https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/`.
- Azure: Virtual WAN `https://learn.microsoft.com/en-us/azure/virtual-wan/`,
  Private Link `https://learn.microsoft.com/en-us/azure/private-link/`,
  Load Balancer `https://learn.microsoft.com/en-us/azure/load-balancer/`.
- GCP: Network Connectivity Center `https://cloud.google.com/network-connectivity/docs/network-connectivity-center`,
  Private Service Connect `https://cloud.google.com/vpc/docs/private-service-connect`,
  Cloud Load Balancing `https://cloud.google.com/load-balancing/docs`.

**Free / stable / refreshable without credentials?**
Free and credential-free, but **inherently editorial** — there is no dataset to
refresh; the value is in the curated mapping and the per-cell asterisks (e.g.
"GCP VPC is global; AWS/Azure VPC/VNet are regional"). This is the
`equivalent-sku` / `kubernetes` / `iam-matrix` model exactly — a hand-built
cross-cloud comparison, no `refresh.sh`.

**Obstacle:** none on the data side — it is squarely in the site's proven
"cross-cloud matrix" format and a natural sibling of the 5 existing matrices.
The only risk is L3/L4: networking limits and "this construct is global vs
regional" claims need source comments in the markup. Effort is editorial, not
engineering. Of all six this is the **lowest-risk fit** — it needs zero new
pipeline machinery.

---

## Candidate 7 — Service Quotas / Account Limits Explorer

**Value proposition:** the default account quota for any service (EC2 vCPUs,
ENIs, Lambda concurrency, S3 buckets…) — the wall every team hits in week one
and currently has to discover the hard way.

**Public data sources:**

- AWS — `https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html`
  **[reached]**: this is a *navigation* page, not data — it points to ~310
  per-service HTML pages and a giant PDF. The structured route is the CLI
  `aws service-quotas list-aws-default-service-quotas` — **but that call
  requires AWS credentials** (confirmed in the AWS CLI reference
  `https://docs.aws.amazon.com/cli/latest/reference/service-quotas/list-aws-default-service-quotas.html`).
  Third-party scrape: AWS Fundamentals "Limits Explorer" claims 12,900+ quotas
  (`https://awsfundamentals.com/limits`) — third-party, not citable as source-of-truth.
- Azure — `https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits`,
  one long HTML doc, no machine endpoint without a subscription.
- GCP — quotas documented per-service; the Cloud Quotas API needs credentials.

**Free / stable / refreshable without credentials?**
**No** — this is the weakest candidate on feasibility. Every *structured* quota
source (AWS Service Quotas API, Azure/GCP quota APIs) is **credential-gated**,
violating the project's hard "credential-free" rule. The only credential-free
form is hundreds of scattered HTML pages — not refreshable, only scrapable
fragilely.

**Obstacle:** fundamental. Quotas are also region- and account-age-dependent
("your actual quota may be less than the default" — AWS's own caveat), so even
a curated snapshot is caveat-heavy. Recommend **not building this** unless
scoped to a tiny curated "headline default limits" editorial card — and even
then it is L4-rot-prone. Listed here for completeness; ranked last.

---

## Candidate 8 — Managed Database Catalog (engine × version × cloud)

**Value proposition:** which managed-DB engines and engine **versions** each
cloud offers — RDS (6 engines) ⇄ Aurora ⇄ Cloud SQL ⇄ AlloyDB ⇄ Azure SQL /
Flexible Server ⇄ OCI Base DB / Autonomous — plus the cloud-native outliers
(Aurora 128 TiB autoscale, AlloyDB columnar engine). The database analogue of
the existing compute explorers and the `kubernetes` version matrix.

**Public data sources (vendor docs, free + credential-free):**

- AWS: RDS engine/version docs
  `https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html`,
  Aurora `https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/`.
  Engine versions are also queryable credential-free-ish only via API.
- GCP: Cloud SQL `https://cloud.google.com/sql/docs/db-versions`,
  AlloyDB `https://cloud.google.com/alloydb/docs`.
- Azure: `https://learn.microsoft.com/en-us/azure/azure-sql/`,
  Flexible Server version docs under
  `https://learn.microsoft.com/en-us/azure/postgresql/`.
- OCI: `https://docs.oracle.com/en-us/iaas/Content/Database/home.htm`.

**Free / stable / refreshable without credentials?**
Docs are free and credential-free, but — like Candidate 6 — there is **no
single dataset to refresh**; supported-version lists live in prose/tables across
many doc pages. This is a **curated editorial matrix** (the `kubernetes`-Atlas
model: "supported versions, control-plane SLA, …" is exactly the same shape
applied to databases).

**Obstacle:** version lists move fairly often (minor-version deprecations) — a
moderate L1/L4 staleness risk, manageable with the `kubernetes` instrument's
existing dated-footnote discipline. Scope risk: "managed databases" is broad
(relational + NoSQL + warehouse) — a v1 should fence to **managed relational
engines** only. Solid fit, but purely editorial effort.

---

## Ranked by data feasibility

Ranking criterion = how cleanly the data satisfies the project's hard
constraints (free, credential-free, refreshable/curatable, citable). It is
*not* a value or effort ranking — value notes appended where they diverge.

| # | Candidate | Free | Cred-free | Machine-readable source | Refresh model | Verdict |
|---|-----------|:----:|:---------:|-------------------------|---------------|---------|
| 1 | **Carbon Intensity Atlas** | yes | yes | **GCP CSV (clean, dated)**; Azure scrape (no date) | `refresh.sh` for GCP; curate Azure | **Most feasible.** GCP `region-carbon-info` CSV is the single best credential-free dataset in this scan — verified, Apache-2.0, self-dating. Build GCP-first, Azure column curated, AWS = honest blank. |
| 2 | Cross-Cloud Networking Primitives | yes | yes | none (vendor docs only) | curated editorial | **Lowest-risk to ship.** No pipeline at all — pure `equivalent-sku`-style matrix. No staleness pipeline needed; fits the 5 existing cross-cloud matrices perfectly. |
| 3 | Inter-Region Latency Matrix | yes | yes | **Azure embeds a full CSV in the doc page** | slow `refresh.sh` (6–9 mo cadence) | Highly feasible **for Azure** (the embedded ```csv block is a gift). Not cross-cloud — AWS/GCP publish nothing. Scope honestly as Azure(+OCI). |
| 4 | Managed Database Catalog | yes | yes | none (vendor docs only) | curated editorial | Feasible as a curated matrix (the `kubernetes` model). No dataset to auto-refresh; moderate version-churn upkeep. Fence v1 to relational engines. |
| 5 | Cloud Cost Almanac (storage tiers **+** egress — merge C3 & C4) | yes | partial | **AWS Price List Bulk API + Azure Retail Prices API both credential-free** (AWS index verified HTTP 200, dated 2026-05-15); **GCP needs an API key** | `refresh.sh` for AWS/Azure; curate GCP tiers | Feasible with one caveat: GCP has no credential-free machine source (same blocker as `gcp-compute`). Treat storage + egress as ONE instrument — they share the AWS Price List plumbing (MEMORY anti-duplication rule). L4 rot risk on retrieval/min-retention fees → dated markers. |
| 6 | GPU / Accelerator Availability Matrix | yes | yes | none clean (GCP interactive table; AWS docs+blogs; Azure filter UI) | curated snapshot | High *value* (landing page already teases it) but **fastest-rotting data in the scan** — capacity shifts monthly. Curated-only, needs aggressive last-verified dating + "snapshot" disclaimer. AWS-only variant could reuse the in-repo Vantage dataset. |
| 7 | Service Quotas / Account Limits | partial | **no** | structured sources all credential-gated | not refreshable credential-free | **Least feasible — recommend against.** Every structured quota API (AWS Service Quotas, Azure/GCP quota APIs) requires credentials; the only open form is ~310 scattered HTML pages. Violates the hard credential-free rule. Account/region-dependent values make even a snapshot caveat-heavy. |

**Cross-cutting observations**

- **The credential-free rule is the real filter.** It cleanly *kills* Candidate 7
  and *handicaps* anything depending on GCP machine data (carbon Azic-side,
  storage, egress all hit the same GCP-billing-API key wall that already forced
  `gcp-compute` to be curated). The verified-open APIs are: GCP `region-carbon-info`
  raw CSV, the AWS Price List Bulk API (`pricing.us-east-1.amazonaws.com`, no auth,
  daily-dated), and the Azure Retail Prices API — those three are the only solid
  auto-refresh foundations found.
- **Asymmetric vendor coverage is the recurring trap.** Carbon and latency both
  have exactly one vendor with good public data (GCP, Azure respectively). A
  rigorous instrument should *show the gap* (blank "AWS publishes nothing" cells)
  rather than fabricate parity — directly consistent with Lesson L3 (no
  first-principles data) and the site's "with the asterisks intact" voice.
- **Two pairs collapse.** C3+C4 are one "Cloud Cost Almanac" (shared AWS Price
  List pipeline — building them separately would duplicate the plumbing, a
  MEMORY-flagged anti-pattern). C5/C6/C8 are all the same proven curated
  cross-cloud-matrix shape as the existing 5 — cheap to add, no new machinery.
- **Staleness budget must be explicit per candidate (Lesson L1).** GPU data
  rots monthly; DB versions quarterly; egress/networking yearly; the GCP carbon
  CSV self-dates. Whatever ships needs the dated-last-verified discipline the
  `kubernetes` instrument already demonstrates — not just a fresh `generated`
  timestamp.
