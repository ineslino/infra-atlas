# Redução de LOC, infra-atlas (síntese da auditoria 2026-06)

Objetivo: reduzir linhas de código mantendo 100% do comportamento, features, dados, UX, output e API públicos.
Método: 4 agentes paralelos, 1 objetivo cada. Relatórios completos em `tasks/loc-reduction-2026-06/agent{1,2,3,4}-*.md`.

> Regra de escrita: este documento evita o carácter travessão por preferência do dono do repo.

## TL;DR

- O repo já é notavelmente limpo: **zero dependências a podar** (não existe sequer manifesto; Python é 100% stdlib), **zero código morto em JS/Python**, e as tabelas grandes **já são data-driven** (renderizadas por `compute-table.js` / `matrix.js`).
- A duplicação real é **CSS de "page chrome" inline copiado verbatim entre páginas da mesma família**, e **cola JS de orquestração das matrizes** repetida em ~9 páginas. O repo já tem o padrão de correção (ficheiros partilhados via `<link>`/`<script>`), por isso não é preciso tooling novo.
- **Achado crítico de verificação:** o guard de CI `scripts/check_matrix_chrome.py` **exige** que cada página de matriz defina `.masthead` num `<style>` inline. Logo a maior fatia de CSS de matriz **não pode ser extraída sem reescrever o guard** (que existe para apanhar um bug real já shipado). Reclassificada para "bloqueada".

## Baseline (LOC atual, ficheiros versionados)

| Camada | LOC | Notas |
|---|---:|---|
| HTML | 38 413 | 64 ficheiros; o grosso da duplicação |
| Python (`scripts/`) | 2 492 | 16 build/sync/check + test |
| JS (autoral) | ~1 784 | nav, globe, compute-table, matrix, feed, filter |
| JS (vendored) | 7 | `assets/three.min.js` (654 KB, 1 linha lógica) |
| CSS | 804 | compute-table, matrix, feed, tools/shared, decisions |
| Shell (`refresh.sh`) | 946 | fora de âmbito desta redução |
| **Código (HTML+CSS+JS autoral+Python)** | **~43 493** | base de comparação |

## Cenários de redução (sem dupla contagem)

| Cenário | LOC poupado | LOC pós | % |
|---|---:|---:|---:|
| Só quick wins (Tier 0, risco baixo) | ~141 | ~43 350 | ~0,3% |
| Tier 0 + Tier 1 (recomendado, risco médio, com precedente) | ~6 200 | ~37 300 | ~14% |
| + Tier 2 (matriz CSS, só se o guard for reescrito) | ~8 200 | ~35 300 | ~19% |

Todos os números são líquidos (já descontam o ficheiro partilhado que cada extração cria).

---

## Propostas, ordenadas por relação ganho/risco

Legenda risco: 🟢 baixo · 🟡 médio · 🔴 alto/bloqueado · ⛔ REJECT (viola não-objetivos).

### Tier 0, quick wins (risco baixo, fazer primeiro)

- [ ] **0.1 — Remover CSS órfão inline (~116 LOC)** 🟢
  Regras CSS deixadas por modelos de UI substituídos, nunca aplicadas a nenhum elemento. Agente 2, alta confiança. Por ficheiro:
  - `apigee/index.html`, `mulesoft/index.html`, `self-hosted-apim/index.html`: bloco `.diagram*` (linhas ~227-245 + override ~305), ~20 LOC cada.
  - `index.html:844-866` `.instrument__status*` (~23) e `index.html:934-944` `.instrument__cta.is-disabled` (~9), substituídos por `.instrument__type[data-type]`.
  - Singletons: `confidential-computing` `.cloud-sub` (3) + `.drawer__prose` (2); `iam-matrix` `.cell-note` (5); `observability` `.chip--section.is-active` (1); `regions` `.continent-label` (~6); `tools/subnet` `.ccard.is-most` (1); `self-hosted-apim` `.compare-card.is-featured` (~6).
  - **Como verificar:** para cada token, `grep -c` em todo o repo (html/js/css/py/json) confirma que aparece só como definição de seletor, nunca em `class="..."` nem em template `${...}`. DOM/visual diff zero. Guards `check_*.py` verdes (não tocam estes seletores).
  - **Não mexer:** `.instrument.is-live`, `.instrument__cta` base, e todas as classes dinâmicas (`col-*`, `hide-*`, `cell-value--*`, etc.) que o Agente 2 confirmou serem construídas por template/`classList`.

