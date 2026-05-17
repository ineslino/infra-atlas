# Infra Atlas — Logo system

_Design — 2026-05-17. Status: built._

A full logo system: an **"IA" monogram** mark, the Instrument Serif wordmark,
defined lockups, colour variants, sizing rules and a file set — so the identity
holds from a 16px favicon to a page header, and contributors don't drift it.

## Decisions

Settled in the 2026-05-17 brainstorm, with one mark revision:

| # | Decision | Choice |
|---|----------|--------|
| 1 | Scope | A full logo **system**. |
| 2 | Mark | An **"IA" monogram** — roman "I" + italic "A", Instrument Serif. *(An earlier contour-rings mark was built and rejected — nested circles read as a generic bullseye.)* |
| 3 | Wordmark typeface | **Instrument Serif** — a masthead / nameplate treatment. |
| 4 | Wordmark expression | "Infra" roman + "Atlas." italic, period kept; **single-colour** — the orange accent lives in the mark only, never the word. |

## 1 · The mark — the "IA" monogram

The mark is a two-letter monogram: a roman **"I"** and an italic **"A"**, set as
a tight pair in Instrument Serif. It is the system's anchor and the **only**
element that carries the orange accent (`#FF7849`).

**Why this construction.** The roman-I / italic-A pairing is the *same move* as
the wordmark — "Infra" roman, "Atlas." italic. The monogram therefore carries
the brand's signature typographic device: it is the project's initials in the
project's own typeface, which makes it ownable rather than generic.

- Built by outlining the "I" (Instrument Serif Regular) and the "A" (Instrument
  Serif Italic) to vector paths, set ~0.05em apart.
- Roughly square — ~753 × 730 in a 1000-unit em.
- No font dependency — the letters ship as outlined paths.

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

1. **Horizontal** (primary) — monogram left, wordmark right, optically centred.
2. **Stacked** — monogram above, wordmark centred below.
3. **Mark only** — favicon, nav glyph, app icon, Open Collective / GitHub avatar.
4. **Wordmark only** — running text, or where the mark already appears nearby.

**Built proportions** — monogram height = `M`:

- **Horizontal**: wordmark cap-height `0.52·M`; monogram-to-wordmark gap
  `0.42·M`; lockup aspect ≈ 4.1 : 1.
- **Stacked**: wordmark cap-height `0.40·M`; vertical gap `0.24·M`; lockup
  aspect ≈ 1.22 : 1 (w : h).

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

The monogram **is** the favicon — no separate simplified variant. "IA" stays
legible down to ~16px; at 16px the high-contrast serif strokes run fine but
hold. `favicon.svg` (repo root) is the monogram; `favicon-16.png` /
`favicon-32.png` are raster fallbacks.

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
- **`favicon.svg`** (repo root) — the monogram.
- This spec.

## 8 · Usage — don'ts

- Don't recolour the wordmark, or move the orange onto the word.
- Don't restyle the monogram — don't re-pick fonts or change the roman/italic
  split; it mirrors the wordmark deliberately.
- Don't place the orange mark on a low-contrast background — use the mono
  variant instead.
- Don't stretch, rotate, skew, or recompose a lockup.
- Don't add effects — shadows, gradients, glows.
- Don't intrude on the clear space.
