# Matrix Shared Extraction — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Extract the duplicated matrix-instrument infrastructure (drawer, render, filter, a11y) into shared `/assets/matrix.{css,js}` and migrate all 8 matrix pages onto it, while applying the audit's a11y/UX fixes that aren't already in.

**Architecture:** Pure vanilla — no build step. A single global `IA.matrix` namespace exposed by `/assets/matrix.js` (loaded with `<script defer>`), a single `/assets/matrix.css` linked from each page. Each instrument keeps its own `VENDORS`/`CATEGORIES`/`FEATURES` data and its `init()` that calls `IA.matrix.mount({...})`. The shared module owns: drawer (open/close/focus-trap/scroll-lock), table render with proper `<th>`/`<td>` semantics + button wrappers, filter + aria-live + empty-state, decorative-element a11y. The page keeps: data, page-specific filter chips, drawer body template (because per-vendor detail varies).

**Tech Stack:** Vanilla HTML/CSS/JS, ES2018+. No npm. No build step. CSP-clean.

**Scope inventory (8 pages):**
- `networking-matrix/` — already partially fixed (current commit `a0be688`)
- `observability/` — already fully fixed (current commit `a0be688`)
- `apim-matrix/` — needs migration + audit fixes
- `egress/` — needs migration + audit fixes
- `ai-atlas/` — needs migration + audit fixes
- `compliance/` — needs migration + audit fixes
- `iam-matrix/` — already partially upgraded; needs migration to shared
- `kubernetes/` — needs migration + audit fixes

---

## Constraints

- **No regressions** — every page that worked before must still work. The Render/Filter contract must be 1:1 with current behaviour.
- **No new external deps** — shared module loads with the same `<script defer>` mechanism nav.js uses.
- **No build step** — Plain JS file with IIFE `IA.matrix = {…}`.
- **`prefers-reduced-motion` honoured** — already covered globally by nav.js `!important` block; new motion must respect it too.
- **Backwards-compat keyboard shortcuts** — networking-matrix has `/` to focus search; observability has Esc-to-close; preserve both.
- **No AI co-author lines in commits/PRs.** Per project rule.

---

## Task 1: Pin baseline behaviour

**Goal:** Before refactoring, capture what each page currently does so we can verify nothing breaks.

**Step 1.1: Browse each matrix locally to confirm current state**

Run a local server:
```bash
cd /Users/ineslino/Documents/Repos/Personal-Repos/infraatlas
python3 -m http.server 7474
```

For each of the 8 pages, visit `http://localhost:7474/<page>/` and verify:
- Page renders
- Filter chips toggle
- Search filters rows
- Clicking a cell opens the drawer with per-vendor detail
- ESC closes the drawer
- Tab navigation reaches cells

Note any pre-existing bugs (e.g. networking-matrix `td.feature-col` vs `<th>` mismatch the audit found) — these get fixed as part of the migration, not separately.

**Step 1.2: Snapshot data shapes**

For each matrix, capture in a scratchpad:
- Number of vendors, categories, features
- Filter chip groups (categories only / categories + vendors / sections etc.)
- Drawer body structure (per-vendor detail card format)

This snapshot is the reference for "behaviour preserved".

No commit at this step — pure observation.

---

## Task 2: Create `/assets/matrix.css`

**Files:**
- Create: `assets/matrix.css`

**Step 2.1: Extract shared CSS**

Copy from `observability/index.html` and `networking-matrix/index.html` (already audit-fixed) the following blocks into a new `assets/matrix.css`:

- `:focus-visible` rules
- `.cell__btn`, `.feature-col__btn` button-wrappers
- `.matrix-empty`, `.matrix-empty.is-shown`
- `.sr-only` visually-hidden helper
- `.tab` + `.tablist` styles (used by observability, will be optional per page)
- Drawer infrastructure: `.drawer-backdrop`, `.drawer`, `.drawer__head`, `.drawer__close`, `.drawer__body`, `.drawer__section`, `.drawer__title`, `.drawer__eyebrow`, `.drawer__desc`, `.vendor-row*`
- Reduced-motion guard for `.status-dot` pulse animation pattern

