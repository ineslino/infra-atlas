# Agent 4 — Auditoria data-driven / colapso de duplicação

**Objetivo:** encontrar dados hardcoded (SKUs, regiões, matrizes, tabelas de vendor) que poderiam vir de config/JSON, e colapsar markup/código duplicado num render genérico, **mantendo comportamento/UX/output/API 100% idênticos**.

## Resumo curto

A maior parte das tabelas/matrizes deste site **já é data-driven**: nenhuma das matrizes nem dos observatórios de compute serve linhas `<tr>` estáticas. Os dados vivem em arrays JS inline (`VENDORS`/`CATEGORIES`/`FEATURES` nas matrizes; `REGIONS`/`FAMILIES` nos compute) e são renderizados client-side por `assets/matrix.js` e `assets/compute-table.js`. Portanto **a oportunidade clássica "mover `<tr>` estáticos para JSON" não existe aqui** — esse trabalho já foi feito.

Onde ainda há LOC a poupar:

1. **A grande vitória real é a "cola" de orquestração das matrizes** (`writeHash`/`applyHash`/`init`/`renderMatrix`/`applyFilter`/`openFeatureDrawer`/`wireEvents`/`bootstrap`), ~190–260 linhas **quase idênticas repetidas em ~9 páginas de matriz**. Isto pode ser içado para `assets/matrix.js` (mecanismo já existente) como um controlador genérico parametrizado. Sem impacto SEO (já é tudo JS-render). **Esta é a única proposta de alto valor e risco gerível.**
2. As páginas **toolbox** (15) partilham estrutura, mas o conteúdo é prosa única por ferramenta e é **HTML estático indexável** → migrar para JSON+render mudaria crawlability/output → **REJECT**.
3. Externalizar os arrays de dados inline das matrizes/compute para `.json` reduziria LOC de HTML mas **muda o payload inicial e o comportamento offline/no-JS**, e nos compute **quebra o pipeline source-of-truth/refresh/CI** (ver ponto crítico abaixo) → **REJECT / HIGH**.

### Ponto crítico descoberto (invalida a ideia óbvia)

Nos observatórios de compute, **o bloco de dados inline É a fonte de verdade**, e `data.json` é o **artefacto derivado**: para `azure-vm`, `gcp-compute`, `oci-compute`, `ovh-instances`, o respetivo `refresh.sh` faz `open('index.html')` e `extract("REGIONS")/("FAMILIES")` para **gerar** o `data.json`. O CI (`.github/workflows/verify-data.yml`) volta a extrair e falha se `data.json` divergir do inline. Logo o "duplicado" inline↔json é **intencional e load-bearing** — remover o inline parte o refresh + o guard de CI. (EC2 é a exceção: puxa do dataset público da Vantage, mas mantém o mesmo invariante de sincronização.)

---

## Tabela de propostas

| bloco | abordagem data-driven proposta | LOC poupado | esforço | risco |
|---|---|---|---|---|
| **Cola de orquestração das matrizes** (`apim-matrix`, `iam-matrix`, `networking-matrix`, `compliance`, `ai-atlas`, `kubernetes`, `confidential-computing`, `observability`, `egress`) | Içar `writeHash/applyHash/init/renderMatrix/applyFilter/openFeatureDrawer/wireEvents/bootstrap` para um controlador genérico em `assets/matrix.js` (mecanismo já existente). Cada página passa só `{VENDORS, CATEGORIES, FEATURES, labels, search-fields, modo-de-toggle}` + chama `IA.matrix.mount(...)`. | **~900–1200** (de ~190–260/página × 9, sobra ~30–50/página de config) | **alto** | **médio** (comportamento idêntico mas exige cuidado nas variações por página, ver abaixo) |
| Toolbox (15 páginas) → 1 render + JSON | Substituir as `.tbx-row` estáticas por fetch de um `tools.json` renderizado client-side | ~1500 bruto | médio | **REJECT** (HTML estático indexável; muda crawlability/no-JS) |
| Dados inline das matrizes → `*.json` externo + fetch | Mover os arrays `VENDORS/CATEGORIES/FEATURES` (200–450 linhas/página) para `.json` e fazer fetch | ~2500 de HTML | médio | **REJECT / HIGH** (muda payload inicial, render no-JS, e estes dados — `value`/`note`/`src` por célula — são conteúdo de referência potencialmente indexável) |
| Dados inline dos compute → só `data.json` (remover snapshot embebido) | Apagar `REGIONS/FAMILIES` inline e depender do fetch | ~2000 de HTML | médio | **REJECT** (inline é a *fonte de verdade* de que `refresh.sh` extrai `data.json`; parte o CI `verify-data` e o estado "Snapshot · embedded" / offline) |
| Lista de instrumentos duplicada (`nav.js` ↔ `build_search_index.py`) | Uma única fonte JSON para `MATRIX/COMPUTE/TOOLBOX` lida por Python e JS | ~25 | baixo | baixo (mas ganho minúsculo; ver nota) |
| Cards de instrumentos na landing (`index.html`) → render de `window.IA.nav` | Gerar os 23 cards via JS a partir do nav | ~250 | médio | **REJECT** (cards estáticos = conteúdo above-the-fold indexável; já há guards `check_landing_stats`/`check_instrument_count` que assumem markup estático) |

