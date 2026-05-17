# Donation Economics — Funding a Donation-Only OSS Reference Site

Research for Infra Atlas (infraatlas.dev). Reference class: a developer-tool OSS
project with a tip jar (htmx, caniuse, caddy, ripgrep) — **not** a SaaS.
Monetization is donations only: no ads, no paid tiers, no accounts.

Scope of this doc: the *economics* of donation-funded OSS reference projects —
real numbers, conversion benchmarks, what drives donations, friction, and a
provider comparison for an EU-based solo maintainer.

**Sourcing rules used here:** every figure carries a URL. Figures that are
estimates, derived, or unverifiable are explicitly labelled `[ESTIMATE]`,
`[DERIVED]`, or `[UNVERIFIED]`. Researched 2026-05-17; donation pages are
live data and will have drifted since.

---

## 1. Real numbers

### caniuse — the closest possible comparable

caniuse.com is the single best reference comparable: a free, editorial,
browser-compatibility reference site, maintained largely by one person (Alexis
Deveria), funded by a tip jar. Its Patreon is public.

- **caniuse Patreon, as observed 2026-05-17: 539 members, €167.9/month.**
  Source: <https://www.patreon.com/caniuse>
- Lowest tier is €1/month; tier detail beyond that not exposed on the public
  page. Source: <https://www.patreon.com/caniuse>
- caniuse's Patreon has been publicly described as **underfunded** relative to
  the site's reach — a Hacker News thread titled literally "Caniuse.com has a
  underfunded patreon" dates the concern to 2017.
  Source: <https://news.ycombinator.com/item?id=14446280>
- Context on caniuse's reach: it is one of the most-used web-dev reference
  sites and has an ongoing data collaboration with Google's Baseline / web.dev
  and MDN. Source: <https://web.dev/blog/baseline-project-2024>

**Takeaway for Infra Atlas:** a famous, daily-used, single-maintainer reference
site converts a massive audience into roughly **540 patrons and ~€170/month**.
This is the realistic ceiling for a tip-jar reference site of this type, and it
is the most important single number in this document. Plan the donation
strategy as "covers hosting + a coffee," not "replaces a salary."

### htmx / Big Sky Software — GitHub Sponsors

- **Big Sky Software (htmx + hyperscript): 75 current sponsors** on GitHub
  Sponsors, as observed 2026-05-17.
  Source: <https://github.com/sponsors/bigskysoftware>
- Tiers: $10/mo (Supporter), $100/mo (Corporate, logo on home page), $500/mo
  (Flagship), $1,000/mo (Platinum). Custom amounts allowed.
  Source: <https://github.com/sponsors/bigskysoftware>
- GitHub Sponsors does **not** publish total monthly $ on the public page, so
  htmx's exact monthly income is **`[UNVERIFIED]`**. htmx's creator Carson
  Gross has said publicly he treats sponsorship money "as not real, because it
  could evaporate tomorrow" — i.e. even a flagship OSS project does not consider
  donations a stable income base.
  Source: <https://dev.to/podrocket/htmx-with-carson-gross>

### Open Collective — public ledgers (real, audited figures)

Open Collective ledgers are fully public. These are large, well-known projects;
they set the *upper bound*, not the expectation for a new solo reference site.

| Project | Total raised (all-time) | Est. annual budget | Current balance | Contributors |
|---|---|---|---|---|
| Babel | $1,798,033.62 | not shown | not shown | 1,262 |
| webpack | $1,726,558.71 | $161,258.55 | $98,164.45 | 2,689 total (1,530+ backers, 216+ sponsors) |

Sources: <https://opencollective.com/babel> · <https://opencollective.com/webpack>

Note: Babel's and webpack's revenue is dominated by *corporate* sponsors
(Airbnb alone gave Babel $217,858; webpack lists 216+ sponsor orgs). Individual
small donors are a minority of dollars. A reference site with no corporate
"logo on the page" hook should expect a far flatter revenue curve.

### Liberapay — public profiles (real figures)

Liberapay shows weekly income and patron counts publicly for every recipient.
Top recipients, as observed 2026-05-17:

| Recipient | Weekly income | Patrons | What it is |
|---|---|---|---|
| Liberapay (itself) | €829.90/wk | 1,779 | the platform |
| Codeberg | €644.08/wk | 624 | non-profit Git host |
| GIMP | €564.60/wk | 1,071 | image editor |
| F-Droid-Data | €512.07/wk | 926 | F-Droid app packaging |
| NewPipe e.V. | €454.89/wk | 910 | Android video player |

