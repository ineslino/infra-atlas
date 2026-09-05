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
  var lastFocused = null, scrollLockY = 0, isolatedNodes = [];
  var FOCUSABLE = 'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"]), input, select, textarea';

  function trapFocus(e) {
    if (e.key !== "Tab" || !drawerEl || !drawerEl.classList.contains("is-open")) return;
    var nodes = drawerEl.querySelectorAll(FOCUSABLE);
    if (!nodes.length) return;
    var first = nodes[0], last = nodes[nodes.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  }
  function isolateDrawer() {
    isolatedNodes = [];
    Array.prototype.forEach.call(document.body.children, function (node) {
      if (node === drawerEl || node === backdropEl) return;
      isolatedNodes.push({ node: node, inert: node.inert, ariaHidden: node.getAttribute("aria-hidden") });
      node.inert = true;
      node.setAttribute("aria-hidden", "true");
    });
  }
  function restoreDrawerIsolation() {
    isolatedNodes.forEach(function (state) {
      state.node.inert = state.inert;
      if (state.ariaHidden == null) state.node.removeAttribute("aria-hidden");
      else state.node.setAttribute("aria-hidden", state.ariaHidden);
    });
    isolatedNodes = [];
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
      isolateDrawer();
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
      restoreDrawerIsolation();
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
          var val = s.value || (s.level === "yes" ? "✓" : s.level === "part" ? "◐" : s.level === "info" ? "≈" : "✗");
          var levelLabel = s.level === "yes" ? "supported"
                         : s.level === "part" ? "partial"
                         : s.level === "info" ? "informational"
                         : "not available";
          // a bare level symbol (✓/◐/✗) renders as the legend's round mark
          // (.cell-mark), a textual value stays text (.cell-value). Keeps in-cell
          // symbols the same size and colour as the legend, not small grey text.
          var isGlyph = val === "✓" || val === "◐" || val === "✗";
          var markCls = isGlyph ? "cell-mark cell-mark--" : "cell-value cell-value--";
          var starCls = isGlyph ? "cell-mark__star" : "cell-value__star";
          // data-vlabel drives the per-cell vendor label in the mobile card view
          html += "<td class='cell col-" + esc(v.key) + "' data-feature='" + esc(f.id) + "' data-vendor='" + esc(v.key) + "' data-vlabel='" + esc(v.short) + "'>"
               +    "<button type='button' class='cell__btn" + (hasNote ? " has-note" : "") + "' data-feature='" + esc(f.id) + "' data-vendor='" + esc(v.key)
               +      "' aria-haspopup='dialog' aria-label='" + esc(f.name) + " — " + esc(v.name) + ": " + esc(val) + " (" + levelLabel + "). Open detail.'>"
               +      "<span class='" + markCls + esc(s.level) + "'>" + esc(val)
               +        (hasNote ? "<span class='" + starCls + "' aria-hidden='true'>*</span>" : "")
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
      row.querySelectorAll("td.cell[data-vendor]").forEach(function (cell) {
        cell.hidden = opts.table.classList.contains("hide-" + cell.dataset.vendor);
      });
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
      var singular = opts.statusNoun || "item";
      var plural = opts.statusNounPlural || (singular + "s");
      var noun = totalVisible === 1 ? singular : plural;
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

  // ─── shareable URL state — encode filter state in the location hash ───
  // read() → { key: value } parsed from "#k=v&k2=v2"; write(obj, defaults)
  // serialises obj into the hash (omitting empty + default values) via
  // replaceState (no scroll jump, no history spam). Multi-value state (e.g.
  // a vendor set) should be passed as a "."-joined string by the caller.
  IA.matrix.urlState = {
    read: function () {
      var out = {}, h = location.hash.replace(/^#/, "");
      if (!h) return out;
      h.split("&").forEach(function (kv) {
        var i = kv.indexOf("=");
        if (i < 0) return;
        var k = decodeURIComponent(kv.slice(0, i));
        if (k) out[k] = decodeURIComponent(kv.slice(i + 1));
      });
      return out;
    },
    write: function (obj, defaults) {
      defaults = defaults || {};
      var parts = [];
      Object.keys(obj).forEach(function (k) {
        var v = obj[k];
        if (v == null || v === "" || defaults[k] === v) return;
        parts.push(encodeURIComponent(k) + "=" + encodeURIComponent(v));
      });
      var url = parts.length ? "#" + parts.join("&") : location.pathname + location.search;
      try { history.replaceState(null, "", url); } catch (e) { /* file:// etc. */ }
    }
  };

  // ─── canonical filter machinery — category + vendor chips ⇄ URL hash ───
  // The cross-cloud matrix pages all carried this verbatim: build the two chip
  // rows, the multi-select vendor toggle with an "all" reset, single-select
  // category, search box + "/" shortcut, and the filter-state ⇄ hash permalink.
  // The page supplies its data, the chip/search elements, the labels, the vendor
  // hash-param name, and an onChange callback that re-runs its own visibility
  // pass. Drawer body, search haystack and counts stay on the page — those are
  // genuinely page-specific. Returns { buildChips, applyHash, writeHash, wire }.
  IA.matrix.filters = function (cfg) {
    var state = cfg.state;
    var vendors = cfg.vendors, categories = cfg.categories;
    var vParam = cfg.vendorParam || "vendors";
    var onChange = cfg.onChange || function () {};
    var $ = function (s) { return document.querySelector(s); };
    var $$ = function (s) { return Array.prototype.slice.call(document.querySelectorAll(s)); };
    // mirrors the per-page escapeHtml (escapes ' too) so chip markup is byte-identical
    function escHtml(s) {
      return String(s).replace(/[&<>"']/g, function (c) {
        return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
      });
    }

    // some pages historically interpolated chip labels raw (no escape); honour that
    // with escapeChips:false so the built markup stays byte-identical to the original.
    var lbl = cfg.escapeChips === false ? function (s) { return String(s); } : escHtml;
    function buildChips() {
      cfg.catChipsEl.innerHTML = '<span class="filter-chips__label">' + (cfg.categoryLabel || "Category") + '</span>\n' +
        '    <button class="chip is-active" data-cat="all" aria-pressed="true">All</button>' +
        categories.map(function (c) {
          return '<button class="chip" data-cat="' + c.key + '" aria-pressed="false">' + lbl(c.label) + '</button>';
        }).join("");
      cfg.vendorChipsEl.innerHTML = '<span class="filter-chips__label">' + (cfg.vendorLabel || "Vendors") + '</span>\n' +
        '    <button class="chip is-active" data-v="all" aria-pressed="true">All</button>' +
        vendors.map(function (v) {
          return '<button class="chip" data-v="' + v.key + '" aria-pressed="false"><span class="swatch" style="background:' + v.swatch + '" aria-hidden="true"></span>' + lbl(v.short) + '</button>';
        }).join("");
    }

    function writeHash() {
      var keys = vendors.map(function (v) { return v.key; });
      var p = new URLSearchParams();
      if (state.vendors.size < keys.length) p.set(vParam, keys.filter(function (k) { return state.vendors.has(k); }).join(","));
      if (state.category !== "all") p.set("cat", state.category);
      if (state.query.trim()) p.set("q", state.query.trim());
      var h = p.toString();
      history.replaceState(null, "", h ? "#" + h : location.pathname + location.search);
    }

    function applyHash() {
      var keys = vendors.map(function (v) { return v.key; });
      var p = new URLSearchParams(location.hash.slice(1));
      var vd = p.get(vParam);
      if (vd) {
        var valid = vd.split(",").filter(function (x) { return keys.indexOf(x) !== -1; });
        if (valid.length) state.vendors = new Set(valid);
      }
      var cat = p.get("cat"); if (cat) state.category = cat;
      state.query = p.get("q") || "";
      var allV = state.vendors.size === keys.length;
      $$('.chip[data-v]').forEach(function (b) {
        if (b.dataset.v === "all") b.classList.toggle("is-active", allV);
        else b.classList.toggle("is-active", !allV && state.vendors.has(b.dataset.v));
      });
      $$('.chip[data-cat]').forEach(function (b) { b.classList.toggle("is-active", b.dataset.cat === state.category); });
      if (cfg.searchEl) cfg.searchEl.value = state.query;
    }

    function wire() {
      document.addEventListener("click", function (e) {
        var c = e.target.closest(".chip[data-cat]");
        if (c) {
          state.category = c.dataset.cat;
          $$('.chip[data-cat]').forEach(function (b) { b.classList.toggle("is-active", b.dataset.cat === state.category); });
          IA.matrix.syncChipsAria('.chip[data-cat]');
          onChange();
          return;
        }
        var v = e.target.closest(".chip[data-v]");
        if (v) {
          var key = v.dataset.v;
          if (key === "all") {
            state.vendors = new Set(vendors.map(function (x) { return x.key; }));
            $$('.chip[data-v]').forEach(function (b) { b.classList.toggle("is-active", b.dataset.v === "all"); });
          } else {
            if ($('.chip[data-v="all"]').classList.contains("is-active")) {
              state.vendors = new Set([key]);
              $$('.chip[data-v]').forEach(function (b) { b.classList.toggle("is-active", b.dataset.v === key); });
            } else if (state.vendors.has(key) && state.vendors.size === 1) {
              state.vendors = new Set(vendors.map(function (x) { return x.key; }));
              $$('.chip[data-v]').forEach(function (b) { b.classList.toggle("is-active", b.dataset.v === "all"); });
            } else {
              state.vendors.has(key) ? state.vendors.delete(key) : state.vendors.add(key);
              v.classList.toggle("is-active");
              $('.chip[data-v="all"]').classList.remove("is-active");
            }
          }
          IA.matrix.syncChipsAria('.chip[data-v]');
          onChange();
          return;
        }
      });
      if (cfg.searchEl) {
        cfg.searchEl.addEventListener("input", function (e) { state.query = e.target.value; onChange(); });
        cfg.searchEl.setAttribute("aria-keyshortcuts", "Alt+/");
        document.querySelectorAll("code").forEach(function (code) {
          if (code.textContent.trim() === "/" && /\bsearch\b/i.test(code.parentNode.textContent)) code.textContent = "Alt+/";
        });
      }
      function isTextEntry(target) {
        return target && (target.matches("input, textarea, select") || target.isContentEditable);
      }
      document.addEventListener("keydown", function (e) {
        if (e.altKey && !e.ctrlKey && !e.metaKey && e.key === "/" && !isTextEntry(e.target) && cfg.searchEl) {
          e.preventDefault(); e.stopImmediatePropagation(); cfg.searchEl.focus();
        }
      }, true);
      document.addEventListener("keydown", function (e) {
        if (!e.altKey && !e.ctrlKey && !e.metaKey && e.key === "/" && !isTextEntry(e.target)) {
          e.preventDefault(); e.stopImmediatePropagation();
        }
      }, true);
    }

    return { buildChips: buildChips, applyHash: applyHash, writeHash: writeHash, wire: wire };
  };

})(window);