---

## Detalhe por proposta

### 1. Cola de orquestração das matrizes — ÚNICA PROPOSTA RECOMENDADA

**O que é:** `assets/matrix.js` já expõe `IA.matrix.{drawer, renderTable, applyVisibility, wireDelegation, escapeHtml, syncChipsAria}`. Mas **cada** página de matriz reimplementa ~190–260 linhas de cola por cima disso, e essa cola é quase byte-a-byte igual entre páginas. Medições (1.ª função de cola → `bootstrap();`):

- `apim-matrix` 193 · `iam-matrix` 213 · `networking-matrix` 195 · `compliance` 203 · `ai-atlas` 243 · `kubernetes` 195 · `egress` 261 · (`confidential-computing` e `observability` têm forma ligeiramente diferente mas comparável).

`diff` entre `apim-matrix` e `networking-matrix` mostra que `writeHash`/`applyHash`/`bootstrap`/`wireEvents`/`openFeatureDrawer` são essencialmente idênticos; as diferenças reais são parametrizáveis:
- rótulos das chips (`"Vendors"` vs `"Clouds"`), título do drawer (`"Per-vendor support"` vs `"Per-cloud detail & sources"`);
- campos incluídos no haystack da pesquisa (`v.cloud` extra no networking);
- o **modo de toggle de vendor**: networking usa o toggle "all + 4 clouds" de 5 botões; apim usa multi-select. São 2 modos finitos → flag de config.

**Abordagem:** mover a cola para `IA.matrix.mount({ tableEl, vendors, categories, features, labels:{vendorChips, category, drawerSection, dimension}, searchFields, vendorToggleMode, statusNoun })`. Cada página fica com o seu `<script>` reduzido a `const VENDORS=[…]; const CATEGORIES=[…]; const FEATURES=[…]; IA.matrix.mount({...});`.

**LOC poupado:** ~190–260/página → ~30–50/página ⇒ **~900–1200 linhas no total** em 9 páginas. É o maior ganho real do site, e cabe no mecanismo já existente (`matrix.js`), sem inventar tooling.

**Verificação de output byte-idêntico:**
- O HTML servido não muda em estrutura estática (a cola já era JS); muda apenas *onde* o JS vive. Logo SEO/no-JS **inalterado** (já não renderizava sem JS).
- DOM diff: abrir cada matriz antes/depois e comparar `#matrix` innerHTML + estado do drawer (snapshot Playwright/`outerHTML`), testando: filtro por categoria, toggle de vendor (ambos os modos), pesquisa `q`, deep-link via `#hash` (`vendors=`/`cat=`/`q=`), abertura de drawer por célula e por cabeçalho, `aria-pressed` das chips.
- CI: `python3 scripts/check_matrix_chrome.py` (continua a exigir o `<style>` inline por página — não tocado) + `check_html_attrs.py` + `check_instrument_count.py` devem passar.
- **Risco médio:** as variações por página (toggle de vendor, campos de pesquisa, rótulos do drawer) têm de ser fielmente parametrizadas; uma diferença subtil no haystack de pesquisa muda quais features aparecem para um dado `q`. Exige um teste de paridade por página antes do merge.

### 2. Toolbox (15 páginas) — REJECT