Source: <https://liberapay.com/explore/recipients>

Even the **top of all of Liberapay** — well-known projects with ~1,000 patrons —
sits around **€450–650/week (~€2,000–2,800/month)**. A new solo reference site
will be far below this. Liberapay is a small pond: its own founder's profile
(Changaco) shows ~€440/week from 1,141 patrons.
Source: <https://liberapay.com/explore/recipients>

### The brutal baseline

- A Java library maintainer, quoted in LWN: **"I had a donation link for ten
  years, got two donations."** Source: <https://lwn.net/Articles/786304/>
- Tidelift survey of several hundred OSS developers: **60% reported their work
  is "self-funded / none"**; only ~1% used dual-licensing; ~4% had foundation
  funding. Source: <https://lwn.net/Articles/786304/>
- 2024 Open Source Software Funding Report (GitHub + Linux Foundation +
  Harvard): of corporate OSS investment, **86% is employees' time, only 14% is
  direct financial contribution** — i.e. money that reaches maintainers as cash
  is a small slice even of corporate goodwill.
  Source: <https://www.linuxfoundation.org/blog/understanding-the-state-of-open-source-funding-in-2024>

---

## 2. Conversion benchmarks (visitor → donor)

There is no single authoritative "OSS docs donation conversion rate" statistic.
The commonly-cited **~0.01–0.1% of users** range is a community rule of thumb,
not a published study. The honest approach is to triangulate from real data
points below — all are `[DERIVED]` unless noted.

### Triangulated data points

- **caniuse:** 539 paying patrons against an audience of (conservatively)
  hundreds of thousands to millions of monthly web developers. If caniuse has
  ~1M monthly users, that is **~0.05% conversion**; at ~5M users, **~0.01%**.
  The user base is **`[ESTIMATE]`** (caniuse does not publish traffic), but the
  539 patrons is real. Source: <https://www.patreon.com/caniuse>
- **800M downloads → ~50 sponsors:** a maintainer profiled by Connor Tumbleson
  has projects "downloaded over 800 million times" and roughly 50 GitHub
  Sponsors. Downloads ≠ users, but this is on the order of **0.00001%** and
  illustrates how weak download-to-donor conversion is.
  Source: <https://connortumbleson.com/2025/05/05/github-sponsor-funding/>
- **Wikipedia (documented, large-scale):** Wikimedia's own 2022 campaign
  messaging states **only 2% of readers ever donate** — and that is *with*
  aggressive, repeated, full-screen banners and a globally trusted brand. A
  passive footer link on a dev reference site will be **one to two orders of
  magnitude below** this.
  Sources: <https://en.wikipedia.org/wiki/Wikipedia:Fundraising/2022_banners> ·
  <https://meta.wikimedia.org/wiki/Fundraising/2022-23_Report>

### Working planning numbers for Infra Atlas

- **Plan for 0.01–0.05% of monthly active users converting to *any* donation
  (mostly one-off).** This is consistent with the caniuse data point and sits
  inside the community ~0.01–0.1% rule of thumb. Labelled `[ESTIMATE]` — treat
  as a planning assumption, not a measured fact.
- **Recurring donors will be a small fraction of that** — see §3; most one-off.
- Concrete sanity check: at 100k monthly visitors and 0.03% one-off conversion,
  that is ~30 donations/month; at a ~€5 median tip that is **~€150/month
  gross** before fees — i.e. roughly the caniuse outcome. `[DERIVED]`

### Adjacent conversion benchmarks (context, not OSS-specific)

- Nonprofit *donation-page* conversion (people who already clicked "donate")
  averages ~12–17%. This is the conversion of an *intent-to-give visitor*, not
  a general reader — do not apply it to total site traffic.
  Sources: <https://fundraiseup.com/blog/average-conversion-nonprofit/> ·
  <https://www.raisely.com/blog/conversion-rate-optimisation-nonprofit-guide>
- Email-appeal conversion is typically 0.1–0.3% — relevant only if Infra Atlas
  ever builds a mailing list. Source:
  <https://virtuous.org/blog/how-to-measure-and-improve-your-nonprofits-conversion-rate/>

---

## 3. What actually drives donations

