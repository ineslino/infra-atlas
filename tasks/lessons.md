# Lessons — recurring patterns

Cross-cutting patterns found during the 2026-05 full review. These are *systemic* — fixing one instance won't fix the class.

## L1 — Data staleness is systemic, not incidental
Stale or wrong data appeared in **every data instrument audited**: EC2 (Melbourne availability ~2× wrong), GCP (C4A 6 regions vs 27), Azure (confidential line a generation behind), OVH (Instance Catalogue missing Paris).
**Root cause:** the daily `refresh.yml` keeps the `generated` *timestamp* fresh but performs **no upstream-accuracy validation** — and the curated instruments (`gcp-compute`, `regions`) have no live source at all, so they drift silently until someone hand-edits `index.html`.
**Class fix:** the refresh pipeline needs an accuracy gate (diff against an authoritative upstream list and fail/flag), not just a re-extraction; and "curated" instruments need an explicit staleness budget.

## L2 — The `vendor` field is mislabeled on GPU shapes (3×, 2 instruments)
Azure `NDv4` tagged Intel (host is AMD); OCI `BM.GPU.B200.8` and `BM.GPU.H100.8` tagged AMD (hosts are Intel). The `vendor` field denotes the *host CPU* and drives the Intel/AMD filter facet.
**Pattern:** when a GPU shape is added, the host-CPU vendor is an afterthought and gets guessed.
**Class fix:** for any accelerated shape, verify host CPU against the vendor's compute-shapes doc — it is not inferable from the GPU.

## L3 — The site's own data violates its "no first-principles" standard
Apigee's "Enterprise Plus Plus" tier and calls/day pricing model, and AWS's "$1.51 above 20B" pricing, **exist in no vendor document** — they are invented. The site demands cited accuracy of itself in tone but doesn't enforce it.
**Class fix:** every numeric/tier claim on the static APIM pages needs a source comment in the markup, or it shouldn't ship.

## L4 — "Hard limit" gotchas are captured once, never re-checked
The AWS REST API "29-second hard timeout" was true when written, became an adjustable soft quota in June 2024, and is now ~2 years stale — on a page that markets itself on precise footnotes.
**Class fix:** capability claims that include words like "hard", "cannot", "only", "never" are the highest-rot risk — they need a dated last-verified marker.

## L5 — Shared data duplicated across files, diverged
OVH regions live in both `regions/index.html` (has Paris) and `ovh-instances/index.html` (missing Paris). Two copies, one source of truth absent.
**Class fix:** shared reference data (region lists especially) should have one canonical file the others derive from.

## L6 — Claim vs reality gaps
"Every instrument refreshes daily" (APIM pages are static); "open / MIT-licensed on GitHub" with dead `href="#"` links (repo is private); "1,338 instance types" (counts size-variants, not AWS's "types" metric).
**Class fix:** audit every headline/colophon claim against what the code and infra actually do — claims rot faster than data.
