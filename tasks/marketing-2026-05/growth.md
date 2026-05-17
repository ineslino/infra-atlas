# Phase 4 — Growth strategy

How a free, editorial, donation-funded reference site grows the *right* audience
without becoming a marketing operation.

**Reference class (held throughout).** The structural twins — crontab.guru,
regexr, pgexercises — grew on essentially **two channels: SEO + one good launch
post**, plus word-of-mouth links ([`research/comparable-projects.md`](research/comparable-projects.md)
§"crontab.guru/regexr/pgexercises", AVOID #6). This is not a venture-SaaS growth
plan; there is no funnel, no CAC, no paid acquisition. Infra Atlas gets
*discovered*, earns *trust*, and converts a fraction of grateful readers — see
[`donations.md`](donations.md) for the conversion half.

**Recommendation format.** Every item below carries:
`rationale · evidence · effort (S/M/L) · brand-fit (1–5) · expected impact`.
Impact is one of *audience growth* / *donations* / *both*.

---

## 4a · The growth model — three slow loops, no funnel

Growth for this project is three compounding loops, none of which is a campaign.

1. **Discovery loop.** SEO is the durable, compounding base (most reference-site
   twins are ~80% search/direct — [`research/comparable-projects.md`](research/comparable-projects.md)
   §caniuse, §crontab.guru); a *small* number of launch events and newsletter
   mentions are the spikes that seed it. The audit found SEO infrastructure
   entirely absent ([`audit.md`](audit.md) §1a) — so the base is not yet built.
2. **Trust loop.** Trust is the actual currency of a reference site, and it
   compounds slowly: Gergely Orosz built Pragmatic Engineer's credibility "over
   years of consistent, accurate, sourced writing"
   ([`research/comparable-projects.md`](research/comparable-projects.md)
   §pragmaticengineer). A visible methodology page, vendor neutrality, dated
   freshness stamps, and a named maintainer are the trust inputs.
3. **Citation loop.** Machine-readable data + an open licence + shareable URLs
   turn passive readers into integrators who cite and embed the data — and every
   citation is simultaneously a backlink (SEO) and a discovery surface. caniuse's
   data is embedded in millions of toolchains *because* it is openly licensed;
   ec2instances.info's JSON "gets hit hundreds of thousands of times per day"
   ([`research/comparable-projects.md`](research/comparable-projects.md)
   §Vantage, §caniuse).

The model's honest ceiling: a famous single-maintainer reference (caniuse)
converts a massive audience to ~540 patrons / ~€170/mo
([`research/donation-economics.md`](research/donation-economics.md) §1). Growth
is worth doing for *reach and usefulness*; it will not produce a salary. The
plan below is sized for a solo maintainer accordingly.

---

## 4b · Launch & re-launch moments — 3 in 6 months

A "periodical" implies periodicity. Three discrete, dated moments over six
months — each a genuine milestone, never a manufactured one. (HN is a
once-or-twice card; repeat submissions decay —
[`research/channels.md`](research/channels.md) §1.)

### Launch moment 1 — "The doors open" · ~Week 6

The first real launch, gated behind a precondition chain that **must** complete
first: repo public → donation surface live → SEO table-stakes shipped → README
refreshed (sequencing in [`plan-90d.md`](plan-90d.md)).

- **L1 · One carefully-timed Show HN, the same week as awesome-list PRs and
  newsletter submissions.** *Rationale:* a front-page HN slot is the single
  highest-leverage discovery event — tens of thousands of the exact primary
  persona in a day — and HN's dry, anti-marketing audience rewards the editorial
  voice rather than taxing it. Frame it as an *interactive, open-source tool*
  ("a vendor-neutral, filterable reference"), not "a site to read," and
  open-source the repo first to de-risk the "reading material" downgrade.
  *Evidence:* [`research/channels.md`](research/channels.md) §1;
  [Show HN guidelines](https://news.ycombinator.com/showhn.html).
  *Effort:* M (1h to post, 4–8h comment window) · *Brand-fit:* 5/5 ·
  *Impact:* both.

The same week, two zero-risk amplifiers (detail in §4e, §4f): submit one-line
PRs to the awesome-* lists, and email DevOps Weekly + Last Week in AWS. None of
these depend on the HN result; all three reinforce each other.

### Launch moment 2 — A flagship comparison essay · ~Week 11–12

The **ripgrep playbook**: a rigorous comparison artefact published *with a
writeup* is an HN-frontpage-able object in its own right, not a quiet page
([`research/comparable-projects.md`](research/comparable-projects.md) §ripgrep,
COPY #2).

- **L2 · Ship the APIM Feature Matrix as a launch, paired with a Field Notes
  essay** (e.g. "What five API gateways quietly disagree about"). Distribute via
  lobste.rs (if invited), one LinkedIn post for the APIM/enterprise-architect
  persona, and a Dev.to cross-post. This is **not** a second Show HN — HN is
  spent on L1; it is a community + secondary-persona moment. *Rationale:* the
  APIM matrix is exactly the rigorous, opinionated, link-worthy artefact the
  ripgrep benchmark post was; the enterprise-architect persona is only reachable
  on LinkedIn. *Evidence:* [`research/comparable-projects.md`](research/comparable-projects.md)
  COPY #2–3; [`research/channels.md`](research/channels.md) §3, §6;
  [`positioning.md`](positioning.md) §3a. *Effort:* M · *Brand-fit:* 5/5 ·
  *Impact:* both.

### Launch moment 3 — "Issue No. 02" + open-data release · ~Month 5–6

The periodical's second issue: a dated milestone bundling new instruments (the
feature roadmap's Egress Cost Map / "X vs Y" pages — `progress.md`) **and** the
publication of the underlying data under an open licence with a citation string.

- **L3 · Publish "Issue No. 02" and release the data under an open licence
  (CC BY 4.0) with a clear citation string and the `data.json` files documented
  as a public API.** *Rationale:* this is the single biggest structural backlink
  multiplier — it converts the site from "a page to read" into "a source to
  cite" (the caniuse / Vantage mechanism) and is a genuine milestone that *could*
  justify a second, milestone-gated Show HN. *Evidence:* [`research/seo.md`](research/seo.md)
  §5 "open data angle"; [`research/comparable-projects.md`](research/comparable-projects.md)
  COPY #7. *Effort:* M · *Brand-fit:* 5/5 · *Impact:* both.

---

## 4c · Channel plan — the 5-channel shortlist

Taken directly from [`research/channels.md`](research/channels.md)'s ranked
shortlist. Every rejected channel and its reason is in that file and in
[`anti-list.md`](anti-list.md); they are **not** relitigated here.

- **C1 · Infra newsletters — DevOps Weekly + Last Week in AWS first, then
  Console.dev and Pointer.** *Rationale:* the top channel for this project — an
  editor *linking* the site is third-party endorsement, sidesteps every
  self-promo rule (the editor posts, not the maintainer), and the editorial
  voice is irrelevant to whether a link is included. DevOps Weekly has an open,
  documented submission path and a curator who "reads everything." *Evidence:*
  [`research/channels.md`](research/channels.md) §8;
  [devopsweekly.com](https://www.devopsweekly.com/),
  [lastweekinaws.com/contribute](https://www.lastweekinaws.com/contribute/).
  *Effort:* S (a handful of dry, factual emails) · *Brand-fit:* 5/5 ·
  *Impact:* audience growth.

- **C2 · Hacker News — one Show HN (= Launch moment 1).** *Rationale/evidence:*
  see L1. *Effort:* M · *Brand-fit:* 5/5 · *Impact:* both.

- **C3 · lobste.rs — conditional on securing an invite.** *Rationale:* the best
  cultural fit of any community — explicitly welcomes authored content, openly
  hostile to marketing register, audience is pure senior practitioners. Lower
  volume than HN but high-quality, low-risk. *Evidence:* [`research/channels.md`](research/channels.md)
  §3; [lobste.rs/about](https://lobste.rs/about). *Effort:* S to post, M to
  secure an invite — **solve the invite cold-start in week 1–2 or mark the
  channel un-actionable.** *Brand-fit:* 5/5 · *Impact:* audience growth.

- **C4 · LinkedIn — narrowly, for the APIM / enterprise-architect persona
  only.** *Rationale:* the *only* channel that reaches the secondary persona
  (solutions architects doing Apigee/Kong/Azure-APIM selection). Post sparingly,
  strictly in the editorial voice, accepting modest reach as the price of not
  breaking brand — never drift to LinkedIn-influencer cadence. *Evidence:*
  [`research/channels.md`](research/channels.md) §6;
  [`positioning.md`](positioning.md) §3a. *Effort:* S per post · *Brand-fit:*
  3/5 (audience fits; native register does not — discipline required) ·
  *Impact:* both.

- **C5 · Dev.to / Hashnode cross-posting — minimal, mechanical, SEO-only.**
  *Rationale:* near-zero marginal cost — repost writing produced anyway, with a
  correct `rel=canonical` (publish on infraatlas.dev first, wait ~a week for
  Google to index the original, *then* cross-post) for a durable search-traffic
  tail. A background SEO asset, not a campaign. *Evidence:* [`research/channels.md`](research/channels.md)
  §4. *Effort:* S · *Brand-fit:* 4/5 · *Impact:* audience growth.

**Medium-term, flagged not scheduled:** a KubeCon EU / European DevOps
conference CfP — excellent cultural and voice fit, but 6+ month lead times put
it outside the 90-day window ([`research/channels.md`](research/channels.md)
§10). Submit a CfP as a deliberate later bet.

**Not channels (do not plan around them):** Reddit, Kubernetes/CNCF Slack,
Twitter/X, podcasts (initially) — all rejected with reasons in
[`research/channels.md`](research/channels.md) and [`anti-list.md`](anti-list.md).

---

## 4d · Content engine — the periodical, actually periodical

Data gets bookmarked; *opinion gets shared and discussed*. htmx grew on essays;
Pragmatic Engineer and Last Week in AWS grew on voice
([`research/comparable-projects.md`](research/comparable-projects.md) COPY #3).
A small body of editorial writing is the highest-leverage distribution move a
solo maintainer has — and it is what "a periodical of infrastructure" promises.

- **E1 · "Field Notes" — one editorial essay per month.** Dry, literary,
  first-person-as-the-cartographer pieces on real infra texture: cloud-region
  sprawl, instance-naming chaos, what the APIM platforms quietly disagree about,
  why a vendor's "equivalent" SKU isn't. Each essay published on infraatlas.dev
  first, then cross-posted (C5). *Rationale:* opinion is the shareable,
  discussable, search-discoverable layer that brings people to the instruments.
  *Evidence:* [`research/comparable-projects.md`](research/comparable-projects.md)
  COPY #3; [`research/channels.md`](research/channels.md) §4. *Effort:* M/month ·
  *Brand-fit:* 5/5 · *Impact:* both.

- **E2 · A real subscribable feed.** `feed.json` exists but is a private file
  the landing page reads — not a subscribable RSS/Atom feed and not advertised
  ([`audit.md`](audit.md) §1c). Publish a proper `feed.xml` (RSS/Atom) covering
  Field Notes + the "What Changed" data updates, link it from the footer, and
  add `<link rel="alternate" type="application/rss+xml">`. *Rationale:* a
  recurring dated dispatch converts one-time visitors into a returning audience;
  RSS is the zero-infrastructure, no-PII, on-brand way to do it (no mailing-list
  database, no consent surface). *Evidence:* [`research/comparable-projects.md`](research/comparable-projects.md)
  COPY #9; [`audit.md`](audit.md) §1c. *Effort:* S · *Brand-fit:* 5/5 ·
  *Impact:* audience growth.

- **E3 · Keep the "Issue" cadence real.** The site already says "Issue No. 01."
  Bundle meaningful batches of new instruments / data into dated "Issues" (No. 02
  at Launch moment 3) rather than shipping silently. *Rationale:* periodicity is
  the brand; dated issues create natural, honest re-launch moments and give
  newsletters something to link. *Evidence:* [`research/comparable-projects.md`](research/comparable-projects.md)
  §lastweekinaws, COPY #9. *Effort:* S (framing, not new work) · *Brand-fit:*
  5/5 · *Impact:* both.

**Cadence guardrail.** One Field Notes essay per month is the *ceiling* for a
solo maintainer, not a quota — a missed month is better than a thin or
off-voice piece. Never generate filler ([`anti-list.md`](anti-list.md) #3).

---

## 4e · SEO playbook

SEO is the compounding base of the discovery loop. The audit found it greenfield
— no `robots.txt`, no `sitemap.xml`, no JSON-LD ([`audit.md`](audit.md) §1a).
Full landscape and citations in [`research/seo.md`](research/seo.md).

### Table-stakes (do these before Launch moment 1)

- **S1 · Ship `robots.txt` + a build-time `sitemap.xml`** with accurate
  `<lastmod>` per instrument (a real recrawl hint; the 4 live-data instruments
  change daily). *Evidence:* [`research/seo.md`](research/seo.md) §4.
  *Effort:* S · *Brand-fit:* 5/5 · *Impact:* audience growth.

- **S2 · Add JSON-LD structured data**, per page type: `Dataset` on the
  data-table instruments (also makes them eligible for Google Dataset Search — a
  channel the listicle competitors are not in), `TechArticle` on the four
  API-gateway *guide* instruments, `SoftwareApplication` on the site root,
  `BreadcrumbList` on the "Department" taxonomy. Validate every template with the
  Rich Results Test. *Evidence:* [`research/seo.md`](research/seo.md) §4.
  *Effort:* M · *Brand-fit:* 5/5 · *Impact:* audience growth.

- **S3 · Give every page a descriptive `<h1>` and question-shaped `<h2>`s.** The
  `<h1>` is currently just the wordmark on every page ([`audit.md`](audit.md)
  §1a). Add a real `<h1>` saying what the page *is* (the wordmark stays as a
  masthead `<p>`/logo — the brand survives); shape `<h2>`/`<h3>`s as the
  questions from the long-tail list and put one plain-text answer sentence above
  each table. *Evidence:* [`research/seo.md`](research/seo.md) §4.
  *Effort:* M · *Brand-fit:* 4/5 · *Impact:* audience growth.

- **S4 · Mint stable, keyword-bearing, anchored URLs** — a deterministic anchor
  per table row / matrix cell (`/ec2-instance-types-by-region#g5-eu-west-1`,
  `#apigee-vs-kong-rate-limiting`). *Rationale:* this single structural change
  captures hundreds of `is <X> available in <Y>` long-tail variants at once —
  the highest-ROI on-page change. *Evidence:* [`research/seo.md`](research/seo.md)
  §3 "templated pattern", §4. *Effort:* M · *Brand-fit:* 5/5 · *Impact:*
  audience growth.

- **S5 · Fully cross-link the 16 instruments by topic.** Every compute explorer
  links to the Region Map and the Equivalent-SKU Finder; the APIM matrix links
  to all four gateway guides and back. *Evidence:* [`research/seo.md`](research/seo.md)
  §4. *Effort:* S · *Brand-fit:* 5/5 · *Impact:* audience growth.

### 10 priority pages (optimise first — the Bucket A wedge + highest-value matrices)

The primary SEO wedge is **cross-cloud "availability by region"** — weak
incumbents, best instrument fit ([`research/seo.md`](research/seo.md) §2).
Optimise in this order:

| # | Instrument | Primary query target |
|---|-----------|----------------------|
| 1 | EC2 Observatory | `ec2 instance types by region` |
| 2 | Region Map | `cloud providers region map` / `which cloud has a region in <city>` |
| 3 | Azure VM Atlas | `azure vm sizes by region` |
| 4 | GCP Compute Index | `gcp machine types by region` |
| 5 | OCI Compute Observatory | `oci compute shapes by region` |
| 6 | OVH Instance Catalogue | `ovh cloud instances / regions` |
| 7 | Equivalent-SKU Finder | `azure equivalent of ec2 <family>` |
| 8 | APIM Feature Matrix | feature-cell long tail (see below) |
| 9 | Kubernetes Atlas | `managed kubernetes comparison eks aks gke` |
| 10 | Compliance Footprint | `cloud compliance certifications comparison` |

### 10 long-tail query targets (capturable with §S3–S4 page structure)

From [`research/seo.md`](research/seo.md) §3 — low individual volume, additive,
low-competition, high-intent:

1. `is g5 available in eu-west-1` (+ the whole templated `is <type> in <region>` family)
2. `which aws regions have h100 gpu`
3. `aws regions with arm graviton instances`
4. `which azure regions support confidential computing`
5. `gcp regions with a100 gpus`
6. `azure equivalent of ec2 m5`
7. `gcp equivalent of aws fargate`
8. `does eks charge for control plane`
9. `aws api gateway timeout limit` / `can you increase the 29 second timeout`
10. `does azure api management support mtls` / `apigee vs kong rate limiting`

— **SEO-L · Treat the long-tail set as one structural job, not 10 content
pieces:** §S3 + §S4 capture all of them at once. *Effort:* (folded into S3/S4) ·
*Brand-fit:* 5/5 · *Impact:* audience growth.

### Backlink targets (unblocked once the repo is public)

- **S6 · Submit one-line PRs to the awesome-* lists:** `donnemartin/awesome-aws`,
  `devtoolsd/awesome-cloud`, `nishantthorat/awesome-aws-cloud`,
  `awesomelistsio/awesome-aws`, `realvz/awesome-eks`, `nathanpeck/awesome-ecs`,
  and a live `awesome-api`/`awesome-apigateway` list. *Rationale:* free,
  durable, compounding backlinks — the closest comparable (ec2instances.info) is
  listed on these today. *Evidence:* [`research/seo.md`](research/seo.md) §5;
  [`research/comparable-projects.md`](research/comparable-projects.md) COPY #6.
  *Effort:* S · *Brand-fit:* 5/5 · *Impact:* audience growth.

- **S7 · Publish the data under CC BY 4.0 with a citation string** (= Launch
  moment 3 / L3). The biggest structural backlink multiplier. *Evidence:*
  [`research/seo.md`](research/seo.md) §5. *Effort:* M · *Brand-fit:* 5/5 ·
  *Impact:* both.

- **S8 · Warm outreach to independent cloud blogs (e.g. cloudonaut)** that
  already publish region-availability content — natural citers of a
  better-structured neutral dataset, no competitive conflict. *Evidence:*
  [`research/seo.md`](research/seo.md) §5. *Effort:* S · *Brand-fit:* 4/5 ·
  *Impact:* audience growth.

---

## 4f · Community & contribution activation

The repo is private with 0 stars while the site advertises "open-source" — every
GitHub link 404s for the public ([`audit.md`](audit.md) headline #1). Nothing in
this section can happen until that is fixed.

- **N1 · Make the repo public — week 1, blocking everything.** *Rationale:*
  "open-source" is the positioning *and currently not true*; stars, contributors,
  GitHub Sponsors, awesome-list PRs, and an honest Show HN all depend on it.
  Make it public *carefully* — httpie permanently lost ~54k stars to a botched
  privatization; never run an admin op that risks the public repo again.
  *Evidence:* [`audit.md`](audit.md) headline #1;
  [`research/comparable-projects.md`](research/comparable-projects.md) §httpie,
  AVOID #4. *Effort:* S · *Brand-fit:* 5/5 · *Impact:* both.

- **N2 · Refresh the README and fix licence detection.** The README says
  "11/11 instruments" (now 16), "Live … (coming soon)" (it is live), has a stale
  data-sources table and no badges; GitHub detects the licence as `"other"`, not
  MIT. *Rationale:* the README is the repo's landing page and the Show HN's
  destination; a stale one undercuts the trust pitch. *Evidence:*
  [`audit.md`](audit.md) §1c. *Effort:* S · *Brand-fit:* 5/5 · *Impact:* both.

- **N3 · Add contributor scaffolding:** `.github/ISSUE_TEMPLATE` (a "data
  correction" template and a "new instrument idea" template), a PR template, a
  handful of labelled `good-first-issue`s (e.g. data corrections, a new region),
  and a public roadmap (the feature roadmap already exists in
  `tasks/features-2026-05/` — surface a public version). *Rationale:* HN
  "overindexes on" open-source repos; a contributable repo converts grateful
  readers into contributors. *Evidence:* [`audit.md`](audit.md) Recon;
  [`research/channels.md`](research/channels.md) §1. *Effort:* M · *Brand-fit:*
  5/5 · *Impact:* audience growth.

- **N4 · Publish a real methodology / colophon page.** caniuse's about page —
  exactly how data is chosen and *hand-verified* — is a core trust mechanism.
  Infra Atlas has `docs/data-policy.md` internally; surface a public, linkable
  "how this data is gathered, how often, with the asterisks intact" page.
  *Rationale:* a reference site lives or dies on trust; visible methodology is
  the proof. *Evidence:* [`research/comparable-projects.md`](research/comparable-projects.md)
  §caniuse, COPY #5. *Effort:* S · *Brand-fit:* 5/5 · *Impact:* both.

- **N5 · Keep an origin story prominent.** "Got tired of grepping vendor docs
  across five tabs" is exactly the disarming, personal *why* that pgexercises and
  crontab.guru lead with — keep it on the about/colophon page. *Rationale:* an
  honest origin story is trust-building and human. *Evidence:*
  [`research/comparable-projects.md`](research/comparable-projects.md)
  §pgexercises, COPY #10. *Effort:* S · *Brand-fit:* 5/5 · *Impact:* both.

---

## 4g · Sequenced summary

| ID | Recommendation | Effort | Brand-fit | Impact | When |
|----|----------------|--------|-----------|--------|------|
| N1 | Make repo public | S | 5/5 | both | Wk 1 |
| N2 | Refresh README, fix licence | S | 5/5 | both | Wk 1 |
| S1 | robots.txt + sitemap.xml | S | 5/5 | audience | Wk 2 |
| S2 | JSON-LD structured data | M | 5/5 | audience | Wk 2–3 |
| S3 | Descriptive `<h1>` + question `<h2>`s | M | 4/5 | audience | Wk 3 |
| S4 | Anchored per-row URLs | M | 5/5 | audience | Wk 3–4 |
| S5 | Cross-link 16 instruments | S | 5/5 | audience | Wk 3 |
| N4 | Methodology / colophon page | S | 5/5 | both | Wk 2 |
| N5 | Origin story prominent | S | 5/5 | both | Wk 2 |
| E2 | Real subscribable RSS feed | S | 5/5 | audience | Wk 4 |
| N3 | Contributor scaffolding | M | 5/5 | audience | Wk 4–5 |
| L1/C2 | Show HN (Launch moment 1) | M | 5/5 | both | Wk 6 |
| S6 | awesome-* list PRs | S | 5/5 | audience | Wk 6 |
| C1 | Newsletter submissions | S | 5/5 | audience | Wk 6 |
| C3 | lobste.rs (if invited) | S | 5/5 | audience | Wk 6+ |
| E1 | Field Notes — monthly essay | M/mo | 5/5 | both | Wk 4 on |
| L2 | APIM matrix + essay (Launch 2) | M | 5/5 | both | Wk 11–12 |
| C4 | LinkedIn (APIM persona) | S | 3/5 | both | Wk 12 on |
| C5 | Dev.to cross-post | S | 4/5 | audience | Wk 8 on |
| S8 | Cloud-blog outreach | S | 4/5 | audience | Wk 8+ |
| L3/S7 | Issue No. 02 + open data (Launch 3) | M | 5/5 | both | Mo 5–6 |

Week-by-week sequencing with dependencies is in [`plan-90d.md`](plan-90d.md).
