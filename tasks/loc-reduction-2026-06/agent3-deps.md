# Agent 3 — Dependency audit (LOC + bundle impact)

Scope: unused deps, deps duplicating stdlib/runtime, heavy deps used for one trivial
thing. Read-only audit. Goal is LOC reduction with **100% identical behaviour/UX/output/API**.

## Summary

Infra Atlas is a static site (Cloudflare Workers, `wrangler.jsonc` → `assets.directory: "."`).
There is **no `package.json`, no lockfile, no `requirements.txt`, no `pyproject.toml`** anywhere
in the repo (`git ls-files` confirms). So there is **nothing declared to be unused** — there is
no dependency manifest to prune at all.

The practical dependency surface is three things:

1. **`assets/three.min.js`** — the one heavy vendored library. 654 KB raw / ~163 KB gzip /
   ~132 KB brotli. Single biggest vendored file in the repo. Used **only** by `globe.js` on
   **only** `index.html`. It is a real WebGL 3D library that `globe.js` genuinely exercises
   (~20 distinct `THREE.*` primitives). Removing/shrinking it **changes the visual** → does
   **not** qualify under the non-objectives. **REJECT for now** (details below).
2. **Python scripts (`scripts/*.py` + 2 task scripts)** — **100% standard library**. Zero
   third-party imports. Nothing to swap, nothing to remove. (One script shells out to a
   system Chrome for OG screenshots, but that is not a vendored/declared dep.)
3. **Google Fonts** (remote `<link>`, bundle-only, not repo LOC) — **no over-fetch**. Every
   requested weight (300/400/500/600/700) and the Instrument Serif italic are actually used
   in CSS. Nothing to trim without changing rendering.

There are **no remote `<script src>` tags at all** (no analytics, no CDN JS, no duplicate-of-vendored
libs). The only remote bundle assets are Google Fonts (CSS + woff2 from gstatic) and the
font preconnect.

**Net actionable LOC/bundle win from a dependency standpoint: effectively zero** without
changing behaviour. This is already a lean, dependency-light static site. The detail below
documents why each candidate is rejected, so a future pass does not re-litigate it.

## Required table

| dep | uso real | substituível por | LOC poupado (repo) | bundle poupado (KB) | risco |
|---|---|---|---|---|---|
| `assets/three.min.js` (Three.js r160 UMD min) | Globe decorativo em `index.html` via `globe.js`; usa ~20 primitivas `THREE.*` (Scene, WebGLRenderer, PerspectiveCamera, Mesh, *Geometry, ShaderMaterial, etc.) | Nada equivalente sem mudar o visual. WebGL nativo/CSS faria outra coisa, não o mesmo globo | 0 (manter) | 0 (manter) | **ALTO / REJECT** — muda o visual |
| Python third-party deps | Nenhuma. Todos os imports são stdlib | n/a | 0 | 0 | n/a (nada a remover) |
| Deps declaradas não usadas | Não existe manifesto (`package.json`/`requirements.txt`/lock) | n/a | 0 | 0 | n/a |
| Google Fonts (`fonts.googleapis.com/css2`) | Instrument Serif (+italic), JetBrains Mono, Manrope; pesos 300–700 todos usados | Sem over-fetch a cortar | 0 | 0 (sem corte seguro) | n/a (já minimal) |
| `wrangler` (CLI) | Só referenciado no `$schema` do `wrangler.jsonc`; não é dep commitada nem node_modules no repo | n/a | 0 | 0 (CLI dev, não vai para o browser) | n/a |
| Libs vendored/inline duplicadas | Nenhuma encontrada | n/a | 0 | 0 | n/a |

**Totais — repo LOC poupado: 0 · bundle KB poupado: 0** (sem alterar comportamento/visual).
A única poupança grande possível (`three.min.js`: ~654 KB repo / ~132 KB brotli no browser)
está marcada **REJECT** porque altera o visual.

---

## Detail per item

### 1. `assets/three.min.js` — the big one (REJECT)

- **Size:** 669,884 bytes (654.1 KB) raw; 167,141 bytes (163.2 KB) gzip; 135,355 bytes
  (132.2 KB) brotli. The file is minified onto effectively one logical line (`wc -l` = 7).
  This is the single largest vendored asset in the repo by far.
