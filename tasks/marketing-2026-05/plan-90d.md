# Phase 8 — The 90-day plan

A weekly, solo-maintainer-achievable sequence. It turns the strategy
([`growth.md`](growth.md), [`donations.md`](donations.md),
[`measurement.md`](measurement.md)) into an order of operations.

**How to read this.** Each week has a *focus*, 2–4 concrete tasks (cross-referenced
to recommendation IDs), a *blocking dependency*, and a *done-when* check. It is a
**sequence, not a deadline** — this is evenings-and-weekends work; slipping a
week is fine, doing tasks out of order is not. Weeks 2–4 are the heaviest
(analytics + SEO engineering); if anything slips, protect the Week-1 and Week-2
foundation and let the launch move.

| Weeks | Phase | Outcome |
|-------|-------|---------|
| 1–2 | Foundation | Repo public, donation rails live, **analytics installed & verified** |
| 3–4 | SEO + editorial | Search table-stakes shipped, first Field Notes published |
| 5–6 | Launch | Show HN + awesome-list PRs + newsletter submissions |
| 7–8 | Channel activation | lobste.rs, Dev.to, newsletter follow-through |
| 9–10 | Contributor activation | Issue/PR templates, good-first-issues, public roadmap |
| 11–12 | Launch 2 + transparency | APIM matrix launch, public `/state`, 90-day review |

**Critical path:** repo public → analytics verified → donation funnel
instrumented → SEO table-stakes → Show HN. Nothing downstream of a broken link
in that chain should start early.

**Two things have external latency — start them in Week 1–2, do not wait:**
the Open Collective / Open Source Europe fiscal-host application (D2), and the
lobste.rs invite (C3).

---

## Week 1 — Repo public + donation rails

