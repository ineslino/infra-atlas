# Elevating Infra Atlas — a 3-phase roadmap

**Date:** 2026-05-29 · **Status:** for review (no code yet)

## Context

Infra Atlas is already differentiated: neutral (no vendor money), every cell sourced, synced daily, 5 clouds wide, beautiful. But those are mostly *one-time* impressions. The goal is a **compounding moat** — something that gets more valuable over time, gives people a reason to *return*, and *spreads on its own*.

Three directions, chosen together, that build on each other rather than competing:

1. **The living changelog** — become the neutral, sourced "what changed in cloud infra" periodical.
2. **Decision-support tooling** — shareable deep-linked comparisons (cheap, high-leverage) → later a cross-cloud equivalent/migration planner.
3. **A living showpiece** — the globe/constellation visualises real change-events.

**Dependency that fixes the order:** ③ is only *alive* if ① is feeding it real events; ① is the data source. ② is independent and its cheapest slice is a quick win. → **Build ① first, ② alongside, ③ on top.**

---

## Key finding (changes the work)

The changelog brain **already exists and is fully wired**, contrary to first impression:

- `scripts/diff_feed.py` (133 lines, **tested** via `scripts/test_diff_feed.py`) diffs two `data.json` snapshots and emits human-readable change tuples: regions added/removed, families added/removed, instance sizes added/removed, on-demand price moves ≥ ±2%. Fail-safe (never blocks the refresh).
- `.github/workflows/refresh.yml` (line 91) runs `diff_feed.py` per instrument against the **previous refresh commit**, appends to `feed.json` (CAP 200), and commits it.
- The homepage already renders the feed: the `#dispatches` section (`index.html`) fetches `./feed.json`, maps `kind`→tone and `instrument`→label, shows up to 18, and **hides itself when empty**.

So why is `feed.json` empty (`{"generated":"","entries":[]}`, untouched since 16 May)? **Because genuine threshold-crossing changes are rare** — the data refreshes daily but content stays within ±2% with no new families/regions, so `diff_feed` correctly emits nothing and the feed never commits.

**Therefore Phase 1 is NOT "wire it up." It is "make it feel alive despite rare raw changes," plus give it a real home + subscribers.** That's the actual differentiator work.

---

## Phase 1 — The living changelog (keystone)

**Goal:** a real periodical — a dedicated, subscribable, neutral cross-cloud change feed that always has content.

**1a. Backfill the feed from git history.** Replay `diff_feed.py` across every historical `*/data.json` commit so the feed launches with weeks of real, dated, sourced entries instead of empty.
- New: `scripts/backfill_feed.py` — walks `git log` for each instrument's `data.json`, diffs consecutive snapshots through the existing `diff()` function, writes a seeded `feed.json`. Reuses `diff_feed.diff()` verbatim (no logic duplication).

