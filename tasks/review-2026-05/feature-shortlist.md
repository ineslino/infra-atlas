# Infra Atlas — Feature shortlist · 2026-05-16

Constraint: must fit the "cross-referenced reference periodical" concept — not a dashboard, not a SaaS, not a SIEM.

## Candidates considered (12)

Equivalent-SKU finder · Kubernetes flavor atlas · Compliance footprint per region · Confidential-computing atlas · IAM/identity matrix · Service-quota atlas · Egress cost comparator · Region latency matrix · Carbon intensity per region · APIM migration path generator · API-gateway pricing simulator · Reserved/Savings/CUD comparator.

**Rejected / deferred:** *Region latency matrix* — needs live RTT measurement infrastructure; incompatible with a credential-free static site. *Carbon intensity* — Electricity Maps API requires an authenticated key; breaks the credential-free model. *API-gateway pricing simulator* — "simulator" drifts toward a tool, not a reference; and the audit showed APIM pricing data is currently unreliable, so build the data integrity first. *Egress cost comparator* — high value but pricing data is volatile and the existing pricing pipeline is already shaky; revisit after Axis-3 fixes land.

## Top 5

### 1. Equivalent-SKU finder
- **Value:** give an EC2 instance type, get the closest Azure / GCP / OCI / OVH match — the single most-asked multi-cloud question.
- **Data source:** none new — the site *already* curates all five instance catalogues; this is a matching/scoring layer over existing data (vCPU, memory, arch, category).
- **Biggest risk:** "closest" is subjective — needs a transparent, documented scoring rubric so it reads as reference, not a black box.
- **Effort:** **M**

### 2. Kubernetes flavor atlas
- **Value:** EKS / AKS / GKE / OKE / OVH Managed K8s compared — supported versions, control-plane SLA, node-pool capabilities, autoscaling limits. A natural 12th instrument.
- **Data source:** public vendor docs (version-support pages, SLA pages).
- **Biggest risk:** K8s version support moves fast — same staleness trap this review flagged; needs a refresh story or honest "snapshot" framing from day one.
- **Effort:** **M–L**

### 3. Compliance footprint per region
- **Value:** which regions carry FedRAMP / IRAP / C5 / ENS / ISO 27001 / HIPAA — a real blocker in regulated procurement, scattered across vendor PDFs today.
- **Data source:** public vendor compliance pages; layers directly onto the existing Region Map.
- **Biggest risk:** compliance scope is nuanced (service-level vs region-level); over-simplification could mislead — cell footnotes (like the APIM matrix) are essential.
- **Effort:** **M**

### 4. Confidential-computing atlas
- **Value:** SGX / SEV-SNP / TDX / Nitro Enclaves by vendor and region. The Azure audit showed this space is genuinely confusing and cross-referenced nowhere.
- **Data source:** public vendor confidential-computing docs.
- **Biggest risk:** small, fast-moving niche — low traffic, and the SGX/TDX/SEV distinctions must be exact (the audit already caught a gap here).
- **Effort:** **M**

### 5. IAM / identity matrix
- **Value:** hyperscaler identity models side by side — auth methods, federation, workload identity, policy languages, session limits. A second matrix instrument, same shape as the APIM Matrix.
- **Data source:** public IAM docs.
- **Biggest risk:** IAM models are deep and not 1:1 comparable — risk of forced-equivalence; the matrix format's footnotes mitigate this.
- **Effort:** **M**

**Ranking rationale:** #1 ships fastest and highest-value because the data already exists in-repo. #2–#5 are all new instruments built from public docs, in descending order of audience size and ascending order of staleness risk. None requires credentials, a backend, or live measurement — all stay inside the static, credential-free model.