Each rule should be reviewed: anything page-specific (e.g. accent colour overrides) stays in the page; anything structural moves out.

**Step 2.2: Test by loading observability with the new shared CSS**

In `observability/index.html`, before the `<style>` block, add:
```html
<link rel="stylesheet" href="/assets/matrix.css">
```

Then remove the now-duplicated rules from the page's `<style>`.

Visit `http://localhost:7474/observability/` and confirm visual identity. If anything regresses, the rule moved was page-specific — restore it.

**Step 2.3: Commit**

```bash
git add assets/matrix.css observability/index.html
git commit -m "extract shared matrix CSS into /assets/matrix.css"
```

---

## Task 3: Create `/assets/matrix.js` — drawer module

**Files:**
- Create: `assets/matrix.js`

**Step 3.1: Skeleton with IIFE + global namespace**

```javascript
/* Shared matrix infrastructure — used by every /matrix-style instrument page.
   See docs/plans/2026-05-28-matrix-shared-extraction.md for the contract. */
(function (window) {
  "use strict";
  var IA = window.IA || (window.IA = {});
  IA.matrix = IA.matrix || {};

  // … methods exported below
})(window);
```

**Step 3.2: Add `IA.matrix.escapeHtml(s)`**

Single source of truth — replaces the per-page `esc`/`escapeHtml` divergence the audit flagged.

```javascript
IA.matrix.escapeHtml = function (s) {
  return String(s).replace(/[&<>"]/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
  });
};
```

**Step 3.3: Add drawer module**

```javascript
// Drawer state (single drawer per page is fine — all instruments work this way)
var drawerEl, backdropEl, lastFocused = null, scrollLockY = 0;
var FOCUSABLE = 'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"]), input, select, textarea';

function trapFocus(e) {
  if (e.key !== "Tab" || !drawerEl || !drawerEl.classList.contains("is-open")) return;
  var f = drawerEl.querySelectorAll(FOCUSABLE);
  if (!f.length) return;
  var first = f[0], last = f[f.length - 1];
  if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
  else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
}

IA.matrix.drawer = {
  init: function (opts) {
    drawerEl = document.getElementById(opts.drawerId || "drawer");
    backdropEl = document.getElementById(opts.backdropId || "drawer-backdrop");
    if (!drawerEl || !backdropEl) return;
    backdropEl.addEventListener("click", IA.matrix.drawer.close);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") IA.matrix.drawer.close(); });
    document.addEventListener("click", function (e) {
      if (e.target.closest('[data-action="close-drawer"]')) IA.matrix.drawer.close();
    });
  },
  open: function (htmlHead, htmlBody) {
    if (!drawerEl) return;
    lastFocused = document.activeElement;
    drawerEl.querySelector(".drawer__head").innerHTML = htmlHead;
    drawerEl.querySelector(".drawer__body").innerHTML = htmlBody;
    backdropEl.classList.add("is-open");
    drawerEl.classList.add("is-open");
    drawerEl.setAttribute("aria-hidden", "false");
    drawerEl.hidden = false;
    // scroll lock
    scrollLockY = window.scrollY;
    document.body.style.position = "fixed";
    document.body.style.top = "-" + scrollLockY + "px";
    document.body.style.left = "0";
    document.body.style.right = "0";
    document.body.style.width = "100%";
    document.addEventListener("keydown", trapFocus);
    var close = drawerEl.querySelector(".drawer__close");
    if (close) close.focus();
  },
  close: function () {
    if (!drawerEl || !drawerEl.classList.contains("is-open")) return;
    backdropEl.classList.remove("is-open");
    drawerEl.classList.remove("is-open");
    drawerEl.setAttribute("aria-hidden", "true");
    document.removeEventListener("keydown", trapFocus);
    // restore scroll
    document.body.style.position = "";
    document.body.style.top = "";
    document.body.style.left = "";
    document.body.style.right = "";
    document.body.style.width = "";
    window.scrollTo(0, scrollLockY);
    setTimeout(function () { if (!drawerEl.classList.contains("is-open")) drawerEl.hidden = true; }, 350);
    if (lastFocused && typeof lastFocused.focus === "function") lastFocused.focus();
  }
};
```

