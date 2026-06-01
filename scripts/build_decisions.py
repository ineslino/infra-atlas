#!/usr/bin/env python3
"""Infra Atlas · Decisions — static-page generator.

Source of truth for the decisions/ department. Holds the curated, sourced
content for each "X vs Y" decision page and emits:
    decisions/index.html              (the hub)
    decisions/<slug>/index.html       (one page per decision)

Every emitted page is static HTML, committed to the repo — there is no
deploy-time build. Re-run after editing the DECISIONS data below:

    python3 scripts/build_decisions.py        # from the repo root

Each comparison-table row carries an HTML <!-- src: URL --> comment with the
vendor doc backing it, and every page lists numbered sources. Bump REVIEWED
when the content is re-verified against the vendor docs.
"""
import html
import json
import os

REVIEWED = "2026-05-19"

# Social-share image. Keep the ?v= in sync with the site-wide cache-bust:
# the bump touches generated *.html, but this generator is a separate source,
# so without the version here a regen would silently revert the cards to a
# stale OG image.
OG_IMAGE = "https://infraatlas.dev/og.png?v=3"

# ── Curated, sourced decision content ───────────────────────────────
# Each decision: slug, cloud tag, title HTML (with one <em>), subtitle,
# verdict (**bold** allowed), column headers, rows [(criterion, [cells], src)],
# pick-when groups, numbered sources, related-instrument cross-links, teaser.
DECISIONS = [
 {
  "slug": "app-engine-vs-compute-engine",
  "cloud": "Google Cloud",
  "title": "App Engine <em>or</em> Compute Engine?",
  "sub": "Google Cloud's PaaS-vs-IaaS choice — ship code, or run the machine.",
  "verdict": "Pick **App Engine** to ship application code and let Google run it — no servers, no OS patching, autoscaling built in. Pick **Compute Engine** when you need the OS, root/SSH access, custom networking, GPUs, or anything that is not a stateless web app. The deciding line is the operations boundary: App Engine trades infrastructure control for near-zero ops burden; Compute Engine gives you full control and the responsibility that comes with it.",
  "cols": ["App Engine", "Compute Engine"],
  "rows": [
   ("Abstraction", ["PaaS — deploy app code, Google runs the servers", "IaaS — you provision and manage the VMs"], "https://docs.cloud.google.com/compute/docs/overview"),
   ("Scale to zero", ["Standard: yes. Flexible: no (min 1 instance)", "Only via schedule-based autoscaling"], "https://docs.cloud.google.com/appengine/docs/the-appengine-environments"),
   ("Cold starts", ["Yes — loading requests; warmup mitigates", "None inherent — you own the VM lifecycle"], "https://docs.cloud.google.com/appengine/docs/standard/how-instances-are-managed"),
   ("Runtimes", ["Standard: Go, Java, Node, Python, PHP, Ruby. Flexible: any (Docker)", "Any — pick the OS, install anything"], "https://docs.cloud.google.com/appengine/docs/standard/runtimes"),
   ("OS / root access", ["Standard: no SSH. Flexible: SSH, OS still managed", "Full root / SSH; Linux or Windows"], "https://docs.cloud.google.com/appengine/docs/the-appengine-environments"),
   ("Pricing model", ["Standard: instance-hours. Flexible: vCPU + memory + disk", "Per-second; sustained- & committed-use discounts"], "https://cloud.google.com/compute/vm-instance-pricing"),
   ("Max request time", ["Standard: 10 min auto / 24 h basic. Flexible: 60 min", "N/A — not a request-scoped platform"], "https://docs.cloud.google.com/appengine/docs/standard/how-instances-are-managed"),
   ("Ideal workload", ["Stateless web apps & HTTP APIs, minimal ops", "Databases, GPU/TPU jobs, daemons, lift-and-shift"], "https://docs.cloud.google.com/compute/docs/overview"),
  ],
  "pick": [
   ("Pick App Engine when", ["You have a stateless web app or HTTP API in a supported language and want to deploy code, not servers.", "Traffic is spiky — autoscaling absorbs it, and Standard can scale to zero between bursts.", "You want minimal ops: no VM lifecycle, no instance groups, no networking setup."]),
   ("Pick Compute Engine when", ["You need root/SSH, a specific OS, kernel modules, or software App Engine will not host.", "The workload is not a web app — databases, batch/HPC, GPU/TPU, long-running daemons.", "You need full VPC control or fine-grained machine sizing and cost levers."]),
  ],
  "sources": [
   ("Choose an App Engine environment", "https://docs.cloud.google.com/appengine/docs/the-appengine-environments"),
   ("Compute Engine overview", "https://docs.cloud.google.com/compute/docs/overview"),
   ("App Engine Standard — instance management", "https://docs.cloud.google.com/appengine/docs/standard/how-instances-are-managed"),
   ("App Engine Standard runtimes", "https://docs.cloud.google.com/appengine/docs/standard/runtimes"),
   ("Compute Engine autoscaler", "https://docs.cloud.google.com/compute/docs/autoscaler"),
   ("Compute Engine VM pricing", "https://cloud.google.com/compute/vm-instance-pricing"),
  ],
  "crosslinks": [("GCP Compute Index", "/gcp-compute/")],
  "teaser": "PaaS or IaaS on Google Cloud — when to hand Google the servers, and when to keep them.",
 },
 {
  "slug": "fargate-vs-ec2",
  "cloud": "AWS · containers",
  "title": "Fargate <em>or</em> EC2 for ECS?",
  "sub": "Serverless containers, or containers on instances you run yourself.",
  "verdict": "Pick **Fargate** for zero infrastructure management, spiky workloads, or simply getting started — you pay per vCPU-second the task requests and AWS owns the host. Pick the **EC2 launch type** for large, steady, high-utilisation workloads that must be price-optimised, or anything needing GPUs, privileged containers, daemon workloads, or custom AMIs. The deciding factor is steady-state utilisation and host control: high predictable load plus any host-level need points to EC2; everything else favours Fargate.",
  "cols": ["Fargate", "EC2 launch type"],
  "rows": [
   ("Host management", ["AWS — no provisioning, patching or scaling", "You — instance choice, config, maintenance"], "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html"),
   ("Pricing model", ["Per-second, on the vCPU + memory the task requests", "The EC2 instances you run — used or idle"], "https://aws.amazon.com/fargate/pricing/"),
   ("Cost at steady high load", ["Less efficient — billed per task, not per packed host", "Cheaper — pack instances to high utilisation"], "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/launch_types.html"),
   ("GPU support", ["Not supported", "Yes — EC2 GPU instances + the GPU-optimized AMI"], "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-gpu.html"),
   ("Privileged / daemon tasks", ["No — privileged and the DAEMON strategy unsupported", "Yes — privileged containers and DAEMON tasks"], "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-tasks-services.html"),
   ("Host access", ["None — no SSH, no custom AMI", "Full — SSH, custom AMIs, instance-type choice"], "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/launch_types.html"),
   ("Networking modes", ["awsvpc only — one ENI per task", "awsvpc, bridge or host"], "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-tasks-services.html"),
   ("Isolation", ["Each task in its own kernel / CPU / memory boundary", "Tasks on an instance share that instance's kernel"], "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html"),
  ],
  "pick": [
   ("Pick Fargate when", ["You want to focus on the application and not provision, patch or scale servers.", "Workloads are variable — you would rather pay per task-second than for idle instances.", "You are starting with containers, or you need strong per-task isolation."]),
   ("Pick the EC2 launch type when", ["You run large, steady, high-utilisation workloads that must be price-optimised.", "You need GPUs, privileged containers, the DAEMON strategy, or bridge/host networking.", "You need custom AMIs, specific instance types, or host-level access."]),
  ],
  "sources": [
   ("Architect for AWS Fargate for Amazon ECS", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html"),
   ("Amazon ECS launch types", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/launch_types.html"),
   ("ECS task definitions for Fargate", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-tasks-services.html"),
   ("ECS task definitions for GPU workloads", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-gpu.html"),
   ("AWS Fargate pricing", "https://aws.amazon.com/fargate/pricing/"),
   ("Amazon ECS pricing", "https://aws.amazon.com/ecs/pricing/"),
  ],
  "crosslinks": [("EC2 Observatory", "/ec2/"), ("Equivalent-SKU Finder", "/equivalent-sku/")],
  "teaser": "Hand AWS the host, or run your own instances — the ECS container-platform call.",
 },
 {
  "slug": "api-gateway-vs-proxy-vs-load-balancer",
  "cloud": "Patterns · AWS reference",
  "title": "API gateway, proxy <em>or</em> load balancer?",
  "sub": "Three things you put in front of services — and they are often layered, not either/or.",
  "verdict": "A **load balancer** spreads traffic across healthy targets for availability and scale. A **reverse proxy** is a general-purpose intermediary you fully control — routing, TLS, caching, rewriting. An **API gateway** is a managed product for publishing and governing APIs — auth, API keys, throttling, transformation, OpenAPI. They are commonly layered (gateway in front of a load balancer in front of services), not a single choice. The deciding factor is how much API-product governance you need.",
  "cols": ["API gateway", "Reverse proxy", "Load balancer"],
  "rows": [
   ("Primary purpose", ["Publish and govern APIs", "A general-purpose request intermediary", "Spread traffic across healthy targets"], "https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html"),
   ("OSI layer", ["L7 — HTTP / REST / WebSocket", "L7", "L7 (ALB) or L4 (NLB)"], "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html"),
   ("Auth & API keys", ["Built in — IAM, Cognito, Lambda authorizers, API keys", "Manual configuration", "ALB: OIDC/Cognito. NLB: none"], "https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html"),
   ("Rate limiting", ["Built in — throttling, usage plans, quotas", "Manual (e.g. limit_req)", "Not provided"], "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html"),
   ("Transformation", ["Yes — mapping templates and parameter mapping", "Manual header / URI rewriting", "None"], "https://docs.aws.amazon.com/apigateway/latest/developerguide/rest-api-data-transformations.html"),
   ("API-product management", ["OpenAPI import/export, SDK generation, stages", "None", "None"], "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-import-api.html"),
   ("Who operates it", ["Fully managed by AWS", "You operate the server / process", "Fully managed by AWS"], "https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html"),
   ("Typical placement", ["Edge entry point for APIs", "Any hop you control", "In front of a fleet, often behind a gateway"], "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html"),
  ],
  "pick": [
   ("Reach for an API gateway when", ["You publish APIs and need API keys, usage plans and quotas.", "You need managed auth and request transformation without running code.", "You manage APIs as products via OpenAPI, stages and SDKs."]),
   ("Reach for a reverse proxy when", ["You need full control of routing, rewriting, caching or static content.", "You want a portable, vendor-neutral intermediary — on-prem, multi-cloud, or a sidecar.", "Your needs sit between a plain load balancer and a gateway, and you will operate it."]),
   ("Reach for a load balancer when", ["The goal is spreading traffic across healthy targets for availability.", "You need L4 throughput and static IPs (NLB) or L7 path routing (ALB).", "You want a managed, health-checked entry point without API-product features."]),
  ],
  "sources": [
   ("Amazon API Gateway — welcome / overview", "https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html"),
   ("API Gateway request throttling", "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html"),
   ("API Gateway data transformations", "https://docs.aws.amazon.com/apigateway/latest/developerguide/rest-api-data-transformations.html"),
   ("Application Load Balancer — introduction", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html"),
   ("Network Load Balancer — introduction", "https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html"),
   ("ALB — authenticate users", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-authenticate-users.html"),
   ("nginx — beginner's guide (reverse proxy)", "https://nginx.org/en/docs/beginners_guide.html"),
  ],
  "crosslinks": [("APIM Feature Matrix", "/apim-matrix/"), ("AWS API Gateway Atlas", "/aws-api-gateway/")],
  "teaser": "Gateway, proxy, load balancer — what each is actually for, and why you often need all three.",
 },
 {
  "slug": "rest-api-vs-http-api",
  "cloud": "AWS · API Gateway",
  "title": "REST API <em>or</em> HTTP API?",
  "sub": "Amazon API Gateway's two API types — the cheaper default, and what still needs the original.",
  "verdict": "**HTTP API** is the right default for new APIs — roughly a third of the price per million requests, and it covers the common cases: Lambda and HTTP proxy integrations, JWT / Lambda / IAM authorization, CORS, custom domains. Choose **REST API** when you specifically need API keys with usage plans, AWS WAF, a private (VPC-only) endpoint, request validation, response caching, an edge-optimized endpoint, or body transformation. The deciding factor: if you need API keys plus usage plans, WAF, or a private endpoint, you must use REST API — HTTP API does not offer them.",
  "cols": ["REST API", "HTTP API"],
  "rows": [
   ("Price per million requests", ["$3.50 (first tier)", "$1.00 (first tier)"], "https://aws.amazon.com/api-gateway/pricing/"),
   ("API keys & usage plans", ["Yes — per-client throttling and quotas", "No"], "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html"),
   ("AWS WAF integration", ["Yes", "No"], "https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-control-access-aws-waf.html"),
   ("Private (VPC-only) endpoint", ["Yes", "No"], "https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-private-apis.html"),
   ("JWT authorizer", ["No — use a Lambda authorizer for JWTs", "Yes — native"], "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html"),
   ("Request validation", ["Yes", "No"], "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vs-rest.html"),
   ("Body transformation", ["Yes — VTL mapping templates", "No — parameter mapping only"], "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vs-rest.html"),
   ("Response caching", ["Yes — per-stage", "No"], "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html"),
   ("Edge-optimized endpoint", ["Yes", "No"], "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vs-rest.html"),
  ],
  "pick": [
   ("Pick HTTP API when", ["You want the lowest cost — about $1.00 vs $3.50 per million requests.", "Your needs are Lambda or HTTP proxy integrations with JWT, Lambda or IAM authorization.", "You do not need API keys, request validation, WAF, caching or private endpoints."]),
   ("Pick REST API when", ["You need API keys with usage plans for per-client throttling and quotas.", "You need AWS WAF, a private (VPC-only) endpoint, or request validation.", "You need body transformation, response caching, or an edge-optimized endpoint."]),
  ],
  "sources": [
   ("Choosing between REST APIs and HTTP APIs", "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vs-rest.html"),
   ("Amazon API Gateway pricing", "https://aws.amazon.com/api-gateway/pricing/"),
   ("Private REST APIs in API Gateway", "https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-private-apis.html"),
   ("Use AWS WAF to protect REST APIs", "https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-control-access-aws-waf.html"),
   ("JWT authorizers for HTTP APIs", "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html"),
   ("Usage plans and API keys for REST APIs", "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html"),
   ("Cache settings for REST APIs", "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html"),
  ],
  "crosslinks": [("AWS API Gateway Atlas", "/aws-api-gateway/"), ("APIM Feature Matrix", "/apim-matrix/")],
  "teaser": "API Gateway's cheaper default vs the feature-complete original — and the features that force the choice.",
 },
 {
  "slug": "cloud-run-vs-app-engine-flex",
  "cloud": "Google Cloud",
  "title": "Cloud Run <em>or</em> App Engine Flexible?",
  "sub": "Two ways to run containers on Google Cloud — and Google's own recommended default.",
  "verdict": "**Cloud Run** is Google's modern default — its own documentation recommends it over App Engine for new users, citing advanced capabilities such as GPUs at lower prices. It scales to zero and bills per request. **App Engine Flexible** is not deprecated and remains supported, but it is a legacy option: it still fits when you need VM-level control (Compute Engine VMs with SSH), workloads that must sit in the Compute Engine network, or steady traffic where an always-on instance is acceptable. The deciding factor is scale-to-zero and billing — Cloud Run charges nothing when idle; Flexible always keeps a billable VM running.",
  "cols": ["Cloud Run", "App Engine Flexible"],
  "rows": [
   ("Scale to zero", ["Yes — idle revisions scale to 0 instances", "No — at least one instance always runs"], "https://docs.cloud.google.com/run/docs/about-instance-autoscaling"),
   ("Billing when idle", ["Request-based billing — no charge when idle", "Instances billed continuously"], "https://docs.cloud.google.com/run/docs/configuring/billing-settings"),
   ("Deploy unit", ["Any OCI / Docker container, as an immutable revision", "A Docker container on Compute Engine VMs"], "https://docs.cloud.google.com/run/docs/resource-model"),
   ("Cold starts", ["Yes — scale-from-zero", "None — no scale-from-zero"], "https://docs.cloud.google.com/run/docs/about-instance-autoscaling"),
   ("Startup speed", ["Seconds", "Minutes — VM boot"], "https://docs.cloud.google.com/appengine/docs/the-appengine-environments"),
   ("Request timeout", ["Default 5 min, configurable to 60 min", "60 min"], "https://docs.cloud.google.com/run/docs/configuring/request-timeout"),
   ("GPU support", ["Yes — NVIDIA L4 and RTX PRO 6000", "No"], "https://docs.cloud.google.com/run/docs/configuring/services/gpu"),
   ("VM-level access", ["No host access", "Yes — SSH into the underlying Compute Engine VM"], "https://docs.cloud.google.com/appengine/docs/flexible/overview"),
   ("Positioning", ["Modern, recommended default for new projects", "Supported; Cloud Run recommended instead"], "https://docs.cloud.google.com/appengine/migration-center/run/compare-gae-with-run"),
  ],
  "pick": [
   ("Pick Cloud Run when", ["Traffic is spiky — scale to zero and pay only per request.", "You are starting a new project — Google recommends it as the default.", "You need GPUs, fast deploys, or percentage-based traffic splitting."]),
   ("Pick App Engine Flexible when", ["You need VM-level control — SSH into the Compute Engine VM for debugging.", "Your app must run inside the Compute Engine network.", "You have an existing Flexible app and migration cost outweighs modernising now."]),
  ],
  "sources": [
   ("Compare App Engine and Cloud Run", "https://docs.cloud.google.com/appengine/migration-center/run/compare-gae-with-run"),
   ("Cloud Run instance autoscaling", "https://docs.cloud.google.com/run/docs/about-instance-autoscaling"),
   ("Cloud Run billing settings", "https://docs.cloud.google.com/run/docs/configuring/billing-settings"),
   ("Cloud Run request timeout", "https://docs.cloud.google.com/run/docs/configuring/request-timeout"),
   ("Cloud Run GPU configuration", "https://docs.cloud.google.com/run/docs/configuring/services/gpu"),
   ("App Engine flexible environment overview", "https://docs.cloud.google.com/appengine/docs/flexible/overview"),
  ],
  "crosslinks": [("GCP Compute Index", "/gcp-compute/")],
  "teaser": "Google's modern serverless-container default vs the legacy VM-backed option.",
 },
 {
  "slug": "aurora-vs-rds",
  "cloud": "AWS · databases",
  "title": "Aurora <em>or</em> RDS?",
  "sub": "Amazon's two managed relational databases — distributed architecture, or the lower floor cost.",
  "verdict": "Pick **Aurora** for a MySQL- or PostgreSQL-compatible database that values its distributed storage: failover in roughly 30 seconds, up to 15 low-lag readers on one volume, a multi-region Global Database, and Serverless v2 scale-to-low. Pick standard **RDS** when you need an engine Aurora does not offer — MariaDB, Oracle, SQL Server, Db2 — or when a small, steady workload costs less on RDS's simple instance-plus-volume pricing. The single biggest factor is the engine: need MariaDB / Oracle / SQL Server and it must be RDS; otherwise it is Aurora's architecture against RDS's lower floor.",
  "cols": ["Aurora", "RDS (standard engines)"],
  "rows": [
   ("Supported engines", ["MySQL- and PostgreSQL-compatible only", "MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Db2"], "https://aws.amazon.com/rds/faqs/"),
   ("Storage architecture", ["One distributed volume — 6 copies across 3 AZs", "An EBS volume per instance; Multi-AZ adds a standby"], "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Overview.StorageReliability.html"),
   ("Read replicas", ["Up to 15, sharing the volume, tens-of-ms lag", "Up to 15 (MySQL/PostgreSQL), async, variable lag"], "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Overview.html"),
   ("Failover speed", ["Typically ~30 s when replicas exist", "Multi-AZ instance: typically 1-2 minutes"], "https://aws.amazon.com/rds/aurora/faqs/"),
   ("Serverless / scale-to-low", ["Serverless v2 — 0.5-ACU steps, can pause to zero", "No serverless option for standard engines"], "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2-auto-pause.html"),
   ("Multi-region", ["Global Database — up to 10 Regions, sub-second lag", "Cross-Region read replicas, asynchronous"], "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html"),
   ("Pricing model", ["Compute + storage + I/O, or I/O-Optimized", "Instance-hours + storage + provisioned IOPS"], "https://aws.amazon.com/rds/aurora/pricing/"),
   ("Cost for small steady workloads", ["Higher floor", "Lower — simple instance plus a single volume"], "https://aws.amazon.com/rds/faqs/"),
  ],
  "pick": [
   ("Pick Aurora when", ["You need MySQL or PostgreSQL with fast (~30 s) failover and high availability.", "You need many low-lag read replicas, or a multi-region Global Database.", "Your workload is spiky — Serverless v2 pauses to near-zero compute cost."]),
   ("Pick standard RDS when", ["You need MariaDB, Oracle, SQL Server or Db2 — Aurora supports none of them.", "You run a small, steady workload where simple instance + volume pricing is cheaper.", "You want a straightforward EBS-backed model with predictable provisioned IOPS."]),
  ],
  "sources": [
   ("Amazon Aurora FAQs", "https://aws.amazon.com/rds/aurora/faqs/"),
   ("Amazon RDS FAQs", "https://aws.amazon.com/rds/faqs/"),
   ("Aurora storage and reliability", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Overview.StorageReliability.html"),
   ("Aurora Serverless v2 auto-pause", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2-auto-pause.html"),
   ("Aurora global databases", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html"),
   ("Amazon Aurora pricing", "https://aws.amazon.com/rds/aurora/pricing/"),
  ],
  "crosslinks": [],
  "teaser": "AWS's cloud-native database engine vs classic managed RDS — architecture, or the cheaper floor.",
 },
 {
  "slug": "azure-app-service-vs-container-apps-vs-vm",
  "cloud": "Azure",
  "title": "App Service, Container Apps <em>or</em> a VM?",
  "sub": "Azure's modern compute choice — the successor to 'web role vs worker role vs VM'.",
  "verdict": "**App Service** is managed PaaS for web apps and APIs — deploy code, Microsoft runs the OS. **Container Apps** is serverless, Kubernetes-based PaaS for containerised microservices and event-driven jobs, with scale-to-zero. **Virtual Machines** is IaaS — full OS control, and the work that comes with it. The deciding factor is control against management: App Service for a code-first web app, Container Apps for containerised or event-driven microservices needing scale-to-zero, and VMs only when you genuinely need OS-level control or software no PaaS supports.",
  "cols": ["App Service", "Container Apps", "Virtual Machines"],
  "rows": [
   ("Hosting model", ["Managed PaaS", "Serverless PaaS, built on Kubernetes", "IaaS — you provision and manage VMs"], "https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/compute-decision-tree"),
   ("Deploy unit", ["Code (.NET, Java, Node, Python, PHP) or a container", "A container image", "A VM / OS image"], "https://learn.microsoft.com/en-us/azure/app-service/overview"),
   ("Scale to zero", ["No — plan instances always run", "Yes — most apps scale to zero", "No"], "https://learn.microsoft.com/en-us/azure/container-apps/overview"),
   ("Autoscaling", ["Built-in autoscale rules", "KEDA — HTTP traffic, events, CPU/memory", "Virtual Machine Scale Sets"], "https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/compute-decision-tree"),
   ("Pricing model", ["Per App Service plan instance", "Serverless consumption — vCPU / GiB-seconds", "Hourly per VM size + OS"], "https://learn.microsoft.com/en-us/azure/app-service/overview-hosting-plans"),
   ("Control & OS access", ["Platform manages the OS — no general access", "Abstracted Kubernetes — no OS or K8s API", "Full — patch and install anything"], "https://learn.microsoft.com/en-us/azure/virtual-machines/overview"),
   ("Best workloads", ["Web apps, REST APIs, mobile back ends", "Microservices, event-driven and background jobs", "Anything — lift-and-shift, HPC, SAP / Oracle"], "https://learn.microsoft.com/en-us/azure/container-apps/overview"),
   ("Ops burden", ["Low", "Low", "High"], "https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/compute-decision-tree"),
  ],
  "pick": [
   ("Pick App Service when", ["You have a web app, REST API or mobile back end in a supported language.", "You want deployment slots, CI/CD and managed certificates without orchestration.", "Traffic is steady and predictable — scale-to-zero is not required."]),
   ("Pick Container Apps when", ["You run containerised microservices or event-driven jobs and want scale-to-zero.", "You want KEDA autoscaling, Dapr, and revision-based blue/green.", "You want Kubernetes patterns without managing a cluster or its API."]),
   ("Pick Virtual Machines when", ["You need full OS control, or must run software no PaaS supports.", "You are doing a like-for-like lift-and-shift of an existing workload.", "You run specialty workloads — SAP, Oracle, HPC, or your own Kubernetes."]),
  ],
  "sources": [
   ("Choose an Azure compute service", "https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/compute-decision-tree"),
   ("Azure App Service overview", "https://learn.microsoft.com/en-us/azure/app-service/overview"),
   ("App Service plans and tiers", "https://learn.microsoft.com/en-us/azure/app-service/overview-hosting-plans"),
   ("Azure Container Apps overview", "https://learn.microsoft.com/en-us/azure/container-apps/overview"),
   ("Azure Virtual Machines overview", "https://learn.microsoft.com/en-us/azure/virtual-machines/overview"),
  ],
  "crosslinks": [("Azure VM Atlas", "/azure-vm/")],
  "teaser": "Azure's PaaS, its serverless containers, or raw VMs — the modern three-way compute call.",
 },
 {
  "slug": "nat-gateway-vs-instance-vs-no-nat",
  "cloud": "AWS · networking",
  "title": "NAT gateway, NAT instance <em>or</em> no NAT?",
  "sub": "How private-subnet workloads reach the internet — or avoid needing to.",
  "verdict": "**NAT Gateway** is the default for private-subnet egress — AWS recommends it for availability, bandwidth and zero administration. A **NAT instance** is now a niche, legacy choice: pick it only for a feature the gateway lacks — port forwarding, doubling as a bastion, or very low traffic where its hourly cost wins. You can **skip NAT entirely** when private workloads only talk to AWS services (a free Gateway endpoint, or Interface endpoints), or when a workload is genuinely public. The deciding factor is cost: the NAT Gateway data-processing charge applies to every GB — including AWS-service traffic a cheaper endpoint could carry.",
  "cols": ["NAT Gateway", "NAT instance", "No NAT"],
  "rows": [
   ("Managed?", ["Fully managed by AWS", "You manage it — OS and patches", "Endpoints and gateways fully managed"], "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-comparison.html"),
   ("Availability", ["Redundant within its AZ", "Single instance — you script failover", "HA, horizontally scaled"], "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-comparison.html"),
   ("Bandwidth", ["5 Gbps, auto-scales to 100 Gbps", "Limited by the instance type", "No NAT bandwidth limit"], "https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-basics.html"),
   ("Hourly cost", ["Per-gateway hourly charge", "EC2 instance hourly rate", "Gateway endpoint: none. Interface: ~$0.01/AZ-hr"], "https://aws.amazon.com/vpc/pricing/"),
   ("Data-processing cost", ["A per-GB charge on all traffic", "None — pay EC2 data transfer only", "Gateway endpoint: none. Interface: ~$0.01/GB"], "https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-pricing.html"),
   ("Port forwarding / bastion", ["Not supported", "Supported — can also serve as a bastion", "Not applicable"], "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-comparison.html"),
   ("Maintenance", ["None", "OS patches; build your own NAT AMI", "None"], "https://docs.aws.amazon.com/vpc/latest/userguide/work-with-nat-instances.html"),
   ("AWS-service-only egress", ["Works, but billed per GB", "Works, with management overhead", "Best fit — a free Gateway endpoint"], "https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html"),
  ],
  "pick": [
   ("Pick NAT Gateway when", ["Private workloads need general outbound internet — it is the AWS-recommended default.", "You want zero maintenance and built-in per-AZ redundancy.", "Traffic is moderate-to-high and the per-GB charge is acceptable."]),
   ("Pick a NAT instance when", ["You need port forwarding, which a NAT Gateway does not support.", "You want one instance to also serve as a bastion / jump host.", "Egress is tiny and infrequent, where a small instance undercuts the gateway."]),
   ("Skip NAT entirely when", ["Private workloads only reach S3 or DynamoDB — use a free Gateway endpoint.", "Egress is only to other AWS services — Interface endpoints usually undercut NAT.", "The workload is genuinely public — put it in a public subnet behind an internet gateway."]),
  ],
  "sources": [
   ("NAT gateway vs NAT instance comparison", "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-comparison.html"),
   ("NAT gateway basics — bandwidth and limits", "https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-basics.html"),
   ("NAT gateway pricing", "https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-pricing.html"),
   ("Amazon VPC pricing", "https://aws.amazon.com/vpc/pricing/"),
   ("Work with NAT instances", "https://docs.aws.amazon.com/vpc/latest/userguide/work-with-nat-instances.html"),
   ("Gateway endpoints for S3 and DynamoDB", "https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html"),
   ("Egress-only internet gateways", "https://docs.aws.amazon.com/vpc/latest/userguide/egress-only-internet-gateway.html"),
  ],
  "crosslinks": [],
  "teaser": "Private-subnet egress on AWS — the managed default, the legacy workaround, and skipping NAT outright.",
 },
 {
  "slug": "sovereign-cloud-legal-vs-operational",
  "cloud": "Cross-cloud · sovereignty",
  "title": "Sovereign region <em>or</em> EU-native provider?",
  "sub": "A US hyperscaler's 'sovereign' region gives you operational sovereignty; only an EU-jurisdiction provider gives legal sovereignty — and the CLOUD Act is the reason.",
  "reviewed": "2026-06-01",
  "verdict": "Pick a **hyperscaler sovereign region** — AWS European Sovereign Cloud, Azure with Bleu, Google with S3NS — when you need the hyperscaler's full service breadth and scale and your requirement is data residency plus EU-resident operations. That buys operational sovereignty, but the US parent stays reachable under the CLOUD Act, so it is not legal sovereignty. Pick an **EU-native provider** — OVHcloud, Scaleway, IONOS, STACKIT, T-Systems, Aruba — when legal sovereignty is the real requirement: an EU-jurisdiction company with no US parent sits outside the CLOUD Act's reach, at the cost of a narrower catalogue and smaller scale. The deciding question is which sovereignty you actually need — **data residency and operational control**, where a sovereign region is enough, or **immunity from foreign legal compulsion**, where you need an EU-parent provider. In a hyperscaler's marketing, 'sovereign' means the first, not the second.",
  "cols": ["Hyperscaler sovereign region", "EU-native provider"],
  "rows": [
    ("Legal sovereignty — immune to US compulsion?",
     ["No — the US parent stays reachable under the CLOUD Act",
      "Yes — EU-jurisdiction parent, outside US reach"],
     "https://www.justice.gov/criminal/cloud-act-resources"),
    ("Operational sovereignty (EU staff + ops)",
     ["Yes — EU regions, EU-resident operations",
      "Yes — EU-resident by default"],
     "/sovereignty/"),
    ("Data residency",
     ["EU region / data boundary",
      "EU only"],
     "/sovereignty/"),
    ("Service breadth & scale",
     ["Full hyperscaler catalogue + global scale",
      "Narrower catalogue, smaller scale"],
     "/sovereignty/"),
    ("Certifications (SecNumCloud / C5 / ENS)",
     ["Often via an EU partner (Bleu, S3NS) — verify per service",
      "Several hold SecNumCloud (ANSSI) outright"],
     "/compliance/"),
    ("Provider parent jurisdiction",
     ["US — sometimes operated via an EU joint venture",
      "EU — company + parent both in-jurisdiction"],
     "https://www.justice.gov/criminal/cloud-act-resources"),
  ],
  "pick": [
    ("Pick a hyperscaler sovereign region when", [
      "You need the hyperscaler's full service breadth, scale, and ecosystem.",
      "Your requirement is data residency + EU-resident operations, not immunity from foreign law.",
      "You are already deep in one hyperscaler and migration cost is high.",
      "You accept that the US parent stays legally reachable — operational, not legal, sovereignty.",
    ]),
    ("Pick an EU-native provider when", [
      "Legal sovereignty / CLOUD-Act immunity is a hard requirement — regulated, public-sector, or defence workloads.",
      "SecNumCloud-grade (ANSSI) assurance is required.",
      "The workload fits a narrower catalogue and needs no hyperscaler-only services.",
      "You want an EU-jurisdiction company end to end, parent included.",
    ]),
  ],
  "sources": [
    ("US CLOUD Act — DOJ resources", "https://www.justice.gov/criminal/cloud-act-resources"),
    ("EU Data Act — Reg (EU) 2023/2854 (switching + egress)", "https://eur-lex.europa.eu/eli/reg/2023/2854/oj/eng"),
    ("GDPR Chapter V — Reg (EU) 2016/679 (international transfers)", "https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng"),
    ("EUCS — EU cloud certification scheme (ENISA)", "https://www.enisa.europa.eu/publications/eucs-cloud-service-scheme"),
    ("Infra Atlas — European Sovereignty (the full sourced matrix)", "/sovereignty/"),
    ("Infra Atlas — Compliance Footprint (certifications)", "/compliance/"),
  ],
  "crosslinks": [("European Sovereignty", "/sovereignty/"), ("Compliance Footprint", "/compliance/")],
  "teaser": "A US hyperscaler's 'sovereign' region buys operational sovereignty; only an EU-parent provider gives legal sovereignty — the CLOUD Act is why.",
 },
]

# ── Hand-authored decisions ─────────────────────────────────────────
# Bespoke pages that don't fit the generated template: they carry custom
# sections (e.g. observability's "hybrid reality"), hand-crafted meta
# descriptions, and finer typography (&rsquo; etc.) than render_page emits.
# They are LISTED in the hub here so a regen never orphans them, but are NOT
# regenerated — edit their index.html directly. Only render_hub reads these
# (slug, cloud, title, teaser, reviewed); main() skips them.
HANDWRITTEN = [
 {
  "slug": "cloud-native-vs-managed-vs-self-hosted-observability",
  "cloud": "Cross-cloud · patterns",
  "title": "Cloud-native, managed <em>or</em> self-hosted observability?",
  "teaser": "Three operating models for the same problem — where you sit on the build-vs-buy spectrum.",
  "reviewed": "2026-05-28",
 },
]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:'
         'ital@0;1&family=JetBrains+Mono:wght@300;400;500;600&family=Manrope:'
         'wght@300;400;500;600;700&display=swap" rel="stylesheet">')


def esc(s):
    return html.escape(str(s), quote=True)


def verdict_html(text):
    """Escape verdict prose, turning **bold** spans into <strong>."""
    out, parts = [], text.split("**")
    for i, p in enumerate(parts):
        out.append(("<strong>" + esc(p) + "</strong>") if i % 2 else esc(p))
    return "".join(out)


def plain_title(d):
    return d["title"].replace("<em>", "").replace("</em>", "")


def render_page(d):
    q = plain_title(d)
    rev = d.get("reviewed", REVIEWED)
    ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": q,
        "description": d["sub"],
        "url": f"https://infraatlas.dev/decisions/{d['slug']}/",
        "datePublished": rev,
        "dateModified": rev,
        "inLanguage": "en",
        "isPartOf": {"@type": "WebSite", "name": "Infra Atlas",
                     "url": "https://infraatlas.dev/"},
    }, indent=2).replace("<", "\\u003c")
    head = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="color-scheme" content="dark">
<title>{esc(q)} · Decisions · Infra Atlas</title>
<link rel="icon" href="/favicon.svg?v=2" type="image/svg+xml">
<meta name="description" content="{esc(d['sub'])}">
<link rel="canonical" href="https://infraatlas.dev/decisions/{d['slug']}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Infra Atlas">
<meta property="og:title" content="{esc(q)} · Infra Atlas Decisions">
<meta property="og:description" content="{esc(d['sub'])}">
<meta property="og:url" content="https://infraatlas.dev/decisions/{d['slug']}/">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(q)} · Infra Atlas Decisions">
<meta name="twitter:description" content="{esc(d['sub'])}">
<meta name="twitter:image" content="{OG_IMAGE}">
<script type="application/ld+json">
{ld}
</script>
{FONTS}
<link rel="stylesheet" href="/decisions/decision.css">
</head>
<body>
<div class="grain"></div>
<div class="scanlines"></div>
<div class="page">"""

    masthead = f"""
  <header class="masthead">
    <a class="eyebrow" href="/decisions/"><span class="arrow">←</span> Infra Atlas · Decisions</a>
    <h1 class="title">{d['title']}</h1>
    <p class="subtitle">{esc(d['sub'])}</p>
    <div class="reviewed"><span class="dot"></span>Reviewed <time datetime="{rev}">{rev}</time></div>
  </header>"""

    verdict = f"""
  <section class="verdict">
    <div class="sec-label">The verdict</div>
    <p>{verdict_html(d['verdict'])}</p>
  </section>"""

    ths = "".join(f"<th>{esc(c)}</th>" for c in d["cols"])
    trs = []
    for crit, cells, src in d["rows"]:
        tds = f'<td class="criterion">{esc(crit)}</td>'
        tds += "".join(f'<td class="val">{esc(c)}</td>' for c in cells)
        # raw src — an HTML comment is not entity-decoded, so esc() here would
        # corrupt a URL containing & (and these are trusted, curated URLs).
        trs.append(f"        <tr><!-- src: {src} -->{tds}</tr>")
    table = ("\n  <section>\n    <div class=\"sec-label\">Head to head</div>\n"
             "    <div class=\"compare-wrap\"><table class=\"compare\">\n"
             f"      <thead><tr><th>Criterion</th>{ths}</tr></thead>\n"
             "      <tbody>\n" + "\n".join(trs) + "\n      </tbody>\n"
             "    </table></div>\n  </section>")

    picks = []
    for heading, bullets in d["pick"]:
        lis = "".join(f"<li>{esc(b)}</li>" for b in bullets)
        picks.append(f'      <div class="pick"><h4>{esc(heading)}</h4><ul>{lis}</ul></div>')
    pickwhen = ("\n  <section>\n    <div class=\"sec-label\">When to pick which</div>\n"
                "    <div class=\"pickwhen\">\n" + "\n".join(picks) + "\n    </div>\n  </section>")

    src_lis = "".join(f'\n      <li>{esc(label)} — <a href="{esc(url)}" '
                      f'target="_blank" rel="noopener">{esc(url)}</a></li>'
                      for label, url in d["sources"])
    sources = ("\n  <section class=\"sources\">\n    <div class=\"sec-label\">Sources</div>\n"
               f"    <ol>{src_lis}\n    </ol>\n  </section>")

    cross = ""
    if d["crosslinks"]:
        links = "".join(f'<a href="{esc(h)}">{esc(l)}</a>' for l, h in d["crosslinks"])
        cross = ("\n  <section>\n    <div class=\"sec-label\">Related instruments</div>\n"
                 f'    <div class="crosslinks"><span class="lbl">See also</span>{links}</div>\n  </section>')

    foot = f"""
  <footer class="colophon">
    Reviewed <time datetime="{rev}">{rev}</time> against vendor documentation — every
    comparison-table row and the verdict carry a source. Part of <a href="/">Infra Atlas</a>
    · <a href="/decisions/">Decisions</a>. Spot a stale fact?
    <a href="https://github.com/ineslino/infra-atlas/issues/new" target="_blank" rel="noopener">Open an issue</a>.
  </footer>
</div>
<script src="/nav.js" defer></script>
</body>
</html>
"""
    return head + masthead + verdict + table + pickwhen + sources + cross + foot


def render_hub():
    cards = []
    for d in DECISIONS + HANDWRITTEN:
        cards.append(
            f'        <a class="dcard" href="/decisions/{d["slug"]}/">\n'
            f'          <div class="dcard__cloud">{esc(d["cloud"])}</div>\n'
            f'          <div class="dcard__q">{d["title"]}</div>\n'
            f'          <div class="dcard__teaser">{esc(d["teaser"])}</div>\n'
            f'          <div class="dcard__foot">Reviewed {d.get("reviewed", REVIEWED)}</div>\n'
            f'        </a>')
    n = len(DECISIONS) + len(HANDWRITTEN)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="color-scheme" content="dark">
<title>Decisions · Infra Atlas</title>
<link rel="icon" href="/favicon.svg?v=2" type="image/svg+xml">
<meta name="description" content="Short, neutral, footnoted answers to the 'which one should I use' questions cloud engineers ask most — Fargate vs EC2, REST vs HTTP API, Aurora vs RDS, and more. With the asterisks intact.">
<link rel="canonical" href="https://infraatlas.dev/decisions/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Infra Atlas">
<meta property="og:title" content="Decisions · Infra Atlas">
<meta property="og:description" content="Short, neutral, footnoted 'which one should I use' references for the cloud comparisons engineers ask most.">
<meta property="og:url" content="https://infraatlas.dev/decisions/">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Decisions · Infra Atlas">
<meta name="twitter:description" content="Short, neutral, footnoted 'which one should I use' references for the cloud comparisons engineers ask most.">
<meta name="twitter:image" content="{OG_IMAGE}">
{FONTS}
<link rel="stylesheet" href="/decisions/decision.css">
</head>
<body>
<div class="grain"></div>
<div class="scanlines"></div>
<div class="page">
  <header class="masthead">
    <a class="eyebrow" href="/"><span class="arrow">←</span> Infra Atlas</a>
    <h1 class="title">The <em>Decisions.</em></h1>
    <p class="subtitle">Short, neutral, footnoted answers to the "which one should I use" questions cloud engineers ask most. One screen each — a plain verdict, a sourced comparison, and when to pick which.</p>
    <div class="reviewed"><span class="dot"></span>{n} decisions · reviewed <time datetime="{REVIEWED}">{REVIEWED}</time></div>
  </header>
  <section>
    <div class="decision-grid">
{chr(10).join(cards)}
    </div>
  </section>
  <footer class="colophon">
    Every decision is a curated, dated snapshot — each verdict and comparison cell sourced to
    vendor documentation. Part of <a href="/">Infra Atlas</a>. Spot a stale fact?
    <a href="https://github.com/ineslino/infra-atlas/issues/new" target="_blank" rel="noopener">Open an issue</a>.
  </footer>
</div>
<script src="/nav.js" defer></script>
</body>
</html>
"""


def main():
    written = []
    hub = os.path.join(ROOT, "decisions", "index.html")
    with open(hub, "w", encoding="utf-8") as f:
        f.write(render_hub())
    written.append("decisions/index.html")
    for d in DECISIONS:
        out_dir = os.path.join(ROOT, "decisions", d["slug"])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(render_page(d))
        written.append(f"decisions/{d['slug']}/index.html")
    print(f"✓ generated {len(written)} pages:")
    for w in written:
        print("  " + w)


if __name__ == "__main__":
    main()