### The "this saved me hours" gratitude reflex

- Gratitude is one of the few *purely emotional* donation triggers, and
  research finds it lifts both **whether** someone donates and **how much**, via
  an "affiliation" motive (wanting to reciprocate / belong).
  Source: <https://www.sciencedirect.com/science/article/abs/pii/S0969698919310227>
- Practical implication: donations cluster around the moment of *received
  value*. The ask should be visible right where a reader has just been helped
  (end of a useful reference page, after a comparison table), not buried in a
  generic "About" page.

### Single-maintainer scarcity / a face to support

- Liberapay's top individual recipients (Changaco, licaon-kter) and caniuse
  itself show that people fund **a named person**, not an abstract project.
  Sources: <https://liberapay.com/explore/recipients> · <https://www.patreon.com/caniuse>
- For Infra Atlas this is an asset: a solo EU maintainer is exactly the
  "scarcity + identifiable victim" pattern donors respond to. Name the
  maintainer, show it is one person, state plainly that donations are the only
  income.

### Transparency — public expense ledgers

- Open Collective's entire value proposition is the **public, real-time
  ledger**: every contribution and every expense is visible and (for collectives)
  expenses are approved before money moves.
  Source: <https://opencollective.com/how-it-works>
- Showing exactly where money goes ("€X/yr hosting, €Y/yr domain, rest = my
  time") converts better than an open-ended ask. This is a deliberate design
  choice Infra Atlas can copy even without using Open Collective — a simple
  public costs page.

### Recurring vs one-off framing

- Across nonprofit data: **~70% of donors are one-time and account for only
  ~27% of total dollars**; the ~30% who give more than once provide ~73% of
  dollars, and a repeat donor is ~5.5× more valuable over their lifetime.
  Source: <https://www.donorperfect.com/nonprofit-technology-blog/featured/donor-behavior/>
- Recommendation: **default the donation UI to one-off** (lowest friction, see
  §4) but make a recurring option clearly available and frame it as "keep the
  lights on each month." Expect most donors to be one-off; treat any recurring
  base as the stable core.

### Suggested-amount anchoring

- Suggested amounts work via **anchoring** — they set the reference point for
  what feels "normal." Higher suggested amounts raise average donation, but a
  too-high anchor depresses participation; the trade-off is real.
  Sources: <https://thedecisionlab.com/intervention/anchording-and-charitable-donations-1> ·
  <https://direct.mit.edu/rest/article/101/5/808/58537/Defaults-and-Donations-Evidence-from-a-Field>
- Optimal layout from CRO research: **3–4 preset amounts plus an "other"
  field**. A large field experiment (23,500 donors) found a higher default
  lifted average donation ~22% and net margin ~36%; a subtler suggested-amount
  cue gave a ~0.7% conversion lift and ~1.3% volume lift.
  Sources: <https://pro.gofundme.com/c/research/highlighting-suggested-amount-increases-donations/> ·
  <https://home.uchicago.edu/ourminsky/Charity_Default_Goswami_Urminsky.pdf>
- For a dev audience, anchor low and concrete — e.g. €3 / €5 / €10 + custom.
  €5 as the visually highlighted default is a defensible starting anchor
  `[ESTIMATE]`; A/B-test later if traffic allows.

### Counter-driver: thank-you gifts can backfire

- Offering tangible thank-you gifts (stickers, t-shirts) can *reduce* giving by
  reframing a gift as a transaction. One OSS maintainer's exact words: "I'm not
  excited to be giving away t-shirts on Patreon."
  Sources: <https://lwn.net/Articles/786304/> ·
  <https://www.sciencedirect.com/science/article/abs/pii/S0167487012000530>
- Recommendation: keep it a pure tip jar. No perks, no tiers — which also
  matches the project's stated "no paid tiers ever" rule.

---

## 4. Donation friction

Each friction point below loses donors who *wanted* to give.

### GitHub-account requirement (GitHub Sponsors)

- GitHub Sponsors requires the donor to **have and be logged into a GitHub
  account**. For a general infra/API audience many *do*, but it still excludes
  non-developers and adds a login step.
  Source: <https://docs.github.com/en/sponsors/getting-started-with-github-sponsors/about-github-sponsors>
- Maintainer-set **high minimums** ($100–$300 seen in the wild) silently kill
  small donations — keep any minimum at $1.
  Source: <https://connortumbleson.com/2025/05/05/github-sponsor-funding/>

### Recurring-default vs one-off-default

- A donation form that defaults to *recurring* (or pre-ticks a recurring box)
  adds a commitment decision at the worst moment and depresses conversion;
  defaulting to **one-off** is the lower-friction choice given ~70% of donors
  are one-time anyway.
  Source: <https://www.donorperfect.com/nonprofit-technology-blog/featured/donor-behavior/>
- Patreon and (largely) Open Collective are *recurring-first* by design; Ko-fi
  and Buy Me a Coffee are *one-off-first*. This is a structural reason a
  Ko-fi-style page may out-convert a Patreon for a reference site.

### Payment-provider geographic limits

- Liberapay routes through **Stripe and PayPal**; donor and recipient must be in
  a country those processors support. Source:
  <https://en.liberapay.com/about/payment-processors>
- GitHub Sponsors payouts to *maintainers* are limited to Stripe-supported
  countries (or require a fiscal host otherwise).
  Source: <https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors/using-a-fiscal-host-to-receive-github-sponsors-payouts>
- For an EU maintainer this is generally fine; the constraint mostly affects
  *which donors* can pay, not the maintainer.

### Minimalist / low-context asks convert worse

- Wikimedia A/B data: a stripped-down banner with **only a donate button** saw
  a **~95% drop** in donation rate vs a banner with bold design and explanatory
  copy. A bare "Donate" link with no context underperforms.
  Source: <https://en.wikipedia.org/wiki/Wikipedia:Fundraising/2022_banners>
- Implication: pair the ask with a short, honest line of context (who runs the
  site, that it is free and donation-funded, what the money covers).

### Banner fatigue / repeated asks

- Wikimedia: >75% of donors give on the **first or second** banner impression;
  conversion is "minuscule" after ~10 impressions.
  Source: <https://diff.wikimedia.org/2017/10/03/fundraising-banner-limit/>
- Implication: a persistent, polite footer/sidebar ask is fine; aggressive
  repeated modals are not — they annoy without converting and clash with an
  editorial reference site's tone.

### Fees as friction

- Every provider loses 3–13% to platform + processing fees (see §5). For small
  tips the **fixed per-transaction fee** (~€0.30 on Stripe/PayPal) hurts most: a
  €2 tip can lose ~20%+. Suggested-amount anchoring at €3–€5 partly mitigates
  this. Source: <https://earnifyhub.com/blog/kofi-vs-buy-me-a-coffee> (fee basis)

---

## 5. Provider comparison (EU-based individual maintainer)

For a **solo EU individual** (not an org, no separate legal entity), accepting
mostly small one-off tips, no perks/tiers.

| Provider | Platform fee | Processing fee | Recurring? | One-off? | Donor needs account? | Public ledger? | EU individual notes |
|---|---|---|---|---|---|---|---|
| **GitHub Sponsors** | 0% for sponsorships *from personal accounts* (up to 6% from org accounts) | 0% passed to dev — GitHub absorbs processing on personal sponsorships | Yes | Yes | **Yes — GitHub login** | No (sponsor count only) | Payouts via Stripe; EU OK if Stripe supports the country, else needs a fiscal host. Audience fit is high (devs). |
| **Open Collective** (via fiscal host) | Host fee: ~8% (Open Source Europe) to 10% (Open Source Collective) | + Stripe/PayPal ~3% | Yes (recurring-first) | Yes | No | **Yes — fully public, real-time** | Strong EU option: Open Source Europe acts as the EU fiscal/legal host so the individual needs no company. Best transparency story. Total take ~11–13%. |
| **Liberapay** | **0% platform fee** (Liberapay is itself donation-funded) | Stripe avg ~3.1%, PayPal avg ~5.1% (varies) | Yes (recurring-first; pre-funded) | Limited | No | **Yes — weekly income + patrons public** | Cheapest. Non-profit, EU-friendly, no account needed by donor. Small audience/brand; one-off giving is weak. |
| **Ko-fi** | **0% on donations** on free plan; Ko-fi Gold ($6/mo) removes fees on all streams | ~2.9% + ~$0.30 per transaction (Stripe/PayPal) | Optional (one-off-first) | **Yes — primary mode** | No | No | Best for low-friction one-off tips. Free plan already 0% platform fee on tips. Funds via the maintainer's own Stripe/PayPal. |
| **Buy Me a Coffee** | **5% flat** on everything (tips + memberships) | ~2.9% + ~$0.30 per transaction | Yes | **Yes — primary mode** | No | No | Same one-off-first UX as Ko-fi but 5% platform fee makes Ko-fi strictly cheaper for a pure tip jar. |
| **Stripe-direct** (own donate page) | 0% platform (no platform) | Standard Stripe: ~1.5% + €0.25 for EEA cards, more for non-EEA/Amex | DIY (Stripe supports it) | Yes | No | No (DIY) | Lowest fees and full control, but the maintainer handles the donate page, receipts, and EU VAT/accounting alone — most engineering + admin effort. |

Sources:
- GitHub Sponsors fees (0% personal / up to 6% org = 3% card + 3% service):
  <https://docs.github.com/en/sponsors/sponsoring-open-source-contributors/about-sponsorships-fees-and-taxes>
- GitHub Sponsors fiscal host requirement:
  <https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors/using-a-fiscal-host-to-receive-github-sponsors-payouts>
- Open Collective / Open Source Collective 10% fiscal-host fee:
  <https://docs.oscollective.org/campaigns-and-partnerships/github-sponsors>
- Open Source Europe (formerly Open Collective Europe) 8% host fee:
  <https://opencollective.com/europe> ·
  <https://documentation.opencollective.com/fiscal-hosts/setting-up-a-fiscal-host/setting-your-fiscal-host-fees>
- Liberapay 0% platform fee, donation-funded model:
  <https://en.liberapay.com/about/faq> · <https://en.wikipedia.org/wiki/Liberapay>
- Liberapay processing-fee averages (Stripe ~3.1%, PayPal ~5.1%):
  <https://en.liberapay.com/about/payment-processors>
- Ko-fi 0% on donations free plan / Ko-fi Gold; Buy Me a Coffee flat 5%;
  ~2.9% + $0.30 processing: <https://earnifyhub.com/blog/kofi-vs-buy-me-a-coffee> ·
  <https://talks.co/p/kofi-vs-buy-me-a-coffee/>
- Stripe EEA card pricing (~1.5% + €0.25) is provider-published standard
  pricing; treat the exact number as `[UNVERIFIED]` here — confirm on
  stripe.com for the maintainer's country before launch.

### Provider recommendation for Infra Atlas

The "no accounts, ever" rule applies to *Infra Atlas's own users*, not to the
maintainer's choice of payout rail — but it argues for keeping the *donor*
experience account-free too.

- **Primary: Open Collective via Open Source Europe** — the public ledger is a
  genuine donation *driver* (§3) and is on-brand for an editorial,
  soon-to-be-open-source project; the EU fiscal host removes the need for a
  company. Cost: ~11–13% all-in. `[ESTIMATE]` that transparency value outweighs
  the fee vs Liberapay.
- **Plus a low-friction one-off option: Ko-fi** (0% platform on tips, one-off-
  first, no donor account) to capture the impulse "this saved me hours" tip
  that a recurring-first platform loses.
- **GitHub Sponsors** is worth adding once the repo is public — it is 0% on
  personal sponsorships and the audience overlap is high — but the GitHub-login
  requirement makes it a secondary, not primary, channel.
- **Liberapay** is the cheapest and most ideologically aligned (non-profit,
  0% fee) but its weak one-off support and small reach make it a "nice to also
  have," not the main rail.
- **Stripe-direct** only if the maintainer wants full control and is willing to
  own the donate page, receipts, and EU VAT/accounting.

---

## Bottom line

Real comparables (caniuse: ~540 patrons / ~€170/mo; top-of-Liberapay: ~1,000
patrons / ~€450–650/wk; "ten years, two donations") show donation-only funding
for a solo reference site realistically yields **hosting-and-coffee money, not
a salary**. Plan for **~0.01–0.05% of monthly users** to donate (`[ESTIMATE]`,
mostly one-off), drive donations with **gratitude-moment placement, a named
solo maintainer, a public costs/expense ledger, and 3–4 anchored amounts
(~€3/€5/€10 + custom)**, minimise friction with a **one-off default** and an
**account-free donor path**, and keep it a **pure tip jar with no perks**
(perks can backfire). Provider mix: **Open Collective (Open Source Europe) for
transparency + Ko-fi for low-friction one-offs**, GitHub Sponsors as a
secondary channel once the repo is public.
