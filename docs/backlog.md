# Infra Atlas — Backlog

Items from the 2026-05-21 UX + expansion audit. Ordered roughly by priority
within each section. "Not doing" section at the bottom explains what was
explicitly ruled out and why.

---

## Formats & Access

### MCP Server
**Priority: 1 — highest leverage per hour**

Expose the Atlas datasets as MCP tools for LLM-assisted workflows
(Claude Desktop, Cursor, any MCP-compatible agent).

Problem: LLMs answer infra questions with stale training data.
InfraAtlas has structured, daily-refreshed JSON — the exact thing
that makes an MCP server useful.

Minimum useful tools:
- `get_compute_instances(cloud, region?, arch?, min_vcpu?, min_memory_gb?)`
- `find_equivalent_sku(source_cloud, sku_name)`
- `get_egress_cost(source_cloud, destination_cloud, gb?)`
- `get_regions(cloud)`

Stack: Python MCP SDK, wraps the public `data.json` endpoints.
No API key needed for consumers — they use their own LLM.

Effort: S–M  
Criterion: `claude "cheapest arm64 in eu-west-1 with 16GB across AWS and GCP"`
returns answer with data from last 24h.

---

### CLI (`infraatlas` command)
**Priority: 2**

Terminal workflow without opening a browser. The ICP lives in terminal.

Cases:
- `infraatlas ec2 --region eu-west-1 --arch arm64 --min-memory 16`
- `infraatlas equivalent m5.xlarge`
- `infraatlas egress aws azure --gb 500`

Stack: Python (matches data pipeline), `pipx install infraatlas`.
Thin wrapper over public `data.json` with local cache.
Do NOT do brew or npm distribution initially — PyPI is enough.

Effort: S–M  
Criterion: core queries work in < 2s against the public data.json API.

---

### Per-instrument feeds
**Priority: 3 — quick win once feed pipeline is stable**

Today `feed.json` is a single aggregate of all instrument changes.
Adding per-instrument feeds (`/ec2/feed.json`, `/regions/feed.json`, …)
lets engineers subscribe to only the cloud/instrument they care about.

Implementation: extend `diff_feed.py` to write to both `feed.json`
(aggregate, already done) and `{instrument}/feed.json` (per-instrument).
Or a post-processing step that splits `feed.json` by instrument.

Effort: S  
Criterion: `/ec2/feed.json` has entries from the last 24h after each
daily refresh run.

---

### Embed mode (filtered matrix view)
**Priority: low — do after deep-links are stable**

An `?view=embed&filter=AWS,GCP` query string that renders a stripped-down
version of the matrix (no nav, no footer, suitable for iframe in blog posts).

Dependency: filter deep-link must be robust and URL structure must be
considered stable before external sites start embedding.

Effort: M  
Risk: URL structure changes break every embed. Needs versioned URL or
commitment to never change paths.

---

## Content — New Instruments

### Serverless / Functions limits
**Priority: 1**

Lambda, Cloud Functions (Gen1/Gen2), Azure Functions (Consumption/Premium),
Cloud Run (2nd gen), OCI Functions.

Dimensions that bite in prod: max timeout, max memory, max concurrency,
deployment package size, cold start behaviour, VPC access, pricing per
invocation + per GB-second.

Data: static (vendor docs, changes on product announcements).
Update cadence: manual, ~quarterly or on announcement.

Effort: M  
Criterion: searching "lambda timeout" in ⌘K returns this instrument.

---

### Storage class pricing cross-cloud
**Priority: 2**

S3 / Azure Blob / GCS / OCI Object Storage / OVH Object Storage.

The hidden asterisk: retrieval costs. GCS Archive retrieval costs per GB,
Glacier Deep Archive has 12h lead time. Nobody publishes this neutral.

Dimensions: $/GB stored per tier, $/GB retrieved, $/10k operations,
minimum storage duration, retrieval latency.

Data: semi-static (vendor pricing pages). Needs monitoring for price changes.

Effort: M–L (scraping per-operation pricing is more complex than compute)  
Criterion: answers "what is the retrieval cost for 1TB from Glacier vs Azure
Archive?" without going to vendor docs.

---

### Service quotas / limits
**Priority: 3**

