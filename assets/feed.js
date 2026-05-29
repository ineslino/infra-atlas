/* ──────────────────────────────────────────────────────────────────
   Infra Atlas · shared "What Changed" feed helpers
   One source of truth for the feed's labels, tones, and row markup,
   consumed by the homepage dispatches section and the /changelog/ page.
   Loaded synchronously (small) so inline page scripts can use it at once.
   ────────────────────────────────────────────────────────────────── */
(function (window) {
  "use strict";
  var IA = window.IA || (window.IA = {});

  var INST = {
    "ec2": "AWS EC2", "azure-vm": "Azure VM", "gcp-compute": "GCP Compute",
    "oci-compute": "OCI", "ovh-instances": "OVHcloud", "regions": "Regions",
    "egress": "Egress", "atlas": "Infra Atlas"
  };
  // kind → tone (drives the badge colour: add=mint, drop=rose, price=accent,
  // note=gold for curated editorial dispatches)
  var TONE = {
    "price-change": "price",
    "instance-added": "add", "family-added": "add", "region-added": "add",
    "instance-removed": "drop", "family-removed": "drop", "region-removed": "drop",
    "dispatch": "note"
  };

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function fmtDate(ts) {
    var d = new Date(ts);
    if (isNaN(d.getTime())) return esc(ts || "—");
    return d.toLocaleDateString("en-GB", { day: "2-digit", month: "short", timeZone: "UTC" }).toUpperCase();
  }

  IA.feed = {
    INST: INST,
    TONE: TONE,
    esc: esc,
    fmtDate: fmtDate,
    instLabel: function (i) { return INST[i] || i || ""; },
    kindLabel: function (k) { return (k || "").replace(/-/g, " "); },
    // inner markup for one entry: date + instrument + kind badge + text.
    // Callers wrap this (homepage: <li class="dispatch-item">…; changelog: same).
    row: function (e) {
      return '<span class="dispatch-date">' + fmtDate(e.ts) + '</span>'
        + '<span class="dispatch-body">'
        +   '<span class="dispatch-inst">' + esc(this.instLabel(e.instrument)) + '</span>'
        +   '<span class="dispatch-kind" data-tone="' + (TONE[e.kind] || "") + '">'
        +     esc(this.kindLabel(e.kind)) + '</span>'
        +   '<span class="dispatch-text">' + esc(e.text || "") + '</span>'
        + '</span>';
    },

    // Load + merge the auto-detected feed (/feed.json) with curated editorial
    // dispatches (/dispatches.json), newest-first. Keeping them in separate
    // files means the daily auto-pipeline can never clobber editorial entries.
    // cb receives the merged, sorted entry array (possibly empty).
    load: function (cb) {
      function get(u) {
        return fetch(u, { cache: "no-cache" })
          .then(function (r) { return r.ok ? r.json() : null; })
          .catch(function () { return null; });
      }
      Promise.all([get("/feed.json"), get("/dispatches.json")]).then(function (res) {
        var a = (res[0] && res[0].entries) || [];
        var b = (res[1] && res[1].entries) || [];
        var all = a.concat(b).filter(function (e) { return e && e.ts; });
        all.sort(function (x, y) { return x.ts < y.ts ? 1 : (x.ts > y.ts ? -1 : 0); });
        cb(all);
      });
    }
  };
})(window);