**Step 3.4: Add `IA.matrix.renderTable(opts)`**

The shared table renderer — emits the canonical button-wrapped `<th>`/`<td>` markup.

```javascript
IA.matrix.renderTable = function (opts) {
  // opts: { tableEl, vendors, categories, features, getCellContent }
  var esc = IA.matrix.escapeHtml;
  var html = "<thead><tr><th class='feature-col' scope='col'>" + esc(opts.dimensionLabel || "Dimension") + "</th>";
  opts.vendors.forEach(function (v) {
    html += "<th class='col-" + esc(v.key) + "' scope='col'><span class='vendor-tag'>"
         + "<span class='swatch' style='background:" + esc(v.swatch) + "' aria-hidden='true'></span>"
         + esc(v.short) + "</span></th>";
  });
  html += "</tr></thead><tbody>";
  opts.categories.forEach(function (cat) {
    var rows = opts.features.filter(function (f) { return f.category === cat.key; });
    if (!rows.length) return;
    html += "<tr class='category-row' data-cat='" + esc(cat.key) + "'>"
         +   "<td colspan='" + (opts.vendors.length + 1) + "'>"
         +     "<span class='cat-label'><span aria-hidden='true'>▸ </span>" + esc(cat.label) + "</span>"
         +   "</td></tr>";
    rows.forEach(function (f) {
      html += "<tr class='feature-row' data-feature='" + esc(f.id) + "' data-cat='" + esc(cat.key) + "'>";
      html += "<th class='feature-col' scope='row'>"
           +    "<button type='button' class='feature-col__btn' data-action='open-feature' data-feature='" + esc(f.id) + "' aria-haspopup='dialog' aria-label='Open detail for " + esc(f.name) + "'>"
           +      esc(f.name)
           +    "</button>"
           +  "</th>";
      opts.vendors.forEach(function (v) {
        var s = (f.support && f.support[v.key]) || { level: "no", value: "—", note: "" };
        var hasNote = !!(s.note && s.note.length > 2);
        var val = s.value || (s.level === "yes" ? "✓" : s.level === "part" ? "◐" : "✗");
        var levelLabel = s.level === "yes" ? "supported" : s.level === "part" ? "partial" : "not available";
        html += "<td class='cell col-" + esc(v.key) + "' data-feature='" + esc(f.id) + "' data-vendor='" + esc(v.key) + "'>"
             +    "<button type='button' class='cell__btn' data-feature='" + esc(f.id) + "' data-vendor='" + esc(v.key) + "' aria-haspopup='dialog' aria-label='" + esc(f.name) + " — " + esc(v.name) + ": " + esc(val) + " (" + levelLabel + "). Open detail.'>"
             +      "<span class='cell-value cell-value--" + esc(s.level) + "'>" + esc(val) + (hasNote ? "<span class='cell-value__star' aria-hidden='true'>*</span>" : "") + "</span>"
             +    "</button>"
             +  "</td>";
      });
      html += "</tr>";
    });
  });
  html += "</tbody>";
  opts.tableEl.innerHTML = html;
};
```

**Step 3.5: Add `IA.matrix.filter(opts)`**

The shared filter helper — manages empty state, aria-live announcement, and category-row hiding. Each page wires `applyFilter` itself (state shape varies) and calls this helper at the end.

