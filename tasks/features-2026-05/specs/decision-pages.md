# Spec — "X vs Y" Decision Pages (candidate E1)

Buildable spec. Implementer should not need a second briefing.

## Goal

Ship a small, fixed set of short, neutral, footnoted "which one / what's the
difference" reference pages for the comparisons engineers ask most. Each answers
one decision in one screen: a plain verdict, a comparison table, "when to use
which", and footnoted sources.

## Non-goals

- Not an infinite listicle — a *fixed* set, gated by evidence (below).
- Not opinion essays — a verdict + a table, every claim sourced.
- Not a calculator, not interactive estimation (see `anti-list.md`).
- Not vendor-vs-vendor marketing ("AWS vs Azure" in general — too broad).

## Inclusion rule

A decision page qualifies **only if** a top-voted Stack Overflow question (or
equivalent cross-source signal) maps to it. Launch set (8, all evidenced in
`research/user-intent.md`):

1. App Engine vs Compute Engine (GCE SO #1, 547▲)
2. Fargate vs EC2 — and ECS-on-EC2 (r/aws 69▲)
3. API Gateway vs reverse proxy vs load balancer (r/devops 156▲; SO 80k views)
4. REST API vs HTTP API (AWS API Gateway) (SO "Regional vs Edge" 46k views)
5. Cloud Run vs App Engine Flex (SO 81▲)
6. Aurora vs RDS
7. Azure web role vs worker role vs VM (SO 119▲) — or its modern successor
8. NAT Gateway vs NAT instance vs no-NAT (ties to the egress map, N1)

## Data model & source

No `data.json`, no pipeline — **pure editorial static HTML**, the same class as
the APIM guide pages (`apigee/`, `mulesoft/`).

```
decisions/
  index.html          hub — lists all decision pages, grouped
  <slug>/index.html    one page per decision (e.g. decisions/fargate-vs-ec2/)
```

Each page is hand-authored. Every comparison-table cell and verdict claim carries
an HTML source comment with the vendor-doc URL (the `lessons.md` L3 rule). Each
page has a visible `reviewed: YYYY-MM-DD` date.

## UI sketch

**Hub (`decisions/index.html`):** masthead "The Decisions." + a list of cards,
each = the question + a one-line verdict teaser + reviewed date. Same design
tokens / `nav.js` as every instrument.

**Decision page:** masthead with the question as the title ("Fargate *or* EC2?").
Then, top to bottom:
- **Verdict box** — 2–3 sentences, the accent-bordered card style already used
  on the cross-cloud matrices' intro.
- **Comparison table** — the two (or three) options as columns, ~8–12 decision
  criteria as rows; cells are short with footnote markers.
- **"Pick X when… / Pick Y when…"** — two short bullet lists.
- **Footnotes** — numbered, each a vendor-doc link.
- **Cross-links** — to the relevant instrument(s) (Fargate-vs-EC2 → EC2
  Observatory + Equivalent-SKU; API-Gateway page → APIM Feature Matrix).
- Footer `reviewed:` date.

## Filter / cross-reference behaviour

No filters (each page is a single decision). Cross-references: every decision
page links to the instrument(s) it touches; the relevant instruments link back
(e.g. EC2 Observatory → "Fargate vs EC2?"). The hub is registered in `nav.js` and
the ⌘K palette as its own group ("Decisions").

## Edge cases & empty/error states

- **A decision goes obsolete** (a product deprecated, e.g. App Engine sunset):
  the page gets a `superseded` banner rather than silent deletion; the hub marks it.
- **A "reviewed" date older than 12 months**: surfaced by the freshness guard
  (extend `verify-freshness.yml` to cover `decisions/*`).
- No data → no empty state needed (static prose).

## Verification strategy

- Every table cell / verdict claim has a source-URL comment — checked in review.
- `reviewed` date present on every page — add `decisions/` to the
  `verify-freshness.yml` instrument list (the `<time datetime>` pattern).
- Manual: each page renders, `nav.js` + ⌘K list it, cross-links resolve.

## Docs to update on launch

- `nav.js` — register the "Decisions" group + each page.
- `index.html` — a landing-page section or department for Decisions; bump the
  instrument/section count.
- `CONTRIBUTING.md` — how to add a decision page (the inclusion rule).
- `verify-freshness.yml` — add `decisions/*` to the snapshot-date check.

## Rollback plan

Pure static pages, no data pipeline. Rollback = delete `decisions/`, remove the
`nav.js` group and the landing-page section. No other instrument depends on it.
