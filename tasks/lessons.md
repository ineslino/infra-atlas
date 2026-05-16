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

## L7 — "34 vs 39 regions" was a definition mismatch, not a regression
**Mistake:** the 2026-05 review and the 2026-05 feature-review brief both treated "the site shows 34 AWS regions, AWS says 39" as a stale, uncorrected undercount and a P0 regression.
**Cause:** 34 and 39 measure different things. 34 = AWS *commercial* GA regions — verified exact against AWS's own docs, every code matching, nothing missing or phantom. 39 = AWS's all-partitions marketing headline (34 commercial + 2 GovCloud + 2 China + 1 European Sovereign Cloud). No written inclusion policy existed, so each reviewer applied a different mental model and a scope gap read as a data bug. The *real* drift was smaller and elsewhere — Azure carried a phantom `taiwannorth` (announced, not GA) and was missing `westcentralus`; OCI was missing `af-casablanca-1`; OVH was missing Mumbai — none of it visible from a headline count, only from a code-level set diff.
**Rule:** a count that disagrees with a vendor's marketing headline is a *scope-definition* question first and a staleness question second. Never declare a regression from a count alone — diff the actual code sets and check the documented inclusion policy. (L1 already predicted the silent-drift mechanism; the fix it called for — an accuracy gate — now exists.)
**Resolution (2026-05-16):** the inclusion policy is now written down in `docs/data-policy.md` and the Region Map shows **all partitions** — AWS 39, Azure 67, OCI 55 — each region labelled by scope (GovCloud / China / Sovereign). The point of the lesson is not which number was chosen but that it was an undocumented *choice*, not a bug.
**Quick check:** `python3 scripts/check_region_drift.py` diffs every region code against the dated, vendor-verified `regions/region-reference.json`; the inclusion rules are written down in `docs/data-policy.md`.