- [ ] **0.2 — `scripts/_common.py` para helpers Python repetidos (~25 LOC)** 🟢
  `ROOT = os.path.abspath(...)` idêntico em 10 scripts; `SKIP_DIRS` + `html_files()` quase idênticos em `check_html_attrs.py` e `check_matrix_chrome.py`. Centralizar num módulo importado.
  - **Como verificar:** correr todos os `build_*`/`check_*` e `git diff` vazio nos artefactos gerados (og.png, sitemap.xml, search-index.json, feed.xml, decisions/*); exit codes inalterados; `python3 scripts/test_diff_feed.py` verde.
  - **Nota:** ganho pequeno, mas risco quase nulo (import puro, não toca output do site).

### Tier 1, alto valor, risco médio, precedente já existe no repo

- [ ] **1.1 — Chrome das páginas "compute" -> `/assets/compute-page.css` (~4 300 LOC)** 🟡
  `ec2`, `azure-vm`, `gcp-compute`, `oci-compute`, `ovh-instances` (+ `regions`, ver abaixo) inline-am ~900 linhas de `<style>` cada, das quais ~880 são byte-idênticas (md5 igual entre oci/ovh; azure difere 1 linha). Precedente direto: `assets/compute-table.css` já foi extraído da mesma família e o seu cabeçalho lista exatamente estas páginas.
  - **Não bloqueado por guards:** estas páginas linkam `compute-table.css`, não `matrix.css`, por isso `check_matrix_chrome.py` ignora-as; `verify-data` extrai os arrays JS (`REGIONS`/`FAMILIES`), não o `<style>`.
  - **Per-page-divergent a manter inline:** tokens `--yes/--no/--part` (valores diferem por página), e a linha `.chip[data-cat=...]` específica por vendor.
  - **`regions/` separado:** 997 LOC de style, partilha ~894 mas não carrega `compute-table.js`; validar isoladamente antes de incluir.
  - **Como verificar:** `<link>` no `<head>` (nunca `defer`/`media` que mude ordem de aplicação, evita FOUC). DOM + pixel diff zero do masthead/filtros/drawer/colophon em desktop e mobile, por página. Todos os `check_*.py` verdes.

- [ ] **1.2 — Cola de orquestração das matrizes -> `IA.matrix.mount()` em `assets/matrix.js` (~900-1200 LOC)** 🟡
  `apim-matrix`, `iam-matrix`, `networking-matrix`, `compliance`, `ai-atlas`, `kubernetes`, `confidential-computing`, `observability`, `egress` reimplementam ~190-260 linhas quase idênticas de `writeHash/applyHash/init/renderMatrix/applyFilter/openFeatureDrawer/wireEvents/bootstrap` por cima do `matrix.js`. Içar para um controlador genérico parametrizado; cada página fica com `const VENDORS=[...]; const CATEGORIES=[...]; const FEATURES=[...]; IA.matrix.mount({...});`.
  - **Não bloqueado por guards:** `check_matrix_chrome.py` valida `.masthead` no `<style>` e a estrutura do drawer no HTML, não a localização do JS. Esta cola é `<script>`, fora do alcance do guard. (É independente, e aditiva, em relação à 1.1/2.1: CSS vs JS.)
  - **Parametrizar com cuidado** (fonte do risco médio): rótulos das chips/drawer, campos no haystack de pesquisa, e o **modo de toggle de vendor** (multi-select vs "all + N clouds"). Uma diferença subtil no haystack muda que features aparecem para um dado `q`.
  - **Como verificar:** SEO/no-JS inalterado (já era tudo JS-render). DOM diff por página (snapshot Playwright do `#matrix` + drawer) cobrindo: filtro por categoria, ambos os modos de toggle, pesquisa `q`, deep-link `#vendors=/cat=/q=`, drawer por célula e por cabeçalho, `aria-pressed` das chips. `check_matrix_chrome.py` + `check_html_attrs.py` + `check_instrument_count.py` verdes.

- [ ] **1.3 — `/assets/base.css` para as páginas "soltas" (~700 LOC)** 🟡
  Páginas fora de compute/matrix que ainda inline-am o bloco base (`:root` tokens + reset + grain/scanlines/selection, ~73 LOC byte-idênticos): `about`, `api`, `support`, `privacy`, `changelog`, `atlas`, `index`, `mulesoft`, `apigee`, `aws-api-gateway`, `self-hosted-apim`. Core de 23 tokens byte-idêntico (md5 igual) em 21 páginas; restantes são subconjuntos puros.
  - **Atenção `line-height`:** `tools/shared.css` usa `1.55` e `decisions/decision.css` usa `1.5`. NÃO unificar tools/decisions neste passo (mudaria o line-height de uma). Consolidar só as páginas soltas (que usam `1.5`). Verificar valor por cluster antes.
  - **Como verificar:** `<link>` no `<head>`; DOM diff; medir `line-height` computado e fundo/grão/scanlines/selection antes/depois.

### Tier 2, bloqueada por guard de CI (só viável com trabalho extra)

- [ ] **2.1 — Chrome das páginas "matrix" -> `matrix.css` (~2 000 LOC) — BLOQUEADA** 🔴
  As 11 páginas matrix inline-am ~205 linhas de chrome (masthead, status-line, filters, chips, legend, colophon) além do `matrix.css`. Extrair pareceria o segundo maior ganho.
  - **Porque está bloqueada:** `scripts/check_matrix_chrome.py` (corre em todo o PR via `verify-data.yml`) **falha** se uma página que linka `matrix.css` e usa `class="masthead"` não definir `.masthead` num `<style>` inline. O guard existe para apanhar o bug "página inteira sem estilo" que o Data Layer já shipou (#23). Mover `.masthead` para `matrix.css` faz `defines_masthead = False` -> CI vermelho.
  - **Para desbloquear seria preciso:** reescrever o guard para verificar a presença do chrome *via stylesheet linkada* em vez de inline. Isso (a) enfraquece um guard que apanhou um bug real, (b) é trabalho não trivial, (c) reintroduz exatamente o risco FOUC/whole-page-unstyled que o guard previne. Esforço alto, risco alto.
  - **Recomendação:** NÃO fazer agora. Manter inline (o guard ganha). Se algum dia se fizer, é uma tarefa própria com reescrita do guard + diff visual reforçado.

### ⛔ REJEITADAS (mudam comportamento/output/SEO ou partem o pipeline)

| Proposta | LOC bruto | Porque REJECT |
|---|---:|---|
| Remover/substituir `assets/three.min.js` | ~654 KB | Globe 3D visível na landing (desktop). Remover muda a UX/visual. Agente 3, 🔴. |
| DRY do `<head>` (OG/Twitter/JSON-LD) | ~0 útil | Sem build step/SSI, meta+JSON-LD têm de estar no documento antes do paint; não há include em runtime. |
| Markup do footer `.colophon` | n/a | Conteúdo (About/Data source/Shortcuts) é específico por instrumento. O CSS já está coberto por Tier 1. |
| Toolbox (15 páginas) -> JSON + render | ~1 500 | Prosa única por ferramenta, HTML estático indexável (SEO de cauda longa). Converter muda crawlability/no-JS. |
| Dados inline das matrizes -> `.json` externo | ~2 500 | Células hand-tuned (`value`/`note`/`src` únicos); muda payload inicial e render no-JS; conteúdo potencialmente indexável. |
| Dados inline dos compute -> só `data.json` | ~2 000 | **O inline é a fonte de verdade:** `refresh.sh` extrai `REGIONS`/`FAMILIES` do `index.html` para gerar `data.json`, e `verify-data.yml` falha se divergir. Remover parte o pipeline + o fallback offline/"Snapshot · embedded". |
| Cards da landing -> render de `window.IA.nav` | ~250 | Cards above-the-fold indexáveis; `check_landing_stats`/`check_instrument_count`/`sync_landing_stats` assumem markup estático. |
| Consolidar `esc()`/`escapeHtml()` nos 3 JS | ~8 | Ganho mínimo; exigiria util partilhado com dependência de ordem de carregamento. Não compensa. |
| Cortar pesos de Google Fonts | 0 | Sem over-fetch: todos os pesos 300-700 + itálico estão em uso. |
| Lista de instrumentos `nav.js` ↔ `build_search_index.py` | ~25 | Ganho marginal e cria acoplamento novo JS↔Python; `build_search_index` precisa de ler o HTML de cada página de qualquer forma. Baixa prioridade, não recomendado. |

---

## Gate de verificação (obrigatório antes de aplicar qualquer corte)

Não há "build" no sentido JS/CSS (site estático servido tal-e-qual). "Build verde" = artefactos gerados idênticos + guards verdes + teste verde + diff de DOM zero.

1. **Guards de CI (corre todos a partir da raiz):**
   ```
   python3 scripts/check_html_attrs.py
   python3 scripts/check_instrument_count.py
   python3 scripts/check_landing_stats.py
   python3 scripts/check_matrix_chrome.py
   python3 scripts/check_og_card.py
   python3 scripts/check_region_drift.py
   python3 scripts/check_sovereignty_freshness.py
   ```
2. **Artefactos derivados idênticos** (gerar e confirmar `git diff` vazio):
   ```
   python3 scripts/build_search_index.py
   python3 scripts/build_sitemap.py
   python3 scripts/build_feed_rss.py
   python3 scripts/build_decisions.py
   # og.png só se build_og.py tiver Chrome disponível
   ```
3. **Teste existente:** `python3 scripts/test_diff_feed.py` (único teste do repo).
4. **Sincronização de dados** (verify-data.yml): para `regions`, `gcp-compute`, `egress`, correr `./<inst>/refresh.sh` e confirmar que `data.json` (ignorando `generated`) não muda.
5. **Diff de DOM/visual = zero** nas páginas afetadas (Playwright snapshot do conteúdo + interações, desktop e mobile). É o gate decisivo para 1.1/1.2/1.3.

Sem todos estes verdes, a proposta fica "não verificável" e não avança.

## Ordem de execução sugerida

1. Tier 0 (0.1 dead CSS, 0.2 `_common.py`): isolado, reversível, baixo risco. Fazer e fundir primeiro.
2. 1.2 (cola das matrizes): maior ganho não bloqueado depois dos quick wins; verificável por DOM diff.
3. 1.1 (compute chrome) começando por uma página piloto (ex.: `oci-compute`), validar, depois propagar; `regions` por último e validado à parte.
4. 1.3 (base.css das soltas): verificar `line-height` por cluster.
5. 2.1 só se houver decisão de reescrever o guard (tarefa própria).

## Notas de risco transversais

- Toda a extração de CSS troca 1 `<style>` inline por 1 `<link>`: colocar sempre no `<head>`, nunca com `defer`/`media` que altere a ordem de aplicação (FOUC).
- 1.1 e 2.1 atacam famílias diferentes com valores reais diferentes (`.colophon margin-top: 80px` compute vs `64px` matrix): a granularidade tem de ser por família, nunca um `chrome.css` global.
- Nenhuma proposta de Tier 0/1 remove features, instrumentos, dados, nem altera output/API. As que o fariam estão todas em REJECT.
