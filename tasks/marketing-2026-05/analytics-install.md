# Phase 6.5 — Analytics install plan

The site has **no analytics**. Until it does, every recommendation in this
strategy is unmeasurable. This is a runbook, not an essay — ship it in week 1.

## 6.5a · Tool choice

Constraints (non-negotiable): no Google Analytics; GDPR-compliant with **no
cookie banner**; EU-hosted or self-hostable; script < 5 KB; public-dashboard
mode; open-source preferred.

| Tool | Cost | Brand fit | Public dashboard | Self-host | Script | Verdict |
|------|------|-----------|------------------|-----------|--------|---------|
| **Plausible Cloud (EU)** | ~€9/mo | ★★★★★ EU, OSS, cookieless | ✅ built-in, one link | optional | ~1 KB | **Recommended** |
| GoatCounter | €0 (donations) | ★★★★★ tiny, OSS, EU | ✅ | ✅ | <3.5 KB | Zero-budget fallback |
| Umami | €0 self-host | ★★★★ OSS | ✅ | ✅ (needs DB) | ~2 KB | Adds a server+DB — breaks "no backend" |
| Fathom | ~$15/mo | ★★★★ | ❌ no public dashboard | ❌ | ~1.6 KB | Fails the `/state` requirement |
| Pirsch | ~€6/mo | ★★★★ EU | ✅ | ❌ | ~3 KB | Fine, but no edge over Plausible |
| Cloudflare Web Analytics | €0 | ★★★ | ❌ | n/a | beacon | **Complement only** — no events, no `/state` |

**Recommendation: Plausible Cloud (EU).** Three lines: (1) it is the only option
that does first-class **custom events with properties** — without which the
Phase 5d donation-conversion funnel cannot be measured — *and* a built-in public
dashboard for the `/state` page; (2) it is EU-hosted, open-source, cookieless →
no banner, perfect brand fit; (3) ~€90–100/yr is a *legitimate, transparent
expense* — it becomes the first honest line item on the public donation ledger
("Plausible keeps the lights measurable"), which is on-message, not off it. Zero
ops burden — the site stays backend-free. **Fallback if €0 expenses are a hard
constraint: GoatCounter self-hosted.** Cloudflare Web Analytics: turn it on
today as a free sanity baseline; it cannot do events or `/state`, so it is not
the primary.

## 6.5b · Install runbook

**Stack confirmed:** plain static HTML, no framework, deployed on Cloudflare
Pages. A shared `nav.js` is already injected on every page via
`<script src="/nav.js" defer>`. There is a `_headers` file (Cloudflare).

1. **Create the Plausible site.** plausible.io → add site `infraatlas.dev` (use
   the **apex**, not a subdomain — a subdomain would split attribution). EU data
   region is the default.
2. **First-party proxy via Cloudflare (do this — dev audiences ad-block heavily;
   without it ~30–50% of traffic is invisible).** Plausible's documented
   Cloudflare method: a **Worker** (or Pages Function) that serves the script at
   `infraatlas.dev/js/script.js` and forwards events from `infraatlas.dev/api/event`
   to Plausible. Plausible publishes the Worker script — deploy it, add a route
   for `infraatlas.dev/js/*` and `infraatlas.dev/api/event`.
3. **Inject the snippet — via `nav.js`, not 17 `<head>`s.** Because every page
   already loads `nav.js`, add the loader there (one place, and every future
   instrument is covered automatically). At the top of the `nav.js` IIFE:
   ```js
   // analytics — proxied Plausible, cookieless, no PII
   var ps = document.createElement('script');
   ps.defer = true;
   ps.setAttribute('data-domain', 'infraatlas.dev');
   ps.src = '/js/script.js';                 // first-party proxied path
   ps.setAttribute('data-api', '/api/event');
   document.head.appendChild(ps);
   window.plausible = window.plausible || function () {
     (window.plausible.q = window.plausible.q || []).push(arguments);
   };
   ```
   `nav.js` is itself `defer` → the analytics script is non-render-blocking and
   loads after content. Acceptable: pageview timing is not LCP-critical.
   *(Per-page `<head>` injection is the textbook static-site method; here the
   pre-existing shared `nav.js` makes single-point injection the better fit.)*