Cada `/toolbox/<dep>/index.html` partilha a casca (`.tbx-filters` + `.tbx-list` + `.tbx-row`, e `toolbox/filter.js` partilhado), mas o conteúdo é **prosa única**: `subtitle` da masthead, `tldr` por ferramenta (parágrafos densos), nota de rodapé `.about` com casos especiais, e as próprias chips de filtro variam por departamento (Form/Language/Picks com tags diferentes). Contagem de `.tbx-row`: 5–16 por página. Total bruto ~3000 LOC.

Migrar para `tools.json` + render client-side **mudaria o output**: hoje cada `tldr`/nome/repo é **HTML estático indexável** (estas páginas existem em grande parte para SEO de cauda longa: "tig", "git-cliff", etc.). `build_search_index.py` raspa `.tbx-row__name` do HTML estático. Converter para JS-render muda crawlability e o no-JS. **REJECT** pelos não-objetivos (alteração de SEO/output para tabela de referência indexável). `filter.js` já é a parte partilhada e está bem.

### 3. Dados inline das matrizes → JSON externo — REJECT / HIGH

Os arrays `FEATURES` carregam por célula `value` + `note` (prosa longa) + `src` (URL) — **altamente hand-tuned**, não uniformes (confirmado em `apim-matrix`: cada `support.<vendor>` é único). Externalizar para `.json` poupa ~200–450 LOC de HTML por página, mas: (a) muda o payload inicial e o render no-JS; (b) este conteúdo de referência (notas + fontes) é potencialmente indexável. **REJECT/HIGH** — relocaliza dados para um ficheiro não contado em vez de eliminar duplicação real, com troca de comportamento.

### 4. Dados inline dos compute → só `data.json` — REJECT

Ver "Ponto crítico" acima. `azure-vm`/`gcp-compute`/`oci-compute`/`ovh-instances` `refresh.sh` **extraem** `REGIONS`/`FAMILIES` de `index.html` para gerar `data.json`; o CI `verify-data` re-extrai e falha se divergir. O inline é também o fallback offline e controla o indicador `Snapshot · embedded` vs `Live · data.json` (`loadData()` em cada página). Remover o inline parte o pipeline e muda comportamento observável. **REJECT.**

### 5. Lista de instrumentos: `nav.js` ↔ `build_search_index.py` — baixo ganho

`nav.js` já é fonte única para o palette ⌘K **e** para a constelação `/atlas/` (`window.IA.nav`). O `sitemap.py` faz `glob` do filesystem (sem lista hardcoded — nada a fazer). O único duplicado é o trio `MATRIX`/`COMPUTE`/`TOOLBOX` (listas de pastas) em `build_search_index.py`, que mesmo assim **precisa** de ler o HTML de cada página para extrair termos — não é a mesma estrutura de dados que `nav.js`. Poupança ~25 LOC, esforço baixo, **mas o ganho é marginal** e cruza a fronteira JS↔Python (acoplamento novo). Mencionado por completude; baixa prioridade.

### 6. Cards da landing → render de `window.IA.nav` — REJECT

`index.html` tem 23 `.instrument` cards estáticos (confirmado: 23 `class="instrument "` + 23 `instrument__title`). São conteúdo above-the-fold indexável, com descrições e chips de stats por card. `check_landing_stats.py`/`sync_landing_stats.py`/`check_instrument_count.py` assumem markup estático (reescrevem chips no HTML). Converter para JS-render muda SEO/output e parte os guards. **REJECT.**

---

## Total estimado LOC poupado

- **Recomendado (sem mudança de comportamento/SEO):** **~900–1200 linhas** — exclusivamente da consolidação da cola das matrizes para `matrix.js` (proposta 1).
- Proposta 5 (baixa prioridade, cross-language): +~25.
- **Tudo o resto (propostas 2, 3, 4, 6): REJECT** por mudarem output/SEO/no-JS ou partirem o pipeline source-of-truth + CI. Em bruto somariam ~5–6 mil linhas, mas violam os não-objetivos.

**Conclusão:** ao contrário do que o mapa do repo sugere, **não há tabelas estáticas grandes para "JSON-ificar"** — já são data-driven. O único ganho data-driven legítimo e seguro é colapsar a **cola JS duplicada das matrizes** num controlador genérico dentro do `matrix.js` já existente (~1k linhas, risco médio, verificável por DOM-diff + CI verde).