Default service quotas that platform engineers hit during scaling:
EC2 vCPU limits per region per family, Lambda concurrent executions,
GCS bucket limits, Azure subscription vCPU limits, OCI compute limits.

Data: semi-static (quota defaults change with product announcements).
The site's manifesto already alludes to this.

Effort: M  
Criterion: searching "ec2 vcpu limit" in ⌘K returns this instrument.

---

### GPU availability cross-cloud (extension, not new instrument)
**Priority: medium — extends existing compute instruments**

Not a separate instrument — a filter/highlight within EC2 Observatory,
Azure VM Atlas, GCP Compute Index, OCI Compute Observatory.

Add a "GPU" family filter and a GPU-type / VRAM column to the instance
comparison modal in each compute instrument.

Data: already in `data.json` (GPU families exist, e.g. p4d, NC, A100 shapes).
Work: plumb GPU metadata through the filter UI.

Effort: S–M  

---

## IA & Navigation

### Cross-link Decisions ↔ Instruments
**Priority: medium**

Today EC2 Observatory links to Azure VM, Equivalent-SKU, Regions (via
`RELATED` in nav.js) but NOT to "Fargate vs EC2" — the decision most
relevant to someone on that page.

Fix: extend `RELATED` in nav.js bidirectionally. Decision pages should
also show related instruments.

Files: `nav.js` (RELATED map), then each decision's index.html gets
the related instrument pills automatically.

Effort: S (< 1 day)  
Criterion: clicking through from EC2 Observatory shows Fargate vs EC2
in the Related strip.

---

### Split "Cross-Cloud" taxonomy
**Priority: when Cross-Cloud exceeds 10 instruments**

Current Cross-Cloud group is a catch-all. Proposed future split:

```
Cloud Compute        → EC2, Azure VM, GCP, OCI, OVH, Regions (~6–10)
Networking & Cost    → Egress, Networking Matrix, + future (~4–6)
Platform Services    → Kubernetes, Serverless/Functions (~3–5)
API Management       → unchanged (~5, stable)
Identity & Security  → IAM Matrix, Compliance, Confidential Computing (~3–5)
Cross-Cloud          → Equivalent-SKU, AI Atlas, + genuinely cross-cutting (~3–4)
```

Do NOT refactor until the group actually overflows (~10 items).
When done: update nav.js groups + pushGroup calls + landing page sections.

Effort: M (mechanical, but touches every RELATED entry)  

---

## Marketing / Community

### "State of Cloud Infra" annual report
**Priority: low — do once, high SEO value**

The daily snapshots already capture cloud evolution over time.
An annual report showing which regions opened, which instance families
were launched/retired, how egress prices evolved is a natural subproduct.

Format: static HTML page (no new infra) + shareable summary for
HN / r/devops / X.

Effort: M (one-time data analysis + static page)  
Criterion: published as `/reports/2026/` and earns inbound links.

---

### Instance right-sizing calculator
**Priority: low — depends on Equivalent-SKU density**

Given a current instance + utilisation %, suggest cheaper alternatives
on the same cloud or cross-cloud via Equivalent-SKU Finder data.

Prerequisite: Equivalent-SKU Finder should cover pricing data.
Current state: SKU matches are by spec, not price.

Effort: M  

---

## Won't do / explicitly ruled out

| Item | Reason |
|---|---|
| Spot / preemptible pricing | Data TTL is hours, not days. A daily snapshot is misleading. Vendor tools do this better with live data. |
| VS Code / browser extension | Bus factor 1 + two distribution surfaces with breaking-change cadence (VS Code API, Chrome ext manifest). ROI does not cover maintenance. |
| Email alerts with backend | Introduces backend, GDPR surface, list management. Per-instrument RSS feeds achieve the same result with zero backend. |
| TUI | The dataset has no "changing state to watch" — no justification over a well-built CLI. |
| Free tier comparison | Not the ICP (professional platform engineers don't optimise free tier). Changes as marketing tool. |
| Managed databases matrix | Too wide a scope (engine × version × cloud) for the value it adds over existing Decisions. Revisit if a specific gap becomes clear. |
| Load balancer / CDN matrix | Each cloud has multiple LB tiers (L4/L7, internal/external, global) — the matrix would be as complex as Networking Matrix to curate, for an unclear ICP need. |