**1b. Broaden what counts as a change** (so the feed isn't only compute-price noise):
- **New instruments / decisions** added to the atlas (detectable from `nav.js` `ITEMS` history, or curated).
- **Compliance certs, new AI models, new regions** — these live in JS-embedded arrays in the matrix pages, not `data.json`, so they need either (i) extracting that data to `*/data.json` (bigger), or (ii) **curated editorial entries** (below). Start with curated; extract later only if worth it.
- Optional: a lower-signal "minor" tier (sub-2% price moves) hidden by default, shown on demand.

**1c. Editorial entries — the periodical voice.** Allow hand-written dispatches alongside auto-detected ones (`"source":"editorial"`), e.g. "Added the Observability Stacks instrument," "GCP launched Axion C4A in europe-west1." This is what turns an automated diff log into a *periodical*. A tiny `dispatches.json` (curated) merged into the feed at build time, or appended directly.

**1d. The destination — `/changelog/` page.** A dedicated instrument-style page (not just the homepage teaser): full history, grouped by week ("This week in cloud infra"), filterable by instrument + kind, each entry dated and — where possible — linking to the instrument/cell it concerns. Reuse the existing tone/label maps from the homepage renderer; consider extracting that renderer to `/assets/feed.js` so homepage + changelog share it.

**1e. RSS — `/feed.xml`.** Generate a static RSS/Atom file from `feed.json` so people can subscribe (the single highest-leverage "return" mechanism). New: `scripts/build_feed_rss.py`, run in `refresh.yml` after `diff_feed` (same pattern as `build_sitemap.py` / `build_search_index.py`). Add `<link rel="alternate" type="application/rss+xml">` to pages + a visible "Subscribe" affordance.
- Email digest = deferred (needs a 3rd-party like Buttondown); RSS first.

**Ships:** a populated, subscribable `/changelog/` + RSS + a no-longer-empty homepage dispatches section.
**Files:** `scripts/diff_feed.py` (reuse), new `scripts/backfill_feed.py` + `scripts/build_feed_rss.py`, `.github/workflows/refresh.yml` (add RSS step), new `changelog/index.html`, `feed.json` (seeded), `nav.js` (nav entry + ⌘K + RELATED), maybe `/assets/feed.js` (shared renderer), curated `dispatches.json`.
**Risk:** a changelog only impresses if it has content — backfill + editorial entries are what de-risk "looks dead." This is the crux; get it right before polishing.

---

## Phase 2 — Shareable deep-linked comparisons (distribution)

**Goal:** every filtered matrix view is a shareable artifact — "send me exactly this comparison." Each shared link markets the site.

- Generalise the URL-state pattern `networking-matrix` already has (`writeHash`/`applyHash`) into a shared helper in `/assets/matrix.js` (`IA.matrix.urlState`): encode active section/category/vendor/search into the URL hash; restore on load.
- Apply across all 8 matrices + the calculators (the egress calculator's inputs → a shareable result link).
- A small "Copy link to this view" affordance when filters are active.
- Per-view OG images = deferred (needs a generator); static per-instrument OG is already fine.

**Ships:** deep-linkable, shareable state across matrices + calculators.
**Files:** `/assets/matrix.js` (+ shared urlState), each matrix page (adopt it), tool pages.
**Note:** the bigger "paste your stack → cross-cloud equivalents + cost/latency delta" planner is a separate, larger build — record as **Phase 2b**, scope later. It leans on `equivalent-sku`, `egress`, `regions` data.

---

## Phase 3 — The living showpiece (wow, on top of ①)

**Goal:** the globe + constellation stop being decorative and start *showing the pulse of the cloud* — powered by Phase 1's change-events.

- `globe.js` currently plots hardcoded region nodes + arcs. Feed it `feed.json`: pulse the regions where something changed recently, draw arcs for the latest change-events, tooltip → the dispatch text. "The cloud, alive."
- `/atlas/` constellation: subtly mark instruments that changed recently (a recency glow), so the map also reads as "what's moving."
- Optional: a compact "pulse" strip on the homepage hero — "3 changes this week" linking to `/changelog/`.

**Ships:** a memorable, data-driven centerpiece that's honest (it animates real events, not filler).
**Files:** `globe.js`, `atlas/index.html`, `index.html` (hero pulse).
**Dependency:** needs Phase 1's feed populated to be meaningful.

---

## Build order & checkpoints

1. **Phase 1a–1b** (backfill + broaden) → feed has real content. *Checkpoint: feed.json populated, homepage dispatches no longer hidden.*
2. **Phase 1d–1e** (`/changelog/` page + RSS) → the destination + subscribe. *Checkpoint: /changelog/ renders, /feed.xml validates.*
3. **Phase 1c** (editorial entries) → periodical voice. *Checkpoint: a curated entry appears in the feed.*
4. **Phase 2** (shareable links) → distribution. *Checkpoint: a shared matrix URL restores its filters.*
5. **Phase 3** (living showpiece) → wow. *Checkpoint: globe pulses a real recent change.*

Each phase ships independently and is verified in-browser (chrome-devtools-mcp) + committed separately. Constraints honoured throughout: vanilla HTML/CSS/JS, no build framework, no backend, static-deployable, accessible (changelog page keyboard/SR-navigable), reduced-motion respected.

## Explicitly deferred
- Email digest (3rd-party dependency).
- Phase 2b migration/equivalent planner (larger build).
- Per-view OG image generation.
- "Ask the Atlas" NL/AI query (needs a backend — against the static ethos).