**Focus:** unblock everything. The repo being private makes "open-source" false
and 404s every GitHub link ([`audit.md`](audit.md) headline #1).

- [ ] **Audit repo history for secrets / PII before flipping visibility** — once
  public it is public; httpie's lost ~54k stars is the cautionary tale
  ([`research/comparable-projects.md`](research/comparable-projects.md) §httpie).
- [ ] Make the repo public (**N1**).
- [ ] Refresh the README — "16 instruments", drop "(coming soon)", current
  data-sources table, add badges; fix `LICENSE` so GitHub detects MIT (**N2**).
- [ ] Ko-fi page live — the immediate one-off rail (**D1**).
- [ ] Submit the Open Collective application via **Open Source Europe** (**D2**)
  — *latency item; it goes live on host approval, not on your schedule.*
- [ ] Enable GitHub Sponsors; add `.github/FUNDING.yml` listing `ko_fi` +
  `github` (add `open_collective` when D2 is approved) (**D3, D4**).

**Blocking dependency:** none — this is the start of the chain.
**Done when:** every GitHub link on the live site resolves; Ko-fi accepts a test
€1; the repo shows a "Sponsor" button.

---

## Week 2 — Analytics install (blocking) + donation surface

**Focus:** make the project measurable and giveable. **Nothing past this week
proceeds until analytics verification passes.**

- [ ] Install Plausible Cloud (EU): create the site on the apex, deploy the
  Cloudflare first-party proxy worker, inject the snippet via `nav.js`
  ([`analytics-install.md`](analytics-install.md) §6.5b).
- [ ] Wire the launch-critical events: `instrument_open`, `donation_cta_view`,
  `donation_cta_click`, `outbound_click` ([`analytics-install.md`](analytics-install.md)
  §6.5c); document them in `docs/analytics-events.md`.
- [ ] Build the `/support` page (**D5**), the footer "Support the atlas" link
  (**D6**), anchored amounts €3/€5/€10+custom (**D8**), and the `/privacy` page
  (**M2**).
- [ ] Register and verify **Google Search Console** ([`measurement.md`](measurement.md)
  §6d).
- [ ] **Start the lobste.rs invite search** (**C3**) — *latency item.*

**Blocking dependency:** Week 1 (repo public, Ko-fi live).
**Done when:** the [`analytics-install.md`](analytics-install.md) §6.5g
verification checklist **fully passes** — test pageview + one custom event in
the dashboard, no render-block, uBlock-tested, `/privacy` linked.

---

## Week 3 — SEO table-stakes

**Focus:** build the discovery base. The audit found SEO greenfield
([`audit.md`](audit.md) §1a).

- [ ] Ship `robots.txt` + build-time `sitemap.xml` with per-instrument
  `<lastmod>` (**S1**).
- [ ] Add JSON-LD: `Dataset` on the data instruments, `TechArticle` on the four
  gateway guides, `SoftwareApplication` on root, `BreadcrumbList` on departments;
  validate each with the Rich Results Test (**S2**).
- [ ] Add a descriptive `<h1>` + question-shaped `<h2>`/`<h3>`s, starting with
  the 10 priority pages (**S3**); fully cross-link the 16 instruments (**S5**).
- [ ] Publish the methodology / colophon page with the origin story (**N4, N5**).

**Blocking dependency:** none (parallel-safe with Week 2 once analytics is done).
**Done when:** `sitemap.xml` submitted in Search Console; Rich Results Test
passes for every schema template; every instrument has a real `<h1>`.

---

## Week 4 — Anchored URLs, RSS, gratitude module, first essay

**Focus:** finish the SEO long-tail surface and the donation conversion moment;
start the content engine.

- [ ] Mint stable anchored per-row / per-cell URLs (`#g5-eu-west-1`) — captures
  the templated long-tail at once (**S4**).
- [ ] Ship the gratitude-moment donation module at the foot of instruments and
  essays (**D7**); confirm `donation_cta_view`/`_click` fire with the
  `placement` property.
- [ ] Publish a real subscribable `feed.xml` (RSS/Atom), linked from the footer
  (**E2**).
- [ ] Write and publish the **first Field Notes essay** on infraatlas.dev
  (**E1**) — candidate: "Why no two clouds name an instance the same way."

**Blocking dependency:** Week 2 (events wired) for the gratitude module.
**Done when:** the donation funnel is measurable end to end per placement; one
essay is live; RSS validates.

---

## Week 5 — Launch preparation

**Focus:** prepare the single highest-leverage event. No new building — rehearse.

- [ ] Final pre-launch checklist: every GitHub link resolves, donation surface
  works on mobile, analytics live, no stale "11 instruments" anywhere (check the
  `og.png` image too — [`audit.md`](audit.md) §1a).
- [ ] Draft the Show HN: title `Show HN: Infra Atlas – a vendor-neutral,
  filterable reference for cloud + API-management infrastructure`; a short, dry,
  marketing-free first comment ([`research/channels.md`](research/channels.md)
  §1).
- [ ] Write the anticipated-Q&A note for yourself: data provenance, update
  cadence, why-not-Vantage, the donations model — answer "like an editor, not a
  founder" ([`research/channels.md`](research/channels.md) §1).
- [ ] Draft the newsletter submission emails (DevOps Weekly, Last Week in AWS)
  and the awesome-list PRs — *ready to send, not sent.*

**Blocking dependency:** Weeks 1–4 all complete and verified.
**Done when:** the pre-launch checklist is 100% green and the Show HN text is
written.

---

## Week 6 — Launch moment 1: "The doors open"

**Focus:** the Show HN, plus the same-week zero-risk amplifiers.

- [ ] Post the Show HN on a weekday morning (EU/US overlap). **Then clear the
  next 4–8 hours** to answer comments in good faith. Never solicit upvotes
  ([`research/channels.md`](research/channels.md) §1) (**L1 / C2**).
- [ ] Same week, independent of the HN result: submit one-line PRs to the
  awesome-* lists (**S6**); email DevOps Weekly + Last Week in AWS (**C1**).
- [ ] Post to lobste.rs **if** the invite was secured (**C3**); if not, mark it
  un-actionable and move on.

**Blocking dependency:** Week 5 checklist green.
**Done when:** the Show HN is posted and the comment window worked; PRs and
newsletter emails are out.

---

## Week 7 — Post-launch consolidation

**Focus:** convert launch attention into durable signal; fix what HN surfaced.

- [ ] Triage HN/lobste.rs feedback: fix real data corrections fast (it
  reinforces the brand), log feature ideas to the roadmap.
- [ ] Submit to the second-tier newsletters: Console.dev and Pointer, accepting
  lower odds ([`research/channels.md`](research/channels.md) §8).
- [ ] Read the Week-1→7 Plausible dashboards: which referrers actually worked
  ([`measurement.md`](measurement.md) §6b Q1).
- [ ] Cross-post the Week-4 Field Notes essay to Dev.to with a correct
  `rel=canonical` — now that the original has had ~3 weeks to index (**C5**).

**Blocking dependency:** Week 6 launch.
**Done when:** launch-surfaced corrections are shipped; referrer mix is reviewed.

---

## Week 8 — Channel rhythm + second essay

**Focus:** establish a sustainable, non-spiky cadence.

- [ ] Publish the **second Field Notes essay** (**E1**).
- [ ] Begin warm outreach to one or two independent cloud blogs (e.g.
  cloudonaut) that already cover region availability (**S8**).
- [ ] If lobste.rs access exists, participate genuinely (comment, don't just
  post — the quarter-of-activity norm).

**Blocking dependency:** none.
**Done when:** essay #2 is live and cross-posted; outreach emails sent.

---

## Week 9 — Contributor activation

**Focus:** turn a now-public repo into a contributable one.

- [ ] Add `.github/ISSUE_TEMPLATE` (a "data correction" and a "new instrument
  idea" template) and a PR template (**N3**).
- [ ] Open a handful of labelled `good-first-issue`s — data corrections, a
  missing region, a new footnote (**N3**).
- [ ] Publish a public roadmap page (a trimmed, public view of
  `tasks/features-2026-05/`) (**N3**).

**Blocking dependency:** Week 1 (repo public).
**Done when:** a new contributor could find a scoped task and a template
unaided.

---

## Week 10 — Contribution support + Launch-2 prep

**Focus:** be responsive to early contributors; prepare the next launch.

- [ ] Review and respond to any issues/PRs within a few days — early
  responsiveness sets the contributor culture.
- [ ] Publish the **third Field Notes essay** (**E1**).
- [ ] Prepare Launch moment 2: finalise the APIM Feature Matrix and draft its
  companion essay ("What five API gateways quietly disagree about") (**L2**).
- [ ] One sober, editorial-voice LinkedIn post aimed at the APIM /
  enterprise-architect persona (**C4**).

**Blocking dependency:** Week 9 scaffolding.
**Done when:** the APIM matrix + essay are launch-ready.

---

## Week 11 — Launch moment 2: the APIM matrix

**Focus:** the ripgrep playbook — a rigorous comparison artefact *with a
writeup* ([`research/comparable-projects.md`](research/comparable-projects.md)
COPY #2).

- [ ] Publish the APIM Feature Matrix + essay (**L2**).
- [ ] Distribute: lobste.rs (if access), a LinkedIn post for the secondary
  persona, a Dev.to cross-post (canonical correct, after ~1 week) — **not** a
  second Show HN (HN was spent in Week 6).
- [ ] Submit the matrix to any `awesome-api` / `awesome-apigateway` list (**S6**).

**Blocking dependency:** Week 10 prep.
**Done when:** the matrix is live and distributed across the non-HN channels.

---

## Week 12 — Transparency + the 90-day review

**Focus:** close the quarter honestly and set up the recurring rhythm.

- [ ] Make `/state` public — monthly uniques, top pages, donations-to-date,
  expenses-YTD; surface the Open Collective ledger if D2 is approved (**M3, D9**).
- [ ] Run the first **monthly measurement review** against
  [`measurement.md`](measurement.md) §6f — capability targets (binary) +
  directional trends (**M4**).
- [ ] Write a short, dry transparency note (Field Notes register): what came in,
  what it paid for, what is planned ([`donations.md`](donations.md) §5f, D10).
- [ ] Scope **Issue No. 02** (Launch moment 3, ~month 5–6): the open-data /
  CC BY 4.0 release + the next instruments ([`growth.md`](growth.md) §4b, L3).

**Blocking dependency:** analytics (Week 2) and the donation rails (Week 1).
**Done when:** `/state` is live; the review is written; Issue No. 02 is scoped.

---

## Explicitly NOT in the 90 days

Deferred deliberately — see [`research/channels.md`](research/channels.md) and
[`anti-list.md`](anti-list.md):

- **Launch moment 3 (Issue No. 02 + open-data release)** — month 5–6; scoped in
  Week 12, executed after the window.
- **Conference CfP (KubeCon EU / European DevOps)** — 6+ month lead time; submit
  as a deliberate medium-term bet, not a 90-day lever.
- **Podcasts** — revisit once the site has standing (post-launch credibility).
- **Reddit, Kubernetes/CNCF Slack, Twitter/X** — not channels for this project;
  rejected with reasons in the research.
- **A mailing list** — RSS (E2) covers cadence with no PII surface; revisit only
  if RSS proves insufficient.

## If the maintainer has less time than this assumes

Minimum viable path, in strict priority order: **Week 1 (repo public + Ko-fi) →
Week 2 (analytics + `/support`) → Week 3 (robots/sitemap/schema) → Week 6 (Show
HN)**. The editorial cadence (Field Notes), contributor scaffolding, and Launch
2 can each slip a month without breaking the foundation. Do not skip analytics —
everything else becomes unmeasurable guesswork ([`measurement.md`](measurement.md)
§6a).
