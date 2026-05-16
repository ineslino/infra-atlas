# Adjacent Verticals — Research (2026-05)

**Task:** assess four verticals adjacent to Infra Atlas's current API-management /
infrastructure scope. For each: the landscape, the public reference data
available, and a recommendation — *in scope as an instrument* / *adjacent but a
separate publication* / *out of scope* — with reasoning.

**Editorial DNA the recommendation is tested against** (from `progress.md`,
`tasks/lessons.md`, `tasks/review-2026-05/feature-shortlist.md`):

- **Credential-free static site.** No backend, no live measurement, no
  authenticated API key. Anything needing RTT probes or a paid key is out.
- **Cited, public-doc data.** Every numeric/capability claim needs a vendor-doc
  source comment (`lessons.md` L3 — the site shipped invented APIM data once).
- **The matrix format** (`apim-matrix`, `iam-matrix`, `kubernetes`) — vendors ×
  capabilities, cells carry `level` + `note` + `src`, "the asterisks stay" when
  things are not 1:1.
- **Staleness is the systemic enemy** (`lessons.md` L1, L4). A vertical that
  rots weekly and has no credential-free refresh path is a liability, not an
  asset — it must support either a real refresh or honest "dated snapshot"
  framing.
- **Multi-vendor is non-negotiable**; the framing is "a reference for the
  infrastructure stack."

A note on date-stamped sources: several cited pages carry "2026" in their slugs
(third-party comparison blogs). They are used here only to characterise *the
existing reference landscape* — i.e. to show what comparison content already
exists and where it is thin. Every *capability or pricing claim* that would feed
an instrument is tied to a first-party vendor or foundation URL.

---

## 1. Service mesh comparators

### Landscape