```javascript
IA.matrix.applyVisibility = function (opts) {
  // opts: { table, features, categories, isVisibleFn, emptyEl, statusEl, statusNoun, anyFilterActive }
  var totalVisible = 0;
  opts.table.querySelectorAll("tbody tr.feature-row").forEach(function (row) {
    var f = opts.features.find(function (x) { return x.id === row.dataset.feature; });
    if (!f) return;
    var show = opts.isVisibleFn(f);
    row.classList.toggle("is-hidden", !show);
    if (show) totalVisible++;
  });
  opts.categories.forEach(function (cat) {
    var visible = Array.prototype.some.call(
      opts.table.querySelectorAll('tbody tr.feature-row[data-cat="' + cat.key + '"]'),
      function (r) { return !r.classList.contains("is-hidden"); }
    );
    var catRow = opts.table.querySelector('tbody tr.category-row[data-cat="' + cat.key + '"]');
    if (catRow) catRow.classList.toggle("is-hidden", !visible);
  });
  if (opts.emptyEl) opts.emptyEl.classList.toggle("is-shown", totalVisible === 0);
  var wrap = opts.table.closest(".matrix-wrap");
  if (wrap) wrap.style.display = totalVisible === 0 ? "none" : "";
  if (opts.statusEl) {
    var noun = totalVisible === 1 ? (opts.statusNoun || "item") : ((opts.statusNoun || "item") + "s");
    opts.statusEl.textContent = opts.anyFilterActive ? (totalVisible + " " + noun + " match the current filters.") : "";
  }
  return totalVisible;
};
```

**Step 3.6: Add wiring helper for the canonical click delegation**

```javascript
IA.matrix.wireDelegation = function (onOpen) {
  // onOpen: function (featureId, vendorKeyOrNull) — page-specific drawer content builder
  document.addEventListener("click", function (e) {
    var cellBtn = e.target.closest("button.cell__btn");
    if (cellBtn) { onOpen(cellBtn.dataset.feature, cellBtn.dataset.vendor); return; }
    var featBtn = e.target.closest("button.feature-col__btn");
    if (featBtn) { onOpen(featBtn.dataset.feature, null); return; }
  });
};
```

**Step 3.7: Commit the module**

```bash
git add assets/matrix.js
git commit -m "add /assets/matrix.js — shared drawer + render + filter for matrix instruments"
```

---

## Task 4: Migrate `observability/` onto shared module (canary)

This is the proof-of-concept. If anything is wrong with the shared module's API, we find it here on a page we just fully tested.

**Files:**
- Modify: `observability/index.html`

**Step 4.1: Add link + script tags**

In `<head>`, after the Google Fonts link, add:
```html
<link rel="stylesheet" href="/assets/matrix.css">
```

Before `<script src="/nav.js" defer>`, add:
```html
<script src="/assets/matrix.js" defer></script>
```

**Step 4.2: Delete duplicated CSS**

Remove from the page's `<style>` block every rule that's now in `/assets/matrix.css`. Keep page-specific styles (mint accent, two-section tabs, masthead, status panel).

**Step 4.3: Delete duplicated JS**

Replace the page's `openDrawer`/`closeDrawer`/`trapFocus` with calls to `IA.matrix.drawer.{open,close}`. Replace the page's `renderMatrix(tableId, ...)` body with `IA.matrix.renderTable({...})`. Replace the `applyFilter` row-hiding+empty-state+aria-live block with `IA.matrix.applyVisibility({...})`.

Keep the page's own:
- `setSection` (tabs are observability-specific)
- Filter category chip rendering (the chip set depends on the active section)
- Drawer body builder (per-vendor card structure is page-specific)
- `init()` calling the helpers

**Step 4.4: Visit and verify**

```bash
python3 -m http.server 7474
```

Then visit `http://localhost:7474/observability/`:
1. Click each tab — section switches, filter chips rebuild
2. Type in search — rows filter, aria-live count updates (check via DevTools), empty state appears at "no match"
3. Click a cell — drawer opens, ESC closes, Tab stays inside
4. Body scroll locks during drawer open
5. Focus returns to the cell on close

