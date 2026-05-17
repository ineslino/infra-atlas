# Phase 2d — SEO & search-intent research

Research pass on the search landscape for Infra Atlas's 16 instruments.
Conducted 2026-05-17 via WebSearch/WebFetch.

**Read this caveat first.** Precise, current search-volume numbers are paywalled
(Ahrefs / Semrush / Google Keyword Planner). This document deliberately does
**not** invent volume figures. Where it estimates demand it does so from
*observable proxies*: the composition of the result page, the existence of
dedicated commercial tools (a strong revealed-demand signal — nobody builds and
maintains a tool for a query nobody searches), AWS re:Post / Stack Overflow
question density, and the breadth of competing content. Every claim cites a URL.
Anything labelled "(approx)" is an inference, not a measured number.

---

## 1 · Search demand & landscape

The 16 instruments cluster into four search-intent buckets. Each behaves
differently in search, so the SEO play differs per bucket.

### Bucket A — "availability by region" (EC2/region map, Azure/GCP/OCI/OVH explorers)

This is the strongest-fit bucket and the clearest revealed demand.

- `ec2 instance types by region` returns, on page one: the AWS docs page, then
  **`instances.vantage.sh`** ranking second as a third-party tool, then the AWS
  instance-types marketing page, an AWS re:Post question, and the cloudonaut
  blog post "Worldwide availability of EC2 instance types"
  ([SERP composition](https://docs.aws.amazon.com/ec2/latest/instancetypes/ec2-instance-regions.html),
  [Vantage](https://instances.vantage.sh/),
  [cloudonaut](https://cloudonaut.io/worldwide-availability-of-ec2-instance-types/)).
  That a community blog post and a commercial tool both rank on a query the
  vendor *also* documents is the tell: the AWS docs page is a flat, hard-to-scan
  wall, and users actively seek a better-structured answer.
- Revealed demand is strong: multiple maintained commercial/free tools exist
  purely to answer region/SKU availability — Vantage `instances.vantage.sh`
  ([acquired ec2instances.info, actively maintained](https://www.vantage.sh/blog/vantage-has-acquired-ec2instances-info)),
  Azure Charts `azurecharts.com/instances` ([rebuilt daily](https://azurecharts.com/instances)),
  WintelGuy's Azure VM lookup ([tool](https://wintelguy.com/azure-vm-lookup.pl)),
  gcloud-compute.com, and DoiT's `gpu-finder` ([GitHub](https://github.com/doitintl/gpu-finder)).
  Tools get built for queries with sustained volume.
- AWS re:Post carries repeated questions like "How check the availability of
  specific types of ec2 by availability zone?" and "Instance type support in
  availability zones in the same region"
  ([re:Post 1](https://repost.aws/questions/QUu5kVNXlTSdC-mEg7Vj3kDA/how-check-the-availability-of-specific-types-of-ec2-by-availability-zone),
  [re:Post 2](https://repost.aws/questions/QUUdXKo5tKQRCU75QVg_qvfA/instance-type-support-in-availability-zones-in-the-same-region)) —
  recurring questions on the official forum are a free demand signal.
- `gcp regions list` page one is almost entirely vendor docs + a couple of
  third-party explainers (Holori, economize.cloud, gcloud-compute.com)
  ([SERP](https://cloud.google.com/about/locations),
  [Holori](https://holori.com/list-of-gcp-regions/),
  [economize](https://www.economize.cloud/resources/gcp/regions-zones-map/)).
- `cloud gpu availability by region` is more contested — GCP docs, a
  `gpu-finder` GitHub repo, and listicles ("Top 60+ Cloud GPU Providers")
  ([SERP](https://docs.cloud.google.com/compute/docs/regions-zones/gpu-regions-zones),
  [aimultiple listicle](https://aimultiple.com/cloud-gpu-providers)) — but
  no neutral cross-cloud "which region has which GPU" matrix dominates.

**Assessment (approx):** mid-volume, *recurring, intent-rich* queries. Not
millions of searches, but durable practitioner demand and weak incumbents
outside Vantage. This is Infra Atlas's home turf.

### Bucket B — "compare X to Y" / APIM feature matrix (APIM matrix, APIM-platform guides)

Highest *commercial* search volume of the four buckets, and the most crowded.

- `apigee vs kong` page one is dominated by **vendor-owned comparison pages**:
  Kong's own `konghq.com/performance-comparison/kong-vs-apigee`, Tyk's
  `tyk.io/apigee-vs-kong`, plus API7.ai and integration-vendor blogs (ApiX-Drive,
  MindMajix, Moesif) ([SERP](https://konghq.com/performance-comparison/kong-vs-apigee),
  [Tyk](https://tyk.io/apigee-vs-kong/),
  [Moesif](https://www.moesif.com/blog/technical/api-gateways/How-to-Choose-The-Right-API-Gateway-For-Your-Platform-Comparison-Of-Kong-Tyk-Apigee-And-Alternatives/)).
  Every one of these has an axe to grind — the comparison always concludes the
  publisher's product wins.
- `mulesoft anypoint vs apigee` is the same picture: G2, Tyk, PeerSpot,
  Taloflow, API7.ai, ApiX-Drive
  ([SERP](https://www.g2.com/compare/apigee-api-management-vs-mulesoft-anypoint-platform),
  [Taloflow](https://www.taloflow.ai/api-management-comparisons/apigee-api-management-vs-mulesoft-anypoint-api-manager)).
- `aws api gateway vs azure api management vs apigee` surfaces aggregator
  comparison pages (SourceForge, PeerSpot, StackShare) and SEO content farms
  (index.dev, Zuplo, API7.ai)
  ([SERP](https://sourceforge.net/software/compare/Amazon-API-Gateway-vs-Apigee-vs-Azure-API-Management/),
  [PeerSpot](https://www.peerspot.com/products/comparisons/amazon-api-gateway_vs_apigee_vs_microsoft-azure-api-management),
  [index.dev](https://www.index.dev/skill-vs-skill/aws-api-gateway-vs-azure-api-management-vs-google-apigee)).

**Assessment (approx):** high volume, **very high competition, low trust**. The
incumbents are either vendors marking their own homework or thin aggregators.
Ranking on the head term `apigee vs kong` is a multi-year backlink fight Infra
Atlas will not win soon. The opening is *neutrality plus specificity* — see §2.

### Bucket C — "how does X behave / what's the limit" (API Gateway guides: AWS APIGW, Apigee, Mulesoft, self-hosted)

- `aws api gateway timeout` page one is healthy and answerable: the AWS
  "What's New" post on the 29s limit increase, an AWS re:Post knowledge-center
  article, the API Gateway quotas doc, plus Medium/LogicMonitor/Catchpoint
  explainers ([SERP](https://aws.amazon.com/about-aws/whats-new/2024/06/amazon-api-gateway-integration-timeout-limit-29-seconds/),
  [re:Post](https://repost.aws/knowledge-center/api-gateway-timeout-limit),
  [quotas doc](https://docs.aws.amazon.com/apigateway/latest/developerguide/limits.html)).
- `self-hosted api gateway open source comparison` returns listicles
  (daily.dev "Top 6", Nordic APIs "6 Best", API7.ai) and one Substack post
  ([daily.dev](https://daily.dev/blog/top-6-open-source-api-gateway-frameworks/),
  [Nordic APIs](https://nordicapis.com/6-open-source-api-gateways/),
  [API7.ai](https://api7.ai/learning-center/api-gateway-guide/api-gateway-comparison-apisix-kong-traefik-krakend-tyk)).

**Assessment (approx):** medium volume. Factual "limit / quota / behaviour"
queries are well-served by vendor docs for the *default* answer but poorly
served for the *cross-vendor* answer ("what's the timeout ceiling on APIGW vs
Apigee vs Azure APIM?"). That comparison cell is Infra Atlas territory.

### Bucket D — cross-cloud matrices (equivalent-SKU, managed K8s, compliance, confidential computing, IAM)

- `aws azure gcp service comparison cheat sheet` is a real, established query
  with a defined SERP: a TechTarget cheat sheet (refreshed yearly), Google's own
  official AWS/Azure mapping doc, DataCamp, tutorialsdojo, DZone, plus Medium
  reposts ([TechTarget](https://www.techtarget.com/searchcloudcomputing/feature/A-cloud-services-cheat-sheet-for-AWS-Azure-and-Google-Cloud),
  [Google doc](https://docs.cloud.google.com/docs/get-started/aws-azure-gcp-service-comparison),
  [tutorialsdojo](https://tutorialsdojo.com/azure-vs-aws-vs-gcp-service-comparison/)).
- `managed kubernetes comparison EKS AKS GKE` is heavily contested by
  vendor-adjacent blogs (SentinelOne, Pluralsight, Sedai, Veeam, Qovery,
  Fairwinds) ([SERP](https://www.sentinelone.com/cybersecurity-101/cybersecurity/eks-vs-aks-vs-gke/),
  [Pluralsight](https://www.pluralsight.com/resources/blog/cloud/aks-vs-eks-vs-gke-managed-kubernetes-services-compared)).
- `aws iam vs azure rbac vs gcp iam` SERP: Tenable, Pluralsight, Trustle,
  TechTarget, plus Medium ([Tenable](https://www.tenable.com/blog/aws-azure-and-gcp-the-ultimate-iam-comparison),
  [Pluralsight](https://www.pluralsight.com/resources/blog/cloud/comparing-aws-azure-and-google-cloud-iam-services)).
- `azure vm confidential computing SGX` is **almost entirely Microsoft Learn**
  with one OneUptime blog — a thin third-party field
  ([SERP](https://learn.microsoft.com/en-us/azure/confidential-computing/overview-azure-products),
  [OneUptime](https://oneuptime.com/blog/post/2026-02-16-how-to-set-up-azure-confidential-computing-with-dcsv3-virtual-machines-for-data-in-use-protection/view)).
- `cloud compliance certifications HIPAA FedRAMP SOC2 comparison` SERP: security
  vendors and consultancies (Tenable-style blogs, Meewco, Censinet, HIPAA Vault)
  — no neutral cert matrix ([SERP](https://meewco.com/blog/azure-vs-aws-vs-gcp-cloud-compliance-comparison),
  [HIPAA Vault](https://www.hipaavault.com/hipaa-hosting/cloud-wars-aws-vs-azure-vs-google-cloud-hipaa/)).

**Assessment (approx):** medium-to-high volume. Most cells are owned by
listicles and vendor-adjacent blogs that go stale fast (cloud SKUs/certs change
quarterly). A neutral matrix that is *visibly fresh* and *cited* can win the
"is X still true" re-check traffic that the listicles cannot retain.

### Cross-cutting landscape observation

Across all four buckets the pattern is identical and it is the strategic core:
the SERPs are split between **(a) vendor docs** — authoritative but
single-cloud, flat, and hard to scan — and **(b) vendor-adjacent / aggregator
content** — cross-cloud but biased, shallow, or stale. There is a persistent,
unoccupied middle: **neutral, structured, dated, multi-vendor reference data.**
That is precisely Infra Atlas's product. The SEO strategy is to occupy that
middle, not to fight vendors on head terms.

---

## 2 · The wedge

Where a neutral reference can realistically win, in priority order.

1. **"Availability by region" cross-cloud (Bucket A) — primary wedge.**
   Vantage owns the *AWS-pricing-and-specs* niche and owns it well
   ([Vantage](https://instances.vantage.sh/)). But Vantage is organised
   per-cloud and its primary axis is *price/specs*, not *"where can I even get
   this"*. There is no single neutral destination for **cross-cloud regional
   availability** — "which clouds offer an SGX-capable VM in Frankfurt", "which
   regions have H100s across AWS+Azure+GCP+OCI". AWS docs answer one cloud as a
   flat list; Azure Charts answers one cloud. Infra Atlas already has the
   multi-cloud region map + five compute explorers — it is one schema/copy pass
   away from owning this. **Lowest competition, best instrument fit.**

2. **The "neutral arbiter" angle on comparison queries (Buckets B/D).** Do not
   target the head term `apigee vs kong` directly — that SERP is a vendor
   knife-fight ([Kong's own page ranks](https://konghq.com/performance-comparison/kong-vs-apigee)).
   Instead win the **trust-differentiated long tail**: the specific feature-cell
   queries where the searcher has *already* been burned by biased results and
   wants a straight matrix answer (e.g. "apigee vs kong rate limiting", "does
   azure api management support mTLS"). Infra Atlas's APIM feature matrix answers
   these per-cell; the wedge is structuring each cell as its own
   linkable/snippet-able answer.

3. **"Is X still true" freshness re-checks (Bucket D).** Listicles like the
   TechTarget cheat sheet are updated ~yearly ([TechTarget](https://www.techtarget.com/searchcloudcomputing/feature/A-cloud-services-cheat-sheet-for-AWS-Azure-and-Google-Cloud) —
   note its companion PDF is dated "OCTOBER 2024"). Cloud SKUs, regions and
   certifications move quarterly. A reference site with a **visible
   `dateModified`** and an honest "last verified" stamp captures the practitioner
   who already saw a listicle and is re-checking whether it is current. The
   editorial "with the asterisks intact" voice (per the audit) is an asset here:
   it signals rigour the listicles lack.

4. **Vendor-docs frustration on flat-list pages (Bucket A/C).** The AWS
   "instance types by Region" doc is authoritative but notoriously unscannable
   ([AWS doc](https://docs.aws.amazon.com/ec2/latest/instancetypes/ec2-instance-regions.html)) —
   the existence of cloudonaut's "Worldwide availability" post ranking alongside
   it proves users want a filterable/sortable alternative
   ([cloudonaut](https://cloudonaut.io/worldwide-availability-of-ec2-instance-types/)).
   Infra Atlas's EC2-by-region instrument *is* that alternative; it needs the
   on-page SEO to be found (§4).

**Where NOT to play:** the bare head comparison terms (`apigee vs kong`,
`EKS vs AKS vs GKE`) as standalone ranking targets — incumbent backlink moats
are too deep for a brand-new site with a (currently private) repo and zero
backlinks (per audit headline gaps #1). Treat those as brand/topical-authority
plays, not near-term traffic plays.

---

## 3 · Long-tail query list (~15)

Concrete queries the *existing* 16 instruments already answer, capturable with
light page-structure / copy changes (anchored sub-sections, a question-shaped
H2/H3 per row or cell, an explicit one-sentence answer above the table). Grouped
by instrument. Volume per query is low individually (long tail) but the set is
additive, low-competition, and high-intent.

**EC2-by-region / region map / compute explorers (Bucket A):**
1. `is g5 available in eu-west-1` — and the templated family: `is <type>
   available in <region>`. Currently answered only by scraping AWS docs or
   running the CLI ([demand evidence — re:Post + GitHub scripts exist](https://gist.github.com/jer-nc/a9a365c6ddc04b11380af3f1fb5f3eb1)).
2. `which aws regions have h100 gpu` / `g6 instance regions` — GPU-by-region is
   contested only by listicles, no neutral matrix ([context](https://docs.cloud.google.com/compute/docs/regions-zones/gpu-regions-zones)).
3. `aws regions with arm graviton instances` — Graviton availability is uneven
   per region; only 9 families are in every region ([AWS doc](https://docs.aws.amazon.com/ec2/latest/instancetypes/ec2-instance-regions.html)).
4. `which azure regions support confidential computing` — Microsoft Learn lists
   SGX VM series but regional availability is buried ([Azure doc](https://learn.microsoft.com/en-us/azure/confidential-computing/virtual-machine-solutions-sgx)).
5. `gcp regions with a100 gpus` — GPU-locations page is per-zone and dense
   ([GCP doc](https://docs.cloud.google.com/compute/docs/regions-zones/gpu-regions-zones)).
6. `oci regions list` / `ovh cloud regions` — under-served vs AWS/Azure/GCP;
   thin third-party coverage ([OCI](https://www.oracle.com/cloud/public-cloud-regions/)).
7. `cloud providers with a region in <city/country>` (e.g. Milan, Spain) — the
   multi-cloud region map answers this directly; competitors are TeleGeography's
   paid-leaning map and vendor pages ([TeleGeography](https://www.datacenterknowledge.com/cloud/telegeography-maps-the-world-s-cloud-data-centers)).

**Equivalent-SKU / cross-cloud matrices (Bucket D):**
8. `azure equivalent of ec2 m5` / `ec2 t3 azure equivalent` — Microsoft's own
   migration doc maps families but not size-for-size; people ask this on Quora
   ([Microsoft doc](https://learn.microsoft.com/en-us/azure/virtual-machines/migration/migrate-from-elastic-compute-cloud-architecture),
   [Quora demand signal](https://www.quora.com/What-is-the-Azure-VM-equivalent-of-AWS-T2-EC2-instances-with-CPU-credits)).
9. `gcp equivalent of aws fargate` (and the general `<aws service> gcp/azure
   equivalent` template) — Google's mapping doc is the incumbent but is GCP-voiced
   ([Google doc](https://docs.cloud.google.com/docs/get-started/aws-azure-gcp-service-comparison)).
10. `aws iam vs gcp iam policy model` — the architecture-difference angle
    (AWS direct-attach vs GCP/Azure RBAC inheritance) is a specific cell of the
    IAM instrument ([Tenable comparison](https://www.tenable.com/blog/aws-azure-and-gcp-the-ultimate-iam-comparison)).
11. `does eks charge for control plane` / `gke vs eks control plane cost` — a
    concrete factual cell of the managed-K8s matrix (EKS ~$0.10/hr, AKS free,
    GKE free for standard) ([Sedai pricing breakdown](https://sedai.io/blog/kubernetes-cost-eks-vs-aks-vs-gke)).
12. `which cloud providers are fedramp authorized` / `gcp hipaa eligible
    services` — compliance-cert matrix cell; SERP is all security-vendor blogs
    ([Meewco](https://meewco.com/blog/azure-vs-aws-vs-gcp-cloud-compliance-comparison)).

**APIM matrix / API-gateway guides (Buckets B/C):**
13. `aws api gateway timeout limit` / `can you increase api gateway 29 second
    timeout` — factual, answerable; the APIGW guide instrument owns this if
    structured as a Q&A block ([AWS What's New](https://aws.amazon.com/about-aws/whats-new/2024/06/amazon-api-gateway-integration-timeout-limit-29-seconds/)).
14. `apigee vs kong rate limiting` / `does azure api management support mtls` —
    feature-cell long tail of the APIM matrix; escapes the biased head-term SERP
    ([head-term SERP for context](https://konghq.com/performance-comparison/kong-vs-apigee)).
15. `open source api gateway comparison` / `kong vs apisix vs krakend` —
    self-hosted-APIM guide; SERP is listicles only, beatable with a real matrix
    ([daily.dev listicle](https://daily.dev/blog/top-6-open-source-api-gateway-frameworks/),
    [API7.ai](https://api7.ai/learning-center/api-gateway-guide/api-gateway-comparison-apisix-kong-traefik-krakend-tyk)).

**Bonus templated pattern (highest leverage):** queries 1, 2, 8, 9 share a
*templatable* shape — `is <X> available in <Y>` and `<X> equivalent of <Y>`.
If each instrument can mint a stable anchored URL per row (e.g.
`/ec2-regions#g5-eu-west-1`), one structural change captures hundreds of
long-tail variants at once. This is the single highest-ROI on-page change.

---

## 4 · SEO table-stakes for a 16-page reference site

Baseline every reference site needs. The audit already found `robots.txt`,
`sitemap.xml`, and JSON-LD all **missing** (audit §1a) — so this is greenfield.

- **`robots.txt` + `sitemap.xml`.** Non-negotiable. 16 URLs is trivial to
  enumerate; generate `sitemap.xml` at build time with accurate `<lastmod>` per
  instrument (the live-data instruments change often — `<lastmod>` is a freshness
  signal). Reference `Sitemap:` from `robots.txt`. Google treats `<lastmod>` as
  a real recrawl hint ([Google structured-data intro](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)).
- **Structured data (JSON-LD, the format Google recommends —
  [docs](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)).
  Note: schema makes a page *eligible for rich results*; it does **not** directly
  lift rankings — Google states this explicitly, and that pages with rich
  results see ~35% higher CTR ([Digital Applied summary](https://www.digitalapplied.com/blog/structured-data-seo-2026-rich-results-guide)).
  Recommended per page type:
  - **`Dataset`** on the data-table instruments (EC2-by-region, region map,
    compute explorers, the matrices). The instruments *are* datasets — name,
    description, creator, `distribution`/format, `dateModified`. This also makes
    them eligible for **Google Dataset Search**, a discovery channel the
    listicle competitors are not in ([Google `Dataset` docs](https://developers.google.com/search/docs/appearance/structured-data/dataset),
    [Dataset Search context](https://www.hillwebcreations.com/google-dataset-search-adds-dataset-schema/)).
    DCAT is an accepted equivalent if ever needed ([Google Dataset docs](https://developers.google.com/search/docs/appearance/structured-data/dataset)).
  - **`TechArticle`** on the four API-gateway *guide* instruments (prose, not
    tables) — `headline`, `dateModified`, `author`
    ([supported types](https://developers.google.com/search/docs/appearance/structured-data/search-gallery)).
  - **`SoftwareApplication`** / `WebApplication` on the site root or the
    interactive explorers (the site is a free web tool) — gives an entity for
    the brand ([supported types](https://developers.google.com/search/docs/appearance/structured-data/search-gallery)).
  - **`BreadcrumbList`** if the periodical "Department I/II/III" structure maps
    to URL paths — cheap, yields breadcrumb rich results
    ([supported types](https://developers.google.com/search/docs/appearance/structured-data/search-gallery)).
  - Validate every template with Google's Rich Results Test before shipping
    ([Google `Dataset` docs reference the test](https://developers.google.com/search/docs/appearance/structured-data/dataset)).
- **Title / H1 patterns.** The audit found the `<h1>` is just the wordmark on
  every page (audit §1a) — an SEO miss. Tables-stakes pattern:
  - `<title>`: `<Specific subject> — <function> | Infra Atlas` (≤ ~60 chars),
    e.g. `EC2 Instance Types by Region — availability table | Infra Atlas`.
    Keyword-bearing and unique per page.
  - One **descriptive `<h1>` per page** carrying the primary keyword, distinct
    from the brand wordmark. The wordmark can stay as a masthead logo/`<p>`; the
    `<h1>` should say what the page *is*. (The editorial brand survives — the
    wordmark stays visible, it just stops being the `<h1>`.)
  - `<h2>`/`<h3>` shaped as the **questions** from §3 ("Is g5 available in
    eu-west-1?", "What is the Azure equivalent of EC2 m5?") — this is what wins
    People-Also-Ask boxes and featured snippets.
  - One concise plain-text answer sentence immediately under each question H2/H3,
    *above* the table — snippet-extractable.
- **Internal linking.** A 16-page site is small enough to be **fully
  cross-linked** by topic: every compute explorer links to the region map and to
  the equivalent-SKU matrix; the APIM matrix links to all four API-gateway
  guides and vice versa. A persistent "the 16 instruments" index in the footer
  or nav distributes link equity evenly and helps crawl discovery. The periodical
  "departments" framing already implies a taxonomy — expose it as real links.
- **Stable, keyword-bearing, anchored URLs.** Per §3, mint a deterministic
  anchor per table row / matrix cell (`#g5-eu-west-1`, `#apigee-vs-kong-rate-limiting`)
  so long-tail queries land on the exact answer. Keep slugs descriptive
  (`/ec2-instance-types-by-region`, not `/instrument-3`).
- **Per-page meta descriptions + canonicals** — the audit confirms these already
  exist (audit §1a). Keep them unique and question-answering.
- **Honest freshness signals.** A visible "last verified <date>" on each data
  instrument, backed by `dateModified` in the `Dataset`/`TechArticle` JSON-LD.
  This is both a ranking-adjacent freshness cue and the on-page expression of
  the §2 "is X still true" wedge.

---

## 5 · Backlink targets

The repo is currently **private with 0 stars** (audit headline gap #1) — most of
this is blocked until it is public. Targets below are realistic for a neutral,
free, open-source reference site once that unblocks. Ordered by
effort-to-payoff.

**Curated "awesome" lists (lowest effort — a PR or issue once the repo is public):**
Verified via the awesome-list ecosystem that the closest comparable
(`ec2instances.info` / `instances.vantage.sh`) is listed in awesome lists today
([Ecosyste.ms record for ec2instances.info](https://awesome.ecosyste.ms/projects/github.com/vantage-sh/ec2instances.info) —
shows it referenced by [gaui/awesome](https://github.com/gaui/awesome) and
[sparticuz/awesome](https://github.com/sparticuz/awesome)). Concrete submission
targets:
- **`donnemartin/awesome-aws`** — the canonical Awesome-AWS list, also mirrored
  at project-awesome.org and trackawesomelist
  ([repo](https://github.com/donnemartin/awesome-aws),
  [project-awesome mirror](https://project-awesome.org/donnemartin/awesome-aws)).
  The EC2-by-region instrument fits its tools section.
- **`devtoolsd/awesome-cloud`** — multi-cloud scope, the best fit for Infra
  Atlas's cross-cloud instruments ([repo](https://github.com/devtoolsd/awesome-cloud)).
- **`nishantthorat/awesome-aws-cloud`** and **`awesomelistsio/awesome-aws`** —
  additional Awesome-AWS variants ([repo 1](https://github.com/nishantthorat/awesome-aws-cloud),
  [repo 2](https://github.com/awesomelistsio/awesome-aws)).
- **`realvz/awesome-eks`** and **`nathanpeck/awesome-ecs`** — niche but
  on-target for the EC2/region instruments ([awesome-eks](https://realvz.github.io/awesome-eks/),
  [awesome-ecs](https://github.com/nathanpeck/awesome-ecs)).
- **Ecosyste.ms Awesome** auto-indexes any project that lands in an awesome
  list, creating a secondary citation page for free
  ([Ecosyste.ms awesome aws-topic listing](https://awesome.ecosyste.ms/lists?topic=aws)).
- For the APIM instruments, search for and target an `awesome-api` /
  `awesome-api-management` / `awesome-apigateway` list with the same PR play
  (these exist in the same ecosystem; identify the live one before submitting).

**Community-launch / discussion link sources (medium effort):**
The comparable reference tools all earned early traction and links from launch
posts:
- **Hacker News.** `instances.vantage.sh` and `cloudping.info` both have
  recurring HN submission histories — HN "Show HN" launches drive both direct
  traffic and follow-on blog citations
  ([Vantage instances on HN](https://news.ycombinator.com/item?id=46217721),
  [cloudping.info HN submissions](https://news.ycombinator.com/from?site=cloudping.info)).
  A "Show HN" for a neutral cross-cloud reference is a natural fit.
- **Lobsters.** `instances.vantage.sh` has a domain page on Lobsters, i.e. it
  has been submitted and discussed there ([Lobsters domain page](https://lobste.rs/domains/instances.vantage.sh)).
- **TanStack Showcase** — `instances.vantage.sh` is featured there
  ([TanStack showcase](https://tanstack.com/showcase/2bac1a02-1331-438a-9c7a-ca7ba1da0ca9));
  if Infra Atlas is built on a showcased framework, equivalent showcase
  submissions are a free, relevant backlink.
- Relevant subreddits (r/aws, r/devops, r/googlecloud, r/AZURE) — the same
  audience that produces the re:Post questions in §1.

**Editorial / organic citations (highest effort, highest value):**
- **Independent cloud blogs** like cloudonaut already publish region-availability
  content and rank for it ([cloudonaut post](https://cloudonaut.io/worldwide-availability-of-ec2-instance-types/)) —
  they are natural citers of a better-structured neutral dataset, and outreach
  to them is warm (shared topic, no competitive conflict).
- **The "open data" angle.** `caniuse.com`'s support data is published under
  CC BY 4.0 with the raw data on GitHub, which is *why* so many tools and
  articles cite and embed it ([caniuse data on GitHub, CC BY 4.0](https://github.com/Fyrd/caniuse),
  [KeyCDN on caniuse embeds](https://www.keycdn.com/support/caniuse)).
  Vantage does the same — a free public API and an open-source repo, which is
  explicitly credited as the reason the community contributes and links
  ([Vantage open-source/API note](https://www.vantage.sh/blog/vantage-has-acquired-ec2instances-info)).
  **Lesson for Infra Atlas:** publishing the underlying data under an open
  licence with a clear citation string (and ideally a small public API or
  downloadable dataset) converts the site from "a page to read" into "a source
  to cite" — the single biggest structural backlink multiplier, and it directly
  reinforces the open-source positioning the site already claims.
- **Vendor-neutral wikis / docs** (e.g. community cloud wikis, OSS project docs
  that need a region/SKU reference) — link naturally to neutral sources over
  vendor docs; pursue once topical authority exists.

**Realism note.** caniuse and Vantage accumulated their backlink profiles over
~10+ years and (for Vantage) a company behind them. Infra Atlas's near-term,
solo-maintainer-achievable set is: make the repo public → submit to the awesome
lists above → one good "Show HN" → publish the data under an open licence with a
citation string. That is a credible 90-day backlink plan; head-term ranking is
a multi-year outcome of it, not a starting move.
