# Infra Atlas

[![Data refresh](https://github.com/ineslino/infra-atlas/actions/workflows/refresh.yml/badge.svg)](https://github.com/ineslino/infra-atlas/actions/workflows/refresh.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> A reference periodical of cloud and API-management infrastructure — sixteen
> instruments covering regions, instance types, API gateways and service
> quotas, cross-referenced and footnoted.

**Live · <https://infraatlas.dev>**

Infra Atlas is the cross-referenced almanac the vendor docs never wrote: every
region, instance type and API-gateway capability laid out side by side,
filterable, and kept honest because no vendor pays for its place. It is free to
read and vendor-neutral — built by independent engineers who got tired of
grepping vendor docs across five tabs.

The site is plain static HTML — no build step, no framework, no bundler. Each
"instrument" is a self-contained folder; the data-driven instruments refresh
daily from public sources, and no instrument needs a cloud account or an API
key.

## The instruments

Seventeen pages: an editorial landing index plus sixteen instruments, in three
departments.

### Cloud compute

| Instrument | Path | Data |
|------------|------|------|
| EC2 Observatory | `ec2/` | AWS EC2 instance types by region — live, ec2instances.info dataset |
| Region Map | `regions/` | Every GA region across all five clouds, all partitions — curated |
| Azure VM Atlas | `azure-vm/` | Azure VM sizes by region — live, Azure Retail Prices API |
| GCP Compute Index | `gcp-compute/` | GCP machine types by region — curated |
| OCI Compute Observatory | `oci-compute/` | Oracle Cloud compute shapes by region — live, Oracle price list |
| OVH Instance Catalogue | `ovh-instances/` | OVHcloud Public Cloud instances — live, OVH order catalogue |

### API management

| Instrument | Path | Data |
|------------|------|------|
| APIM Feature Matrix | `apim-matrix/` | Cross-vendor API-management feature comparison — dated snapshot |
| AWS API Gateway Atlas | `aws-api-gateway/` | AWS API Gateway reference — dated snapshot |
| Apigee Atlas | `apigee/` | Google Apigee reference — dated snapshot |
| Mulesoft Atlas | `mulesoft/` | MuleSoft Anypoint reference — dated snapshot |
| Kong · Gravitee · IBM | `self-hosted-apim/` | Self-hosted API gateways — dated snapshot |

### Cross-cloud matrices

| Instrument | Path | Data |
|------------|------|------|
| Equivalent-SKU Finder | `equivalent-sku/` | Instance/SKU equivalents across clouds — dated snapshot |
| Kubernetes Atlas | `kubernetes/` | Managed Kubernetes (EKS · AKS · GKE · OKE) compared — dated snapshot |
| Compliance Footprint | `compliance/` | Certifications by cloud and region — dated snapshot |
| Confidential Computing | `confidential-computing/` | Confidential-compute offerings compared — dated snapshot |
| IAM Matrix | `iam-matrix/` | Identity and access models compared — dated snapshot |

## How the data stays current

Three tiers, by design — the full policy is in
[`docs/data-policy.md`](docs/data-policy.md).

- **Live — refreshed daily.** `ec2`, `azure-vm`, `oci-compute` and
  `ovh-instances` each carry a `refresh.sh` that pulls a public API or dataset
  with no credentials. `.github/workflows/refresh.yml` runs them at 06:00 UTC
  and commits any change.
- **Curated.** `regions` and `gcp-compute` are hand-maintained — no
  credential-free price source exists for them. Their `refresh.sh` only
  re-serialises the data embedded in `index.html`.
- **Dated snapshots.** The API-management and cross-cloud instruments are static
  editorial pages, hand-verified against vendor docs and stamped with a visible
  snapshot date.

After each refresh, `scripts/diff_feed.py` records what changed into the shared
`feed.json` — the landing page's "What Changed" log.

**Guards (CI):**

- `verify-data.yml` — on every push/PR: checks each curated `data.json` still
  matches its `index.html`, pins the region set to the vendor-verified
  `regions/region-reference.json`, and checks the landing-page stat chips
  against the instruments' data.
- `verify-freshness.yml` — monthly: fails when a curated snapshot ages past 180
  days, a nudge to re-verify it against the vendor docs.

## Repo layout

```
infra-atlas/
├── index.html              The editorial landing index
├── nav.js                  Shared nav bar + ⌘K palette, injected into every page
├── feed.json               "What Changed" log, appended by the refresh workflow
├── 404.html  _headers  _ogcard.html  .assetsignore  favicon.svg  og.png
│
├── <instrument>/           One folder per instrument (16 total)
│   ├── index.html          Self-contained UI; source of truth for the embedded data
│   ├── data.json           Generated artifact — never hand-edited (data instruments only)
│   └── refresh.sh          Regenerates data.json (data instruments only)
│
├── docs/data-policy.md     What counts as a region, a source, "available"
├── scripts/                refresh + feed + verification helpers
└── .github/workflows/      refresh · verify-data · verify-freshness
```

## Local development

Plain static HTML — no build step. Serve it so `fetch('./data.json')` works:

```bash
python3 -m http.server 8080
# open http://localhost:8080
```

Opening `index.html` over `file://` works too — the embedded snapshot is the
fallback when `fetch` is blocked.

To regenerate an instrument's data locally:

```bash
./ec2/refresh.sh        # live instrument — pulls the public dataset
./regions/refresh.sh    # curated instrument — re-serialises the embedded data
```

Requires `curl`, `jq` and `python3` — nothing else.

## Deploy

Hosted on Cloudflare Pages, deploying on every push to `main`:

- Framework preset **None** · build command *(empty)* · output directory `/`.
- Custom domains `infraatlas.dev` + `www.infraatlas.dev`; the `www → apex`
  redirect is a Cloudflare Redirect Rule (the `_redirects` file cannot do
  cross-domain redirects).

`refresh.yml` needs only `contents: write` — no cloud account, no secrets.

## Contributing

The most valuable contribution is keeping the data right — a wrong region or a
stale limit is a bug. [`CONTRIBUTING.md`](CONTRIBUTING.md) explains how data is
sourced and edited; [`docs/data-policy.md`](docs/data-policy.md) defines what
counts as a region and an authoritative source. Spotted something off?
[Open an issue](https://github.com/ineslino/infra-atlas/issues/new) with the
upstream source that contradicts the site.

The site is intentionally one static file per page — no framework, no build
pipeline. Added complexity needs justification.

## License

[MIT](./LICENSE).

Infra Atlas is not affiliated with Amazon Web Services, Microsoft Azure, Google
Cloud, Oracle Cloud, OVHcloud, Apigee, MuleSoft, Kong, Gravitee, IBM, or any
other vendor referenced. All trademarks are the property of their respective
owners and are used here for factual reference only.
