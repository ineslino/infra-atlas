# Phase 5 — Donation strategy

Donations are the **only** revenue model — no ads, no tiers, no accounts, no
product (mission hard rule). This phase designs the donation surface, picks
providers, and — just as importantly — fixes expectations so low revenue is not
mistaken for failure.

Full economics, conversion benchmarks and provider comparison:
[`research/donation-economics.md`](research/donation-economics.md).
Recommendation format as in [`growth.md`](growth.md):
`rationale · evidence · effort · brand-fit (1–5) · impact`.

---

## 5a · The honest frame — size the expectation before building anything

The single most important number in the research: **caniuse — a famous,
daily-used, single-maintainer reference site — converts a massive audience to
~539 patrons and ~€167.9/month** ([`research/donation-economics.md`](research/donation-economics.md)
§1; [patreon.com/caniuse](https://www.patreon.com/caniuse), observed 2026-05-17).
Oh My Zsh raises ~$4.2k/year despite 2,000+ contributors; Homebrew reaches
~$100k/year *only* because it is installed on millions of machines
([`research/comparable-projects.md`](research/comparable-projects.md) §Homebrew,
§"Oh My Zsh"). A Java maintainer had "a donation link for ten years, got two
donations" ([`research/donation-economics.md`](research/donation-economics.md)
§1).

**Planning assumption:** 0.01–0.05% of monthly active users donate, mostly
one-off (`[ESTIMATE]`, triangulated from caniuse —
[`research/donation-economics.md`](research/donation-economics.md) §2). Concrete
sanity check: at 100k monthly visitors and 0.03% one-off conversion at a ~€5
median tip, that is **~€150/month gross before fees** — i.e. roughly the caniuse
outcome.

So: donations realistically cover **hosting, the domain, and the Plausible
analytics line** ([`analytics-install.md`](analytics-install.md) §6.5a) — and a
symbolic thank-you for the maintainer's evenings. They are not income. Build the
surface well, then judge it against "the lights are paid for," not against a
salary. Setting this expectation *now* is itself a deliverable.

---

## 5b · What donations are — and are NOT — for

Stated explicitly so future growth pressure cannot quietly relitigate it.
Every "NOT" cross-references [`anti-list.md`](anti-list.md).

**Donations ARE for:**

- Hosting and the domain (Cloudflare Pages is currently ~free; the domain is a
  real annual cost).
- The Plausible analytics subscription (~€90–100/yr) — the *first honest line
  item* on the public ledger.
- A symbolic thank-you for the solo maintainer's unpaid time.

**Donations are NOT for, and never will be:**

- **Not a precondition for access.** The data is €0 to read, always, regardless
  of how much (or how little) is donated. "€0 cost to read" is a homepage
  promise ([`anti-list.md`](anti-list.md) #7).
- **Not tiered.** No perks, no "supporter" badges, no donor-only features, no
  paywalled data — ever. Perks also *backfire*: tangible thank-you gifts can
  *reduce* giving by reframing a gift as a transaction
  ([`research/donation-economics.md`](research/donation-economics.md) §3
  "counter-driver"). It stays a pure tip jar ([`anti-list.md`](anti-list.md)
  #7, #9).
- **Not income, not a salary.** See §5a — framing it as income guarantees the
  project reads as a failure.
- **Not a substitute for neutrality.** No paid placements, no sponsored vendor
  rows, no "comparison" pages that favour a payer — vendor neutrality *is* the
  product ([`anti-list.md`](anti-list.md) #4, #10).
- **Not extracted with pressure.** No fake urgency, no scarcity, no guilt, no
  exit-intent popups ([`anti-list.md`](anti-list.md) #2, #12) — see §5d.

---

## 5c · Provider choice

The research recommendation: **Open Collective (Open Source Europe host) for
transparency + Ko-fi for low-friction one-offs**, GitHub Sponsors as a secondary
channel once the repo is public ([`research/donation-economics.md`](research/donation-economics.md)
§5 "Provider recommendation"). Sequenced by setup latency, not preference:

- **D1 · Ko-fi — the immediate, one-off rail. Launch week 1.** *Rationale:*
  zero setup, **0% platform fee on tips** (free plan), one-off-first UX, no donor
  account required — it captures the "this saved me hours" impulse tip that a
  recurring-first platform loses, and it can go live the same day with no fiscal
  host or approval queue. *Evidence:* [`research/donation-economics.md`](research/donation-economics.md)
  §4, §5. *Effort:* S · *Brand-fit:* 4/5 · *Impact:* donations.

- **D2 · Open Collective via Open Source Europe — the transparency rail. Apply
  week 1, goes live on host approval.** *Rationale:* the public, real-time
  ledger is itself a donation *driver* (§5f) and is perfectly on-brand for an
  editorial-honesty project; Open Source Europe acts as the **EU fiscal/legal
  host** so the solo maintainer needs no registered company. Cost ~11–13%
  all-in — the transparency value is judged to outweigh the fee vs cheaper
  rails. Recurring-first, but also takes one-offs. *Evidence:*
  [`research/donation-economics.md`](research/donation-economics.md) §5;
  [`research/comparable-projects.md`](research/comparable-projects.md) COPY #8.
  *Effort:* M (application + host onboarding) · *Brand-fit:* 5/5 · *Impact:*
  donations.

- **D3 · GitHub Sponsors — secondary, switch on once the repo is public.**
  *Rationale:* **0% on sponsorships from personal accounts** and the audience
  overlap is high (devs) — but it *requires the donor to be logged into a GitHub
  account*, which adds a friction step, so it is a secondary channel, not the
  primary. *Evidence:* [`research/donation-economics.md`](research/donation-economics.md)
  §4, §5. *Effort:* S · *Brand-fit:* 4/5 · *Impact:* donations.

- **D4 · `.github/FUNDING.yml` — wire the repo affordance.** One file enables
  GitHub's native "Sponsor" button and lists `ko_fi`, `open_collective`, and
  `github` together. *Rationale:* free, native repo-side surface; keep it in
  sync with the providers actually live. *Evidence:* [`audit.md`](audit.md) §1d
  (currently absent). *Effort:* S · *Brand-fit:* 5/5 · *Impact:* donations.

**Liberapay** is the cheapest and most ideologically aligned (non-profit, 0%
fee) but has weak one-off support and small reach — a "nice to also have," kept
*off* the donation surface for now to avoid choice overload
([`research/donation-economics.md`](research/donation-economics.md) §5). Add it
later only if asked for. **Stripe-direct** is rejected for now: lowest fees but
the maintainer would own the donate page, receipts and EU VAT/accounting alone
([`research/donation-economics.md`](research/donation-economics.md) §5).

**Keep the surface short.** Three providers exist, but the donor is shown a
*two-way* choice framed by intent — *one-off tip* (Ko-fi) vs *recurring + see
the books* (Open Collective) — with GitHub Sponsors listed once, lower down, for
those who prefer it. A wall of four equal buttons is decision friction
([`research/comparable-projects.md`](research/comparable-projects.md) COPY #8).

---

## 5d · The donation surface — placement & copy

The audit found **no donation surface anywhere** — no `/support` page, no footer
link, no `FUNDING.yml` ([`audit.md`](audit.md) headline #2). Donations cluster
at the **moment of received value** — the gratitude reflex lifts both *whether*
someone gives and *how much* ([`research/donation-economics.md`](research/donation-economics.md)
§3). So the surface is placed *where value was just delivered*, never as an
interrupt.

- **D5 · A `/support` page — the full editorial ask.** The honest pitch: who
  runs the site (one named person, EU, evenings), that it is free and
  donation-funded, exactly what the money covers, a link to the public ledger,
  and the provider choice. *Rationale:* a bare "Donate" link with no context
  converts ~95% worse than an ask paired with explanatory copy (Wikimedia A/B
  data) — context is not optional. *Evidence:* [`research/donation-economics.md`](research/donation-economics.md)
  §3, §4. *Effort:* S · *Brand-fit:* 5/5 · *Impact:* donations.

- **D6 · A quiet, persistent footer link** in the colophon ("Support the
  atlas") on every page. *Rationale:* a polite, always-available, never-modal
  ask is the on-brand baseline; >75% of donors who give do so on the first or
  second impression, so a calm permanent link suffices — repeated modals annoy
  without converting. *Evidence:* [`research/donation-economics.md`](research/donation-economics.md)
  §4 "banner fatigue". *Effort:* S · *Brand-fit:* 5/5 · *Impact:* donations.

- **D7 · A gratitude-moment module at the *end* of instruments and Field Notes
  essays.** A calm, in-flow block after the reader has been helped — after a
  comparison table, at the foot of an essay — not a popup, not mid-content.
  *Rationale:* this is the gratitude-reflex placement; caniuse's strongest
  small-dollar lever ("donate to remove ads") is unavailable here since ads are
  ruled out, so Infra Atlas must *over-invest in the moment-of-gratitude prompt*
  to compensate. *Evidence:* [`research/donation-economics.md`](research/donation-economics.md)
  §3; [`research/comparable-projects.md`](research/comparable-projects.md)
  §caniuse, AVOID #3. *Effort:* M · *Brand-fit:* 4/5 · *Impact:* donations.

- **D8 · Amounts: €3 / €5 / €10 + a custom field, one-off as the default,
  €5 visually highlighted.** *Rationale:* 3–4 anchored presets plus an "other"
  field is the CRO-optimal layout; anchor low and concrete for a dev audience;
  default to one-off because ~70% of donors are one-time and a recurring default
  adds a commitment decision at the worst moment. *Evidence:*
  [`research/donation-economics.md`](research/donation-economics.md) §3
  "anchoring", §4 "recurring-default". *Effort:* S (mostly Ko-fi/OC config) ·
  *Brand-fit:* 4/5 · *Impact:* donations.

**The ask copy** — held to the editorial bar ([`positioning.md`](positioning.md)
§3c: editorial, never pleading, never urgent). Draft:

> Infra Atlas is made by one person, in the evenings, in the EU. No investors,
> no ads, no vendor money, nothing to sell you — which is the whole point:
> nothing pulls the data off-true. It does cost a little to run: a domain,
> hosting, and the analytics that keep it measurable. If the atlas saved you a
> morning of grepping vendor docs across five tabs, you can cover a slice of
> that. €0 to read, always. A tip is a thank-you, not a toll.

This names the solo maintainer (a documented donation driver — people fund *a
person*), states what money covers, reaffirms the €0 promise, and carries zero
urgency or guilt ([`research/donation-economics.md`](research/donation-economics.md)
§3; [`anti-list.md`](anti-list.md) #12).

---

## 5e · Conversion moments

The measurable funnel, instrumented via the Phase-6.5 events
([`analytics-install.md`](analytics-install.md) §6.5c):

`donation_cta_view {placement}` → `donation_cta_click {placement, provider}` →
confirmed donation (reconciled manually against the provider — the redirect
leaves the site).

The three `placement` values map to D5/D6/D7: `support_page`, `footer`,
`gratitude_module`. Measuring per-placement view→click→confirm shows which
moment actually converts, so the gratitude module (D7) can be tuned or moved
without guesswork. **Do not** add more placements chasing conversion — banner
fatigue and the anti-list (#1, #2) cap the surface at these three.

---

## 5f · Transparency & the public ledger

For a project whose entire brand is editorial honesty, showing the books is not
a nice-to-have — it is on-message, and it *drives* donations: "showing exactly
where money goes converts better than an open-ended ask"
([`research/donation-economics.md`](research/donation-economics.md) §3).

- **D9 · A public ledger, surfaced on the `/state` page.** Open Collective
  provides a fully public, real-time ledger for free (D2); mirror the headline
  figures — donations-to-date, expenses-YTD — onto the `/state` page alongside
  the Plausible public stats ([`analytics-install.md`](analytics-install.md)
  §6.5e). Itemise expenses honestly (domain €X, hosting €Y, Plausible €Z).
  *Rationale:* Homebrew and Oh My Zsh both run donations transparently through
  Open Collective; a public ledger is a genuine trust multiplier and exactly the
  register of this brand. *Evidence:* [`research/comparable-projects.md`](research/comparable-projects.md)
  §Homebrew, COPY #8; [`research/donation-economics.md`](research/donation-economics.md)
  §3. *Effort:* S (Open Collective does the work; `/state` just links/mirrors) ·
  *Brand-fit:* 5/5 · *Impact:* donations.

- **D10 · An annual "Issue"-style transparency note.** Once a year, a short,
  dry Field Notes-style post: what came in, what it paid for, what is planned.
  *Rationale:* turns the ledger into a periodical ritual, on-brand, and a
  natural honest re-engagement moment. *Evidence:*
  [`research/comparable-projects.md`](research/comparable-projects.md) COPY #9;
  [`research/donation-economics.md`](research/donation-economics.md) §3.
  *Effort:* S/yr · *Brand-fit:* 5/5 · *Impact:* both.

---

## 5g · Summary

| ID | Recommendation | Effort | Brand-fit | When |
|----|----------------|--------|-----------|------|
| D1 | Ko-fi — one-off rail | S | 4/5 | Wk 1 |
| D2 | Open Collective (Open Source Europe) | M | 5/5 | Apply wk 1, live on approval |
| D3 | GitHub Sponsors — secondary | S | 4/5 | Wk 1 (after repo public) |
| D4 | `.github/FUNDING.yml` | S | 5/5 | Wk 1 |
| D5 | `/support` page — full ask | S | 5/5 | Wk 1–2 |
| D6 | Quiet footer link | S | 5/5 | Wk 1–2 |
| D7 | Gratitude-moment module | M | 4/5 | Wk 2 |
| D8 | Anchored amounts €3/€5/€10 + custom | S | 4/5 | Wk 1–2 |
| D9 | Public ledger on `/state` | S | 5/5 | When OC live |
| D10 | Annual transparency note | S/yr | 5/5 | Year 1+ |

**The discipline:** the donation ask is editorial, honest, and *quiet*. It earns
a euro on gratitude, never on pressure. A manipulated ask earns one euro and
loses a reader ([`anti-list.md`](anti-list.md) #12) — and for a trust project,
the reader is worth far more than the euro.
