# User Intent Research — Infra Atlas Feature Mining

Research date: 2026-05-16. Goal: mine real, observed user intent and unmet needs from
cloud/DevOps engineers to guide the next batch of Infra Atlas instruments.

Method note: Reddit and Hacker News thread contents were pulled via their public JSON
APIs (`reddit.com/.../.json`, `hn.algolia.com`). Stack Overflow data was pulled via the
Stack Exchange API (`api.stackexchange.com`), sorted by votes per tag — direct page
fetches to `stackoverflow.com` are blocked, and broad `WebSearch` queries returned
vendor blog summaries rather than raw user signal, so quoted SO material is limited to
question titles + vote/view counts (a strong proxy for "recurring confusion"). Every
claim below cites a URL. Where a source could not be reached it is stated explicitly.

---

## 1. Reddit

### 1a. The "official pages are fluff, not data" complaint — strongest theme

Thread: **"Amazon's Instance type page used to have great info. Now it's all fluff and
nothing useful."** — r/aws, 194 upvotes.
<https://reddit.com/r/aws/comments/1o1jsis/amazons_instance_type_page_used_to_have_great/>

This thread is almost a product brief for Infra Atlas. Quoted signals:

- OP: *"someone went and tried to make the page Pretty, and now it's useless ... I could
  pick which type of instance I wanted, click the actual [type]"* — wants the old dense
  table back.
- *"I'll give you a little hint — When I worked at AWS, everyone I knew used vantage
  instead of the official page"* (156 upvotes — the top reply).
- *"The fancy boxes don't help me understand what instance size has what specs any
  better than a table with fast filtering, ordering, searching"* (20 upvotes).
- *"They need to know their audience. Most of us using that page don't care about
  pretty. We want simple, fast, full of data we need ... I'm not [t]here for 'an
  enriched customer journey'."* (13 upvotes).
- *"it is nigh on impossible to work out what instance types are available in a given
  region. For example, how would one know if any of the newer AMD Zen instance types
  are available in London? (Spoiler, they aren't)"* (17 upvotes).
- *"What should have been a 5min task took 15mins of useless clicking."* (13 upvotes).

Thread: **"Anyone else also thinks AWS documentation is full of fluff and makes finding
useful information difficult?"** — r/aws, 393 upvotes, 105 comments.
<https://reddit.com/r/aws/comments/1g0aaek/anyone_else_also_thinks_aws_documentation_is_full/>

- *"You need documentation to learn how to use AWS documentation. Once you figure it
  out, it's only half terrible."* (13 upvotes).
- *"Azure has tons of information about the same thing in different locations and some
  are in different versions and outdated."* (153 upvotes) — cross-provider doc-quality
  comparison is itself something engineers debate.
- *"GCP docs ... incomplete (to the point key steps to actually make the use cases
  functional are missing), and in a few cases outright incorrect"* (35 upvotes).

**Signal for Infra Atlas:** a vendor-neutral, dense, fast, footnoted reference is a
*recognised gap* — engineers already route around official pages to third-party tools,
and they explicitly want tables with filter/sort/search, not marketing layouts.

### 1b. Egress / NAT / data-transfer cost is a perennial trap

Thread: **"NAT gateways are too expensive"** — r/aws, 171 upvotes, 119 comments.
<https://reddit.com/r/aws/comments/w3zrwz/nat_gateways_are_too_expensive/>

- OP: *"I was looking at my AWS bill and saw a line item called EC2-other which was
  about half of my bill ... I didn't have any real traffic so why does it cost so
  much."* — the classic "surprise line item I can't decode" problem.
- *"NAT Gateways are one of the classic AWS gotchas. They can really run up a bill
  quickly without you realizing it."* (103 upvotes).
- *"I have seen organizations where 25% of their total bill is just NAT gateways. I
  cannot overstate how wildly expensive these damn things are relative to their
  function/value."* (9 upvotes).

Thread: **"Cloud NAT pricing caught us completely off guard"** — r/googlecloud.
<https://reddit.com/r/googlecloud/comments/1rdduom/cloud_nat_pricing_caught_us_completely_off_guard/>

- OP: *"realized Cloud NAT charges are now competing with our actual compute costs.
  We've got services talking between regions and apparently every byte is getting taxed
  twice."* — confusion about *which* byte is billed and at what layer.