If any step fails, fix the shared module (not the page) and retry.

**Step 4.5: Commit**

```bash
git add observability/index.html assets/matrix.js
git commit -m "migrate /observability/ onto /assets/matrix.{css,js}"
```

---

## Task 5: Migrate `networking-matrix/` onto shared module

**Files:**
- Modify: `networking-matrix/index.html`

**Step 5.1–5.5: Same procedure as Task 4**

Specific differences to handle:
- `/` keyboard shortcut to focus search — keep page-local
- Vendor visibility toggling (`hide-aws`, `hide-azure` classes on the table) — the shared `renderTable` already emits `col-${v.key}` classes; the page-local visibility logic via `state.vendors` Set keeps working
- Hash routing (`writeHash`/`applyHash`) — keep page-local

**Step 5.6: Verify by clicking through every interaction listed in Task 4**

**Step 5.7: Commit**

```bash
git add networking-matrix/index.html
git commit -m "migrate /networking-matrix/ onto /assets/matrix.{css,js}"
```

---

## Task 6: Migrate the 6 remaining matrices (parallel dispatch)

Once Tasks 4 and 5 confirm the shared module's API holds, the remaining 6 matrices are independent migrations. Each agent gets the same instructions; differences are page-specific data and filter chip shape.

**REQUIRED SUB-SKILL:** Use superpowers:dispatching-parallel-agents — one agent per matrix file.

**Agent prompt template (per matrix):**

```
Migrate the matrix instrument at <path>/index.html onto the shared module at /assets/matrix.{css,js}.

Reference implementations:
- observability/index.html — uses IA.matrix fully
- networking-matrix/index.html — uses IA.matrix fully
- /assets/matrix.css — shared styles
- /assets/matrix.js — shared drawer + renderTable + applyVisibility + wireDelegation

Required changes:
1. Add <link rel="stylesheet" href="/assets/matrix.css"> in <head>
2. Add <script src="/assets/matrix.js" defer></script> before nav.js
3. Delete CSS rules that are now in matrix.css (button-wrap, sr-only, matrix-empty, drawer, vendor-row, etc.)
4. Replace renderMatrix body with IA.matrix.renderTable({...})
5. Replace openDrawer/closeDrawer/trapFocus with IA.matrix.drawer
6. Replace filter row-hiding + empty-state + aria-live block with IA.matrix.applyVisibility
7. Replace click delegation with IA.matrix.wireDelegation
8. Add empty-state HTML: <div class="matrix-empty" id="matrix-empty" role="status" aria-live="polite">…</div>
9. Add aria-live status region: <div class="sr-only" id="filter-status" role="status" aria-live="polite"></div>
10. Add sr-only label + aria-label on search input
11. Add aria-pressed on every filter chip + sync helper
12. Remove opacity dims from vendor-row__mark--no / cell-value--no rules (already in matrix.css unset)
13. Reduced-motion guard on status-dot pulse
14. ESC button text → ✕ glyph with aria-label="Close (Esc)"

Preserve all page-specific behaviour:
- VENDORS/CATEGORIES/FEATURES data unchanged
- Page-specific filter chips (vendor toggles, etc.)
- Hash routing if present
- Keyboard shortcuts (e.g. "/" focus)
- Drawer body template (per-vendor detail structure)

Verify locally:
- Page renders identically
- Filters still work
- Drawer opens/closes correctly with focus trap and scroll lock
- aria-live announces filter result count
- Empty state shows on 0 matches

Return: a summary of what changed and any structural divergence you found that didn't fit the shared API.
```

**Six parallel agents:**
1. `apim-matrix/index.html`
2. `egress/index.html`
3. `ai-atlas/index.html`
4. `compliance/index.html`
5. `iam-matrix/index.html`
6. `kubernetes/index.html`

**Step 6.7: Single commit for the sweep**

