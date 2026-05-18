# Instance detail enrichment + Generative AI Atlas — design

**Date:** 2026-05-18
**Origin:** user feedback after the 2026-05 cheap-wins batch review.

Two features:

1. Richer instance detail on the compute instruments.
2. A new comparison instrument for cloud AI platforms and the model families they host.

---

## 1 · Instance detail enrichment

**Problem.** A bare instance name (`m5.large`, `Standard_D4s_v5`) is vague — the
reader cannot tell what the machine is *for* or what hardware it carries.

**Constraint found.** The compute `data.json` feeds carry only `vcpu / mem /
price` per size. Storage, network and GPU are not present. Of the five compute
instruments only EC2 has a rich upstream feed (Vantage `instances.json`);
`azure-vm`, `gcp-compute` and `oci-compute` are hand-curated / derived in
`index.html` with no spec feed.

**Decision — "EC2 full + honest gaps".**

- **EC2 — Hardware section.** Extend `ec2/refresh.sh` to also extract from the
  Vantage feed: local storage (NVMe/SSD size & count, or "EBS-only"), network
  performance, GPU (count + model), physical processor + clock. These join
  `specs[size]`. The EC2 instance drawer gains a "Hardware" block beside the
  existing vCPU / Memory / Price. Fully automatic — re-verified every refresh.
- **Role clarity — all 5 instruments.** Surface the family description
  (currently drawer-only) as a hover tooltip (`title` attribute) on each
  instance list row, so a bare name always has a one-line "what it's for".
- **azure-vm / gcp-compute / oci-compute / ovh-instances.** No spec feed → no
  fabricated numbers. They keep category + description + vCPU + memory. OVH
  gets the Hardware section if its catalogue carries storage/bandwidth per
  flavour (confirm during build).

**Files.** `ec2/refresh.sh`, `ec2/index.html` (drawer), `ec2/data.json`
(regenerated); `{ec2,azure-vm,gcp-compute,oci-compute,ovh-instances}/index.html`
(row tooltip).

---

## 2 · Generative AI Atlas (new instrument)

**Goal.** Compare (a) the foundation-model families available on each cloud AI
platform and (b) the platforms' capabilities — accurate, sourced, never
silently stale.

**Why curated, not scraped.** Auto-refresh feasibility is uneven: only OVH AI
Endpoints exposes a clean credential-free JSON API; AWS/Azure/OCI publish
scrapable but restructure-prone HTML; GCP Vertex Model Garden has no clean
source at all. A daily five-site scraper would be brittle and could silently
publish wrong data — the opposite of the requirement. Model-*family*
availability and platform capabilities both rot slowly, so a curated, sourced
matrix with a freshness guard is the accurate and robust choice.

**Design.** A new Cross-Cloud instrument — a matrix on the existing engine
(Kubernetes Atlas shape: `VENDORS` / `CATEGORIES` / `FEATURES`, with
`level` + `value` + `note` + `src` per cell). Proposed slug `ai-atlas/`.

- **Platforms (columns, 5):** Amazon Bedrock · Azure AI Foundry · Vertex AI ·
  OCI Generative AI · OVHcloud AI Endpoints.
- **Categories (rows):**
  - *Model families* — Anthropic Claude, OpenAI GPT, Google Gemini, Meta Llama,
    Mistral, Cohere, Amazon Nova/Titan, xAI Grok, DeepSeek, … — each cell
    ✓/✗/◐ + a dated note of which models of that family are live there.
  - *Customisation* — fine-tuning, distillation.
  - *Retrieval & agents* — managed RAG / knowledge bases, agent runtime.
  - *Safety & governance* — guardrails, content filtering.
  - *Access & throughput* — serverless vs provisioned, OpenAI-compatible API.
- **Every cell sourced** to official vendor documentation (site standard).

**Freshness.** A visible "verified" date on the masthead + a CI guard that
fails the build once the verified date ages past a tight window (~30 days —
this topic moves fast). Optional v2: a "drift watch" CI job that diffs OVH's
live `/v1/models` API against the curated data and flags changes — automatic
*detection* without unsafe auto-publishing.

**Files.** New `ai-atlas/index.html`; `index.html` (landing-page card);
`nav.js` + ⌘K registration; the freshness workflow under `.github/workflows/`;
`docs/data-policy.md` (note the curated + guarded model).

---

## Build order

1. Design doc (this) — commit.
2. Instance detail enrichment — build, verify, commit.
3. Generative AI Atlas — build, verify, commit.
