# Agent 2 — Dead / unused code audit

**Âmbito:** exports nunca importados, funções nunca chamadas, ramos inalcançáveis, CSS órfão,
assets não referenciados, HTML órfão, refs `<link>`/`<script>` mortas, `?v=` inconsistentes.
**Regra:** read-only; comportamento/UX/output/API públicos 100% idênticos.

## Resumo

A base é notavelmente limpa. Toda a **JS partilhada** (`nav.js`, `globe.js`, `assets/compute-table.js`,
`assets/matrix.js`, `assets/feed.js`, `toolbox/filter.js`) tem todos os exports/funções usados; verifiquei
cada export contra todas as páginas que o carregam. Todos os **18 scripts Python** estão limpos: nenhuma
função/constante por usar, nenhum ramo morto, nenhum bloco comentado (confirmado por AST + grep, sem
imports cruzados entre scripts — são CLIs autónomos). Todos os ficheiros de dados (`*/data.json`, `feed.json`,
`dispatches.json`, `search-index.json`, `region-reference.json`, `feed.xml`) estão referenciados. **Sem**
refs locais `<link>`/`<script>` mortas; **sem** desencontros de `?v=` (cada asset usa um único valor coerente
em todas as páginas).

O que existe de morto é quase todo **CSS órfão dentro dos `<style>` inline** das páginas grandes: regras
deixadas por modelos de UI já substituídos, e um bloco de "diagrama" copiado para 3 páginas APIM e nunca
aplicado. Mais um diretório de marca (`/brand/`) que o site servido nunca referencia (decisão do dono, não é
quick win).

**Nota crítica sobre falsos positivos (confirmados e descartados):** as classes `col-*`, `hide-*`,
`cell-value--*`, `vendor-row__mark--*`, `cloud-row__mark--*`, `prov-row__rate--*`, `brief__flag--*`,
`tier-*`, `why--*`, `cloud-/bd-/sw-*`, `cloud-tag`/`swatch` são **construídas dinamicamente** via template
literals (`col-${v.key}`, `--${s.level}`, etc.) ou `classList.toggle`. NÃO são mortas. Igualmente, `w3`/`org`
nos resultados de grep são artefactos da minha regex a apanhar `w3.org` dentro de URLs SVG/namespaces.

---

## Lista (ficheiro:símbolo | confiança remoção | LOC)

### HIGH (quick wins seguros — CSS órfão, zero impacto visual/comportamental)

| ficheiro:símbolo | confiança | LOC |
|---|---|---|
| `apigee/index.html:227-245` + `:305` — bloco `.diagram`, `.diagram__node`, `.diagram__node.is-aws`, `.diagram__arrow`, `.diagram__label` + override `@media .diagram` | alta | ~20 |
| `mulesoft/index.html:227-245` + `:305` — mesmo bloco `.diagram*` | alta | ~20 |
| `self-hosted-apim/index.html:227-245` + `:305` — mesmo bloco `.diagram*` | alta | ~20 |
| `index.html:844-866` — `.instrument__status` + `.instrument__status.is-live/.is-dev/.is-planned` (modelo de "status badge" substituído por `.instrument__type[data-type]`) | alta | ~23 |
| `index.html:934-944` — `.instrument__cta.is-disabled` + `.instrument__cta.is-disabled .instrument__cta-arrow` (nenhum CTA é `is-disabled`) | alta | ~9 |
| `confidential-computing/index.html:230-232` — `.matrix th .cloud-tag .cloud-sub` (o template de `cloud-tag` na linha 838 só emite `.swatch` + texto) | alta | 3 |
| `iam-matrix/index.html:206-210` — `.cell-note` | alta | 5 |
| `observability/index.html:126` — `.chip--section.is-active` (os chips são gerados como `.chip`, nunca `.chip--section`) | alta | 1 |
| `regions/index.html:335-340` — `.world-chart .continent-label` (o SVG `.world-chart` existe mas nenhum `.continent-label` é emitido) | alta | ~6 |
| `tools/subnet/index.html:66` — `.ccard.is-most` | alta | 1 |
| `self-hosted-apim/index.html:141-146` — `.compare-card.is-featured` + `.compare-card.is-featured::before` (nenhum `.compare-card` recebe `is-featured`) | alta | ~6 |
| `confidential-computing/index.html:373-374` — `.drawer__prose` + `.drawer__prose strong` (drawer body não usa `drawer__prose`) | média-alta | 2 |

**Subtotal HIGH:** ~116 LOC.

### LOW / juízo do dono (não mexer sem decisão)

| ficheiro:símbolo | confiança | LOC / nota |
|---|---|---|
| `brand/` — diretório inteiro (`preview.html` + 17 PNG/SVG) nunca referenciado por nenhuma página servida | baixa (decisão) | 123 LOC de HTML + 17 ficheiros binários |
| `brand/*.png` (7 ficheiros: `apple-touch-icon`, `favicon-16/32`, `lockup-*-{ink,paper}.png`) — não referenciados nem sequer por `preview.html` | baixa (decisão) | 7 ficheiros binários (0 LOC) |