r/googlecloud search for "egress cost" surfaces a string of denial-of-wallet horror
stories (e.g. *"One public Firebase file. One day. $98,000"*, 532 upvotes:
<https://reddit.com/r/googlecloud/comments/1kg9icb/one_public_firebase_file_one_day_98000_how_it/>)
and posts titled *"About those egress fees..."* and *"undocumented Free standard tier
egress"* — i.e. egress pricing rules are opaque enough that engineers cannot predict
them.
<https://reddit.com/r/googlecloud/comments/195807q/about_those_egress_fees/>
<https://reddit.com/r/googlecloud/comments/1740ack/undocumented_free_standard_tier_egress/>

**Signal for Infra Atlas:** a clear, footnoted "data-transfer / egress cost map" —
per-provider, per-direction (internet egress, cross-AZ, cross-region, NAT processing,
inter-cloud) — is wanted. Current instruments don't cover network cost.

### 1c. Cross-cloud cost comparison tools are distrusted

Thread: **"Cloud vs. On-Prem Cost Calculator"** — r/devops, 61 upvotes, 73 comments.
<https://reddit.com/r/devops/comments/1nt2ib6/cloud_vs_onprem_cost_calculator/>

- OP: *"Every 'cloud pricing calculator' I've used is either from a cloud provider or a
  storage vendor. Surprise: their option always comes out cheapest."* — explicit
  distrust of vendor-supplied calculators; demand for a *neutral* one. This is exactly
  Infra Atlas's editorial-independence positioning.
- The thread also shows how hard honest TCO is: *"Does it include the cost of
  maintaining the thing? Like having specialized networking people, 7x24 coverage"*
  (67 upvotes); *"Are you including time? I can spin up a full datacenter's worth [of]
  systems in a day in cloud, but it would take 6-12 months ... on prem"* (35 upvotes).

Thread: **"Built a EC2 & VM price comparator to save my own sanity"** — r/devops.
<https://reddit.com/r/devops/comments/1nq8tk5/built_a_ec2_vm_price_comparator_to_save_my_own/>

- OP (a cloud engineer at a European bank): *"I basically got tired of juggling to find
  the cheapest but still capable EC2 type in the CLI for each test while keeping
  performance decent."*
- On why Vantage's `instances.vantage.sh` did not satisfy them: *"I felt that was too
  bloated with much information that I did not need ... when I clicked onto an instance
  it has no price comparison between regions, which is the main use case I am looking
  for, just find the cheapest one across all AWS regions."* — **per-instance,
  cross-region price comparison is a named missing feature.**
- A commenter immediately asks: *"How about allowing you to compare between
  providers?"* — cross-provider equivalence demand again.

### 1d. Fargate vs EC2 / "what is the equivalent" sizing confusion

Thread: **"Anyone here start on ECS Fargate and later migrate back to ECS EC2 (or vice
versa)?"** — r/aws, 69 upvotes, 90 comments.
<https://reddit.com/r/aws/comments/1n4oksq/anyone_here_start_on_ecs_fargate_and_later/>

- OP: *"How much of a premium am I really paying for that convenience compared to ECS
  EC2? Which EC2 instance family/type would be the closest equivalent to common Fargate
  task sizes? e.g. 1 vCPU / 2 GB Memory."* — a direct "translate this SKU to that SKU"
  request, the same shape as Infra Atlas's Equivalent-SKU matrix but *within* one cloud
  (Fargate ↔ EC2).
- *"1 vCPU on Fargate is $30/month which is more than a lot of the EC2 instance types
  that have 1 vCPU."* (20 upvotes).
- *"fargate drawback - you can't choose machine specs ... people were reporting old CPUs
  being used for ECS fargate."* (9 upvotes) — links to an SO question on what a Fargate
  vCPU actually *is*.

### 1e. Capacity / region availability is unpredictable

Thread: **"Suddenly cannot start VM due to VM size being unavailable in current
availability zone."** — r/AZURE, 18 upvotes.
<https://reddit.com/r/AZURE/comments/luptz2/suddenly_cannot_start_vm_due_to_vm_size_being/>

- OP: *"The requested VM size 'Standard_F4s_v2' is not available in the current
  availability zone ... I've tried moving to another region"* — engineers cannot tell,
  ahead of time, which SKU exists in which zone/region.

