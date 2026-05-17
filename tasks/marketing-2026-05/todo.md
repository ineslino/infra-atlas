# Infra Atlas — Marketing & Positioning Audit · 2026-05

**Mission:** a strategy document that grows the right audience, builds
sustainable **donation** revenue, and protects the editorial brand from SaaS
drift. Donations are the *only* revenue. Reference class: developer-tool OSS
with a tip jar (htmx, caddy, caniuse, ripgrep, Vantage) — **not** a SaaS launch.

## Recon (done 2026-05-17, before research)

- **No donation surface anywhere.** Grep found zero donate / sponsor / ko-fi /
  liberapay / opencollective mentions; no `.github/FUNDING.yml`. This is the #1
  gap — Phase 5 is the priority deliverable.
- **No analytics installed.** Every growth recommendation is unmeasurable until
  Phase 6.5 ships — it is a blocking dependency for the 90-day plan.
- **No SEO infrastructure** — no `robots.txt`, no `sitemap.xml`, no JSON-LD
  structured data on any page.
- **No contributor scaffolding** — `.github/` holds only the 3 workflows; no
  issue templates, no PR template, no public roadmap, no good-first-issues.
- **README is stale** — "11/11 instruments" (now 16), "Live … *(coming soon)*"
  (it is live), stale data-sources table, no badges, a thin Contributing note.
- OG tags, `favicon.svg`, per-page meta descriptions and canonicals **are** in
  place — a decent share/SEO baseline to build on.
- 16 instruments; editorial "periodical" brand; EU-based solo maintainer (Inês);
  Cloudflare Pages hosting. The site itself is genuinely good — the gap is
  everything *around* it: discovery, donations, measurement.

## Phases

- [x] **P1** — Inventory & current state → `audit.md`
- [x] **P2** — External research, 4 subagents → `research/{comparable-projects,donation-economics,channels,seo}.md`
- [x] **P3** — Positioning → `positioning.md`
- [x] **P4** — Growth strategy → `growth.md`
- [x] **P5** — Donation strategy → `donations.md`
- [x] **P6** — Measurement → `measurement.md`
- [x] **P6.5** — Analytics install plan → `analytics-install.md`
- [x] **P7** — Risks & anti-patterns → `anti-list.md`
- [x] **P8** — 90-day plan → `plan-90d.md`
- [x] **Wrap** — `report.md` + update `progress.md`, `session_summary.md`

## Truthful-status notes

- Traffic, search rankings, donor numbers: **unmeasurable today** — no analytics,
  no donations. The audit states this plainly; Phase 6.5 closes the gap.
- GitHub stars / contributors: taken from `gh repo view` at audit time.
- Every recommendation carries: `rationale · evidence link · effort (S/M/L) ·
  brand-fit (1–5) · expected impact`.