The serious field is small and stable: **Istio**, **Linkerd**, **Cilium**
(service-mesh mode), **HashiCorp Consul** (Connect), plus **AWS App Mesh** as
the cloud-managed entry. Istio, Linkerd and Cilium are all CNCF **Graduated**
projects; Istio and Linkerd sit in CNCF's explicit "Service Mesh" category
([CNCF Projects](https://www.cncf.io/projects/)). Consul and the now-archived
Open Service Mesh / Kuma do not appear on the current CNCF graduated/incubating
list.

The architectural split is sharp and *comparable in a matrix*: Istio uses Envoy
sidecars (and now an "ambient" sidecarless mode); Linkerd uses a purpose-built
Rust micro-proxy; Cilium uses an eBPF kernel datapath with no per-pod proxy;
Consul Connect extends Consul service discovery to mesh and spans VMs +
Kubernetes
([service mesh comparison, oneuptime](https://oneuptime.com/blog/post/2026-02-20-kubernetes-service-mesh-comparison/view)).

The space is in active motion in a way that matters for a reference site.
**Istio ambient mode reached GA in 2025**; at KubeCon EU 2026 Istio announced
ambient multicluster beta and a Gateway API Inference Extension
([CNCF announcement, Mar 2026](https://www.cncf.io/announcements/2026/03/25/istio-brings-future-ready-service-mesh-to-the-ai-era-with-new-ambient-multicluster-gateway-api-inference-extension-and-more/)).
Cilium reported 5,000+ production deployments by late 2025 and is now
Gateway-API-compatible
([Kubernetes Gateway API in 2026, dev.to](https://dev.to/mechcloud_academy/kubernetes-gateway-api-in-2026-the-definitive-guide-to-envoy-gateway-istio-cilium-and-kong-2bkl)).
The "sidecar vs sidecarless" question is the live debate of the moment.

### Reference content that already exists, and its gaps

There is a **glut** of "Istio vs Linkerd vs Consul" comparison content — Tetrate,
oneuptime, mkdev, and a long tail of SEO blogs all publish one
([Tetrate](https://tetrate.io/blog/istio-vs-linkerd-vs-consul);
[mkdev](https://mkdev.me/posts/the-best-service-mesh-linkerd-vs-kuma-vs-istio-vs-consul-connect-comparison-cilium-and-osm-on-top)).
Gaps in that content: (a) almost all are prose, not a structured matrix with
per-cell sourcing; (b) most are 3-way (Istio/Linkerd/Consul) and **omit Cilium's
mesh mode and AWS App Mesh**; (c) performance numbers are quoted without
reproducible methodology; (d) they are not cross-referenced to a Kubernetes or
IAM reference — exactly the cross-linking Infra Atlas already does well. So a
*matrix* treatment is genuinely under-served even though *prose comparisons* are
saturated.

### Public data available

Strong. Capability data — mTLS model, proxy architecture, multi-cluster, VM
support, Gateway API conformance, observability stack, CNI integration — is all
documented in first-party project docs and the CNCF landscape, and is
**structurally identical to what the `kubernetes` instrument already captures**.
The two soft spots: (a) **performance/latency numbers cannot be cited
credibly** — they vary by config and the site has no measurement rig, so any
matrix must exclude them or mark them clearly as "see vendor benchmark"; (b)
ambient-mode churn means a snapshot dates within a release cycle.

### Recommendation — **IN SCOPE, as an instrument** (high confidence)

A **Service Mesh Atlas** is the cleanest fit of the four. It is the same matrix
shape as `kubernetes`, draws purely on public project docs (credential-free),
covers exactly 5 vendors (Istio/Linkerd/Cilium/Consul/App Mesh — multi-vendor
satisfied), and is a *natural cross-reference* from the existing Kubernetes
Atlas — managed K8s and the mesh layered on top are the same buyer's adjacent
question. It sits squarely inside the "infrastructure stack" framing: a mesh is
infrastructure, not an application concern.

Caveats to bake into the spec: (1) **exclude latency/throughput numbers** or
quarantine them behind an explicit "vendor-reported, not verified" label — the
site has no way to cite them honestly (`lessons.md` L3); (2) treat
ambient/sidecarless as a first-class column and **date-stamp the snapshot**, per
the L4 "hard-claim rot" rule, because this space moves every release.

---

## 2. Event streaming & messaging brokers

### Landscape

Two overlapping categories that buyers conflate: **streaming logs** (Kafka,
Pulsar, AWS Kinesis & MSK, Azure Event Hubs, GCP Pub/Sub) and **traditional
brokers** (RabbitMQ, plus NATS as a modern entrant). Architecturally they are
*comparable but not 1:1*: Kafka is a partitioned commit log; Pulsar separates
serving (brokers) from storage (BookKeeper); RabbitMQ is a lightweight
queue/routing broker holding messages short-term
([ByteByteGo, RabbitMQ vs Kafka vs Pulsar](https://blog.bytebytego.com/p/ep203-rabbitmq-vs-kafka-vs-pulsar);
[Confluent, Kafka vs Pulsar](https://www.confluent.io/kafka-vs-pulsar/)).

The managed-cloud layer is where Infra Atlas's multi-cloud DNA bites: AWS MSK
(real Kafka), AWS Kinesis (shard-based, Kafka-incompatible), Azure Event Hubs
(Kafka-protocol-compatible ingestion), GCP Pub/Sub (serverless, partition
abstracted)
([Kafka vs Kinesis vs Pub/Sub, datavidhya](https://datavidhya.com/blog/kafka-vs-kinesis-vs-pubsub/)).
On the CNCF side only **NATS** and **Strimzi** appear (both Incubating) and
**CloudEvents** is Graduated ([CNCF Projects](https://www.cncf.io/projects/)) —
Kafka and Pulsar are Apache Software Foundation, not CNCF.

The space is moving: Kafka shed ZooKeeper for KRaft, and **KIP-1150 "Diskless
Topics"** — object-storage-backed topics claiming up to 80% TCO reduction —
was accepted into Apache Kafka on 2 March 2026
([KIP-1150, Apache wiki](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1150:+Diskless+Topics)).

### Reference content that already exists, and its gaps

The "Kafka vs Pulsar vs RabbitMQ" comparison is **one of the most-written
articles on the infrastructure internet** — Confluent, ByteByteGo, Memgraph,
Redpanda, Tinybird and dozens more
([Confluent benchmark](https://www.confluent.io/blog/kafka-fastest-messaging-system/);
[Redpanda, Kafka alternatives](https://www.redpanda.com/guides/kafka-alternatives)).
Crucially, **much of the best content is vendor-published** (Confluent,
Redpanda, Memgraph) and therefore not neutral — a genuine gap an editorial,
vendor-independent reference could fill. The second real gap: almost nobody puts
the **self-hosted brokers and the four managed cloud services in one matrix** —
the cloud-managed comparison ("MSK vs Kinesis vs Event Hubs vs Pub/Sub") and the
OSS comparison are nearly always separate articles. That unified view is exactly
what Infra Atlas is shaped to do.

### Public data available

Mixed. *Capability* data (delivery semantics, ordering, retention model, replay,
protocol compatibility, stream processing, multi-tenancy) is well documented and
matrix-able. *Pricing* is the problem: the managed services price on
**incompatible axes** — Kinesis per shard-hour, MSK per broker-hour, Event Hubs
per throughput unit, Pub/Sub per GiB
([Pub/Sub pricing, GCP](https://cloud.google.com/pubsub/pricing)). The 2026
review already flagged that Infra Atlas's *existing* pricing pipeline is shaky
(`tasks/review-2026-05/feature-shortlist.md` rejected the egress-cost comparator
for this reason). A capability matrix is safe; a pricing matrix is a known trap.

### Recommendation — **ADJACENT — instrument only as a capability matrix, defer pricing** (medium-high confidence)

A **Streaming & Messaging Atlas** *does* fit the editorial DNA — it is
infrastructure, it is multi-vendor, and the unified OSS-plus-managed view is a
real gap. It is a legitimate instrument. **But scope it as a capability/semantics
matrix only** and explicitly exclude per-unit pricing, mirroring the shortlist's
own decision on egress cost. The streaming-vs-queue distinction also needs an
honest editorial split (the matrix should not pretend RabbitMQ and Kafka answer
the same question) — the APIM matrix's footnote discipline handles this.

Net: build it *after* the higher-fit Service Mesh Atlas, and only the
capability half. It is an instrument, not a separate publication — the "stack"
framing comfortably contains a broker layer.

---

## 3. Identity providers / CIAM

### Landscape

The vertical splits into **workforce IAM** (cloud-native, *already* covered by
Infra Atlas's `iam-matrix`: AWS/Azure/GCP/OCI identity) and **CIAM** —
customer-facing identity: **Auth0** (now Okta-owned), **Okta** Customer
Identity, **AWS Cognito**, **Microsoft Entra External ID** (the rebranded
successor to Azure AD B2C), **Keycloak** (Red Hat, open source), **Firebase
Auth** / Firebase Authentication with Identity Platform (Google)
([Descope, CIAM solutions](https://www.descope.com/blog/post/ciam-solutions);
[miniOrange, CIAM vendors 2026](https://www.miniorange.com/blog/ciam-vendors/)).

This is a **large, crowded, analyst-covered** market: the 2025 Gartner Magic
Quadrant for Access Management named Ping, Microsoft, Okta, ForgeRock and IBM as
Leaders
([Microsoft Security blog, Nov 2025](https://www.microsoft.com/en-us/security/blog/2025/11/21/microsoft-named-a-leader-in-the-gartner-magic-quadrant-for-access-management-for-the-ninth-consecutive-year/)) —
note that field (Ping/ForgeRock/IBM) only partially overlaps the
cloud-infrastructure vendors Infra Atlas otherwise tracks.

### Reference content that already exists, and its gaps

CIAM comparison content is **abundant and intensely commercial** — Descope,
miniOrange, Infisign, LoginRadius, CloudEagle and a dozen others all publish
"top CIAM vendors" lists, and the bulk are SEO pieces by *competing CIAM
vendors* steering toward their own product
([guptadeepak CIAM directory](https://guptadeepak.com/comprehensive-ciam-providers-directory-top-identity-authentication-solutions/);
[Infisign, Keycloak alternatives](https://www.infisign.ai/blog/best-keycloak-alternatives-competitors)).
A neutral matrix would have *some* editorial value over that. **But** the
authoritative reference layer already exists in the form of the Gartner MQ and
the IETF/FIDO standards themselves — and the CIAM market is far less
"infrastructure" and far more "application/product."

### Public data available

Adequate but uneven. Protocol support (OAuth2, OIDC, SAML, SCIM, WebAuthn /
passkeys) is documented per vendor
([login protocols, Medium](https://medium.com/h7w/understanding-login-protocols-oidc-oauth2-saml-and-webauthn-c1f1b733f3f7)).
**Free-tier / MAU pricing is unusually well documented and citable** — Auth0
free to 7,500 MAU then paid from $35/mo, Cognito 10,000 MAU under the AWS Free
Tier, Entra External ID 50,000 MAU free, Okta has no forever-free tier, Keycloak
has no per-MAU charge
([Auth0 pricing](https://auth0.com/pricing);
[Okta pricing](https://www.okta.com/pricing/)). The catch: feature parity is
*nuanced and plan-gated* (Auth0 charges extra for SAML on lower tiers
[Frontegg, Auth0 SAML](https://frontegg.com/guides/auth0-saml)), so a matrix
risks the same "forced-equivalence" + plan-asterisk problem the IAM matrix
already wrestles with.

### Recommendation — **ADJACENT-BUT-SEPARATE — out of scope as an instrument now** (medium confidence)

CIAM is the **weakest fit** of the four for the *current* publication. Reasons:
(1) **Editorial-DNA drift** — CIAM is an *application/product* layer (login UX,
user databases, consent), not the cloud-infrastructure substrate the other 16
instruments occupy; the "infrastructure stack" framing stretches thin here.
(2) **Vendor-set divergence** — the leaders (Ping, ForgeRock, IBM, Auth0) are
largely *not* the hyperscalers Infra Atlas tracks, so it would not cross-link to
the existing region/compute/IAM instruments. (3) The market is *already*
saturated with comparison content and an authoritative analyst quadrant; the
"tired of grepping docs" origin pain is weaker here than for, say, service mesh.

There **is** one narrow, high-fit move: the existing **`iam-matrix` is
workforce-IAM only**. Adding a **workload-identity / federation row-set** there
(OIDC federation, workload identity federation, short-lived credentials across
AWS/Azure/GCP/OCI) stays inside the infrastructure DNA and deepens an instrument
that already exists — far better than a new CIAM instrument. Full CIAM, if ever
pursued, belongs in a *separate* identity-focused publication, not Infra Atlas.

---

## 4. Secrets management

### Landscape

A focused field: **HashiCorp Vault** (self-managed / HCP managed, the
feature-depth leader — dynamic secrets, PKI, encryption-as-a-service, SSH CA),
**AWS Secrets Manager**, **Azure Key Vault** (secrets + keys + certs + Managed
HSM), **GCP Secret Manager**, and **Infisical** (open-source, developer-focused)
([guptadeepak, secrets tools 2026](https://guptadeepak.com/top-5-secrets-management-tools-hashicorp-vault-aws-doppler-infisical-and-azure-key-vault-compared/);
[Infisical, AWS SM vs Vault](https://infisical.com/blog/aws-secrets-manager-vs-hashicorp-vault)).

A clean, comparable axis exists — **true dynamic secrets** (Vault) vs
**rotation-based** (AWS Secrets Manager, Azure Key Vault) — and a clear
self-hosted-vs-managed split, exactly the kind of distinction the matrix format
with footnotes handles well.

One licensing fact materially affects the editorial story: HashiCorp moved Vault
from MPL 2.0 to the **Business Source License (BSL 1.1)** in 2023; the community
fork **OpenBao** (Vault 1.14, MPL 2.0, now under the Linux Foundation, v2.5.0
released Feb 2026) is now a real sixth option
([OpenBao](https://openbao.org/);
[The New Stack, OpenBao](https://thenewstack.io/meet-openbao-an-open-source-fork-of-hashicorp-vault/)).
An editorial reference can document the BSL/MPL split factually — that *is* the
kind of asterisk the site is good at.

### Reference content that already exists, and its gaps

"Vault vs AWS Secrets Manager vs Azure Key Vault" is well-covered (Infisical,
DevOps Daily, qcecuring, sanj.dev) — but, as with streaming, **a large share is
vendor-published** (Infisical's own blog is a top result)
([DevOps Daily, Vault vs AWS SM](https://devops-daily.com/comparisons/vault-vs-aws-secrets-manager)).
Gaps: (a) comparisons rarely include GCP Secret Manager *and* OpenBao together;
(b) the BSL-license dimension is usually a footnote, not a tracked column;
(c) no comparison cross-references the *cloud regions / compliance* surface the
way Infra Atlas could (e.g. Managed HSM availability per region).

### Public data available

Good for capabilities — auth methods, dynamic-secret support, PKI/encryption,
HSM backing, replication — all in first-party docs. Pricing is **more tractable
here than for streaming**: the cloud services price on broadly similar axes
(GCP Secret Manager $0.06 per active secret version/month + free tier; AWS
Secrets Manager per-secret + per-10k-API-calls; Azure Key Vault per-operation)
([GCP Secret Manager pricing](https://cloud.google.com/secret-manager/pricing);
[AWS Secrets Manager pricing](https://aws.amazon.com/secrets-manager/pricing/)).
A "$/secret/month + $/10k ops" normalisation is feasible and citable — *more*
defensible than the streaming pricing matrix.

### Recommendation — **IN SCOPE, as an instrument** (medium-high confidence)

A **Secrets Management Atlas** fits. It is infrastructure (it sits beside IAM
and Kubernetes in the platform layer), it is genuinely multi-vendor (5–6
vendors: Vault/OpenBao/AWS SM/Azure KV/GCP SM/Infisical), the
dynamic-vs-rotation and self-hosted-vs-managed axes are clean matrix columns,
and it is a **natural cross-reference from the existing `iam-matrix`** — "how do
I authenticate" and "where do my secrets live" are the same platform engineer's
adjacent questions.

It also plays to a site strength: the **Vault BSL-vs-MPL / OpenBao licensing
split** is precisely the kind of nuance Infra Atlas's footnote-heavy format
exists to capture, and which the SEO competition glosses over.

Sequence it *after* the Service Mesh Atlas: slightly smaller audience, and the
pricing column — though more tractable than streaming — should still be added
cautiously given the review's standing warning about the pricing pipeline.
Capability matrix first; pricing as a clearly-dated second pass.

---

## Recommendations summary

| Vertical | Verdict | Fit with "infrastructure stack" DNA | Public data quality | Existing-reference gap | Build sequence |
|---|---|---|---|---|---|
| **Service mesh** (Istio / Linkerd / Cilium / Consul / App Mesh) | **In scope — instrument** | Strong — same layer as the K8s Atlas; a mesh is infrastructure | Strong for capabilities; **exclude latency numbers** (no rig to cite them) | Prose comparisons saturated, but **no neutral structured matrix incl. Cilium + App Mesh** | **1st** — cleanest fit, reuses `kubernetes` matrix shape |
| **Event streaming & messaging** (Kafka / Pulsar / Kinesis / MSK / Event Hubs / Pub/Sub / RabbitMQ) | **Adjacent — instrument, capability-only; defer pricing** | Good — broker layer fits the stack | Capabilities good; **pricing axes incompatible** — known trap (cf. egress comparator rejection) | Unified OSS-plus-managed matrix is genuinely missing; most rivals are vendor-published | **2nd** — capability matrix only |
| **Identity / CIAM** (Auth0 / Okta / Cognito / Entra External ID / Keycloak / Firebase) | **Out of scope as instrument; adjacent-but-separate** | **Weak** — CIAM is an app/product layer; leaders aren't the hyperscalers | Protocols + MAU pricing citable; feature parity plan-gated and nuanced | Saturated + Gartner MQ already authoritative | **Not now** — instead extend `iam-matrix` with workload-identity/federation rows |
| **Secrets management** (Vault / OpenBao / AWS SM / Azure Key Vault / GCP SM / Infisical) | **In scope — instrument** | Strong — sits beside IAM in the platform layer | Capabilities good; pricing tractable (`$/secret/mo` normalises) — more defensible than streaming | GCP SM + OpenBao rarely in one matrix; BSL-license angle under-tracked | **3rd** — capability matrix first, dated pricing pass second |

**One-line synthesis:** Service mesh and secrets management are true Infra Atlas
instruments — same matrix shape, public-doc data, infrastructure-layer, natural
cross-links to the Kubernetes and IAM atlases. Event streaming fits too but only
as a capability matrix (its pricing is the same volatility trap the egress
comparator was rejected for). CIAM is the outlier: an application-layer market
whose leaders aren't the hyperscalers — best served by *deepening the existing
IAM matrix* with workload-identity rows rather than adding a new instrument.
