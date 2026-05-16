/* ──────────────────────────────────────────────────────────────────
   Infra Atlas · shared navigation
   One file, included by every page via <script src="/nav.js" defer>.
   Injects a sticky top bar + a ⌘K command palette. No build step.
   ────────────────────────────────────────────────────────────────── */
(function () {
  "use strict";

  // [ href, name, vendor, search keywords ]
  var CLOUD = [
    ["/ec2/",           "EC2 Observatory",     "AWS",         "amazon elastic compute instance type graviton arm vcpu memory"],
    ["/regions/",       "Region Map",          "Multi-cloud", "datacenter location geography latency availability zone world"],
    ["/azure-vm/",      "VM Atlas",            "Azure",       "microsoft virtual machine instance size series compute"],
    ["/gcp-compute/",   "Compute Index",       "GCP",         "google cloud machine type compute engine instance"],
    ["/oci-compute/",   "Compute Observatory", "OCI",         "oracle cloud compute shape instance ocpu"],
    ["/ovh-instances/", "Instance Catalogue",  "OVH",         "ovhcloud instance range public cloud compute"]
  ];
  var APIM = [
    ["/apim-matrix/",      "Feature Matrix",        "APIM",        "compare comparison vendor capability oauth mtls rate limiting graphql"],
    ["/aws-api-gateway/",  "API Gateway Atlas",     "AWS",         "amazon rest http websocket authorizer stage usage plan"],
    ["/apigee/",           "Apigee Atlas",          "Apigee",      "google apigee x hybrid edge policy proxy kvm"],
    ["/mulesoft/",         "Mulesoft Atlas",        "Mulesoft",    "salesforce anypoint cloudhub rtf flex gateway dataweave"],
    ["/self-hosted-apim/", "Kong · Gravitee · IBM", "Self-hosted", "kong gravitee ibm api connect open source kubernetes"]
  ];

  // Normalise current path → "/ec2/" form
  var here = location.pathname.replace(/index\.html$/, "");
  if (here.charAt(here.length - 1) !== "/") here += "/";

  var isMac = /Mac|iPod|iPhone|iPad/.test(navigator.platform || "");
  var kLabel = isMac ? "⌘K" : "Ctrl K";

  // Flat item model for the palette
  var ITEMS = [{
    href: "/", name: "The Atlas — all instruments", vendor: "Home",
    group: "", keywords: "home overview index landing start"
  }];
  function pushGroup(arr, label) {
    arr.forEach(function (it) {
      ITEMS.push({ href: it[0], name: it[1], vendor: it[2], group: label, keywords: it[3] });
    });
  }
  pushGroup(CLOUD, "Cloud Compute");
  pushGroup(APIM, "API Management");

  var current = null;
  ITEMS.forEach(function (it) {
    it.cur = (it.href === "/") ? (here === "/") : (here.indexOf(it.href) !== -1);
    if (it.cur && it.href !== "/") current = it;
  });

  // ── Styles ───────────────────────────────────────────────────────
  var css = ''
    + '.ia-nav{position:sticky;top:0;z-index:60;display:flex;align-items:center;'
    + 'justify-content:space-between;height:46px;padding:0 clamp(20px,4vw,48px);'
    + 'background:rgba(10,9,7,0.92);backdrop-filter:blur(10px);'
    + '-webkit-backdrop-filter:blur(10px);border-bottom:1px solid var(--line,rgba(244,239,230,0.08));'
    + 'font-family:var(--mono,monospace);}'
    + '.ia-nav a{text-decoration:none;}'
    + '.ia-nav__brand{display:flex;align-items:center;gap:10px;}'
    + '.ia-nav__glyph{width:17px;height:17px;flex:none;display:block;}'
    + '.ia-nav__word{font-size:11.5px;letter-spacing:0.18em;text-transform:uppercase;'
    + 'color:var(--paper,#F4EFE6);font-weight:500;}'
    + '.ia-nav__here{font-size:10.5px;letter-spacing:0.1em;color:var(--paper-3,rgba(244,239,230,0.42));'
    + 'border-left:1px solid var(--line-2,rgba(244,239,230,0.14));padding-left:12px;margin-left:2px;}'
    + '.ia-nav__here em{font-style:normal;color:var(--paper-2,rgba(244,239,230,0.66));}'
    + '@media(max-width:560px){.ia-nav__here{display:none;}}'
    + '.ia-nav__btn{background:transparent;border:1px solid var(--line-2,rgba(244,239,230,0.14));'
    + 'color:var(--paper-2,rgba(244,239,230,0.66));font-family:var(--mono,monospace);'
    + 'font-size:10.5px;letter-spacing:0.14em;text-transform:uppercase;padding:7px 11px;'
    + 'border-radius:99px;cursor:pointer;display:inline-flex;align-items:center;gap:9px;'
    + 'transition:border-color .15s,color .15s;}'
    + '.ia-nav__btn:hover{border-color:var(--paper-3,rgba(244,239,230,0.42));color:var(--paper,#F4EFE6);}'
    + '.ia-nav__btn.is-open{background:var(--paper,#F4EFE6);color:var(--ink,#0A0907);border-color:var(--paper,#F4EFE6);}'
    + '.ia-nav__btn svg{display:block;flex:none;}'
    + '.ia-nav__btn kbd{font-family:var(--mono,monospace);font-size:9px;letter-spacing:0.03em;'
    + 'text-transform:none;border:1px solid currentColor;border-radius:3px;padding:1px 4px;opacity:0.6;}'
    /* command palette */
    + '.ia-cmdk{position:fixed;inset:0;z-index:200;display:none;align-items:flex-start;'
    + 'justify-content:center;padding:13vh 16px 16px;background:rgba(10,9,7,0.74);'
    + 'backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);}'
    + '.ia-cmdk.is-open{display:flex;}'
    + '.ia-cmdk__box{width:min(560px,100%);background:var(--ink-2,#100E0C);'
    + 'border:1px solid var(--line-2,rgba(244,239,230,0.14));border-radius:10px;'
    + 'box-shadow:0 30px 80px rgba(0,0,0,0.6);overflow:hidden;}'
    + '.ia-cmdk__input{width:100%;background:transparent;border:0;outline:0;'
    + 'font-family:var(--sans,sans-serif);font-size:16px;color:var(--paper,#F4EFE6);'
    + 'padding:17px 19px;border-bottom:1px solid var(--line,rgba(244,239,230,0.08));}'
    + '.ia-cmdk__input::placeholder{color:var(--paper-3,rgba(244,239,230,0.42));}'
    + '.ia-cmdk__results{max-height:54vh;overflow-y:auto;padding:7px;}'
    + '.ia-cmdk__group{font-family:var(--mono,monospace);font-size:9px;letter-spacing:0.2em;'
    + 'text-transform:uppercase;color:var(--paper-3,rgba(244,239,230,0.42));margin:11px 8px 4px;}'
    + '.ia-cmdk__group:first-child{margin-top:3px;}'
    + '.ia-cmdk__row{display:flex;align-items:center;gap:11px;padding:9px 10px;'
    + 'border-radius:6px;cursor:pointer;}'
    + '.ia-cmdk__row.is-sel{background:var(--surface-2,#1E1A15);}'
    + '.ia-cmdk__row.is-sel .ia-cmdk__name{color:var(--accent,#FF7849);}'
    + '.ia-cmdk__vd{font-family:var(--mono,monospace);font-size:8.5px;letter-spacing:0.12em;'
    + 'text-transform:uppercase;color:var(--paper-3,rgba(244,239,230,0.42));min-width:62px;flex:none;}'
    + '.ia-cmdk__name{font-family:var(--sans,sans-serif);font-size:13.5px;'
    + 'color:var(--paper,#F4EFE6);flex:1;}'
    + '.ia-cmdk__dot{width:5px;height:5px;border-radius:50%;background:var(--accent,#FF7849);flex:none;}'
    + '.ia-cmdk__go{font-family:var(--mono,monospace);font-size:10px;'
    + 'color:var(--paper-3,rgba(244,239,230,0.42));opacity:0;}'
    + '.ia-cmdk__row.is-sel .ia-cmdk__go{opacity:1;}'
    + '.ia-cmdk__empty{padding:26px 14px;text-align:center;'
    + 'color:var(--paper-3,rgba(244,239,230,0.42));font-family:var(--mono,monospace);font-size:12px;}'
    + '.ia-cmdk__foot{display:flex;gap:15px;padding:9px 15px;'
    + 'border-top:1px solid var(--line,rgba(244,239,230,0.08));'
    + 'font-family:var(--mono,monospace);font-size:9.5px;letter-spacing:0.07em;'
    + 'color:var(--paper-3,rgba(244,239,230,0.42));}'
    + '.ia-cmdk__foot kbd{font-family:inherit;border:1px solid var(--line-2,rgba(244,239,230,0.14));'
    + 'border-radius:3px;padding:1px 5px;margin-right:4px;}'
    + '@media(max-width:560px){.ia-nav__btn kbd{display:none;}.ia-cmdk__foot{display:none;}}'
    /* keep page sticky elements clear of the 46px nav bar */
    + '.filters{top:60px !important;}'
    + '.section__head{top:62px !important;}'
    + '.matrix thead th{top:46px !important;}';

  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  // ── Bar ──────────────────────────────────────────────────────────
  var nav = document.createElement("header");
  nav.className = "ia-nav";

  var hereHtml = current
    ? '<span class="ia-nav__here">' + current.vendor + ' · <em>' + current.name + '</em></span>'
    : '';

  nav.innerHTML =
      '<a class="ia-nav__brand" href="/">'
    +   '<svg class="ia-nav__glyph" viewBox="0 0 32 32" aria-hidden="true">'
    +     '<g fill="none" stroke="var(--accent,#FF7849)" stroke-width="2.1">'
    +       '<circle cx="16" cy="16" r="12.6"/>'
    +       '<circle cx="14.8" cy="14.8" r="8.3"/>'
    +       '<circle cx="13.6" cy="13.6" r="4.2"/>'
    +     '</g>'
    +     '<circle cx="13.6" cy="13.6" r="2.6" fill="var(--accent,#FF7849)"/>'
    +   '</svg>'
    +   '<span class="ia-nav__word">Infra Atlas</span>'
    +   hereHtml
    + '</a>'
    + '<button class="ia-nav__btn" id="ia-nav-btn" aria-haspopup="dialog" aria-expanded="false">'
    +   '<svg viewBox="0 0 16 16" width="12" height="12" aria-hidden="true" fill="none" '
    +     'stroke="currentColor" stroke-width="1.7">'
    +     '<circle cx="6.8" cy="6.8" r="4.3"/><path d="M10 10 L14 14" stroke-linecap="round"/>'
    +   '</svg>'
    +   'Instruments <kbd>' + kLabel + '</kbd>'
    + '</button>';

  // ── Palette ──────────────────────────────────────────────────────
  var overlay = document.createElement("div");
  overlay.className = "ia-cmdk";
  overlay.id = "ia-cmdk";
  overlay.setAttribute("role", "dialog");
  overlay.setAttribute("aria-modal", "true");
  overlay.setAttribute("aria-label", "Search instruments");
  overlay.innerHTML =
      '<div class="ia-cmdk__box">'
    +   '<input class="ia-cmdk__input" id="ia-cmdk-input" type="text" '
    +     'placeholder="Search instruments — cloud, vendor, capability…" '
    +     'autocomplete="off" spellcheck="false" aria-label="Search instruments">'
    +   '<div class="ia-cmdk__results" id="ia-cmdk-results"></div>'
    +   '<div class="ia-cmdk__foot">'
    +     '<span><kbd>↑</kbd><kbd>↓</kbd>navigate</span>'
    +     '<span><kbd>↵</kbd>open</span>'
    +     '<span><kbd>esc</kbd>close</span>'
    +   '</div>'
    + '</div>';

  document.body.insertBefore(nav, document.body.firstChild);
  document.body.appendChild(overlay);

  // ── Behaviour ────────────────────────────────────────────────────
  var btn = document.getElementById("ia-nav-btn");
  var input = document.getElementById("ia-cmdk-input");
  var results = document.getElementById("ia-cmdk-results");
  var visible = [];
  var sel = 0;

  function esc(s) {
    return s.replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function filter(q) {
    q = (q || "").trim().toLowerCase();
    if (!q) return ITEMS.slice();
    var toks = q.split(/\s+/);
    return ITEMS.filter(function (it) {
      var hay = (it.name + " " + it.vendor + " " + it.group + " " + it.keywords).toLowerCase();
      return toks.every(function (t) { return hay.indexOf(t) !== -1; });
    });
  }
  function render() {
    visible = filter(input.value);
    if (sel >= visible.length) sel = visible.length - 1;
    if (sel < 0) sel = 0;
    if (!visible.length) {
      results.innerHTML = '<div class="ia-cmdk__empty">No instrument matches “'
        + esc(input.value.trim()) + '”</div>';
      return;
    }
    var html = "", lastGroup = "\0";
    visible.forEach(function (it, i) {
      if (it.group !== lastGroup) {
        if (it.group) html += '<div class="ia-cmdk__group">' + it.group + '</div>';
        lastGroup = it.group;
      }
      html += '<div class="ia-cmdk__row' + (i === sel ? ' is-sel' : '') + '" '
           +    'data-idx="' + i + '" data-href="' + it.href + '">'
           +    '<span class="ia-cmdk__vd">' + it.vendor + '</span>'
           +    '<span class="ia-cmdk__name">' + it.name + '</span>'
           +    (it.cur ? '<span class="ia-cmdk__dot" title="Current page"></span>' : '')
           +    '<span class="ia-cmdk__go">↵</span>'
           +  '</div>';
    });
    results.innerHTML = html;
  }
  function scrollSel() {
    var el = results.querySelector(".is-sel");
    if (el) el.scrollIntoView({ block: "nearest" });
  }
  function move(d) {
    if (!visible.length) return;
    sel = (sel + d + visible.length) % visible.length;
    render();
    scrollSel();
  }
  function go() {
    if (visible[sel]) location.href = visible[sel].href;
  }
  function openCmdk() {
    overlay.classList.add("is-open");
    btn.classList.add("is-open");
    btn.setAttribute("aria-expanded", "true");
    input.value = "";
    sel = 0;
    var all = filter("");
    for (var i = 0; i < all.length; i++) { if (all[i].cur) { sel = i; break; } }
    render();
    scrollSel();
    input.focus();
  }
  function closeCmdk() {
    if (!overlay.classList.contains("is-open")) return;
    overlay.classList.remove("is-open");
    btn.classList.remove("is-open");
    btn.setAttribute("aria-expanded", "false");
    btn.focus();
  }
  function toggle() {
    overlay.classList.contains("is-open") ? closeCmdk() : openCmdk();
  }

  btn.addEventListener("click", function (e) { e.stopPropagation(); toggle(); });
  input.addEventListener("input", function () { sel = 0; render(); });
  input.addEventListener("keydown", function (e) {
    if (e.key === "ArrowDown") { e.preventDefault(); e.stopPropagation(); move(1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); e.stopPropagation(); move(-1); }
    else if (e.key === "Enter") { e.preventDefault(); e.stopPropagation(); go(); }
    else if (e.key === "Escape") { e.preventDefault(); e.stopPropagation(); closeCmdk(); }
  });
  results.addEventListener("click", function (e) {
    var row = e.target.closest(".ia-cmdk__row");
    if (row) location.href = row.getAttribute("data-href");
  });
  results.addEventListener("mousemove", function (e) {
    var row = e.target.closest(".ia-cmdk__row");
    if (row) {
      var i = +row.getAttribute("data-idx");
      if (i !== sel) { sel = i; render(); }
    }
  });
  overlay.addEventListener("mousedown", function (e) {
    if (e.target === overlay) closeCmdk();
  });
  document.addEventListener("keydown", function (e) {
    if ((e.metaKey || e.ctrlKey) && (e.key === "k" || e.key === "K")) {
      e.preventDefault();
      toggle();
    } else if (e.key === "Escape" && overlay.classList.contains("is-open")) {
      e.preventDefault();
      closeCmdk();
    }
  }, true);
})();
