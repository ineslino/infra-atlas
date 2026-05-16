# Phase 0c — Extended data audit

**Date:** 2026-05-16. Sample audit beyond regions, per the mission. Where a
claim could not be verified without cloud credentials, that is stated plainly
rather than guessed.

## Headline finding — the site disagrees with *itself*

Every instrument stores its own region list. They were never cross-checked, so
they have drifted apart. Same root cause as Phase 0b (no guard), now visible as
**instrument-to-instrument inconsistency**:

| Provider | `regions` map | compute instrument | upstream (Phase 0a) | Consistent? |
|----------|--------------|--------------------|--------------------|-------------|
| AWS   | 34 | `ec2` 34            | 34 | ✓ all agree |
| Azure | 56 | `azure-vm` 52       | 56 | ✗ map vs VM Atlas differ by 4 |
| GCP   | 43 | `gcp-compute` 42    | 43 | ✗ `gcp-compute` missing `asia-southeast3` (Bangkok) |
| OCI   | 44 | `oci-compute` 38   | 45 | ✗ three different numbers |
| OVH   | 14 | `ovh-instances` 15 | 15 | ✗ live catalogue has Mumbai; map doesn't |

Notes:
- **Azure 56 vs 52** — `azure-vm` is built from the Retail Prices API and lists
  only regions with VM pricing; the 4-region gap is mostly restricted DR-only
  regions. Defensible, but undocumented — looks like a bug to any reader.
- **OVH 14 / 15 / 15** — the `ovh-instances` *live OVH order catalogue* returns
  15 regions **including Mumbai (`MUM`)**. The hand-curated `regions` map has 14
  and is missing Mumbai. The site's own live data already knew. (OVH lists are
  themselves messy: `ovh-instances` carries `MAD` Madrid and no Toronto; the
  marketing availability page carries Toronto and no Madrid. OVH's region vs
  datacenter naming is inconsistent at source — see Phase 0a OVH notes.)
- **OCI 44 / 38 / 45** — `oci-compute` (live price list) returns only 38 regions
  (those with tracked compute shapes priced), so it is *not* a clean "all
  regions" source either. The `regions` map (44) is closest but missing
  `af-casablanca-1`.

## Landing-page stat cards are stale

The landing page (`index.html`) hard-codes per-instrument stat chips. They were
typed by hand and never re-derived, so they have drifted from the instruments'
own `data.json`:

| Card | Landing page says | Instrument `data.json` | Drift |
|------|-------------------|------------------------|-------|
| EC2 Observatory | `32 regions` · `~700 types` | 34 regions · **1338** instance types (196 families) | both stale; "~700" off by ~2× |
| Region Map | `~95 cities` · `~150 regions` | 88 cities · **191** regions | "~150" badly stale |
| GCP Compute Index | `41 regions` · `22 families` · `291 machine types` | 42 · 26 · 379 | all three stale |
| OVH Instance Catalogue | `14 datacenters` | `ovh-instances` 15 regions | stale by 1 |
| Azure VM Atlas | `52 regions` | `azure-vm` 52 | matches |
| OCI Compute Observatory | `38 regions` | `oci-compute` 38 | matches |

The EC2 card is the worst: `~700 types` vs an actual 1338 rows in the
instrument's own data, and `32 regions` while the EC2 instrument itself renders
34. The landing page contradicts the page it links to.

## EC2 instance-type count

`ec2/data.json` carries **1338 instance types across 196 family keys**. Whether
1338 is the "true" AWS number depends on the Vantage dataset's scope (it
includes legacy generations and every size); that is a separate question. The
auditable fact: **the landing page's "~700" does not match the instrument's own
data** — fix the card or compute it.

## Not verified (no credentials / needs a dedicated pass)

Per the mission's truthful-status rule, these were **not** confirmed and should
not be treated as audited:

- **AWS per-region instance-type counts** (`il-central-1`, `ap-southeast-5`,
  `mx-central-1`) — needs `describe-instance-type-offerings`; the audit machine
  has no AWS credentials. The site's per-region family membership comes from the
  Vantage dataset, which Phase 0a's `ec2/refresh.sh` already documents as
  inaccurate for newer regions (the `REGION_FAMILY_OVERRIDES` table pins
  Melbourne). Treat per-region EC2 family lists as **best-effort, not audited**.
- **Azure SGX / SEV-SNP confidential-VM SKU claims** — needs the confidential-VM
  SKU list per region; not checked. Candidate for the drift guard.
- **OCI B200 GPU shape GA status** — not verified against Oracle GA docs.
- **GPU availability per region, all vendors** — not audited; this is itself a
  strong candidate for a new instrument (carried to Phase 4).

## Drifts to fix in Phase 0d

1. `regions` map — Azure: remove phantom `taiwannorth`, add `westcentralus`.
2. `regions` map — OCI: add `af-casablanca-1`.
3. `regions` map — OVH: add Mumbai.
4. `gcp-compute` — add `asia-southeast3` (Bangkok). *(Lower priority — separate
   instrument; flag if not fixed in this pass.)*
5. Landing-page stat cards — de-hardcode or correct (EC2, Region Map, GCP, OVH).

## Drifts to flag (not a clean one-line fix)

- OVH Toronto vs Madrid — OVH's own surfaces disagree; needs a chosen
  authoritative OVH source before reconciling. Do not guess.
- Azure `regions` map (56) vs `azure-vm` (52) — decide whether the map should
  equal the full region set or the priced-VM set, then document it.
