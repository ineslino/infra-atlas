# Phase 6 — Measurement

You cannot market what you cannot measure — and the audit found **no analytics
installed** ([`audit.md`](audit.md) headline #3); traffic, rankings, referrers
and donor numbers are all unmeasurable today ([`audit.md`](audit.md) §"What the
audit could NOT measure"). But the *wrong* metrics are worse than none: chasing
raw pageviews and star counts is exactly the SaaS-funnel thinking the mission
rules out. This phase defines **what to measure and why**.

The install runbook is separate: [`analytics-install.md`](analytics-install.md)
(Phase 6.5) is the *how*; this file is the *what* and *so-what*.

---

## 6a · The principle — measure trust and usefulness, not vanity

A donation-funded editorial reference succeeds when practitioners **trust it
enough to return to it and, occasionally, fund it**. That is the thing to
measure. Pageviews, stars and followers are inputs at best and vanity at worst —
caniuse has an enormous audience and ~540 patrons; the audience number predicts
almost nothing on its own ([`research/donation-economics.md`](research/donation-economics.md)
§1). Every metric below is chosen because it resists gaming and reflects real
value delivered.

**Two health signals stand above the rest:**

- **Returning practitioners** — returning-visitor share × engagement depth. The
  truest signal that the atlas has become someone's reference. Hard to fake,
  impossible to buy.
- **Donations cover running costs** — the sustainability check (not a growth
  metric). Binary and honest: are the lights paid for?

Everything else is diagnostic detail under these two.

---

## 6b · Metrics that matter — the metric tree

Four questions, mapped to the three growth loops ([`growth.md`](growth.md)
§4a). Each metric names its **source** and whether it is **leading** (moves
early, predictive) or **lagging** (confirms an outcome slowly).

### Q1 · Is the atlas being found? — *discovery loop*

| Metric | Source | Lead/Lag |
|--------|--------|----------|
| Referrer mix by channel (HN / newsletter / search / direct / lobste.rs / LinkedIn) | Plausible — acquisition view | Leading |
| Search impressions, clicks, top queries, average position | Google Search Console | Leading |
| Monthly unique visitors | Plausible | Context (not a goal) |
| New vs returning split | Plausible | Leading |

Referrer mix answers "which channel actually worked" — it is how the 90-day
plan's channel bets ([`growth.md`](growth.md) §4c) get judged. Uniques are
*context*, never a target.

### Q2 · Is the atlas useful? — *the truest signal*

| Metric | Source | Lead/Lag |
|--------|--------|----------|
| **Returning-visitor share** | Plausible | Leading — the closest thing to a north star |
| `instrument_open` rate; `filter_apply` per session | Plausible events | Leading |
| `cross_reference_click` — are people exploring it *as an atlas* | Plausible events | Leading |
| `editorial_read_complete` — do Field Notes hold attention | Plausible events | Lagging |
| Exit rate on instrument pages | Plausible | Lagging |

A reference site people *come back to* has succeeded; one they visit once and
forget has not — regardless of the pageview count.

### Q3 · Is the atlas trusted enough to support? — *donation loop*

| Metric | Source | Lead/Lag |
|--------|--------|----------|
| Funnel: `donation_cta_view` → `donation_cta_click` → confirmed, **per placement** | Plausible events + manual reconcile | Leading → lagging |
| Donor count; recurring vs one-off split | Open Collective + Ko-fi | Lagging |
| Donation revenue vs running costs (the sustainability ratio) | Public ledger | Lagging (slow) |

The per-placement funnel ([`donations.md`](donations.md) §5e) shows *which*
gratitude moment converts — the only donation metric that is actionable early.
Revenue itself is slow and small by design (§6a); judge it against costs, not a
salary.

### Q4 · Is the atlas being cited? — *citation loop*

| Metric | Source | Lead/Lag |
|--------|--------|----------|
| Referring domains / backlinks | Search Console + manual tally | Lagging |
| `data.json` / API request volume | Cloudflare logs/analytics | Lagging |
| Newsletter mentions, awesome-list inclusions | Manual tally | Lagging |

Citations are the compounding asset (ec2instances.info's JSON is hit hundreds of
thousands of times/day — [`research/comparable-projects.md`](research/comparable-projects.md)
§Vantage); slow to move, but the strongest long-run health sign.

---

## 6c · Vanity metrics — explicitly demoted

Named so they are not mistaken for goals:

- **Raw pageviews / sessions as a target.** Context only (Q1). A spike from one
  HN hit that never returns is not growth.
- **GitHub stars as a goal.** A trust *byproduct*, never a target — and fragile
  (httpie lost ~54k stars to one botched repo op —
  [`research/comparable-projects.md`](research/comparable-projects.md) §httpie).
  Buying stars or followers is forbidden outright ([`anti-list.md`](anti-list.md)
  #13).
- **Social follower counts.** Off-model for a project that is *discovered*, not
  *marketed*.
- **Time-on-page maximised.** A reference site that answers a question *fast* is
  working; long dwell can mean confusion. Read engagement (`filter_apply`,
  `cross_reference_click`) instead.

---

## 6d · The privacy-respecting stack

The stack is itself a trust signal — the audience is privacy-conscious
developers, and one third-party tracker would undo the positioning
([`anti-list.md`](anti-list.md) #8). Chosen in [`analytics-install.md`](analytics-install.md)
§6.5a; the *why* in brief:

- **Plausible Cloud (EU)** — cookieless, no banner, EU-hosted, open-source,
  ~1 KB script, first-class custom events (needed for the §6b Q2/Q3 events) and
  a built-in public dashboard. First-party proxied via Cloudflare so dev
  ad-blockers do not erase 30–50% of traffic.
- **Google Search Console** — *not* a visitor tracker: it adds no script to the
  site, sets no cookie, and collects no visitor data; it only reports how
  Google's index sees the site. It is the *only* source for Q1 search metrics
  and Q4 backlinks, and table-stakes for the SEO playbook ([`growth.md`](growth.md)
  §4e). Adding it does not touch the privacy promise to visitors.
- **Cloudflare** — already in the stack; its free Web Analytics is a sanity
  baseline and its logs give the Q4 API-request volume.

- **M1 · No cookie banner, ever.** Plausible is cookieless and uses no
  persistent identifier — under current EU guidance it needs no consent banner,
  and a banner on a privacy-respecting site would undermine the very claim.
  *Evidence:* [`analytics-install.md`](analytics-install.md) §6.5f. *Effort:* S
  (it is a non-action) · *Brand-fit:* 5/5 · *Impact:* both.

- **M2 · A one-paragraph `/privacy` page**, linked from the footer colophon —
  what is collected (aggregate pageviews + the §6b events, no cookies, no PII,
  no cross-site identity), retention, and the provider. No legalese. *Evidence:*
  [`analytics-install.md`](analytics-install.md) §6.5f. *Effort:* S ·
  *Brand-fit:* 5/5 · *Impact:* both.

---

## 6e · The public dashboard — `/state`

The periodical showing its own circulation figures — on-brand, and a transparency
signal in itself.

- **M3 · A public `/state` page.** Plausible exposes a shareable public
  dashboard via one link. Combine on `/state`: monthly uniques ✅, top pages ✅,
  and the donation ledger headline — donations-to-date + expenses-YTD
  ([`donations.md`](donations.md) §5f). **Not** public: the referrer mix ❌ — it
  exposes the channel strategy and invites gaming. *Evidence:*
  [`analytics-install.md`](analytics-install.md) §6.5e; [`donations.md`](donations.md)
  §5f. *Effort:* S · *Brand-fit:* 5/5 · *Impact:* both.

---

## 6f · What "good" looks like at day 90

The site is brand-new with no analytics — so honest targets are **capability and
direction**, not invented traffic numbers (the research deliberately refuses to
fabricate volume figures — [`research/seo.md`](research/seo.md) preamble).

**Capability targets (binary — done / not done):**

- Analytics live, verified, and trusted — the [`analytics-install.md`](analytics-install.md)
  §6.5g checklist fully passes.
- The donation funnel is instrumented end to end and producing per-placement
  data (§6b Q3).
- `/state` is public and accurate.
- Google Search Console is verified and reporting query data.

**Directional targets (trend, not absolute):**

- Returning-visitor share is measurable and *trending up* month over month.
- Referrer mix shows ≥3 distinct working channels (e.g. search + one newsletter
  + HN), not single-source dependence.
- ≥3 external citations logged (awesome-list inclusions + newsletter mentions).
- ≥1 confirmed donation — proof the funnel works end to end. *(One. The bar is
  "the mechanism functions," not a revenue figure — see §6a and
  [`research/donation-economics.md`](research/donation-economics.md): "ten
  years, two donations" is a real outcome for this class.)*

One illustrative scenario, clearly labelled an `[ESTIMATE]` not a target: at
~100k cumulative visitors over the quarter and 0.03% one-off conversion at ~€5,
that is ~€150 gross — i.e. roughly the caniuse monthly outcome compressed into a
launch quarter ([`research/donation-economics.md`](research/donation-economics.md)
§2). Treat any revenue as a bonus on top of the capability targets.

---

## 6g · Review cadence

- **M4 · A monthly measurement review** — 30 minutes against this file: read the
  five Plausible dashboards ([`analytics-install.md`](analytics-install.md)
  §6.5d), update the citation tally, check the funnel. The review *feeds the
  next decision*: which channel to repeat, which Field Notes topic landed,
  whether a donation placement needs tuning. *Evidence:* this file; the
  dashboards in [`analytics-install.md`](analytics-install.md) §6.5d. *Effort:*
  S/month · *Brand-fit:* 5/5 · *Impact:* both.

The first such review lands at the end of the 90-day plan ([`plan-90d.md`](plan-90d.md)
week 12) and becomes the recurring ritual thereafter — and an input to the
annual transparency note ([`donations.md`](donations.md) §5f, D10).
