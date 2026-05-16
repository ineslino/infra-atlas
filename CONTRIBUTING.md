# Contributing to Infra Atlas

Infra Atlas is a cross-referenced reference for cloud and API-management infrastructure. The most valuable contribution is **keeping the data right** — a wrong region or a stale limit is a bug.

## Principles

- **Static and credential-free.** Plain HTML/CSS/JS, no build step, no framework. Every data refresh runs from public sources — no cloud account, no API keys.
- **Every claim is sourced.** A number, a limit, a tier, an availability fact — if it isn't backed by a vendor doc, it doesn't ship. Cite the upstream URL in a comment next to the data.
- **Editorial, not a dashboard.** New instruments are reference pages, not apps.

## Repo layout

```
index.html              landing page
<instrument>/index.html  one folder per instrument (ec2, regions, apim-matrix, …)
<instrument>/data.json   generated artifact — do not hand-edit
<instrument>/refresh.sh  regenerates data.json
nav.js                   shared nav bar + ⌘K palette, injected into every page
.github/workflows/       daily refresh + data-sync verification
```

## Fixing data

1. Data lives **embedded in the instrument's `index.html`** (a `const` array in a `<script>` block) — that is the source of truth.
2. Edit the embedded data. Add a comment with the upstream source URL.
3. Run `./<instrument>/refresh.sh` to regenerate `data.json`.
4. Commit both files. CI (`verify-data.yml`) checks they stay in sync.

Never edit `data.json` directly — it is overwritten by `refresh.sh`.

## Adding an instrument

Copy an existing instrument folder, keep the shared design tokens (`:root` CSS variables) and `<script src="/nav.js" defer>`, register it in `nav.js`'s instrument list.

## Issues & pull requests

- **Spotted wrong data?** [Open an issue](https://github.com/ineslino/infraatlas/issues/new) — include the upstream source that contradicts the site.
- PRs: keep them scoped to one instrument; include the source for any data change.

MIT-licensed. Built by independent engineers who got tired of grepping vendor docs across five tabs.
