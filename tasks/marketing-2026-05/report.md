# Infra Atlas — Marketing & Positioning Audit
## Report · 2026-05-17

A strategy to grow the right audience, build sustainable **donation** revenue,
and protect the editorial brand from SaaS drift. Donations are the *only*
revenue model. Reference class: developer-tool OSS with a tip jar (htmx, caniuse,
ripgrep, Vantage) — not a venture SaaS launch.

**Read this in 10 minutes.** The full reasoning, every citation, and every
scored recommendation are in the linked phase documents.

---

### In one paragraph

Infra Atlas is a genuinely good, genuinely distinctive product with three things
missing *around* it: the repo is **private** (so "open-source" is currently
false and every GitHub link 404s), there is **no way to donate** a single euro,
and there is **no analytics** (so nothing is measurable). Fix those three, build
the SEO base the site entirely lacks, and grow through a small number of
high-trust channels — infra newsletters, one Show HN, lobste.rs — that *reward*
the dry editorial voice instead of taxing it. Donations will realistically cover
hosting and coffee, not a salary; that is the honest, deliberate trade for a
neutral, no-product reference. The brand is the asset — the 13-entry anti-list
exists to protect it.

---

### The diagnosis — three blockers

From [`audit.md`](audit.md):

1. 🔴 **The GitHub repo is private.** `"visibility":"PRIVATE"`, 0 stars. The
   footer, manifesto and README all advertise "open-source on GitHub" — those
   links 404 for everyone. Nothing — stars, contributors, Sponsors, awesome-list
   backlinks, an honest Show HN — can happen until this is fixed.
2. 🔴 **No donation surface of any kind.** No `/support` page, no `FUNDING.yml`,
   no Ko-fi / Open Collective / Sponsors. Donations are the *only* revenue model
   and there is currently no way to give.
3. 🟠 **No analytics.** Every growth recommendation is unmeasurable until this
   lands. It is the blocking dependency for the whole 90-day plan.

The site itself is not the problem. The voice — editorial, dry, exacting — is a
real asset and shows no drift. The gap is everything *around* the product:
discovery, donations, measurement.

---

### The positioning — why it deserves to exist

In one sentence ([`positioning.md`](positioning.md) §3b):

> Vendor docs are single-cloud and selling you something; Vantage's comparator
> is lead-gen for a paid FinOps product and AWS-centric — **Infra Atlas is the
> only cross-cloud infrastructure reference that is genuinely free, genuinely
> neutral (no product to upsell), and genuinely *edited*** (it explains the
> asterisks instead of hiding them).

Primary audience: the senior cloud/platform engineer doing architecture work,
five vendor-doc tabs open, who distrusts marketing copy. Secondary: the solutions
architect doing APIM vendor selection. The literary tone is a deliberate filter —
it excludes the cert-cram crowd by design, and that is correct.

---

### The strategy in brief

- **Growth ([`growth.md`](growth.md))** — three slow compounding loops, no
  funnel: *discovery* (SEO base + a few launch spikes), *trust* (methodology
  page, neutrality, dated freshness, a named maintainer), *citation* (open data
  → backlinks). Five channels: infra newsletters (top — an editor linking you is
  endorsement and sidesteps every self-promo rule), one Show HN, lobste.rs (if
  invited), LinkedIn (APIM persona only), Dev.to cross-posts (SEO only). Three
  dated launch moments in six months. A monthly "Field Notes" essay is the
  highest-leverage move a solo maintainer has.

- **Donations ([`donations.md`](donations.md))** — Ko-fi for low-friction
  one-offs + Open Collective (Open Source Europe fiscal host) for a public
  ledger + GitHub Sponsors once the repo is public. The ask is editorial,
  honest, quiet — placed at the *moment of gratitude* (end of an instrument, foot
  of an essay), never as a popup. Anchored amounts €3/€5/€10. A public expense
  ledger is on-brand and converts better than an open-ended ask.

- **Measurement ([`measurement.md`](measurement.md), [`analytics-install.md`](analytics-install.md))**
  — Plausible Cloud (EU, cookieless, no banner, first-party proxied) + Google
  Search Console. Measure **returning practitioners** and **costs covered**, not
  pageviews or stars. A public `/state` page shows the periodical's own
  circulation figures.

