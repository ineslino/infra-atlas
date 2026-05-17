# Phase 3 — Positioning

## 3a · Audience

The site's literary, no-hand-holding tone is a filter, and that is *intentional*.
It excludes the cert-cram / "explain it like I'm new" crowd by design — so this
strategy embraces that and does not chase them.

**Primary persona — the senior cloud / platform engineer doing architecture
work.** Has five vendor-doc tabs open, is choosing regions, instance families,
or an API gateway, and distrusts marketing copy. Already routes around official
docs to third-party references — the 2026-05 feature research recorded the
verbatim signal *"everyone I knew used Vantage instead of the official page"*
and *"AWS docs full of fluff"* (`tasks/features-2026-05/research/user-intent.md`).
Wants dense, filterable, footnoted tables and vendor neutrality. This persona is
the centre of gravity for every recommendation.

**Secondary persona — the solutions architect / consultant doing vendor
selection**, especially on the API-management side (enterprise architects
evaluating Apigee vs Kong vs Azure APIM). Builds proposals, needs a neutral
source to cite, and — unlike the primary — is reachable on LinkedIn. The 5 APIM
instruments and the cross-cloud matrices serve this persona.

**Not targeted** (state it so the strategy stays focused): students / cert
crammers, no-code / beginner audiences, and "AI hype" GPU-tourists. AI/ML
practitioners hunting GPU availability are a *sub-segment of the primary*, not a
separate persona — served, not courted.

## 3b · Positioning statement

> Infra Atlas is a free, vendor-neutral **reference periodical** for cloud and
> API-management infrastructure. It is the cross-referenced almanac the vendor
> docs never wrote: every region, instance type, and API-gateway capability laid
> out side by side, filterable, and footnoted — kept honest because no vendor
> pays for its place and there is nothing to sell you. It replaces the five tabs
> of vendor documentation, the stale Notion spreadsheet, and the senior
> engineer's tribal knowledge that the answer currently lives in.

**One sentence — why it deserves to exist next to Vantage and vendor docs:**

> Vendor docs are single-cloud and selling you something; Vantage's comparator
> is lead-gen for a paid FinOps product and AWS-centric — Infra Atlas is the
> only cross-cloud infrastructure reference that is genuinely free, genuinely
> neutral (no product to upsell), and genuinely *edited* (it explains the
> asterisks instead of hiding them).

Evidence the wedge is real: the feature-review competitive scan found *no single
competitor is free + neutral + readable at once* — data tools (Vantage, DevZero,
cloudprice) are lead-gen for paid SaaS; Cloud Mercato is enterprise-gated;
Gartner is paywalled; hyperscaler calculators are single-vendor by construction
(`tasks/features-2026-05/research/competitive.md`).

## 3c · Voice & brand guardrails

One page. Codified so contributors don't drift it.

**Three voice adjectives:**

| Adjective | In-voice | Off-voice |
|-----------|----------|-----------|
| **Editorial** | "A note from the cartographer." · "Issue No. 01." | "Welcome to Infra Atlas! 🚀" |
| **Exacting** | "31 families · ~700 size variants · with the asterisks intact." | "Tons of instance types and more!" |
| **Dry** | "This page isn't on the map." (the 404) | "Oops! Looks like you got lost 😅" |

**Words / patterns to avoid:** *revolutionize, AI-powered, platform, solution,
empower, seamless, supercharge, game-changer, unlock, leverage, "we're excited
to", "blazing fast"*; emoji in headings; exclamation marks; growth-marketing
verbs.

**Words / patterns that fit:** *instrument, atlas, almanac, observatory, the
cartographer, issue, department, footnote, "asterisks intact", cross-reference,
periodical, reference, curated, snapshot*.

**Tone modulation:**
- *Editorial copy* (manifesto, Field Notes, the donation ask) — serious,
  considered, first-person-singular as "the cartographer".
- *Tool descriptions* — dry and factual; state what the instrument does, no sell.
- *Data labels & footnotes* — terse; numbers and codes, no adjectives.

**The donation ask is held to the same bar.** It is editorial, never pleading,
never urgent — see `donations.md` §5a.