- **Version:** Three.js **r160**, the deprecated UMD `build/three.min.js` global build
  (the file even emits the r150+ deprecation `console.warn` at load). Copyright banner
  "2010-2023 Three.js Authors", MIT.
- **Where used:** loaded **only** in `index.html`, and only via a deferred loader
  (`index.html` lines ~52-69): it is skipped entirely when
  `prefers-reduced-motion: reduce`, when `window.innerWidth <= 768` (mobile), or when
  `navigator.connection.saveData` is set; otherwise injected on `requestIdleCallback`
  (4 s timeout). `globe.js` (the only consumer) also re-guards on
  `typeof THREE === 'undefined'` and on WebGL availability.
- **What `globe.js` actually uses** (real WebGL 3D, not decoration-by-CSS):
  `THREE.Scene`, `WebGLRenderer`, `PerspectiveCamera`, `Group`, `Mesh` (×5),
  `SphereGeometry` (×4), `RingGeometry`, `BufferGeometry` (×3), `Line` (×3),
  `MeshBasicMaterial`/`MeshPhongMaterial`/`LineBasicMaterial`/`ShaderMaterial`,
  `Vector3` (×4), `Color` (×4), `AmbientLight`, `DirectionalLight`,
  `AdditiveBlending`, `DoubleSide`/`FrontSide`. It renders a rotating textured/shaded
  globe with AWS region markers and arc lines. This is genuine 3D rendering.
- **Could a smaller subset / native WebGL / CSS do the same?** Not at identical visual
  output. A hand-rolled WebGL globe or a CSS globe would be a **different artefact**, and
  building a tree-shaken Three.js ESM subset would (a) add a build step (new
  tooling/complexity, against the spirit of "no build step" stated in `globe.js`'s own
  header) and (b) is a new-dep/refactor move, not a behaviour-identical removal.
