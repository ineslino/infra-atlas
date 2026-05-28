/* ──────────────────────────────────────────────────────────────────
   Infra Atlas · shared matrix-instrument JS
   Exposes window.IA.matrix.{drawer,renderTable,applyVisibility,
   wireDelegation,escapeHtml}. Loaded with <script defer>.

   Each matrix page keeps its own VENDORS/CATEGORIES/FEATURES data,
   filter chip rendering, and per-vendor drawer body template; the
   shared module owns the drawer modal infrastructure, the canonical
   button-wrapped table render, the empty-state + aria-live filter
   helper, and the click delegation.
   ────────────────────────────────────────────────────────────────── */
(function (window) {
  "use strict";
  var IA = window.IA || (window.IA = {});
  IA.matrix = IA.matrix || {};

  // ─── escape helper ─────────────────────────────────────────────
  IA.matrix.escapeHtml = function (s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  };
  var esc = IA.matrix.escapeHtml;

  // ─── drawer ────────────────────────────────────────────────────
  var drawerEl = null, backdropEl = null;
  var lastFocused = null, scrollLockY = 0;
  var FOCUSABLE = 'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"]), input, select, textarea';

  function trapFocus(e) {
    if (e.key !== "Tab" || !drawerEl || !drawerEl.classList.contains("is-open")) return;
    var nodes = drawerEl.querySelectorAll(FOCUSABLE);
    if (!nodes.length) return;
    var first = nodes[0], last = nodes[nodes.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  }

  IA.matrix.drawer = {
    init: function (opts) {
      opts = opts || {};
      drawerEl = document.getElementById(opts.drawerId || "drawer");
      backdropEl = document.getElementById(opts.backdropId || "drawer-backdrop");
      if (!drawerEl || !backdropEl) return;
      backdropEl.addEventListener("click", IA.matrix.drawer.close);
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") IA.matrix.drawer.close();
      });
      document.addEventListener("click", function (e) {
        if (e.target.closest('[data-action="close-drawer"]')) IA.matrix.drawer.close();
      });
    },
    open: function (headHtml, bodyHtml) {
      if (!drawerEl) return;
      lastFocused = document.activeElement;
      var head = drawerEl.querySelector(".drawer__head");
      var body = drawerEl.querySelector(".drawer__body");
      if (head) head.innerHTML = headHtml;
      if (body) body.innerHTML = bodyHtml;
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
      // hide after the slide-out animation so AT doesn't see briefly-hidden content
      setTimeout(function () {
        if (drawerEl && !drawerEl.classList.contains("is-open")) drawerEl.hidden = true;
      }, 350);
      if (lastFocused && typeof lastFocused.focus === "function") lastFocused.focus();
    }
  };

  // ─── table renderer — emits canonical button-wrapped markup ────
  IA.matrix.renderTable = function (opts) {
    // opts: { tableEl, vendors, categories, features, dimensionLabel }
    var html = "<thead><tr>";
    html += "<th class='feature-col' scope='col'>" + esc(opts.dimensionLabel || "Dimension") + "</th>";
    opts.vendors.forEach(function (v) {
      html += "<th class='col-" + esc(v.key) + "' scope='col'><span class='vendor-tag'>"
           +    "<span class='swatch' style='background:" + esc(v.swatch) + "' aria-hidden='true'></span>"
           +    esc(v.short)
           +  "</span></th>";
    });
    html += "</tr></thead><tbody>";
    opts.categories.forEach(function (cat) {
      var rows = opts.features.filter(function (f) { return f.category === cat.key; });
      if (!rows.length) return;
      html += "<tr class='category-row' data-cat='" + esc(cat.key) + "'>"
           +    "<td colspan='" + (opts.vendors.length + 1) + "'>"
           +      "<span class='cat-label'><span aria-hidden='true'>▸ </span>" + esc(cat.label) + "</span>"
           +    "</td></tr>";
      rows.forEach(function (f) {
        html += "<tr class='feature-row' data-feature='" + esc(f.id) + "' data-cat='" + esc(cat.key) + "'>";
        // <th scope=row> preserves row-header semantics; <button> inside makes it actionable
        html += "<th class='feature-col' scope='row'>"
             +    "<button type='button' class='feature-col__btn' data-action='open-feature' data-feature='" + esc(f.id)
             +      "' aria-haspopup='dialog' aria-label='Open detail for " + esc(f.name) + "'>"
             +      esc(f.name)
             +    "</button>"
             +  "</th>";
        opts.vendors.forEach(function (v) {
          var s = (f.support && f.support[v.key]) || { level: "no", value: "—", note: "" };
          var hasNote = !!(s.note && s.note.length > 2);
          var val = s.value || (s.level === "yes" ? "✓" : s.level === "part" ? "◐" : "✗");
          var levelLabel = s.level === "yes" ? "supported" : s.level === "part" ? "partial" : "not available";
          html += "<td class='cell col-" + esc(v.key) + "' data-feature='" + esc(f.id) + "' data-vendor='" + esc(v.key) + "'>"
               +    "<button type='button' class='cell__btn' data-feature='" + esc(f.id) + "' data-vendor='" + esc(v.key)
               +      "' aria-haspopup='dialog' aria-label='" + esc(f.name) + " — " + esc(v.name) + ": " + esc(val) + " (" + levelLabel + "). Open detail.'>"
               +      "<span class='cell-value cell-value--" + esc(s.level) + "'>" + esc(val)
               +        (hasNote ? "<span class='cell-value__star' aria-hidden='true'>*</span>" : "")
               +      "</span>"
               +    "</button>"
               +  "</td>";
        });
        html += "</tr>";
      });
    });
    html += "</tbody>";
    opts.tableEl.innerHTML = html;
  };

  // ─── filter helper — empty state + aria-live + category-row hiding ─
  IA.matrix.applyVisibility = function (opts) {
    // opts: { table, features, categories, isVisibleFn, emptyEl?, statusEl?, statusNoun?, anyFilterActive? }
    var totalVisible = 0;
    var rows = opts.table.querySelectorAll("tbody tr.feature-row");
    for (var i = 0; i < rows.length; i++) {
      var row = rows[i];
      var f = null;
      for (var j = 0; j < opts.features.length; j++) {
        if (opts.features[j].id === row.dataset.feature) { f = opts.features[j]; break; }
      }
      if (!f) continue;
      var show = opts.isVisibleFn(f);
      row.classList.toggle("is-hidden", !show);
      if (show) totalVisible++;
    }
    opts.categories.forEach(function (cat) {
      var sel = 'tbody tr.feature-row[data-cat="' + cat.key + '"]';
      var anyVisible = false;
      opts.table.querySelectorAll(sel).forEach(function (r) {
        if (!r.classList.contains("is-hidden")) anyVisible = true;
      });
      var catRow = opts.table.querySelector('tbody tr.category-row[data-cat="' + cat.key + '"]');
      if (catRow) catRow.classList.toggle("is-hidden", !anyVisible);
    });
    if (opts.emptyEl) opts.emptyEl.classList.toggle("is-shown", totalVisible === 0);
    var wrap = opts.table.closest(".matrix-wrap");
    if (wrap) wrap.style.display = totalVisible === 0 ? "none" : "";
    if (opts.statusEl) {
      var noun = totalVisible === 1 ? (opts.statusNoun || "item") : ((opts.statusNoun || "item") + "s");
      opts.statusEl.textContent = opts.anyFilterActive
        ? (totalVisible + " " + noun + " match the current filters.")
        : "";
    }
    return totalVisible;
  };

  // ─── click delegation — wire once per page ─────────────────────
  IA.matrix.wireDelegation = function (onOpen) {
    document.addEventListener("click", function (e) {
      var cellBtn = e.target.closest("button.cell__btn");
      if (cellBtn) { onOpen(cellBtn.dataset.feature, cellBtn.dataset.vendor); return; }
      var featBtn = e.target.closest("button.feature-col__btn");
      if (featBtn) { onOpen(featBtn.dataset.feature, null); return; }
    });
  };

  // ─── aria-pressed sync helper for filter chip groups ───────────
  IA.matrix.syncChipsAria = function (selector) {
    document.querySelectorAll(selector).forEach(function (b) {
      b.setAttribute("aria-pressed", b.classList.contains("is-active") ? "true" : "false");
    });
  };

})(window);
