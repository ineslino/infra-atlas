/* ──────────────────────────────────────────────────────────────────
   Infra Atlas · shared navigation
   One file, included by every page via <script src="/nav.js" defer>.
   Injects a sticky top bar + an instruments menu. No build step.
   ────────────────────────────────────────────────────────────────── */
(function () {
  "use strict";

  var CLOUD = [
    ["/ec2/",            "EC2 Observatory",        "AWS"],
    ["/regions/",        "Region Map",             "Multi-cloud"],
    ["/azure-vm/",       "VM Atlas",               "Azure"],
    ["/gcp-compute/",    "Compute Index",          "GCP"],
    ["/oci-compute/",    "Compute Observatory",    "OCI"],
    ["/ovh-instances/",  "Instance Catalogue",     "OVH"]
  ];
  var APIM = [
    ["/apim-matrix/",      "Feature Matrix",          "APIM"],
    ["/aws-api-gateway/",  "API Gateway Atlas",       "AWS"],
    ["/apigee/",           "Apigee Atlas",            "Apigee"],
    ["/mulesoft/",         "Mulesoft Atlas",          "Mulesoft"],
    ["/self-hosted-apim/", "Kong · Gravitee · IBM",   "Self-hosted"]
  ];

  // Normalise current path → "/ec2/" form
  var here = location.pathname.replace(/index\.html$/, "");
  if (here.charAt(here.length - 1) !== "/") here += "/";

  function findCurrent() {
    var all = CLOUD.concat(APIM);
    for (var i = 0; i < all.length; i++) {
      if (here.indexOf(all[i][0]) !== -1) return all[i];
    }
    return null;
  }
  var current = findCurrent();

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
    + 'font-size:10.5px;letter-spacing:0.14em;text-transform:uppercase;padding:7px 13px;'
    + 'border-radius:99px;cursor:pointer;display:inline-flex;align-items:center;gap:8px;'
    + 'transition:border-color .15s,color .15s;}'
    + '.ia-nav__btn:hover{border-color:var(--paper-3,rgba(244,239,230,0.42));color:var(--paper,#F4EFE6);}'
    + '.ia-nav__btn.is-open{background:var(--paper,#F4EFE6);color:var(--ink,#0A0907);border-color:var(--paper,#F4EFE6);}'
    + '.ia-nav__caret{transition:transform .2s;}'
    + '.ia-nav__btn.is-open .ia-nav__caret{transform:rotate(180deg);}'
    + '.ia-nav__panel{position:fixed;top:54px;right:clamp(12px,4vw,48px);'
    + 'width:min(340px,calc(100vw - 24px));background:var(--ink-2,#100E0C);'
    + 'border:1px solid var(--line-2,rgba(244,239,230,0.14));border-radius:6px;'
    + 'padding:16px;z-index:61;box-shadow:0 18px 50px rgba(0,0,0,0.55);'
    + 'opacity:0;transform:translateY(-8px);pointer-events:none;transition:opacity .18s,transform .18s;}'
    + '.ia-nav__panel.is-open{opacity:1;transform:translateY(0);pointer-events:auto;}'
    + '.ia-nav__grouplabel{font-family:var(--mono,monospace);font-size:9px;letter-spacing:0.2em;'
    + 'text-transform:uppercase;color:var(--paper-3,rgba(244,239,230,0.42));'
    + 'margin:14px 6px 6px;display:flex;align-items:center;gap:8px;}'
    + '.ia-nav__grouplabel:first-child{margin-top:2px;}'
    + '.ia-nav__grouplabel::after{content:"";flex:1;height:1px;background:var(--line,rgba(244,239,230,0.08));}'
    + '.ia-nav__link{display:flex;align-items:baseline;gap:9px;padding:8px 8px;border-radius:4px;'
    + 'transition:background .12s;}'
    + '.ia-nav__link:hover{background:var(--surface,#161310);}'
    + '.ia-nav__link.is-current{background:var(--surface-2,#1E1A15);}'
    + '.ia-nav__link.is-current .ia-nav__lname{color:var(--accent,#FF7849);}'
    + '.ia-nav__vendor{font-family:var(--mono,monospace);font-size:8.5px;letter-spacing:0.12em;'
    + 'text-transform:uppercase;color:var(--paper-3,rgba(244,239,230,0.42));'
    + 'min-width:64px;flex:none;}'
    + '.ia-nav__lname{font-family:var(--sans,sans-serif);font-size:13px;'
    + 'color:var(--paper,#F4EFE6);}'
    + '.ia-nav__home{display:block;padding:8px;border-radius:4px;font-family:var(--mono,monospace);'
    + 'font-size:10px;letter-spacing:0.14em;text-transform:uppercase;'
    + 'color:var(--paper-3,rgba(244,239,230,0.42));transition:background .12s,color .12s;}'
    + '.ia-nav__home:hover{background:var(--surface,#161310);color:var(--paper,#F4EFE6);}'
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
    ? '<span class="ia-nav__here">' + current[2] + ' · <em>' + current[1] + '</em></span>'
    : '';

  nav.innerHTML =
      '<a class="ia-nav__brand" href="/">'
    +   '<svg class="ia-nav__glyph" viewBox="0 0 32 32" aria-hidden="true">'
    +     '<circle cx="16" cy="6.2" r="3.1" fill="var(--accent,#FF7849)"/>'
    +     '<path d="M16 9.3 L5.8 27.2 M16 9.3 L26.2 27.2 M10.4 20.6 L21.6 20.6" '
    +       'fill="none" stroke="var(--accent,#FF7849)" stroke-width="3.1" '
    +       'stroke-linecap="round" stroke-linejoin="round"/>'
    +   '</svg>'
    +   '<span class="ia-nav__word">Infra Atlas</span>'
    +   hereHtml
    + '</a>'
    + '<button class="ia-nav__btn" id="ia-nav-btn" aria-expanded="false" aria-haspopup="true">'
    +   'Instruments <span class="ia-nav__caret">▾</span>'
    + '</button>';

  function renderGroup(label, items) {
    var html = '<div class="ia-nav__grouplabel">' + label + '</div>';
    items.forEach(function (it) {
      var cur = (here.indexOf(it[0]) !== -1) ? ' is-current' : '';
      html += '<a class="ia-nav__link' + cur + '" href="' + it[0] + '">'
            +   '<span class="ia-nav__vendor">' + it[2] + '</span>'
            +   '<span class="ia-nav__lname">' + it[1] + '</span>'
            + '</a>';
    });
    return html;
  }

  var panel = document.createElement("div");
  panel.className = "ia-nav__panel";
  panel.id = "ia-nav-panel";
  panel.innerHTML =
      '<a class="ia-nav__home' + (here === "/" ? " is-current" : "") + '" href="/">↑ The Atlas — all instruments</a>'
    + renderGroup("Cloud Compute", CLOUD)
    + renderGroup("API Management", APIM);

  document.body.insertBefore(nav, document.body.firstChild);
  document.body.appendChild(panel);

  // ── Behaviour ────────────────────────────────────────────────────
  var btn = document.getElementById("ia-nav-btn");
  function setOpen(open) {
    btn.classList.toggle("is-open", open);
    panel.classList.toggle("is-open", open);
    btn.setAttribute("aria-expanded", String(open));
  }
  btn.addEventListener("click", function (e) {
    e.stopPropagation();
    setOpen(!panel.classList.contains("is-open"));
  });
  document.addEventListener("click", function (e) {
    if (panel.classList.contains("is-open") && !panel.contains(e.target)) setOpen(false);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") setOpen(false);
  });
})();