- **The anti-list ([`anti-list.md`](anti-list.md))** — 13 explicit "do nots"
  (no popups, no AI SEO farm, no paid placements, no paywalling free data, no
  SaaS tier, no dark-pattern donation framing). The test for any future tactic:
  does it keep the site calm, free, neutral, privacy-respecting and editorial?

---

### The honest frame — set expectations now

caniuse — a famous, daily-used, single-maintainer reference site — converts a
massive audience to **~540 patrons and ~€170/month** ([`research/donation-economics.md`](research/donation-economics.md)).
That is the realistic ceiling. Donations cover the domain, hosting, and the
~€90–100/yr analytics line — and a symbolic thank-you. They are **not** income.
Build the surface well, then judge it against "the lights are paid for," not a
salary. Every commercially-*sustained* comparable (Vantage, crontab.guru, httpie)
monetizes an attached paid product; Infra Atlas has deliberately declined that.
That is a legitimate choice — it just caps the resourcing, and that must be
accepted consciously, not discovered with disappointment.

---

### Do these three things this week

1. **Make the repo public** — after scrubbing the history for anything
   sensitive. This single act makes "open-source" true again and unblocks the
   Show HN, awesome-list backlinks, GitHub Sponsors and contributors. *(Then
   refresh the stale README and fix the `LICENSE` so GitHub detects MIT.)*

2. **Stand up a donation surface** — at minimum a Ko-fi page and a
   `.github/FUNDING.yml`. Right now there is literally no way to give a euro;
   Ko-fi takes an hour and needs no fiscal host. *(Also submit the Open
   Collective / Open Source Europe application now — it has approval latency, so
   start the clock.)*

3. **Create the Plausible site and deploy the Cloudflare proxy** — start the
   analytics install ([`analytics-install.md`](analytics-install.md) §6.5b).
   Until it lands, every other recommendation here is unmeasurable guesswork.

*(And kick off the two slow latency items: the Open Collective application, and
asking around for a lobste.rs invite.)*

---

### The 90-day shape

Weekly detail in [`plan-90d.md`](plan-90d.md):

| Weeks | Outcome |
|-------|---------|
| 1–2 | Repo public · donation rails live · **analytics installed & verified** |
| 3–4 | SEO table-stakes shipped · first Field Notes essay |
| 5–6 | Show HN + awesome-list PRs + newsletter submissions |
| 7–8 | lobste.rs · Dev.to · newsletter follow-through |
| 9–10 | Contributor scaffolding · public roadmap |
| 11–12 | APIM-matrix launch · public `/state` · 90-day review |

It is a sequence, not a deadline — solo evenings-and-weekends work. If time is
short, the minimum viable path is Week 1 → Week 2 → Week 3 → the Show HN; the
editorial cadence and contributor work can each slip a month without breaking
the foundation.

---

### Deliverables in this folder

| File | Phase |
|------|-------|
| [`audit.md`](audit.md) | 1 — Inventory & current state |
| [`research/comparable-projects.md`](research/comparable-projects.md) | 2 — Growth/sustainability of comparables |
| [`research/donation-economics.md`](research/donation-economics.md) | 2 — Donation economics |
| [`research/channels.md`](research/channels.md) | 2 — Discovery channels |
| [`research/seo.md`](research/seo.md) | 2 — SEO & search intent |
| [`positioning.md`](positioning.md) | 3 — Audience, positioning, voice |
| [`growth.md`](growth.md) | 4 — Growth strategy |
| [`donations.md`](donations.md) | 5 — Donation strategy |
| [`measurement.md`](measurement.md) | 6 — Measurement |
| [`analytics-install.md`](analytics-install.md) | 6.5 — Analytics install runbook |
| [`anti-list.md`](anti-list.md) | 7 — Risks & anti-patterns |
| [`plan-90d.md`](plan-90d.md) | 8 — 90-day plan |
| `report.md` | This summary |

Every recommendation in the phase documents carries `rationale · evidence link ·
effort (S/M/L) · brand-fit (1–5) · expected impact`. Every external claim cites
a URL; estimates are labelled as estimates.
