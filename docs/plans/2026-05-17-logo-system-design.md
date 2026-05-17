# Infra Atlas — Logo system

_Design — 2026-05-17. Status: built._

A full logo system: a **compass-star** mark, the Instrument Serif wordmark,
defined lockups, colour variants, sizing rules and a file set — so the identity
holds from a 16px favicon to a page header, and contributors don't drift it.

## Decisions

| # | Decision | Choice |
|---|----------|--------|
| 1 | Scope | A full logo **system**. |
| 2 | Mark | An **8-point compass star** — the cartographer's instrument. *(Two earlier marks were built and rejected: a contour-rings mark read as a generic bullseye; an "IA" monogram read as a confusing letter-junction.)* |
| 3 | Wordmark typeface | **Instrument Serif** — a masthead / nameplate treatment. |
| 4 | Wordmark expression | "Infra" roman + "Atlas." italic, period kept; **single-colour** — the orange accent lives in the mark only, never the word. |

## 1 · The mark — the compass star

An **8-point compass star**: four long cardinal points and four short
intercardinal points, sharp straight edges, solid fill. It is the cartographer's
instrument — navigation, the compass rose engraved on an atlas — which ties it
straight to the project's name and voice ("Atlas", "the cartographer"). It is
the system's anchor and the **only** element that carries the orange accent
(`#FF7849`).

**Why this mark.** It is unmistakably a compass — simple, sharp, eye-catching —
and it is *not* the iconography cloud/infra tools default to (clouds, hexagons,
node-graphs), so it is distinctive in this space. As a solid silhouette it also
reads cleanly at every size, down to a 16px favicon.

**Geometry.** 8 points; cardinal tip radius 100, intercardinal tip radius 50,
inner (valley) radius 28; a 200 × 200 box, one point straight up. Pure vector —
no font dependency.

## 2 · The wordmark

"Infra Atlas." set in **Instrument Serif**:

- **"Infra"** roman, **"Atlas."** italic — the period kept, set in the italic.
- Mixed case — not caps.
- **Single ink**: `#0A0907` on light, `#F4EFE6` on dark. No colour split, no
  weight change. The roman → italic shift is the only contrast, and it is
  typographic, so the wordmark survives in any single colour.
- Outlined to vector paths in every deliverable — no font dependency.
  Instrument Serif is OFL-licensed; outlining it is permitted.

## 3 · The lockups

Four forms:

1. **Horizontal** (primary) — compass star left, wordmark right, optically
   centred.
2. **Stacked** — compass star above, wordmark centred below.
3. **Mark only** — favicon, nav glyph, app icon, Open Collective / GitHub avatar.
4. **Wordmark only** — running text, or where the mark already appears nearby.

**Built proportions** — mark height = `M`:

- **Horizontal**: wordmark cap-height `0.46·M`; mark-to-wordmark gap `0.32·M`;
  lockup aspect ≈ 3.66 : 1.
- **Stacked**: wordmark cap-height `0.36·M`; vertical gap `0.16·M`; lockup
  aspect ≈ 1.19 : 1 (w : h).

## 4 · Clear space

A margin equal to the **wordmark's cap-height** on every side of any lockup.
Nothing — text, page edges, other logos — intrudes.

## 5 · Colour variants

| Variant | Background | Mark | Wordmark |
|---------|-----------|------|----------|
| On paper | light (`#F4EFE6`) | orange `#FF7849` | ink `#0A0907` |
| On ink | dark (`#0A0907` / `#161310`) | orange `#FF7849` | paper `#F4EFE6` |
| Mono | any | single ink | same single ink |

The **mono** variant — the whole logo in one ink, no orange — is for one-colour
print, embossing, busy photographic backgrounds, or anywhere colour can't be
trusted. Same shapes, one colour, never a redraw.

## 6 · Sizing & the favicon

The compass star **is** the favicon — a solid silhouette, legible down to 16px,
no separate simplified variant needed. `favicon.svg` (repo root) is the star;
`favicon-16.png` / `favicon-32.png` are raster fallbacks.

| Form | Minimum | Below the minimum |
|------|---------|-------------------|
| Mark only | ~16px | — |
| Stacked lockup | ~72px tall | step down to mark only |
| Horizontal lockup | ~120px wide | step down to mark only |

## 7 · File set

All under `brand/`:

- **SVG sources** — `mark.svg`, `mark-mono.svg`, `wordmark.svg`,
  `lockup-horizontal-{paper,ink,mono}.svg`, `lockup-stacked-{paper,ink,mono}.svg`.
- **PNG exports** — `avatar.png` (1024², Open Collective / GitHub avatar),
  `apple-touch-icon.png` (180²), `favicon-16.png`, `favicon-32.png`,
  `lockup-horizontal-{ink,paper}.png`, `lockup-stacked-{ink,paper}.png`.
- **`preview.html`** — a visual contact sheet of the whole system.
- **`favicon.svg`** (repo root) — the compass star.
- This spec.

## 8 · Usage — don'ts

- Don't recolour the wordmark, or move the orange onto the word.
- Don't restyle the mark — don't change the point count or proportions.
- Don't place the orange mark on a low-contrast background — use the mono
  variant instead.
- Don't stretch, rotate, skew, or recompose a lockup.
- Don't add effects — shadows, gradients, glows.
- Don't intrude on the clear space.