4. **CSP / `_headers`.** With first-party proxying, the script and events are
   same-origin — if a `Content-Security-Policy` is later added, `script-src` and
   `connect-src` only need `'self'`. No third-party origin to allowlist. (Today
   `_headers` has no CSP; nothing to change now.)
5. **Verify** — see §6.5g.

## 6.5c · Event taxonomy

Pageviews alone can't measure the donation moments (Phase 5d). Minimal,
snake_case, low-cardinality events — fired via `plausible('name', {props:{…}})`:

| Event | Properties | Fires when |
|-------|-----------|-----------|
| `instrument_open` | `instrument` | an instrument page loads |
| `filter_apply` | `instrument`, `filter_type` | a filter/chip is toggled |
| `cross_reference_click` | `from`, `to` | an in-body link to another instrument |
| `export_click` | `instrument`, `format` | a CSV/JSON export (once it exists) |
| `share_click` | `instrument` | a permalink/share action |
| `donation_cta_view` | `placement` | a donation ask scrolls into view |
| `donation_cta_click` | `placement`, `provider` | a donation ask is clicked |
| `outbound_click` | `destination` (domain only) | an external link |
| `editorial_read_complete` | `slug` | ≥90% scroll on a Field Notes page |

**Rules:** no PII ever; no user IDs, no fingerprinting; cap distinct property
values (`instrument` ≤ ~20, `provider` ≤ 4 — high cardinality breaks dashboards
and can cost money). **Document every event in `docs/analytics-events.md`** when
it is wired, so future contributors don't invent a parallel taxonomy.

## 6.5d · First dashboards

Save these as Plausible filtered views — the 90-day plan depends on them:
1. **Acquisition** — top referrers by week (HN / Reddit / Mastodon / search / direct / newsletter).
2. **Audience** — monthly uniques, returning-visitor share, country.
3. **Engagement per instrument** — `instrument_open` rate, `filter_apply` per session, time on page, exit rate.
4. **Donation funnel** — `donation_cta_view` → `donation_cta_click` → confirmed
   donation (the last step reconciled manually against the provider, since the
   redirect leaves the site).
5. **Content health** — top 10 entry pages, top 10 exit pages, top search queries.

## 6.5e · Public `/state` dashboard

Plausible supports a shared public dashboard via one link. Wire this as part of
the install, not later. Public: monthly uniques ✅, top pages ✅. Not public:
referrers ❌ (exposes channel strategy, invites gaming). Combine on one `/state`
page with donations-to-date + expenses-YTD (those come from the donation
provider, not analytics — see `donations.md` §5c). On-brand: it is the
periodical showing its own circulation figures.

## 6.5f · Privacy & compliance

- Add a one-paragraph `/privacy` page: what's collected (aggregate pageviews +
  the events above, no cookies, no PII, no cross-site identity), retention, and
  the provider (Plausible, EU). No legalese.
- Link `/privacy` from the footer colophon.
- **No cookie banner.** Plausible is cookieless and uses no persistent
  identifier — under current EU guidance it needs no consent banner. A cookie
  banner on a privacy-respecting site undermines the very claim. Do not add one.

## 6.5g · Verification — don't claim "installed" until

- A test pageview appears in the Plausible dashboard from a clean browser within 60 s.
- At least one custom event (`instrument_open`) fires and shows in real-time view.
- Homepage Lighthouse performance score is within 1 point of the pre-install baseline.
- DevTools Performance confirms the script does not block render.
- uBlock Origin (default lists) is tested — the first-party `/js/script.js` path
  evades it; if any gap remains it is consciously accepted and noted.
- `/privacy` exists and is linked from the footer.
- `docs/analytics-events.md` exists and lists every event the code actually fires.
