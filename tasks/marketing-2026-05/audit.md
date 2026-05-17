# Phase 1 — Inventory & current state

Audit of infraatlas.dev's marketing surface, 2026-05-17. Findings only —
recommendations come in Phases 3–8. Severity: 🔴 blocker · 🟠 major gap · 🟡 polish.

## Headline gaps (read this first)

1. 🔴 **The GitHub repo is private.** `gh repo view` → `"visibility":"PRIVATE"`,
   0 stars, 0 forks. The site's footer, manifesto and README all say
   "open-source / MIT-licensed on GitHub" and link to `github.com/ineslino/infraatlas`
   — every one of those links **404s for the public**. "Open-source" is the
   site's positioning *and is currently not true*. Nothing in this strategy —
   stars, contributors, GitHub Sponsors, good-first-issues — can happen until
   the repo is public. **Week-1 blocker.**
2. 🔴 **No donation surface of any kind.** No `/support` page, no footer link,
   no `.github/FUNDING.yml`, no Ko-fi / Liberapay / Open Collective / Sponsors —
   grep found zero. Donations are the *only* revenue model and there is
   currently no way to give. **The biggest revenue gap.**
3. 🟠 **No analytics.** Nothing installed. Every growth recommendation in this
   document is unmeasurable until this is fixed (Phase 6.5).

## 1a · On-site marketing surface

- **The hook (first 3 seconds).** Hero: the serif wordmark "Infra Atlas.", the
  eyebrow "A New Periodical of Infrastructure", then a lead naming "cloud
  regions, instance types, API gateways, service quotas." The editorial framing
  is **distinctive and memorable** — it does not read as AI-generated SaaS. Risk:
  the `<h1>` itself is just the wordmark; a cold visitor relies on the lead
  paragraph to learn this is a *cloud reference tool*. Helps the brand; mild cost
  to instant comprehension. 🟡
- **Value props vs proof.** Hero stat cards: "16 / 16 instruments shipping
  today", "5 cloud providers", "7 APIM platforms", "€0 cost to read". Credible
  and on-brand; "€0" is the memorable one. No social proof (stars, "used by",
  press) — acceptable for a 2-day-old project, but nothing yet says *others
  trust this*. 🟡
- **Conversion paths.** None beyond "Open" an instrument. No donate CTA, no
  star-the-repo CTA, no follow/subscribe. The implicit goal of a visit is
  undefined. **Define it:** primary = "use an instrument and trust it"; the
  marketing job is then (a) be found, (b) convert a fraction of grateful users
  to donors/stargazers. 🟠
- **Donation surface.** None. See headline gap #2.
- **Social / share.** OG tags (`og:title/description/image/url` + width/height/
  alt), `twitter:card=summary_large_image`, `favicon.svg`, per-page meta
  descriptions and canonicals — **all present**. A solid share baseline. Caveat:
  `og.png` is a static asset that may still read "11 instruments" (stale — the
  site has 16); needs a visual check. 🟡
- **SEO basics.** Title tags ✓, one `<h1>` per page (the masthead) ✓, canonical
  URLs ✓. **Missing: `robots.txt`, `sitemap.xml`, and any JSON-LD structured
  data** (`Dataset`, `SoftwareApplication`, `TechArticle`). For a 16-page
  reference site, a sitemap + per-instrument `Dataset` schema is low-effort,
  high-leverage. 🟠
- **Performance.** Static HTML on the Cloudflare CDN; fonts via Google Fonts
  with `preconnect`. The prior 2026-05 review fixed an EC2 layout shift
  (CLS 0.237 → 0.012). LCP was **not** freshly measured in this audit — *truthful
  status:* propose Lighthouse CI in the repo + real-user monitoring once
  analytics lands (Phase 6.5). 🟡

## 1b · Brand and voice

- **Voice — three adjectives from the actual copy:** **editorial, dry, exacting.**
  Evidence: "A New Periodical of Infrastructure", "a note from the cartographer",
  "with the asterisks intact", "got tired of grepping vendor docs across five
  tabs", the 404's "This page isn't on the map." It is genuinely literary and
  un-SaaS — a real asset. No drift found in the copy audited.
- **Visual identity.** Instrument Serif / JetBrains Mono / Manrope; dark
  ink-on-paper palette; the 3-ring contour logo; "Issue No. 01", "Department I/
  II/III", colophon. The token system is coherent site-wide (verified in the
  prior UI audit). The periodical/almanac metaphor is consistently executed.
- **Naming.** "instruments", "departments", "the cartographer", and the per-tool
  nouns (Observatory / Atlas / Index / Matrix / Catalogue / Finder / Footprint).
  The metaphor holds at the tool level — mastheads, status blocks and footnotes
  carry it through. Intentional noun variety, on-brand.

## 1c · Distribution surface

- **GitHub repo.** Exists (`github.com/ineslino/infraatlas`), created 2026-05-15,
  **private** (blocker #1). README is 141 lines but **stale**: says "11/11
  instruments" (now 16), "Live … *(coming soon)*" (it is live), a data-sources
  table that predates the live-API instruments, **no badges**, and a 3-line
  Contributing section. License detected by GitHub as `"other"`, not `MIT` —
  the `LICENSE` file isn't matching GitHub's MIT detector. Repo "About" homepage
  URL field is empty. 1 human contributor (the maintainer) + the refresh bot. 🟠
- **Social presence.** No accounts found (Twitter/X, Mastodon, Bluesky,
  LinkedIn) — *unverified, none referenced anywhere on the site or repo.* 🟠
- **Newsletter / RSS.** None. `feed.json` exists but it is a private JSON the
  landing page reads for its "What Changed" section — not a subscribable RSS/
  Atom feed and not advertised. 🟠
- **Analytics.** None — see headline gap #3. Can't market what you can't measure.

## 1d · Funding surface

- **Donation channels.** None — no GitHub Sponsors (`FUNDING.yml` absent), Open
  Collective, Ko-fi, Buy Me a Coffee, Liberapay, Stripe, or crypto. 🔴
- **Transparency.** No public ledger of donations/expenses — moot until
  donations exist, but Phase 5 should design it *before* the first donation.
- **Tax/legal.** Maintainer is EU-based and solo. Donations to an individual vs
  a fiscal host (Open Collective + a host like OCF) is a real trade-off —
  flagged here, resolved in Phase 5b.

## What the audit could NOT measure (truthful status)

- Traffic, unique visitors, referrers, bounce — **no analytics installed.**
- Search rankings for target queries — needs the Phase 2d research pass.
- Donor count / revenue — **no donation channel exists.**
- Real-user LCP — needs RUM. All three are unblocked by Phase 6.5.