Thread: **"VM Right Sizing Advisor (CPU / Memory) Tool or Script"** — r/AZURE.
<https://reddit.com/r/AZURE/comments/1312f8a/vm_right_sizing_advisor_cpu_memory_tool_or_script/>

- OP: *"we have a few VM's that we feel ... are way over allocated on Sizing ... Does
  anyone have any scripts or tools that can do this on Azure, I feel the Azure Advisor
  doesn[']t give you these"* — wants a sizing reference Azure's own tool doesn't supply.

### 1f. API gateway taxonomy confusion

Thread: **"Difference between Reverse Proxy, Load Balancer and API Gateway"** —
r/devops, 156 upvotes.
<https://reddit.com/r/devops/comments/py1q54/difference_between_reverse_proxy_load_balancer/>

- OP: *"I am seeing different companies taking different approach. I am not sure anymore
  where each should be actually used. On top of that tech like Kong make me question
  whether API Gateway should be one thing for all."*
- Top reply (160 upvotes) is a community-written definition of the three — i.e. there is
  no canonical neutral reference, so Reddit keeps re-deriving one.

### 1g. Gateway API vs Ingress migration is a current, hot pain (2026)

The r/kubernetes front page right now is dominated by ingress-nginx retirement and the
Gateway API migration: *"Ingress NGINX Retirement"* (345 upvotes, 173 comments),
*"Ingress NGINX EOL in 120 Days - Migration Options and Strategy"* (233 upvotes),
*"Hot Take: If Kubernetes wants us to start using gateway api instead of ingress, it
should no longer be an addon"* (207 upvotes).
<https://reddit.com/r/kubernetes/comments/1ove0t5/ingress_nginx_retirement_what_you_need_to_know/>
<https://reddit.com/r/kubernetes/comments/1sxmti8/hot_take_if_kubernetes_wants_us_to_start_using/>

- In the Hot Take thread: *"so many people equating ingress with ingress-nginx ... it
  was insanity to wade through all the Ingress is dead posts ... I wish switching to
  Gateway API was as easy as switching ingress controllers was but it definitely is a
  different beast, and controllers still seem to be playing catchup."* (5 upvotes).
- *"We really wanted to use Gateway API, but too many things we wanted to use weren't GA
  yet ... ingress-nginx deprecation didn't line up with a good time to move."*

**Signal for Infra Atlas:** an Ingress-vs-Gateway-API reference (resource mapping,
controller support matrix, GA-status-by-feature) addresses a live, time-sensitive need
and is adjacent to both the Kubernetes matrix and the APIM material already on the site.

### 1h. r/sysadmin and r/sre

- r/sysadmin searches for cloud/region comparison are dominated by career and
  cloud-philosophy posts (e.g. *"What The Cloud REALLY Is..."*, 884 upvotes:
  <https://reddit.com/r/sysadmin/comments/8dozx3/what_the_cloud_really_is/>) rather than
  tooling requests — weaker signal for a reference site.
- r/sre's top recent thread is *"Our observability costs are now higher than our AWS
  bill"* (277 upvotes, 174 comments):
  <https://reddit.com/r/sre/comments/1ow3ltg/our_observability_costs_are_now_higher_than_our/>
  — cost-of-tooling is a live SRE pain, but more FinOps than infra-reference.

---

## 2. Hacker News

### 2a. "Show HN" cloud-comparison tools keep appearing — the niche is unsaturated

A standing stream of Show HN posts builds the same thing, which signals durable demand
and no agreed canonical answer:

- *"Show HN: AWS, Azure, GCP instance comparison. Region pricing, savings options"*
  <https://news.ycombinator.com/item?id=39691690>
- *"Show HN: CloudRunr Cross Cloud Pricing Calculator and Cloud Intel Platform"*
  <https://news.ycombinator.com/item?id=41876734>
- *"Show HN: Easy cloud instance comparison (AWS, GCP, Azure, IBM, Alibaba and more)"*
  <https://news.ycombinator.com/item?id=26846163>
- *"Show HN: CloudPriceCheck – Cloud pricing comparison for 8 providers"*
  <https://news.ycombinator.com/item?id=47206524>

On the long-running "Easy Amazon EC2 Instance Comparison" thread (285 points, 35
comments) commenters describe the underlying pain and missing features:
<https://news.ycombinator.com/item?id=12709820>

- *"is an invaluable resource given the ec2 pricing isn't particularly easy to work out
  in the docs."*
- *"It is missing ... storage and bandwidth costs, which can be a nontrivial chunk of an
  EC2 bill. And yes, it is hair pullingly frustrating ... trying to figure out how much
  an EC2 instance is going to cost you using Amazon's tools."*
- *"Navigating the EC2 pricing documentation is such a hassle. I tend to think of costs
  in terms of monthly ... valuable when working out cost-proposal estimates."*

### 2b. "Cloud price comparisons are apples to oranges" — the methodology gap

Thread: **"Cloud Pricing Comparison: AWS vs. Azure vs. Google Cloud Platform in 2022"**
(67 points, 32 comments). <https://news.ycombinator.com/item?id=31282930>

This thread is the single best argument for an *editorial, footnoted* approach over a
raw price table:

- *"Cloud price comparisons are often apples to oranges. Due in part to an extremely
  large number of hidden factors. I'm not just talking about direct cost, but even
  1vCPU != 1vCPU ... This would look much more like a series of a million graphs than a
  table."*
- *"it's useless to look at just prices, you really need to take performance and other
  parts into consideration too."*
- *"is 1 CPU / Memory in Fargate the same as in App Runner and Lambda?"* — even
  same-vendor vCPU definitions are unclear.
- *"In some ways AWS locks in its customers with their egress pricing. It can be so
  expensive to move away ... that it's economically not viable."*
- *"One killer no one seems to notice is the bandwidth between availability zones. When
  you have a proper best practice cross AZ deployment it can be rather expensive."*
- *"I see no mention of bandwidth pricing ... the monthly price of that traditional
  private server, which included a fixed bandwidth limit, ended up being lower than what
  it would cost just for the bandwidth on AWS."*

### 2c. "Ask HN" — engineers explicitly ask for these comparisons

- *"Ask HN: How to compare costs of compute providers?"*
  <https://news.ycombinator.com/item?id=13444683>
- *"Ask HN: Why Google/AWS/Azure's bandwidth is 10x more expensive than competition?"* —
  the OP points to an r/devops thread of the same question, showing the topic recurs
  across communities.
  <https://news.ycombinator.com/item?id=22034131>
- *"Ask HN: Google Cloud vs. Amazon Web Services Comparison?"*
  <https://news.ycombinator.com/item?id=8619964>

### 2d. Region selection / region-down is a recurring HN topic

- *"AWS Outage: A Single Cloud Region Shouldn't Take Down the World. But It Did"* (306
  points). <https://news.ycombinator.com/item?id=45642951>
- *"Google Cloud region currently down due to water intrusion"* (289 points, 173
  comments). <https://news.ycombinator.com/item?id=35732384>
- *"Carolina Cloud – One third the cost of AWS for data science workloads"* (142 points,
  76 comments) <https://news.ycombinator.com/item?id=46267283> — commenters dwell on
  egress and bandwidth as the real differentiator: *"95%~98% cheaper egress costs, with
  20TB included"* (re: Hetzner); *"We have no egress fees."*

### 2e. Spot capacity and "even on-demand isn't guaranteed"

Thread: **"Farewell to the Era of Cheap EC2 Spot Instances"** (254 points, 109
comments). <https://news.ycombinator.com/item?id=35802157>

- *"We run stateless calculations on EC2 across regions, and we definitely see that
  instances are harder to come by. Especially instances with GPUs."*
- *"Even on-demand isn't guaranteed capacity. There have been a handful of times in my
  career where I've tried to spin up a lot more instances and got met with an out of
  capacity error."*
- *"I've tried to spin up c6i.24xlarge instances and gotten an error that there aren't
  any more available in the region."*
- *"Our group regularly maxes out instance types in a region for some of our
  simulations. Have to overflow the requests over to other regions."*

**Signal for Infra Atlas:** capacity/availability — *which SKU is obtainable in which
region/zone, and how spot interruption/availability varies* — is a real planning input
the Region Map could surface.

---

## 3. Stack Overflow (top-voted by tag, via Stack Exchange API)

Highest-voted = highest recurring confusion. Question titles tell the story.

### 3a. aws-api-gateway — top by votes
<https://stackoverflow.com/questions/tagged/aws-api-gateway?tab=Votes>

| Votes | Views | Question |
|------:|------:|----------|
| 518 | 530k | How to pass a querystring or route parameter to AWS Lambda from Amazon API Gateway |
| 263 | 428k | Missing Authentication Token while accessing API Gateway? |
| 189 | 281k | API Gateway CORS: no 'Access-Control-Allow-Origin' header |
| 176 | 80k | **API gateway vs. reverse proxy** |
| 156 | 130k | AWS Lambda API Gateway error: "Malformed Lambda proxy response" |
| 150 | 254k | getting message: forbidden reply from AWS API gateway |
| 125 | 134k | Is there a way to change the http status codes returned by Amazon API Gateway? |
| 119 | 46k | **Regional/Edge-optimized API Gateway VS Regional/Edge-optimized custom domain name** |
| 94 | 202k | **Amazon API gateway timeout** |
| 82 | 40k | AWS API Gateway - Remove Stage Name From URI |

Recurring confusion clusters: (1) request/response mapping ("Malformed Lambda proxy
response", passing path/query params, changing status codes); (2) auth errors ("Missing
Authentication Token", "forbidden", "user anonymous is not authorized"); (3) CORS;
(4) **the 29-second timeout** ("Amazon API Gateway timeout", 202k views); (5) the
**conceptual "what even is this"** questions — "API gateway vs. reverse proxy" (80k
views), "Regional vs Edge-optimized" (46k views). The conceptual and timeout/limits
questions are exactly what a footnoted reference page resolves.
The AWS API Gateway 29-second integration-timeout limit is corroborated by an open
aws-cdk issue: <https://github.com/aws/aws-cdk/issues/30539>

### 3b. apigee — top by votes
<https://stackoverflow.com/questions/tagged/apigee?tab=Votes>

Low absolute vote counts (Apigee is a smaller community), but the highest-voted
*conceptual* questions are telling:

- *"What is the difference between GCP endpoint and Apigee"* (14 votes, 11k views)
  <https://stackoverflow.com/questions/58281261/what-is-the-difference-between-gcp-endpoint-and-apigee>
- *"Differences between API development platform e.g APIGEE and ESB"* (11 votes)
  <https://stackoverflow.com/questions/16815957/differences-between-api-development-platform-e-g-apigee-and-esb>
- *"With Apigee Load Balancer why do i need ELB,ALB,NLB, Global Load Balancers"* (6
  votes)
  <https://stackoverflow.com/questions/52243784/with-apigee-load-balancer-why-do-i-need-elb-alb-nlb-global-load-balancers>
- *"Best way to export and import all Apigee Edge objects related to an org?"* (5 votes)

The "how does Apigee relate to / differ from X" questions dominate — positioning, not
syntax, is the confusion. Aligns with Infra Atlas's APIM guides.

### 3c. azure-api-management — top by votes
<https://stackoverflow.com/questions/tagged/azure-api-management?tab=Votes>

- *"API management URL is giving Missing subscription key Issue"* (30 votes, 78k views)
- *"How to debug 500 error from Azure API Management call?"* (27 votes)
- *"What does the 'Ocp' stand for in Ocp-Apim-Subscription-Key header?"* (24 votes) — a
  pure "the naming is opaque" question.
- *"Make back end APIs only accessible via Azure API management"* (21 votes)
- *"Use Azure Api Management as a passthrough"* (19 votes)

### 3d. kong / generic API gateway — top by votes
<https://stackoverflow.com/questions/tagged/kong?tab=Votes>

The highest-voted Kong questions that are *not* generic Docker/Keycloak noise are direct
vendor-comparison questions — a clear signal for the APIM Feature Matrix:

- *"Is there a comprehensive comparison between Tyk vs Kong?"* (19 votes, 10k views)
  <https://stackoverflow.com/questions/46769814/is-there-a-comprehensive-comparison-between-tyk-vs-kong>
- *"Netflix-Zuul vs Mashape-Kong"* (19 votes, 13k views)
  <https://stackoverflow.com/questions/40972026/netflix-zuul-vs-mashape-kong>
- *"How good is Krakend compared to Kong?"* (17 votes, 24k views)
  <https://stackoverflow.com/questions/60050154/how-good-is-krakend-compared-to-kong>

### 3e. azure-virtual-machine — top by votes
<https://stackoverflow.com/questions/tagged/azure-virtual-machine?tab=Votes>

- *"In Windows Azure: What are web role, worker role and VM role?"* (119 votes, 97k
  views) — taxonomy confusion.
- *"what is the difference between virtual machine classic and virtual machine in
  azure?"* (52 votes).
- *"Do Azure VM pricing include storage in the VHD?"* (27 votes) — pricing-scope
  confusion.
- *"Azure VM Core vs vCPU"* (20 votes, 38k views) — what a "core" means, again.

### 3f. google-compute-engine — top by votes
<https://stackoverflow.com/questions/tagged/google-compute-engine?tab=Votes>

- *"What is the difference between Google App Engine and Google Compute Engine?"* (547
  votes, 175k views) — the single highest-voted question in the tag is a "which
  product" question.
- *"When to use Google App Engine Flex vs Google Cloud Run"* (81 votes).
- *"GCP error: Quota 'GPUS_ALL_REGIONS' exceeded. Limit: 0.0 globally"* (98 votes, 93k
  views) — GPU quota/availability pain.
- *"Google Compute Engine: what is the difference between disk snapshot and disk
  image?"* (67 votes).
- *"How to change Region / Zone in Google Cloud?"* (51 votes, 105k views).

### 3g. oracle-cloud-infrastructure — top by votes
<https://stackoverflow.com/questions/tagged/oracle-cloud-infrastructure?tab=Votes>

OCI's top questions are overwhelmingly *Always Free tier* mechanics and basic
networking — its audience is hobbyists hitting unintuitive defaults:

- *"Opening port 80 on Oracle Cloud Infrastructure Compute node"* (92 votes, 188k views).
- *"Can't access Oracle Cloud Always Free Compute http port"* (60 votes).
- *"How to keep 'always free' account from being terminated?"* (8 votes).
- *"What is the difference between Boot volume and Block volume?"* (8 votes).

**SO synthesis:** across every cloud tag, the top-voted questions split into (a) "what
is the difference between X and Y / which do I use" and (b) "this limit/error/naming is
opaque". Both are reference-page material. API-gateway tags add a third: explicit
**product-vs-product comparison** demand.

---

## 4. Google autocomplete & "People also ask"

`WebSearch` does not expose Google's autocomplete or PAA boxes directly; it returns
ranked results. The *shape* of what ranks for each seed query is itself signal — every
seed term resolves to a dense field of comparison/calculator content, confirming high
search intent. Cannot quote the literal PAA list; the following is inferred from
result-set composition and stated as such.

- Seed **"ec2 vs azure vm which is better"** → top results are head-to-head comparison
  articles, and notably *"Finding the Azure EC2 Equivalent — A 2026 Comparison Guide"*
  (cloudtoggle.com) — i.e. **"X equivalent" / SKU-translation is a live search intent**,
  matching Infra Atlas's Equivalent-SKU matrix.
  <https://www.cloudtoggle.com/blog-en/azure-ec-2-equivalent/>
- Seed **"cheapest cloud region"** → result set is wall-to-wall multi-cloud price
  calculators (Holori, CloudPrice, Cast AI, LeanOps), confirming "which region is
  cheapest" is a heavily-served query. One result frames the core methodology problem:
  *"List rates are region-sensitive — the same instance class can vary materially
  between US-East, Europe, and APAC ... cross-region normalization is therefore
  essential."* <https://leanopstech.com/blog/aws-vs-azure-vs-gcp-cost-comparison/>
- Seed **"which region has h100"** → results are GPU-region/price comparison pages;
  vendor-neutral framing seen in result snippets: *"No single cloud provider can
  guarantee GPU availability — AWS spot instances disappear during training, Azure
  reserves H100s for priority customers, and GCP limits quota in popular regions."*
  <https://www.cloudzero.com/blog/cloud-gpu-pricing-comparison/>
  <https://cloud.google.com/compute/docs/gpus/gpu-regions-zones>
- Seed **"apigee vs kong"** → dense field of comparison articles (Kong's own, Tyk's own,
  API7, StackShare), most vendor-authored — so a *neutral* comparison is differentiated.
  <https://stackshare.io/stackups/apigee-vs-kong>
- Seed **"api gateway timeout"** → results converge on the AWS API Gateway 29-second
  hard limit and async-pattern workarounds, e.g. *"For REST APIs the hard ceiling is 29
  seconds — AWS will not raise it"*; *"Look for integrationLatency: -1 in your access
  logs to confirm timeout vs. slow response."*
  <https://repost.aws/knowledge-center/api-gateway-504-errors>
  <https://www.smplogs.com/guides/api-gateway-504-timeouts>

**Signal for Infra Atlas:** the highest-intent queries — "X equivalent", "cheapest
region", "which region has H100", "API gateway timeout" — map directly to either
existing instruments (Equivalent-SKU, Region Map, APIM) or to clear new ones (a
gateway-limits/quotas reference; a GPU-availability-by-region overlay).

---

## 5. GitHub — what people build because nothing canonical exists

Searched `api.github.com` repositories sorted by stars.

### 5a. Instance-selection / pricing tooling is actively built and starred

- **infracost/infracost** — 12,305 stars. *"Cloud cost estimates for Terraform in pull
  requests."* <https://github.com/infracost/infracost>
- **aws/amazon-ec2-instance-selector** — 931 stars. *"A CLI tool ... which recommends
  instance types based on resource criteria like vcpus and memory."*
  <https://github.com/aws/amazon-ec2-instance-selector>
- **opencost/opencost** — 6,546 stars. Kubernetes + cloud cost monitoring.
  <https://github.com/opencost/opencost>
- **banzaicloud/telescopes** — 164 stars. *"cloud instance types and full cluster layout
  recommender."* <https://github.com/banzaicloud/telescopes>
- **alexei-led/spotinfo** — 161 stars. *"CLI for exploring AWS EC2 Spot inventory ...
  saving, price, and interruption fre[quency]."* <https://github.com/alexei-led/spotinfo>
- **arc53/llm-price-compass** — 223 stars. *"collects GPU benchmarks from various cloud
  providers and compares them to fixed per token costs."*
  <https://github.com/arc53/llm-price-compass>
- **bytebase/dbcost** — *"The simple pricing calculator and comparison tool for the
  cloud databases."* <https://github.com/bytebase/dbcost>
- **Cyclenerd/aws-pricing** — *"Choose the optimal Amazon EC2 instance type in the many
  AWS locations."* <https://github.com/Cyclenerd/aws-pricing>
- **iconara/ec2pricing**, **tedivm/ec2details**, **ilia-semenov/awspricingfull** — three
  separate community projects whose sole purpose is to extract and expose EC2 instance
  type + pricing data, because the official source is hard to consume.

The sheer count of *independent* EC2-pricing-data projects (ec2pricing, ec2details,
aws-pricing, awspricingfull, the famous ec2instances.info / `instances.vantage.sh`) is
itself the signal: the official data is painful enough that the community keeps
re-scraping and re-publishing it.

### 5b. GPU benchmark-vs-price is an emerging gap

`llm-price-compass` exists specifically because raw GPU hourly price says nothing about
tokens/sec — engineers want **price normalised to delivered performance**, not list
price. This is a strong candidate: a GPU-instance reference that pairs spec + region
availability + a normalised performance figure.

---

## Recurring pains, ranked

Ranked by strength of signal (cross-source corroboration × engagement × directness of
"I wish this existed" language).

1. **Official vendor pages/docs are "fluff", not usable data — engineers route to
   third-party references.** Strongest, most direct signal. r/aws "instance type page is
   all fluff" (194 up) and "AWS docs full of fluff" (393 up); the standing fact that "at
   AWS everyone used vantage instead of the official page"; HN praise for
   ec2instances.info as an "invaluable resource ... unsung hero". This *validates Infra
   Atlas's entire premise* — and says: dense tables with filter/sort/search beat pretty
   layouts, every time.
   *Implication: keep doubling down on dense, fast, footnoted instruments; the audience
   explicitly does not want "an enriched customer journey".*

2. **Data-transfer / egress / NAT cost is opaque and a recurring billing trap.** r/aws
   "NAT gateways are too expensive" (171 up); r/googlecloud "Cloud NAT pricing caught us
   off guard"; HN threads repeatedly flag cross-AZ and egress bandwidth as the
   un-modelled cost; multiple "About those egress fees" / "$98k Firebase" posts.
   *Implication: a new instrument — a footnoted egress / data-transfer cost map (internet
   egress, cross-AZ, cross-region, NAT processing, inter-cloud) per provider. Nothing on
   the site covers network cost today.*

3. **Cross-cloud / cross-SKU equivalence and "what is the X equivalent of Y".** r/aws
   Fargate↔EC2 "closest equivalent" question (69 up); r/devops price-comparator author
   asked "compare between providers?"; Google "ec2 vs azure vm" surfaces "Azure EC2
   Equivalent" guides; HN CloudRunr's whole pitch is "maps usage to equivalent VMs".
   *Implication: Equivalent-SKU matrix is on-target; extend it to intra-cloud
   abstractions (Fargate/Cloud Run/Container Apps task sizes ↔ raw VM SKUs).*

4. **"Which product / what's the difference" — the top-voted SO question in almost every
   tag.** GCE's #1 question (547 votes) is App Engine vs Compute Engine; Azure VM's #1
   (119 votes) is web/worker/VM role; api-gateway's #4 is "API gateway vs reverse
   proxy"; Apigee's top questions are all "Apigee vs X". r/devops "Reverse Proxy vs Load
   Balancer vs API Gateway" (156 up).
   *Implication: short, neutral, footnoted "X vs Y / when to use which" decision pages —
   cheap to produce, high evergreen search traffic, fits the editorial format.*

5. **Vendor cost calculators are distrusted; a neutral comparison is wanted.** r/devops
   "every cloud pricing calculator is from a cloud/storage vendor — surprise, their
   option always wins" (61 up); HN "cloud price comparisons are apples to oranges ...
   1vCPU != 1vCPU". Engineers want an *independent* arbiter and acknowledge raw price is
   misleading without performance normalisation.
   *Implication: Infra Atlas's editorial independence is a genuine differentiator —
   state it loudly; and where comparing, normalise (note vCPU definitions, CPU model,
   clock) rather than just listing list price.*

6. **API gateway limits/quotas confusion — especially the 29-second timeout.** SO
   "Amazon API gateway timeout" (202k views), the open aws-cdk issue, and "api gateway
   timeout" being a high-intent Google query.
   *Implication: a per-gateway "hard limits & quotas" reference (timeout ceilings,
   payload sizes, rate-limit defaults, regional vs edge behaviour) — slots into the
   existing APIM material.*

7. **Region/zone capacity & SKU availability is unpredictable.** Azure "VM size not
   available in this zone" (18 up); HN spot-instances thread — "even on-demand isn't
   guaranteed", "out of capacity" errors, "which AMD Zen types are available in
   London?"; GCE "GPUS_ALL_REGIONS quota exceeded" (93k views).
   *Implication: enrich the Region Map / compute explorers with "which SKU families
   exist in which region/zone", and a GPU-availability-by-region view.*

8. **GPU sizing/pricing normalised to performance.** GitHub `llm-price-compass` (223
   stars) exists purely for this; HN/Google GPU-region threads stress availability +
   price together. Cloud GPU pricing is one of the highest-velocity 2026 topics.
   *Implication: a GPU-instance instrument — spec + region availability + a normalised
   performance/$ figure — is a timely, defensible addition.*

9. **Ingress → Gateway API migration (Kubernetes, live in 2026).** Multiple
   r/kubernetes front-page threads (345/233/207 up) on ingress-nginx retirement and
   Gateway API; explicit "I wish switching to Gateway API was as easy as switching
   controllers".
   *Implication: an Ingress-vs-Gateway-API reference (resource mapping, controller
   support matrix, per-feature GA status) — time-sensitive, adjacent to the Kubernetes
   matrix and APIM guides.*

10. **Fargate/serverless-compute premium vs raw VM.** r/aws Fargate-vs-EC2 thread (69
    up) wants the *quantified* convenience premium and the equivalent SKU; HN asks "is 1
    CPU in Fargate the same as in App Runner and Lambda?".
    *Implication: a managed-compute comparison (Fargate / Cloud Run / Container Apps /
    App Runner) — pricing model, vCPU definition, cold-start, limits — vs raw VMs.*