---

## Como verificar que cada remoção é segura

**Bloco `.diagram*` (apigee / mulesoft / self-hosted-apim):**
- `grep -coE 'class="[^"]*(diagram__node|diagram__arrow|diagram__label|is-aws)' <page>` → `0` em todas.
- `grep -nE 'class="[^"]*diagram' <page>` → vazio (o container `.diagram` também não é aplicado).
- As vars `--apigee` (13 usos) / `--mulesoft` (13 usos) usadas no bloco continuam usadas noutros sítios — remover o bloco não orfã a var.
- É CSS copiado de um template de "deployment diagram" que estas páginas nunca renderizaram.
- Verificação: página continua a renderizar idêntica (nenhum elemento usa estas classes).

**`index.html` `.instrument__status*` + `.instrument__cta.is-disabled`:**
- `grep -nE 'class="[^"]*(instrument__status|is-dev|is-planned|is-disabled)' index.html` → vazio.
- Os cartões são markup estático (`<a class="instrument is-live" …>`), todos `is-live`; a UI atual usa `.instrument__type[data-type=...]` (linhas 871-885) que se mantém.
- **MANTER** `.instrument.is-live` (linha 772) e `.instrument__cta`/`.instrument__cta-arrow` base — esses são usados (markup linha 1226+).

**`cloud-sub`, `cell-note`, `chip--section.is-active`, `continent-label`, `is-most`, `compare-card.is-featured`, `drawer__prose`:**
- Para cada token: `grep -oc '<token>' <page>` devolve exatamente `1` (ou `2` quando há 2 selectores), ou seja só a definição do selector, nunca uma aplicação em `class="…"` nem num template `${…}`.
- Confirmei que os pais/irmãos ativos (`.chip`, `.world-chart`, `.compare-card`, `.cloud-tag`/`.swatch`, `.drawer__head/__body`) continuam usados — só o filho/modificador específico é órfão.

**`/brand/`:**
- `grep -rn '/brand/' --include='*.html' --include='*.js' .` (excl. `tasks/`, `brand/preview.html`) → vazio.
- Favicon servido = `/favicon.svg?v=2`; OG = `/og.png?v=3`; ícones inline. Nada aponta para `/brand/`.
- `preview.html` só se referencia a si próprio (título) e a 8 dos SVGs/avatar; os 7 PNG não são usados por ninguém.
- **Cuidado:** é material de marca intencional e *é servido* (não está no `.assetsignore`). Remover é decisão editorial, não dead-code óbvio. Listado como baixa confiança.

**Garantia geral:** removendo apenas regras CSS cujas classes não aparecem em nenhum `class="…"` nem em
nenhuma string de template `${…}` em todo o repo (html/js/css/py/json), o output renderizado é byte-idêntico.
CI relevante: `verify-data.yml`, `verify-freshness.yml`, `refresh.yml` não tocam CSS inline; os guardas
`check_matrix_chrome.py` / `check_landing_stats.py` / `check_html_attrs.py` validam estrutura/atributos, não
estes selectores órfãos — devem manter-se verdes.

---

## Total estimado de LOC poupado

- **HIGH (CSS órfão, seguro, comportamento idêntico):** **~116 LOC** distribuídas por 8 páginas.
- **LOW / decisão do dono:** `brand/preview.html` 123 LOC + 17 ficheiros de imagem (binários, 0 LOC de código) — só se o dono decidir descontinuar o kit de marca.

**Recomendação:** aplicar só o tier HIGH (~116 LOC). O tier LOW é juízo editorial sobre o kit de marca, não dead code de comportamento.

---

## O que verifiquei e está LIMPO (sem ações)

- `nav.js`, `globe.js`, `assets/compute-table.js`, `assets/matrix.js`, `assets/feed.js`, `toolbox/filter.js` — todos os exports/funções usados (cross-check contra todas as páginas que os carregam: `syncChipsAria`, `urlState`, `wireDelegation`, `applyVisibility`, `renderTable`, `drawer.*`, `computeTable.{render,clear,deselect,hideDock}` — todos com call-sites).
- `assets/matrix.css`, `assets/compute-table.css`, `assets/feed.css`, `tools/shared.css`, `decisions/decision.css` — classes todas usadas (incl. dinâmicas e legendas).
- 18 scripts Python — AST: nenhuma def/const por usar, nenhum ramo morto, nenhum bloco comentado, `check_region_drift.py` `update()`/`check()` ambos alcançáveis via CLI.
- Ficheiros de dados todos referenciados; `_ogcard.html` é intencional (usado por `build_og.py`, validado por `check_og_card.py`, excluído via `.assetsignore`).
- Sem refs `<link>`/`<script>` locais mortas; sem desencontros de `?v=`.
- Os CSV em `tasks/` e `panel-raw.json` são artefactos de dev, não servidos (a única menção a `.csv` em `regions/index.html` linha 1636 é um comentário, não um fetch).
