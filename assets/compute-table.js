/* ──────────────────────────────────────────────────────────────────
   Infra Atlas · shared compute-observatory table + compare
   Exposes window.IA.computeTable.{render, clear, deselect, hideDock}.
   Loaded NON-deferred (in <head>) so it is available synchronously when
   each observatory's inline bootstrap calls render().

   render(container, entries, cfg):
     entries: [{ id, name, cat, catLabel, catColor, arch, vendor,
                 vcpu, mem, price, regions, _fam, _size }]
     cfg: { currency, priceRef, sort, onSort(str), onOpen(entry),
            fmtPrice(price)->string|null, maxCompare }
   The page keeps ownership of filtering/data; this module owns the
   tabular layout, column sorting, and the compare tray.
   ────────────────────────────────────────────────────────────────── */
(function (window) {
  "use strict";
  var IA = window.IA = window.IA || {};
  if (IA.computeTable) return;

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  // Columns. `num` → right-aligned numeric; `nosort` → categorical (filter via chips).
  var COLS = [
    { key: "name",    label: "Instance", cls: "ctbl__name" },
    { key: "class",   label: "Class",    cls: "ctbl__class", nosort: true },
    { key: "vcpu",    label: "vCPU" },
    { key: "mem",     label: "Memory",  unit: "GiB" },
    { key: "price",   label: "$/hr" },
    { key: "pervcpu", label: "$/vCPU" },
    { key: "regions", label: "Regions" }
  ];

  function parseSort(s) {
    if (!s || s === "name") return { key: "name", dir: 1 };
    if (s === "name-desc") return { key: "name", dir: -1 };
    var m = String(s).match(/^(vcpu|mem|price|pervcpu|regions)-(asc|desc)$/);
    if (m) return { key: m[1], dir: m[2] === "asc" ? 1 : -1 };
    return { key: "name", dir: 1 };
  }
  function sortStr(key, dir) {
    return key === "name" ? (dir === 1 ? "name" : "name-desc") : (key + "-" + (dir === 1 ? "asc" : "desc"));
  }
  function valOf(e, key) {
    if (key === "name") return e.name;
    if (key === "pervcpu") return (e.price != null && e.vcpu) ? e.price / e.vcpu : null;
    return e[key];
  }
  function sortEntries(entries, sort) {
    var byName = function (a, b) { return String(a.name).localeCompare(String(b.name), undefined, { numeric: true }); };
    if (sort.key === "name") { entries.sort(function (a, b) { return sort.dir * byName(a, b); }); return; }
    entries.sort(function (a, b) {
      var av = valOf(a, sort.key), bv = valOf(b, sort.key);
      if (av == null && bv == null) return byName(a, b);
      if (av == null) return 1;
      if (bv == null) return -1;
      return sort.dir * (av - bv) || byName(a, b);
    });
  }

  IA.computeTable = {
    _cfg: null, _entries: [], _sort: { key: "name", dir: 1 }, _sel: new Map(), _built: false, _container: null,

    render: function (container, entries, cfg) {
      this._cfg = cfg || {};
      this._entries = entries || [];
      this._container = container;
      this._sort = parseSort(cfg && cfg.sort);
      // drop any selected ids that are no longer in the (re-filtered) result set
      var ids = {}; this._entries.forEach(function (e) { ids[e.id] = e; });
      var self = this;
      Array.from(this._sel.keys()).forEach(function (id) { if (ids[id]) self._sel.set(id, ids[id]); else self._sel.delete(id); });
      this._ensureDom();
      this._draw();
      this._syncDock();
    },

    _fmt: function (price) {
      var cfg = this._cfg;
      if (cfg.fmtPrice) return cfg.fmtPrice(price);
      if (price == null) return null;
      var s = price.toFixed(4).replace(/0+$/, "").replace(/\.$/, "");
      if (s.indexOf(".") === -1) s += ".00";
      return (cfg.currency === "EUR" ? "€" : "$") + s;
    },

    _draw: function () {
      var self = this, container = this._container;
      sortEntries(this._entries, this._sort);

      var head = "<thead><tr><th class='ctbl__check'><span class='ctbl-sr'>Select for comparison</span></th>";
      COLS.forEach(function (c) {
        var cls = c.cls || "";
        if (c.nosort) { head += "<th class='" + cls + "'><span class='ctbl__colhead'>" + esc(c.label) + "</span></th>"; return; }
        var on = self._sort.key === c.key;
        var ariaSort = on ? (self._sort.dir === 1 ? "ascending" : "descending") : "none";
        var arrow = on ? (self._sort.dir === 1 ? "▲" : "▼") : "";
        head += "<th class='" + cls + "' aria-sort='" + ariaSort + "'>"
          + "<button type='button' class='ctbl__sort" + (on ? " is-active" : "") + "' data-sort='" + c.key + "'>"
          + esc(c.label) + (c.unit ? " <span class='ctbl__unit'>" + esc(c.unit) + "</span>" : "")
          + " <span class='ctbl__arrow' aria-hidden='true'>" + arrow + "</span></button></th>";
      });
      head += "</tr></thead>";

      var na = "<span class='ctbl__na'>—</span>";
      var rows = this._entries.map(function (e) {
        var sel = self._sel.has(e.id);
        var price = self._fmt(e.price);
        var per = (e.price != null && e.vcpu) ? self._fmt(e.price / e.vcpu) : null;
        return "<tr class='" + (sel ? "is-sel" : "") + "' data-id='" + esc(e.id) + "'>"
          + "<td class='ctbl__check'><input type='checkbox' data-check='" + esc(e.id) + "'" + (sel ? " checked" : "") + " aria-label='Compare " + esc(e.name) + "'></td>"
          + "<td class='ctbl__name'>" + esc(e.name) + "</td>"
          + "<td class='ctbl__class'><span class='ctbl__dot' style='background:" + esc(e.catColor || "var(--paper-3)") + "'></span>" + esc(e.catLabel || e.cat || "") + (e.arch ? " · " + esc(e.arch) : "") + "</td>"
          + "<td>" + (e.vcpu != null ? e.vcpu : na) + "</td>"
          + "<td>" + (e.mem != null ? e.mem : na) + "</td>"
          + "<td class='ctbl__price'>" + (price ? price : na) + "</td>"
          + "<td>" + (per ? per : na) + "</td>"
          + "<td>" + (e.regions != null ? e.regions : na) + "</td>"
          + "</tr>";
      }).join("");

      container.innerHTML = "<div class='ctbl-wrap'><table class='ctbl' aria-label='Instance types'>" + head + "<tbody>" + rows + "</tbody></table></div>";

      container.querySelectorAll(".ctbl__sort").forEach(function (btn) {
        btn.addEventListener("click", function () {
          var key = btn.dataset.sort;
          if (self._sort.key === key) self._sort.dir = -self._sort.dir;
          else { self._sort.key = key; self._sort.dir = key === "name" ? 1 : -1; } // numbers default high→low
          if (self._cfg.onSort) self._cfg.onSort(sortStr(self._sort.key, self._sort.dir));
          self._draw();
        });
      });
      container.querySelectorAll("input[data-check]").forEach(function (cb) {
        cb.addEventListener("click", function (ev) { ev.stopPropagation(); });
        cb.addEventListener("change", function () {
          var id = cb.dataset.check;
          if (cb.checked) {
            var max = self._cfg.maxCompare || 4;
            if (self._sel.size >= max) { cb.checked = false; return; }
            var e = self._entries.find(function (x) { return x.id === id; });
            if (e) self._sel.set(id, e);
          } else self._sel.delete(id);
          var tr = cb.closest("tr"); if (tr) tr.classList.toggle("is-sel", cb.checked);
          self._syncDock();
        });
      });
      container.querySelectorAll("tbody tr").forEach(function (tr) {
        tr.addEventListener("click", function (ev) {
          if (ev.target.closest(".ctbl__check")) return;
          var e = self._entries.find(function (x) { return x.id === tr.dataset.id; });
          if (e && self._cfg.onOpen) self._cfg.onOpen(e);
        });
      });
    },

    _ensureDom: function () {
      if (this._built) return; this._built = true; var self = this;
      var dock = document.createElement("div");
      dock.className = "ctbl-dock"; dock.id = "ctbl-dock";
      dock.innerHTML = "<span class='ctbl-dock__label'>Compare</span>"
        + "<div class='ctbl-dock__chips' id='ctbl-dock-chips'></div>"
        + "<button type='button' class='ctbl-dock__go' id='ctbl-dock-go'>Compare</button>"
        + "<button type='button' class='ctbl-dock__clear' id='ctbl-dock-clear'>Clear</button>";
      document.body.appendChild(dock);

      var ov = document.createElement("div");
      ov.className = "ctbl-cmp"; ov.id = "ctbl-cmp";
      ov.setAttribute("role", "dialog"); ov.setAttribute("aria-modal", "true"); ov.setAttribute("aria-label", "Instance comparison");
      ov.innerHTML = "<div class='ctbl-cmp__panel'><div class='ctbl-cmp__head'>"
        + "<span class='ctbl-cmp__title'>Compare instances</span>"
        + "<button type='button' class='ctbl-cmp__close' id='ctbl-cmp-close'>Close ✕</button></div>"
        + "<div id='ctbl-cmp-body'></div>"
        + "<div class='ctbl-cmp__hint'>✓ marks the cheapest per row · prices are on-demand list, never the invoiced price</div></div>";
      document.body.appendChild(ov);

      dock.querySelector("#ctbl-dock-go").addEventListener("click", function () { self._openCmp(); });
      dock.querySelector("#ctbl-dock-clear").addEventListener("click", function () { self.clear(); });
      ov.querySelector("#ctbl-cmp-close").addEventListener("click", function () { self._closeCmp(); });
      ov.addEventListener("click", function (e) { if (e.target === ov) self._closeCmp(); });
      document.addEventListener("keydown", function (e) { if (e.key === "Escape" && ov.classList.contains("is-open")) self._closeCmp(); });
    },

    _syncDock: function () {
      var dock = document.getElementById("ctbl-dock"); if (!dock) return; var self = this;
      var items = Array.from(this._sel.values());
      dock.querySelector("#ctbl-dock-chips").innerHTML = items.map(function (e) {
        return "<span class='ctbl-chip'>" + esc(e.name) + "<button type='button' data-rm='" + esc(e.id) + "' aria-label='Remove " + esc(e.name) + "'>✕</button></span>";
      }).join("");
      dock.querySelectorAll("button[data-rm]").forEach(function (b) {
        b.addEventListener("click", function () { self.deselect(b.dataset.rm); });
      });
      dock.classList.toggle("is-shown", items.length > 0);
      var go = dock.querySelector("#ctbl-dock-go");
      go.disabled = items.length < 2;
      go.textContent = "Compare (" + items.length + ")";
    },

    deselect: function (id) {
      this._sel.delete(id);
      document.querySelectorAll("input[data-check]").forEach(function (c) {
        if (c.dataset.check === id) { c.checked = false; var tr = c.closest("tr"); if (tr) tr.classList.remove("is-sel"); }
      });
      this._syncDock();
    },
    clear: function () {
      this._sel.clear();
      document.querySelectorAll("input[data-check]").forEach(function (c) { c.checked = false; var tr = c.closest("tr"); if (tr) tr.classList.remove("is-sel"); });
      this._syncDock();
    },
    hideDock: function () { var d = document.getElementById("ctbl-dock"); if (d) d.classList.remove("is-shown"); },

    _openCmp: function () {
      var self = this, items = Array.from(this._sel.values());
      if (items.length < 2) return;
      // metric key on a row → highlight the lowest (cheapest) cell; categorical/size rows aren't "best/worst"
      var ROWS = [
        ["Class",        function (e) { return e.catLabel || e.cat || "—"; }],
        ["Architecture", function (e) { return e.arch || "—"; }],
        ["Processor",    function (e) { return e.vendor || "—"; }],
        ["vCPU",         function (e) { return e.vcpu != null ? e.vcpu : "—"; }],
        ["Memory (GiB)", function (e) { return e.mem != null ? e.mem : "—"; }],
        ["$/hr",         function (e) { return self._fmt(e.price) || "—"; }, "price"],
        ["$/vCPU",       function (e) { return (e.price != null && e.vcpu) ? self._fmt(e.price / e.vcpu) : "—"; }, "pervcpu"],
        ["$/GiB",        function (e) { return (e.price != null && e.mem) ? self._fmt(e.price / e.mem) : "—"; }, "pergib"],
        ["Regions",      function (e) { return e.regions != null ? e.regions : "—"; }]
      ];
      function rawVal(e, metric) {
        if (metric === "price") return e.price;
        if (metric === "pervcpu") return (e.price != null && e.vcpu) ? e.price / e.vcpu : null;
        if (metric === "pergib") return (e.price != null && e.mem) ? e.price / e.mem : null;
        return null;
      }
      function cheapestIdx(metric) {
        var best = null, idx = -1;
        items.forEach(function (e, i) { var v = rawVal(e, metric); if (v == null) return; if (best == null || v < best) { best = v; idx = i; } });
        return idx;
      }
      var head = "<thead><tr><th>Spec</th>" + items.map(function (e) { return "<td>" + esc(e.name) + "</td>"; }).join("") + "</tr></thead>";
      var body = "<tbody>" + ROWS.map(function (r) {
        var metric = r[2], bi = metric ? cheapestIdx(metric) : -1;
        return "<tr><th>" + esc(r[0]) + "</th>" + items.map(function (e, i) {
          return "<td" + (metric && i === bi ? " class='is-best'" : "") + ">" + esc(r[1](e)) + "</td>";
        }).join("") + "</tr>";
      }).join("") + "</tbody>";
      document.getElementById("ctbl-cmp-body").innerHTML = "<table class='ctbl-cmp__grid'>" + head + body + "</table>";
      document.getElementById("ctbl-cmp").classList.add("is-open");
      document.getElementById("ctbl-cmp-close").focus();
    },
    _closeCmp: function () { var o = document.getElementById("ctbl-cmp"); if (o) o.classList.remove("is-open"); }
  };
})(window);