- **Verdict:** **HIGH risk / REJECT under the non-objectives.** The globe is decorative
  but it is a visible part of the landing UX on desktop, so removing or replacing it is a
  UX/visual change, not a behaviour-identical LOC trim. Honestly: this is the only place
  with a large repo-LOC and bundle win, and it does **not** qualify.
  - *If* the project owner ever decides the globe is expendable (separate product decision,
    outside this audit's mandate), deleting `assets/three.min.js` + `globe.js` + the loader
    block in `index.html` would remove ~403 repo "lines" (but ~684 KB of source) and ~132 KB
    brotli off the desktop landing page. Flagging the magnitude only; **not recommending it.**
- **How to verify (if ever touched):** load `index.html` on desktop with motion enabled →
  globe must render and spin identically; check `prefers-reduced-motion`, mobile width, and
  save-data paths still render the page with no globe and no console errors. Any pixel
  difference = behaviour change = reject.

### 2. Python scripts — already 100% stdlib (nothing to do)

Audited all 18 `scripts/*.py` plus `tasks/expert-review-2026-06/build_report.py` and
`tasks/features-2026-05/integrity/build_region_audit.py`. **Every import is Python standard
library:** `json, os, sys, re, glob, html, csv, datetime, hashlib, subprocess, tempfile,
contextlib, functools, threading, socket, socketserver, http.server, shutil, importlib.util,
collections.{Counter,defaultdict}, email.utils.format_datetime, xml.sax.saxutils.escape`.

- No `requests`, `beautifulsoup4`, `lxml`, `Pillow/PIL`, `jinja2`, `markdown`, `yaml`, etc.
- The brief's hypothesis ("heavy lib for a trivial job that stdlib covers") **does not apply
  here** — the scripts already use the stdlib equivalents directly (e.g. `xml.sax.saxutils`
  for RSS escaping in `build_feed_rss.py`, `html` in `build_decisions.py`,
  `http.server`/`socketserver` for the local screenshot server in `build_og.py`).
- `scripts/build_og.py` shells out to a **system-installed Chrome** (`find_chrome()` →
  `subprocess.run([chrome, "--headless=new", ...])`) to screenshot the OG card. That is an
  external system binary, **not** a vendored or declared Python dependency, so there is
  nothing in-repo to remove and no LOC to reclaim. Leave as-is.
- **Verdict:** zero LOC savings available; no risk taken. Nothing to change.

### 3. Unused declared deps — none, because no manifest exists

`git ls-files | grep -iE 'package.*json|lock|requirements|pyproject|setup|Pipfile|poetry'`
returns nothing. There is no dependency manifest in the repo, so there is nothing declared-
but-unused to prune. `wrangler` appears only as a `$schema` path hint inside `wrangler.jsonc`
(`node_modules/wrangler/config-schema.json`); `node_modules/` is not committed and there is no
lockfile, so `wrangler` is a dev CLI, not a committed/shipped dependency. No action.

### 4. Google Fonts / remote assets — bundle-only, no over-fetch (no action)

- 63 HTML pages reference `fonts.googleapis.com`. Two distinct `css2` requests:
  - **Full set** (61 pages): `Instrument+Serif:ital@0;1` + `JetBrains+Mono:wght@300;400;500;600`
    + `Manrope:wght@300;400;500;600;700`.
  - **Reduced set** (2 pages: `404.html`, `_ogcard.html`): `Instrument+Serif:ital@0;1` +
    `JetBrains+Mono:wght@400;500` + `Manrope:wght@400;500`. (`_ogcard.html` is in
    `.assetsignore` anyway, so it never ships.)
- **Are the fetched weights actually used?** Yes. Counting `font-weight` declarations across
  all committed CSS/HTML: 300 ×6, 400 ×112, 500 ×140, 600 ×28, 700 ×9 — **all five weights
  are used.** Instrument Serif italic (`ital@1`) is also genuinely used (`font-style: italic`
  on `var(--serif)` in `assets/matrix.css`, `decisions/decision.css`, `tools/shared.css`).
- **Conclusion:** **no over-fetch to trim.** The request is already matched to real usage.
  Cutting any weight would change rendering (browser would synthesise/fallback) → behaviour
  change → reject. Self-hosting is explicitly out of scope (adds files/complexity). **No action.**
- This is a **bundle-only** consideration (remote `<link>` + gstatic woff2), not repo LOC.

### 5. Duplicate / re-vendored libs — none

- The only vendored third-party JS is `assets/three.min.js`. The other JS files
  (`globe.js` 396, `nav.js` 755, `assets/matrix.js` 235, `assets/compute-table.js` 254,
  `assets/feed.js` 74, `toolbox/filter.js` 70) are all first-party, hand-written, no minified
  vendor blobs inside them.
- No CDN library duplicates anything vendored (there are **no** remote `<script src>` tags).
- Grep hits for `lodash`/`d3.`/etc. in HTML were **content text false positives** (e.g. the
  word "lodash" in prose, `VM.Standard3.*` SKU strings matching `d3.`), not library usage.
- **No action.**

---

## Totals

| Bucket | Removable now (behaviour-identical) |
|---|---|
| **Repo LOC saved** | **0** |
| **Bundle KB saved** | **0** |

Largest theoretical win (`three.min.js`, ~654 KB repo source / ~132 KB brotli on the desktop
landing page) is **REJECTED**: it is a visible UX/visual element, so removing it violates the
"100% identical behaviour/UX" constraint. Documented for magnitude only.

## Behaviour-changing items explicitly flagged

- **`assets/three.min.js` removal/replacement → HIGH risk / REJECT** (visual change to the
  landing globe).
- **Trimming any Google Font weight / italic → REJECT** (changes text rendering; all weights
  are in use).
- Everything else: nothing to remove (no manifest, all-stdlib Python, no duplicate libs).

## How this was verified

- Manifest/lockfile search: `git ls-files | grep -iE 'package.*json|lock|requirements|pyproject|...'` → empty.
- Python imports: enumerated every `import`/`from` line across all `.py` files → all stdlib.
- Three.js size: `wc -c`, `gzip -c | wc -c`, `brotli -c | wc -c`.
- Three.js usage: `grep -oE 'THREE\.[A-Za-z0-9_]+' globe.js`; loaders via `index.html` lines 52-69.
- Fonts: counted `fonts.googleapis` `<link>` URLs and cross-checked every `font-weight` /
  `font-style: italic` declaration in committed CSS/HTML.
- Remote scripts: `grep -rnE '<script[^>]*src="https?://'` → none.

To regression-check any future change here: run the repo's own CI guards (`scripts/check_*.py`),
load the affected page (landing `index.html` for the globe; any content page for fonts), and
diff rendered output / take a visual pass. Any difference = reject.
