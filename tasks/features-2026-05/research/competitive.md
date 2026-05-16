# Competitive landscape — Infra Atlas

**Task:** Phase 2a. Map what already exists in the cloud-infra / API-management
reference space and how Infra Atlas (free, static, credential-free, *editorial*,
vendor-neutral, footnoted) compares.

**Method:** WebFetch + WebSearch, May 2026. Every external claim is cited inline.
Sources that could not be reached are flagged explicitly.

**Reading the verdicts:** for each competitor — *does well* / *does NOT cover* /
*Infra Atlas angle* (absorb = steal the idea; differentiate = lean into a gap).

---

## Vantage instance comparator (instances.vantage.sh, formerly ec2instances.info)

URL: https://instances.vantage.sh/ — `ec2instances.info` 301-redirects here
(confirmed: the redirect was returned on fetch).

**What it does well.** The reference implementation of an instance table. Covers
AWS EC2 plus RDS, ElastiCache, Redshift and OpenSearch instance families, with
Azure and GCP comparison pages as secondary surfaces [https://instances.vantage.sh/].
Per-instance it shows vCPU, memory, storage, network rating, on-demand / reserved
/ spot / savings-plan pricing, Linux-vs-Windows cost, and — notably —
**CoreMark and FFmpeg performance benchmarks**, which most clones lack
[https://instances.vantage.sh/]. It has an expression-based filter language
(comparisons, ranges, logical operators), customizable columns, region/currency
selectors, CSV export and an API [https://instances.vantage.sh/]. Tone is
neutral and technical, free, no login for browsing [https://instances.vantage.sh/].

**What it does NOT cover.** It is a *table*, not a reference work — zero
editorial narrative, no "why" behind the numbers, no footnoted provenance per
cell. It is compute-instance-centric: no storage, networking, data-transfer, no
regions/AZ availability matrix, no compliance, no API-management content. Azure
and GCP are clearly second-class. Crucially, **Vantage is a paid FinOps vendor**
and the tool is lead-gen for that product [https://instances.vantage.sh/] — its
neutrality is structurally compromised even if the data is fair.

**Infra Atlas angle.** Do not try to out-table Vantage on EC2 — they have the
benchmarks and the filter language. *Differentiate* on (a) editorial framing —
EC2 Observatory should explain naming generations, deprecations, the gp2→gp3
story, not just list rows; (b) genuine vendor-neutrality — Infra Atlas has no
FinOps product to upsell, so it can say "instance X is a trap" without conflict;
(c) the cross-cloud and APIM instruments Vantage simply does not have. *Absorb*:
their per-instance benchmark idea is worth a footnoted "performance notes" field
sourced from public benchmarks.

---

## ec2instances.info

URL: https://ec2instances.info/ — **now defunct as a standalone site.** Confirmed
via WebFetch: it returns `301 Moved Permanently` to `instances.vantage.sh`. It
was the original community EC2 table; Vantage acquired and absorbed it. Worth
noting because it is the name engineers still type — Infra Atlas's EC2
Observatory competes for that muscle-memory query, and the original brand no
longer answers it independently.

---

## cloudprice.net

URL: https://cloudprice.net/

**What it does well.** Broad multi-cloud VM pricing: "700+ VM sizes"
(its own claim) across Azure (primary focus), AWS (EC2, RDS, OpenSearch,
ElastiCache, Redshift, SageMaker) and GCP Compute Engine [https://cloudprice.net/].
Pricing in hour/day/month/year units, PAYG / reserved (1–3 yr) / savings plans,
20+ currencies, 50+ regions [https://cloudprice.net/]. Rich spec surface —
GPU type/VRAM, RDMA, accelerated networking, ACUs, IOPS, NUMA — plus
"best price region", cost-per-vCPU / cost-per-GB derived metrics, alternative-VM
suggestions, spot price history, batch export (CSV/JSON/XML/Excel) and an API
[https://cloudprice.net/].

**What it does NOT cover.** Non-compute services (storage, networking beyond NIC
specs). No editorial content — it is a pricing grid. And it is **freemium with a
paywall**: "Full Access" requires a subscription [https://cloudprice.net/];
a free *comparison* tier exists [https://cloudprice.net/pricing] but advanced
features sit behind payment. That breaks the "€0 to read, asterisks intact"
promise Infra Atlas makes.

**Infra Atlas angle.** *Differentiate hard on the paywall* — Infra Atlas's
entire pitch is that the full thing is free with no account, where cloudprice
gates depth. cloudprice's derived cost-per-vCPU / cost-per-GB columns are a good
*absorb* for Azure VM Atlas / GCP Compute Index — they are trivial to compute
and genuinely useful, and Infra Atlas can footnote the formula. Do not try to
match its currency/region permutation matrix; that is a maintenance sink with no
editorial payoff.

---

## cloud-mercato (Cloud Mercato)

URL: https://www.cloud-mercato.com/

**What it does well.** The closest thing to a *neutral institution* in this
space — explicitly a "Cloud Transparency Platform" offering vendor-independent
data [https://www.cloud-mercato.com/]. Products: Public Cloud Reference (PCR)
covering "50+ cloud providers", Projector (comparative performance benchmarks),
a GraphQL API, a price/performance portal, plus DocHub, NewsBoard and Observer
[https://www.cloud-mercato.com/]. They publish original research (serverless,
ARM compute, EC2 evolution) and position as objective evaluators, not advocates
[https://www.cloud-mercato.com/]. This is the competitor whose *posture* is
nearest to Infra Atlas.

**What it does NOT cover.** Access is gated — "Unlock the full power" / "Become
client" CTAs indicate a freemium model with premium consulting/reporting for
enterprises [https://www.cloud-mercato.com/]. It is B2B and enterprise-facing,
not a thing an individual engineer casually reads. No API-management coverage.
The tone is research-report / data-platform, not periodical-editorial.

**Infra Atlas angle.** This is the most strategically important comparison.
Cloud Mercato owns "neutral cloud data, sold to enterprises". Infra Atlas should
*differentiate* by owning the adjacent, unoccupied slot: **neutral cloud data,
given away, written for a human to read in one sitting** — the periodical /
"Issue 01" framing is exactly the wedge. Where Cloud Mercato sells a GraphQL
firehose, Infra Atlas curates and *narrates*. Do not compete on provider breadth
(50+) — compete on legibility and zero-friction access.

---

## cloudping.co

URL: https://www.cloudping.co/ (the `/grid` path 404s — confirmed; the matrix
lives at the root).

**What it does well.** Focused and excellent at one job: inter-region latency
for **all 35 AWS regions**, real-time browser-based ping, with a color-coded
matrix (<100ms green / 100–180ms yellow / >180ms red) and historical views over
1 day / week / month / year [https://www.cloudping.co/]. Free, no login,
donation-supported [https://www.cloudping.co/].

**What it does NOT cover.** AWS only — no Azure/GCP/OCI [https://www.cloudping.co/].
No intra-region or service-level latency. It is a single-purpose widget, not a
reference; no editorial layer.

**Infra Atlas angle.** Latency is a *gap* in Infra Atlas's current 16
instruments — the Multi-Cloud Region Map shows *where* regions are but not how
far apart they *feel*. *Absorb* the concept: a "latency footnote" on the region
map, or a cross-cloud latency instrument. But do NOT replicate the live-ping
mechanism — that needs the visitor's browser to do real network calls, which
collides with Infra Atlas's "static, credential-free, no monitoring" identity.
Use *published* latency datasets (AWS/Azure publish some) and footnote them, or
link out to cloudping rather than rebuild it.

---

## cloudpingtest.com

URL: https://cloudpingtest.com/

**What it does well.** Broader provider coverage than cloudping.co — 16
providers including AWS, Azure, GCP, Oracle, OVHcloud, plus the budget tier
(Hetzner, Contabo, Scaleway, Vultr, Linode, DigitalOcean, IBM, Gcore, CoreWeave,
servers.com) [https://cloudpingtest.com/]. Browser-based latency test, free, no
login, donation-optional, maintained by Systron Labs, updated 2025
[https://cloudpingtest.com/].

**What it does NOT cover.** Latency only — no specs, pricing, region metadata or
editorial. No matrix/grid; it measures *your* latency to a provider, not
provider-to-provider [https://cloudpingtest.com/]. Region/bandwidth detail is
thin and it openly invites users to request missing providers
[https://cloudpingtest.com/].

**Infra Atlas angle.** Same verdict as cloudping.co. The one *absorb*-worthy
idea: its provider list is the best free enumeration of the **non-hyperscaler
tier** (Hetzner, Scaleway, OVH, Vultr, etc.). Infra Atlas already has OVH and OCI
instruments; cloudpingtest's roster is a checklist for which alt-clouds an
engineer audience actually cares about — useful input for the OVH Catalogue's
scope and any future alt-cloud instrument.

---

## GCP Cloud Pricing Calculator

URL: https://cloud.google.com/products/calculator

**What it does well.** The official Google estimator — add/configure GCP
products, generate a shareable cost estimate, 26+ currencies
[https://cloud.google.com/products/calculator]. Authoritative for GCP list
prices.

**What it does NOT cover.** It is a **single-vendor sales tool**, and admits it:
no competitive comparison against AWS/Azure, no spec-vs-spec comparison, no
neutral editorial, and an explicit disclaimer that estimates "may not accurately
reflect the final costs on your monthly Google Cloud bill"
[https://cloud.google.com/products/calculator]. Partial login is needed for
billing-account rates [https://cloud.google.com/products/calculator].

**Infra Atlas angle.** Not a real competitor — it is a *forecasting* tool, Infra
Atlas is a *reference*. The takeaway is structural: every hyperscaler calculator
is vendor-captured by construction. Infra Atlas's GCP Compute Index wins simply
by being cross-comparable and neutral. Do not build a "calculator" (stateful,
estimate-y, looks like SaaS) — that would dilute the periodical identity.

---

## gcloud-compute.com (gcosts)

URL: https://gcloud-compute.com/

**What it does well.** A genuinely impressive *single-cloud* reference and the
closest analogue to what Infra Atlas's GCP Compute Index should be. 495 GCE
machine types across Intel/AMD/Arm, 9 disk types, 43 GCP regions, 12,394
machine-region cost combinations including sustained-use and commitment
discounts, OS licensing costs, and SAP/SAP-HANA certification status
[https://gcloud-compute.com/]. Interactive "Instance Picker" grid with combined
filters, keyboard nav, CSV export [https://gcloud-compute.com/]. Free, no login,
**open-source on GitHub**, built by Nils Knieling, sourced from official Google
docs, with an honest "accuracy not guaranteed" disclaimer
[https://gcloud-compute.com/]. The `gcosts` CLI even computes everything locally
with no network needed [https://gcloud-compute.com/gcosts.html].

**What it does NOT cover.** GCP only — no other clouds, no cross-cloud mapping
[https://gcloud-compute.com/]. Tone is "neutral and functional" — straightforward
docs, *no editorial narrative* [https://gcloud-compute.com/]. No API-management,
no compliance, no IAM.

**Infra Atlas angle.** This is the bar for the GCP Compute Index — and Infra
Atlas's own todo.md flags that `gcp-compute` is **CURATED** (a human must hand-
edit `index.html` to add a machine type) whereas gcloud-compute pulls from
official docs. That is a real freshness disadvantage; flag it. *Differentiate*
by being cross-cloud (gcloud-compute is single-cloud) and editorial (it is not).
*Absorb*: SAP-HANA certification status and OS-licensing-cost columns are smart,
footnotable fields. Its open-source + "accuracy not guaranteed" honesty is also
a model for Infra Atlas's own data-trust posture.

---

## DevZero instance comparison

URL: https://www.devzero.io/instances/compare

**What it does well.** Multi-cloud instance comparison — AWS, Azure, GCP,
"24,051 instances match" with vCPU, RAM, on-demand and spot pricing, regional
availability, GPU filter; filter by vCPU/memory/GPU/OS/region/provider, sort by
price [https://www.devzero.io/instances/compare]. Free, no login for browsing
[https://www.devzero.io/instances/compare].

**What it does NOT cover.** No storage, networking, data-transfer or egress
pricing, no performance benchmarks [https://www.devzero.io/instances/compare].
No editorial. And **DevZero is a commercial vendor** (DevInfra Inc) — the tool
funnels to a paid "live rightsizing MicroVMs" product and a "free assessment"
sign-up [https://www.devzero.io/instances/compare]. Same lead-gen pattern as
Vantage.

**Infra Atlas angle.** A me-too instance grid behind a SaaS funnel. *Differentiate*
on neutrality (no product to sell) and on coverage breadth beyond instances.
Nothing here to absorb that cloudprice/Vantage do not already do better.

---

## Holori

URL: https://holori.com/ and https://holori.com/gcp-pricing-calculator/

**What it does well.** Two-faced: a public free **GCP pricing calculator** with
adjustable CPU/GPU/memory/price/storage/location filters
[https://holori.com/gcp-pricing-calculator/], plus per-provider region lists
(e.g. OCI regions) [https://holori.com/oracle-cloud-regions/], and AWS/GCP/Azure
architecture-**diagram builders**. The free calculators are real, useful and
ungated.

**What it does NOT cover.** The core product is a **paid FinOps SaaS** — "The
Modern FinOps Platform for the AI era", login/sign-up required, subscription
pricing [https://holori.com/]. The free calculators and region pages are
content-marketing top-of-funnel for that SaaS. No editorial periodical layer; no
APIM coverage.

**Infra Atlas angle.** Holori's free region pages overlap directly with the
Multi-Cloud Region Map — but they are SEO landing pages, not a coherent map.
*Differentiate* by being one cohesive, navigable, footnoted region instrument
rather than scattered marketing pages. The diagram-builder is out of scope (it
is a tool, not a reference) and a good *anti-list* candidate.

---

## Cloud Infrastructure Map (TeleGeography)

URL: https://www.cloudinfrastructuremap.com/ — **content could not be fully
retrieved**: WebFetch returned only the page title with no body text (likely a
JS-rendered SPA that returns an empty shell to scrapers). Findings below are from
the search-result description, not a direct read.

**What it appears to do** (per search result
[https://www.cloudinfrastructuremap.com/], surfaced via WebSearch). TeleGeography
maintains an interactive map of cloud regions and the submarine-cable / network
backbone connecting them — its specialty is the *physical network* layer, not
specs or pricing.

**What it does NOT cover** (inferred — flagged as unverified). No instance specs,
no pricing, no compliance — it is a geography/connectivity visualization.

**Infra Atlas angle.** *Differentiate*: the Multi-Cloud Region Map should stay a
*reference* (region codes, AZ counts, launch dates, per the city-modelled
`regions/data.json`) rather than chase TeleGeography's cartography. If anything,
link out to it for the network-topology view. **Caveat:** re-verify this entry
directly before relying on it — the page would not yield content.

---

## Karpenter / EKS node-selector explorers (ec2-instance-selector, eks-node-viewer)

URLs: https://github.com/awslabs/eks-node-viewer and the AWS `ec2-instance-selector`
CLI (https://github.com/aws/amazon-ec2-instance-selector).

**What they do well.** These are CLIs/tooling, not reference sites.
`ec2-instance-selector` filters the EC2 catalogue by resource criteria to feed a
*diverse instance list* into a Karpenter NodePool — AWS guidance is to give
Karpenter the widest possible instance list for its price-capacity-optimized
strategy [https://aws.github.io/aws-eks-best-practices/karpenter/]. `eks-node-viewer`
visualizes live EKS node allocation/cost and can filter to Karpenter-managed
nodes [https://github.com/awslabs/eks-node-viewer]. Karpenter itself provisions
via the EC2 Fleet API, choosing instance type / AZ / purchase option per pending
pod [https://docs.aws.amazon.com/eks/latest/best-practices/karpenter.html].

**What they do NOT cover.** They are operational tooling that runs against a live
cluster or the live EC2 API — not a static, browsable reference. No cross-cloud
view, no editorial, no Azure/GKE/OKE equivalent in one place.

**Infra Atlas angle.** Infra Atlas's Kubernetes Atlas should *not* become a node
provisioner — that requires credentials and a cluster, violating the
credential-free identity. The genuine *absorb*: there is no neutral, static
**reference** explaining how each managed-K8s service (EKS/AKS/GKE/OKE) does node
autoscaling — Karpenter vs Cluster Autoscaler vs node auto-provisioning, which
instance families each supports, spot integration. That is editorial,
footnotable, and unoccupied. The Kubernetes Atlas could add a "node lifecycle /
autoscaling" comparison row-set.

---

## AWS Regional Services table

URL: https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/

**What it does well.** The authoritative source for *which AWS service is in
which region*. Official AWS doc, updated daily, with a filter control
[https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/].
Maintained by AWS's Regional Information Provider team
[https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/].

**What it does NOT cover.** AWS only. No pricing, no specs, no comparison with
other clouds, no detailed service docs
[https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/].
It is a raw availability matrix with no narrative — and it is single-vendor by
definition.

**Infra Atlas angle.** This is a strong *absorb* target. There is no neutral,
**cross-cloud** "is service X live in region Y" matrix — AWS, Azure and GCP each
publish their own, in different formats, none comparable. A "regional service
availability" layer on the Multi-Cloud Region Map (does region Y have managed-K8s
/ confidential-compute / this APIM product) would be genuinely novel and footnote
cleanly to the three official tables. Note: AWS's table updates daily and is
authoritative — Infra Atlas's region instruments are CURATED per its own todo.md,
so any availability data must be honestly dated.

---

## Azure Retail Prices API and its consumers

URL: https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices

**What it does well.** A free, public, no-auth REST API exposing official list
prices for every Azure service, paginated at 1,000 records/request — the
canonical feed that powers Azure-pricing tools and lets anyone build SKU/region
price comparisons [https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices].
Consumers range from cloudprice.net to an "Azure Pricing MCP Server"
[https://mcpservers.org/servers/charris-msft/azure-pricing-mcp].

**What it does NOT cover.** It is *infrastructure*, not a competitor — a raw data
source with no UI, no specs, no editorial. The API returns list prices that can
diverge from actual invoiced cost [https://www.technetexperts.com/azure-retail-prices-api-billing-validation/].

**Infra Atlas angle.** This is an *input*, not a rival. The Azure VM Atlas should
be consuming this API in its refresh pipeline — and per todo.md, `azure-vm` is
one of the instruments that genuinely does pull a public API, so that is already
right. The competitive lesson: anyone can hit this API, so an Azure price *table*
is a commodity. Infra Atlas's edge is the editorial/cross-cloud layer on top, and
honestly footnoting "list price, not invoiced price" — a nuance most consumers
of this API silently get wrong.

---

## Gartner / Forrester APIM comparisons (publicly leaked summaries)

URLs: vendor-hosted reprints of the 2025 Gartner Magic Quadrant for API
Management — e.g. https://cloud.google.com/resources/content/2025-gartner-mq-apim
(Google/Apigee), https://konghq.com/resources/reports/gartner-magic-quadrant-full-lifecycle-api-management
(Kong), https://www.mulesoft.com/lp/reports/gartner-magic-quadrant-api (MuleSoft),
https://www.ibm.com/new/announcements/ibm-named-a-leader-in-the-2025-gartner-magic-quadrant-for-api-management
(IBM).

**What they do well.** The 2025 Gartner MQ for API Management evaluates 17
vendors and is the industry's reference for vendor positioning
[https://www.gartner.com/en/documents/7020998]. Apigee is a Leader, positioned
highest for Ability to Execute, 10th consecutive year
[https://cloud.google.com/blog/products/ai-machine-learning/apigee-a-leader-in-2025-gartner-api-management-magic-quadrant];
Kong is a Leader, furthest for Completeness of Vision, 6th consecutive year
[https://finance.yahoo.com/news/kong-named-leader-gartner-magic-150000161.html];
IBM is a Leader, 10th consecutive time
[https://www.ibm.com/new/announcements/ibm-named-a-leader-in-the-2025-gartner-magic-quadrant-for-api-management];
MuleSoft a Leader 10 times consecutively
[https://www.mulesoft.com/lp/reports/gartner-magic-quadrant-api]; Boomi a Leader
[https://boomi.com/blog/gartner-magic-quadrant-apim-boomi/]. Gartner Peer
Insights adds crowd-sourced reviews [https://www.gartner.com/reviews/market/api-management].

**What they do NOT cover.** The full reports are paywalled — only vendor-hosted
"complimentary" reprints (each spun by the sponsoring vendor) and quadrant blurbs
are public; the Visionaries/Challengers/Niche-Players detail did not surface in
open search. Gartner's framing is enterprise-procurement (Ability to Execute /
Completeness of Vision), *not* a hands-on feature/pricing comparison. It does not
tell an engineer which gateway to pick for a Lambda backend.

**Infra Atlas angle.** This is the single biggest opportunity for the APIM
instruments. *Differentiate* sharply: Gartner answers "which vendor is safe to
buy" for a CIO; Infra Atlas's APIM Feature Matrix can answer "what does each
product actually *do*, by feature, footnoted" for an engineer/architect — and
give it away. Where Gartner is paywalled and abstract, Infra Atlas is free and
concrete. *Absorb*: Gartner's vendor list (17 vendors) is a good completeness
checklist — verify the APIM Feature Matrix covers the Leaders (Apigee, Kong, IBM,
MuleSoft, Boomi) plus Azure APIM and AWS API Gateway. The APIM Feature Matrix
could even carry a footnoted, neutral "Gartner 2025 position" column citing the
public reprints — context Gartner itself does not give away in usable form.

---

## API gateway comparison content (api7.ai, neosalpha, zuplo, digitalapi.ai)

URLs: https://api7.ai/api-gateway-comparison, https://neosalpha.com/apigee-vs-mulesoft-vs-kong-api-platform-comparison/,
https://zuplo.com/blog/top-10-api-management-tools-for-2025-a-deep-dive-for-architects,
https://www.digitalapi.ai/blogs/best-api-gateway

**What they do well.** A dense field of free, no-login APIM comparison articles.
api7.ai hosts "30+ head-to-head comparisons" spanning APISIX, Kong, AWS API
Gateway, Apigee, Tyk, Traefik, Azure APIM, MuleSoft, Gloo, KrakenD, Gravitee,
WSO2, Layer7, 3scale, IBM DataPower [https://api7.ai/api-gateway-comparison].
Collectively these articles surface useful concrete facts — e.g. Kong vs Apigee X
vs MuleSoft Flex throughput benchmarks (54,250 vs 1,750 vs 1,250 TPS), the
distinction that AWS/Cloudflare gateways are routing proxies without
portals/monetization while Apigee/Azure APIM are full lifecycle platforms, and
self-host infra cost bands (~$500–2,000/mo) vs enterprise contracts
($50k–500k+/yr) [https://www.digitalapi.ai/blogs/best-api-gateway].

**What they do NOT cover.** Almost all are **vendor-published and biased** —
api7.ai sells API7 Enterprise (built on APISIX) and the comparison favors APISIX,
e.g. dinging Kong's PostgreSQL "overhead" [https://api7.ai/api-gateway-comparison];
zuplo, digitalapi.ai, neosalpha each sell or consult on API products. They are
prose blog posts, not a maintained matrix — no consistent footnoted feature grid,
no neutral custodian, content drifts stale, and "best of 2026" listicles are SEO
plays.

**Infra Atlas angle.** This is exactly the gap the APIM Feature Matrix and the
Kong/Gravitee/IBM self-hosted comparison are built for. *Differentiate* on the
two things every one of these articles lacks: **(1) genuine vendor-neutrality** —
Infra Atlas sells nothing — and **(2) a maintained, footnoted matrix** instead of
a once-written blog post. *Absorb* the good raw facts (throughput numbers, the
proxy-vs-platform taxonomy, self-host cost bands) — but each must be re-verified
against a primary/vendor-neutral source and footnoted, never taken from a
competitor's marketing post.

---

## "Last Week in AWS" / Corey Quinn

URL: https://www.lastweekinaws.com/

**What it does well.** The reference *editorial voice* for cloud infrastructure —
Corey Quinn's newsletter, blog and podcasts ("Last Week in AWS",
"Screaming in the Cloud") filter AWS news with sharp, opinionated commentary;
free, supported by the Duckbill Group FinOps consultancy
[https://www.lastweekinaws.com/]. Quinn's AWS pricing/billing teardowns are the
gold standard for making infra economics legible and entertaining. Primarily
AWS, with multi-cloud on the podcast [https://www.lastweekinaws.com/].

**What it does NOT cover.** It is *commentary and journalism*, not a structured
reference — you cannot look up "m7g.xlarge spec" or "is service X in eu-west-3"
in it. No matrices, no instrument-style data, no footnoted reference tables. It
is a stream of takes, organized by date, not by topic.

**Infra Atlas angle.** Not a competitor — a *spiritual sibling*, and a tone
template. Infra Atlas's "Issue 01 / editorial / asterisks intact" framing lives
in the same neighborhood as Last Week in AWS, but occupies the complementary
slot: **Quinn is the columnist, Infra Atlas is the almanac.** *Absorb* the
lesson that opinionated voice + rigor is what makes infra content readable —
the editorial framing of each instrument should have a point of view, not just
data. *Differentiate* by being the structured, footnoted, look-it-up reference
Quinn's format deliberately is not. (Realistically: a link/citation from that
audience is a plausible distribution channel.)

---

## The Pragmatic Engineer (infra deep-dives) and Spare Cores

URLs: https://newsletter.pragmaticengineer.com/p/spare-cores and https://sparecores.com/

**What they do well.** Pragmatic Engineer (Gergely Orosz) publishes long-form
infra deep-dives — the relevant one profiles **Spare Cores**, a 3-person team
building transparent cross-cloud instance pricing/benchmarking
[https://newsletter.pragmaticengineer.com/p/spare-cores]. Spare Cores' Navigator
benchmarks 2,000+ instance types across **AWS, GCP, Azure and Hetzner** with
real-time pricing and *workload* benchmarks (LLM, database, compression), tracks
server/storage/traffic pricing and regional availability
[https://sparecores.com/]; its Resource Tracker is open-source (MPL), no login
for the core benchmarking tools [https://sparecores.com/].

**What they do NOT cover.** Spare Cores is explicitly scoped to "bursty,
episodic ML workloads — not 24/7 web services" [https://sparecores.com/], and its
Sentinel monitoring product is freemium/sign-up [https://sparecores.com/] —
i.e. it is drifting toward being a SaaS. It has no APIM, compliance or
cross-cloud-mapping content. Pragmatic Engineer is a paid newsletter and a
journalism outlet, not a reference.

**Infra Atlas angle.** Spare Cores is the most *philosophically aligned* tooling
competitor — open-source, neutral, transparency-driven, even sourcing benchmarks.
*Differentiate* on two axes: (1) Spare Cores targets ML/episodic workloads;
Infra Atlas is general-purpose infra reference including steady-state and APIM;
(2) Spare Cores is a *tool/SaaS* trajectory, Infra Atlas is a *periodical* — no
sign-up, no Sentinel-style monitoring. *Absorb*: their workload-level benchmarks
(LLM/db/compression rather than synthetic CoreMark) are a strong, footnotable
idea for the compute instruments, and Hetzner is a notable alt-cloud they cover
that Infra Atlas does not. The Pragmatic Engineer's existence proves there is a
real, paying audience for legible infra writing — validation for the editorial
bet, and another plausible citation/distribution path.

---

## "awesome-*" curated lists (awesome-cloud, awesome-alt-clouds, etc.)

URLs: https://github.com/JStumpp/awesome-cloud, https://github.com/datum-cloud/awesome-alt-clouds,
https://github.com/Noovolari/awesome-cloudops

**What they do well.** The incumbent "curated anthology" format — free, no login,
community-maintained GitHub link-lists of cloud services, tools and resources
[https://github.com/JStumpp/awesome-cloud]. awesome-alt-clouds is notable: a
curated list of non-hyperscaler / specialized clouds
[https://github.com/datum-cloud/awesome-alt-clouds].

**What they do NOT cover.** They are *link directories* — no data, no specs, no
comparison, no footnoted claims, no editorial synthesis. Quality varies, many go
stale, and a flat bullet list of links is not a reference work.

**Infra Atlas angle.** Infra Atlas's "anthology of instruments" framing competes
loosely with this genre — and wins easily. *Differentiate*: awesome-lists *point*
at things; Infra Atlas's instruments *contain* the comparison, the data and the
footnotes. The only *absorb*: awesome-alt-clouds is a useful scoping input for
which alt-clouds (beyond OVH/OCI) might deserve future instruments.

---

## Differentiation opportunities for Infra Atlas

Synthesis of the above. Each opportunity ties to a named competitor gap.

**1. Own "free + neutral + readable" — the slot nobody holds.** Every serious
data competitor is compromised on one of those three axes:
- *Vantage, DevZero, Holori, cloudprice* — free-ish but **lead-gen for a paid
  FinOps/SaaS product**, so structurally not neutral, and several gate depth
  behind a paywall [https://instances.vantage.sh/; https://www.devzero.io/instances/compare;
  https://holori.com/; https://cloudprice.net/pricing].
- *Cloud Mercato* — genuinely neutral but **enterprise-gated and B2B**, not
  something an engineer casually reads [https://www.cloud-mercato.com/].
- *Gartner/Forrester* — authoritative but **paywalled and abstract**
  [https://www.gartner.com/en/documents/7020998].
- *Hyperscaler calculators* — free but **single-vendor by construction**
  [https://cloud.google.com/products/calculator].
Infra Atlas is the only candidate that can be *all three*: €0, no account,
no product to upsell, written to be read. The "Issue 01 / periodical /
asterisks intact" framing is the right wedge — lean into it hard.

**2. Cross-cloud is the moat; nobody does it neutrally and for free.** The best
data tools are single-cloud (gcloud-compute = GCP only
[https://gcloud-compute.com/]; AWS regional table = AWS only
[https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/];
cloudping.co = AWS only [https://www.cloudping.co/]). Multi-cloud tools that
exist are paywalled/SaaS. Infra Atlas's Equivalent-SKU Finder, IAM Matrix,
Kubernetes Atlas, Compliance Footprint, Confidential Computing instruments have
*no direct free neutral competitor* — invest there preferentially over
out-tabling Vantage on EC2.

**3. APIM is wide open.** There is no free, neutral, maintained, footnoted API-
management feature matrix. The field is Gartner (paywalled, abstract) on one side
and vendor-biased blog comparisons (api7.ai, zuplo, digitalapi.ai, neosalpha) on
the other [https://api7.ai/api-gateway-comparison; https://www.digitalapi.ai/blogs/best-api-gateway].
Infra Atlas's five APIM instruments are its most defensible territory. Concrete
moves: ensure the Feature Matrix covers all 2025 Gartner Leaders (Apigee, Kong,
IBM, MuleSoft, Boomi) plus Azure APIM and AWS API Gateway; consider a footnoted
"Gartner 2025 position" column citing public reprints.

**4. Absorb these specific, footnotable fields** (each cheap, each cites cleanly):
- *cost-per-vCPU / cost-per-GB* derived columns — from cloudprice
  [https://cloudprice.net/].
- *SAP/SAP-HANA certification* and *OS-licensing cost* columns — from
  gcloud-compute [https://gcloud-compute.com/].
- *workload-level benchmarks* (LLM / database / compression, not just synthetic
  CoreMark) — from Spare Cores [https://sparecores.com/].
- *"list price ≠ invoiced price"* honesty footnote on all pricing — a nuance
  consumers of the Azure Retail Prices API routinely miss
  [https://www.technetexperts.com/azure-retail-prices-api-billing-validation/].

**5. Two genuine content gaps worth a new instrument or row-set:**
- *Cross-cloud regional service availability* — "is managed-K8s / confidential-
  compute / APIM-product live in region Y" across AWS+Azure+GCP. Each vendor
  publishes its own table in its own format; nobody unifies them
  [https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/].
  A natural layer on the Multi-Cloud Region Map.
- *Managed-Kubernetes node-autoscaling reference* — Karpenter vs Cluster
  Autoscaler vs GKE node auto-provisioning vs AKS, what each supports, spot
  integration. Today this lives only in operational CLIs and AWS best-practice
  docs [https://aws.github.io/aws-eks-best-practices/karpenter/], never as a
  neutral static reference. A natural row-set for the Kubernetes Atlas.

**6. Anti-patterns — explicitly do NOT build these** (they would erode the
identity; candidates for `anti-list.md`):
- A **cost calculator** — stateful, estimate-y, indistinguishable from a SaaS;
  hyperscalers own this and it is the wrong genre [https://cloud.google.com/products/calculator].
- **Live browser-based latency ping** — needs the visitor to run real network
  calls; collides with "static, credential-free, no monitoring of user infra".
  Use published latency datasets and footnote them, or link to cloudping
  [https://www.cloudping.co/].
- **Architecture-diagram builders** — a tool, not a reference; Holori already
  does it [https://holori.com/].
- **A node provisioner / cluster-connected explorer** — requires credentials and
  a live cluster, violating the credential-free promise
  [https://github.com/awslabs/eks-node-viewer].

**7. Honesty as a differentiator — and a known weakness to fix.** gcloud-compute
ships an "accuracy not guaranteed" disclaimer and is open-source
[https://gcloud-compute.com/]; Spare Cores is open-source and transparency-first
[https://sparecores.com/]. Infra Atlas's footnote-everything ethos is the same
instinct and should be made *visible* (per-cell provenance, "last verified"
dates). But the project's own `todo.md` records a real gap: the `regions` and
`gcp-compute` instruments are **CURATED** — a daily refresh cannot discover a new
region or machine type, a human must hand-edit `index.html` first — whereas
gcloud-compute and the AWS regional table refresh from official docs. That is a
genuine freshness disadvantage versus those two competitors. Either close it
(pipeline that reads vendor docs) or footnote it honestly with visible
"last verified" dates so the editorial-integrity promise is not quietly broken.

---

### Sources that could not be fully reached

- **cloudinfrastructuremap.com** — WebFetch returned only the page title, no body
  (JS-rendered SPA). That entry relies on a WebSearch-result description and is
  flagged unverified; re-check directly before relying on it.
- **cloudregionsmap.com** — `ECONNREFUSED` on fetch; not used as a source.
- **cloudping.co/grid** — returns HTTP 404; the latency matrix is at the site
  root (https://www.cloudping.co/), which was fetched successfully.
- **Full Gartner / Forrester APIM reports** — paywalled; only vendor-hosted
  reprints and quadrant blurbs are public, so Visionary/Challenger/Niche-Player
  detail is not covered here.