```bash
git add apim-matrix/index.html egress/index.html ai-atlas/index.html compliance/index.html iam-matrix/index.html kubernetes/index.html
git commit -m "migrate 6 remaining matrices onto /assets/matrix.{css,js}"
```

---

## Task 7: Cross-page verification

**Step 7.1: Spin up local server**

```bash
cd /Users/ineslino/Documents/Repos/Personal-Repos/infraatlas
python3 -m http.server 7474
```

**Step 7.2: Visit each of the 8 matrix pages and run the checklist:**

For each page, in DevTools:
- No console errors
- Network tab shows `matrix.css` and `matrix.js` loaded
- Tab-key navigation reaches cells (lighthouse-style)
- ESC closes the drawer
- aria-live region announces filter results (inspect element `#filter-status`)

**Step 7.3: Lighthouse a11y audit on `/observability/`**

```bash
# Use Chrome DevTools Lighthouse manually, or:
npx -y lighthouse http://localhost:7474/observability/ --only-categories=accessibility --view --quiet
```

Score should be ≥95. Fix anything below.

**Step 7.4: Lighthouse a11y audit on one more page (`/iam-matrix/`)**

Same threshold.

**Step 7.5: ⌘K palette spot-check**

Open `http://localhost:7474/` and test that ⌘K still surfaces every matrix page.

**Step 7.6: Commit any final fixes**

If anything fails, fix at the shared-module level (no per-page workarounds).

---

## Task 8: Cleanup

**Step 8.1: Remove dead CSS from each page**

After the migration, each page's `<style>` block should be ≤ 50% of its previous size. Any rule duplicated between matrix.css and a page's style block should be removed from the page.

**Step 8.2: Consistency pass**

Run a grep across all matrices for stale references:
```bash
cd /Users/ineslino/Documents/Repos/Personal-Repos/infraatlas
grep -l 'role="button"' **/*.html  # should return nothing
grep -l 'function escapeHtml\|function esc(' **/*.html  # should return only assets/matrix.js
```

**Step 8.3: Commit cleanup**

```bash
git add -A
git commit -m "remove dead CSS + JS from matrix pages post-extraction"
```

---

## Verification — final state

| Check | Method |
|---|---|
| All 8 matrices load and render | Visit each at `localhost:7474` |
| No `role="button"` on `<th>`/`<td>` anywhere | `grep -r 'role="button"' .` returns 0 |
| Single source for `escapeHtml` | `grep -l 'function escapeHtml' .` returns only `assets/matrix.js` |
| Drawer focus trap works | Tab inside drawer never escapes |
| Drawer scroll lock works | Body doesn't scroll behind backdrop |
| `aria-live` announces filter | DevTools inspect `#filter-status` while typing |
| Empty state appears | Type gibberish → "No items match…" panel |
| Lighthouse a11y ≥95 on every matrix | Run Lighthouse on each |
| Reduced-motion respected | OS-level "Reduce motion" disables pulse animation |
| ⌘K still finds every matrix | Open palette, type each matrix name |

---

## Rollback strategy

The work is staged as 5 separate commits (Tasks 2–6) plus cleanup (Task 8). If any commit introduces a regression, `git revert <hash>` reverts only that page or step. The shared module commits (Tasks 2, 3) are pure additions — they can't break anything until a page actually consumes them.

If the shared API itself turns out to be wrong (e.g. one of the 6 remaining matrices has a structural shape that doesn't fit), we revert Task 6's commit and either: (a) extend the shared API on a side branch, or (b) leave that one page on the legacy pattern and document why.

---

## Out of scope (deferred per audit)

These were flagged in the audit but aren't part of this extraction:

- **#2 sticky-element pile-up** — needs cross-matrix top-offset math; address in a separate UX pass once the shared module is in place
- **#16 prices in matrix cells** — content/policy question, needs decision before code
- **#23 dynamic page-index counts** — homepage-only, low drift risk
