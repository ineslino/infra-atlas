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
  var XCLOUD = [
    ["/equivalent-sku/",         "Equivalent-SKU Finder", "Cross-cloud", "translate translator equivalent sku instance type match migrate vcpu memory aws azure gcp oci ovh"],
    ["/kubernetes/",             "Kubernetes Atlas",      "Cross-cloud", "managed kubernetes k8s eks aks gke oke ovh container control plane version sla node pool"],
    ["/compliance/",             "Compliance Footprint",  "Cross-cloud", "compliance certification fedramp iso soc hipaa pci dss gdpr irap c5 ens audit attestation"],
    ["/confidential-computing/", "Confidential Computing","Cross-cloud", "confidential enclave sgx sev snp tdx nitro tee trusted execution memory encryption attestation"],
    ["/iam-matrix/",             "IAM Matrix",            "Cross-cloud", "iam identity access management rbac abac policy entra id permissions roles authorization"]
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
  pushGroup(XCLOUD, "Cross-Cloud");

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
    + '.matrix thead th{top:46px !important;}'
    /* skip link — first focusable element on every page */
    + '.ia-skip{position:fixed;top:8px;left:8px;z-index:300;background:var(--accent,#FF7849);'
    + 'color:var(--ink,#0A0907);font-family:var(--mono,monospace);font-size:12px;font-weight:600;'
    + 'letter-spacing:0.04em;padding:9px 16px;border-radius:5px;text-decoration:none;'
    + 'transform:translateY(-160%);transition:transform .15s;}'
    + '.ia-skip:focus{transform:translateY(0);}'
    /* donation surface — gratitude module + footer support strip */
    + '.ia-grat{margin:56px 0 4px;}'
    + '.ia-grat__in{display:flex;align-items:center;justify-content:space-between;'
    + 'gap:26px;flex-wrap:wrap;border:1px solid var(--line-2,rgba(244,239,230,0.14));'
    + 'border-radius:10px;background:var(--surface,#161310);padding:26px 30px;}'
    + '.ia-grat__kick{font-family:var(--mono,monospace);font-size:10px;'
    + 'letter-spacing:0.18em;text-transform:uppercase;color:var(--accent,#FF7849);'
    + 'margin-bottom:9px;}'
    + '.ia-grat__txt p{font-family:var(--sans,sans-serif);font-size:14px;'
    + 'line-height:1.6;color:var(--paper-2,rgba(244,239,230,0.66));'
    + 'max-width:600px;margin:0;}'
    + '.ia-grat__cta{flex:none;display:inline-flex;align-items:center;gap:9px;'
    + 'font-family:var(--mono,monospace);font-size:11px;letter-spacing:0.12em;'
    + 'text-transform:uppercase;font-weight:500;color:var(--ink,#0A0907);'
    + 'background:var(--accent,#FF7849);border-radius:99px;padding:13px 22px;'
    + 'text-decoration:none;transition:background .15s;}'
    + '.ia-grat__cta span{transition:transform .15s;}'
    + '.ia-grat__cta:hover{background:var(--accent-2,#FFA66E);}'
    + '.ia-grat__cta:hover span{transform:translateX(3px);}'
    + '.ia-support{border-top:1px solid var(--line,rgba(244,239,230,0.06));'
    + 'padding:20px clamp(20px,4vw,48px);text-align:center;'
    + 'font-family:var(--mono,monospace);font-size:10px;letter-spacing:0.13em;'
    + 'text-transform:uppercase;color:var(--paper-3,rgba(244,239,230,0.55));}'
    + '.ia-support a{color:var(--paper,#F4EFE6);text-decoration:none;'
    + 'border-bottom:1px solid var(--accent,#FF7849);padding-bottom:2px;'
    + 'transition:color .15s;}'
    + '.ia-support a:hover{color:var(--accent,#FF7849);}'
    + '@media(max-width:560px){.ia-grat__in{padding:22px;}'
    + '.ia-grat__cta{width:100%;justify-content:center;}}';

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
    +   '<svg class="ia-nav__glyph" viewBox="-116 -116 232 232" aria-hidden="true">'
    +     '<path d="M0.00 -100.00L10.72 -25.87L35.36 -35.36L25.87 -10.72L100.00 -0.00L25.87 10.72L35.36 35.36L10.72 25.87L0.00 100.00L-10.72 25.87L-35.36 35.36L-25.87 10.72L-100.00 0.00L-25.87 -10.72L-35.36 -35.36L-10.72 -25.87Z" fill="var(--accent,#FF7849)"/>'
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

  // ── Skip link — first focusable element, jumps past the nav ──
  var mainEl = document.querySelector("main");
  if (mainEl) {
    if (!mainEl.id) mainEl.id = "ia-main";
    mainEl.setAttribute("tabindex", "-1");
    var skip = document.createElement("a");
    skip.className = "ia-skip";
    skip.href = "#" + mainEl.id;
    skip.textContent = "Skip to content";
    document.body.insertBefore(skip, document.body.firstChild);
  }

  // ── Donation surface — gratitude module + footer support strip ───
  // Injected here once so all 16 instruments stay consistent without a
  // copy-paste into every file. See tasks/marketing-2026-05/donations.md.
  (function () {
    var SUPPORT = "/support/";

    // Gratitude module — instrument pages only, at the foot of <main>.
    if (current && mainEl) {
      var grat = document.createElement("aside");
      grat.className = "ia-grat";
      grat.innerHTML =
          '<div class="ia-grat__in">'
        +   '<div class="ia-grat__txt">'
        +     '<div class="ia-grat__kick">Free to read · no ads · no vendor money</div>'
        +     '<p>One of sixteen instruments, kept current and kept honest by one '
        +     'person. If it saved you a detour through the vendor docs, you can '
        +     'help keep the atlas running.</p>'
        +   '</div>'
        +   '<a class="ia-grat__cta" href="' + SUPPORT + '" data-ia-cta="gratitude_module">'
        +     'Support Infra Atlas <span>→</span></a>'
        + '</div>';
      mainEl.appendChild(grat);
    }

    // Footer support strip — every page except /support itself.
    if (here !== SUPPORT) {
      var strip = document.createElement("div");
      strip.className = "ia-support";
      strip.innerHTML =
          'Infra Atlas is free to read and reader-supported · '
        + '<a href="' + SUPPORT + '" data-ia-cta="footer">Support the atlas →</a>';
      document.body.appendChild(strip);
    }

    // Donation CTAs → analytics. No-op until Plausible is installed
    // (analytics-install.md); fires donation_cta_click once it is.
    document.addEventListener("click", function (e) {
      var a = e.target && e.target.closest && e.target.closest("[data-ia-cta]");
      if (a && typeof window.plausible === "function") {
        window.plausible("donation_cta_click", {
          props: { placement: a.getAttribute("data-ia-cta") }
        });
      }
    });
  })();

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
