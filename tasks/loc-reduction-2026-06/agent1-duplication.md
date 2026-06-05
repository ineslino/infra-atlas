# Agent 1 — Duplicação de código entre instrumentos (auditoria LOC)

**Âmbito:** repositório `infra-atlas` (64 ficheiros HTML, 38 413 LOC; 16 scripts Python, 2 097 LOC; assets partilhados em `/assets/*` e raiz).
**Regra de base:** site estático servido tal-e-qual pela Cloudflare (`wrangler.jsonc` → `assets.directory = "."`), **sem build step** para o HTML dos instrumentos. Qualquer extração tem de usar um mecanismo que já existe em runtime: `<link rel="stylesheet" href="/assets/x.css">` ou `<script src="/x.js">`, exatamente como `nav.js`, `assets/compute-table.css`, `assets/matrix.css`, `tools/shared.css` e `decisions/decision.css` já fazem.

## Resumo

A maior fonte de duplicação é **CSS inline repetido entre páginas da mesma família**. Os instrumentos partilham um bloco de *page chrome* (tokens `:root`, reset, `.grain`/`.scanlines`, `.masthead`, `.status-line`, `.filters`, `.chip`, `.colophon`) que está copiado verbatim dezenas de vezes. O precedente para o corrigir **já existe no próprio repo**: as 20 páginas de `/tools` + `/toolbox` carregam `tools/shared.css` e as 11 páginas de `/decisions` carregam `decisions/decision.css`, ambos contendo exatamente esse bloco de chrome. Os ~30 instrumentos restantes continuam a inline-ar o mesmo bloco. As páginas "compute" (ec2, azure-vm, gcp-compute, oci-compute, ovh-instances, regions) são o caso extremo: têm **~900 linhas de `<style>` inline cada, das quais ~880 são idênticas entre si** (md5 igual entre oci e ovh; azure difere numa só linha). As 11 páginas "matrix" já carregam `matrix.css` mas ainda assim inline-am ~205 linhas de chrome cada.

A duplicação de **JS inline** é menor do que o esperado (não há helpers partilhados tipo `debounce`/clipboard repetidos; cada página tem lógica própria). Há sim um `esc()`/`escapeHtml()` quase idêntico nos três ficheiros JS partilhados (`compute-table.js`, `feed.js`, `matrix.js`), mas é minúsculo.

A duplicação **Python** é real mas modesta: o one-liner `ROOT = …` (10 scripts) e o par `SKIP_DIRS` + `html_files()` (2 scripts) → um `scripts/_common.py`.

O **boilerplate de `<head>`** (OG/Twitter/JSON-LD) é estruturalmente quase idêntico mas com valores por página, e sem build step **não é redutível em runtime → REJECT** (com nota sobre as poucas linhas verdadeiramente constantes).

---

## Tabela de padrões

| padrão repetido | nº ocorrências | LOC poupado estimado | risco de extração |
|---|---|---|---|
| **A. Bloco de *chrome* das páginas "compute"** (`:root` + reset + grain/scanlines + masthead + status-line + filters + chip + colophon + restante CSS de layout) → novo `/assets/compute-page.css` | 6 páginas (ec2, azure-vm, gcp-compute, oci-compute, ovh-instances, regions); ~880 linhas comuns por página | **~4 300** (≈860 × 5 + parcial em regions) | **médio** |
| **B. Bloco de *chrome* das páginas "matrix"** (masthead, status-line, filters, chips, legend, colophon, base) → estender `/assets/matrix.css` ou novo `/assets/matrix-chrome.css` | 11 páginas (apim-matrix, iam-matrix, networking-matrix, compliance, kubernetes, observability, observability-stacks, sovereignty, egress, ai-atlas, data-layer); ~205 linhas comuns por página | **~2 000** (≈200 × ~10) | **médio** |
| **C. Bloco base de tokens+reset+grain+scanlines+selection** (`:root` … `::selection`, ~73–78 LOC) nas páginas que **não** são compute nem matrix (about, api, support, privacy, changelog, atlas, index, confidential-computing, mulesoft, apigee, aws-api-gateway, self-hosted-apim) → novo `/assets/base.css` global | 30 páginas inline-am `.grain {`; bloco base byte-idêntico por cluster | **~700** (apenas as ~12 páginas fora de A/B; o resto já está contado em A/B) | **médio** |
| **D. `esc()` / `escapeHtml()`** quase idêntico em `assets/compute-table.js:20`, `assets/feed.js:25`, `assets/matrix.js:18` | 3 ficheiros JS | **~8** | **médio** |
| **E. Python: `ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))`** + `SKIP_DIRS`/`html_files()` → `scripts/_common.py` | `ROOT`: 10 scripts; `html_files()`+`SKIP_DIRS`: 2 scripts quase idênticos | **~25** | **baixo** |
| **F. Boilerplate `<head>` OG/Twitter/JSON-LD** (estrutura idêntica, valores por página) | ~61 páginas | **0 (REJECT)** | n/a |
| **G. Footer `.colophon` (markup)** — estrutura repetida mas conteúdo por instrumento | 61 páginas | **0 (REJECT no markup; o CSS já está em A/B/C)** | n/a |

> Nota anti-dupla-contagem: A, B e C sobrepõem-se (o bloco base de C está dentro de A e de B). O total agregado em baixo conta **cada linha de cada página uma só vez**.

---

## Detalhe por padrão

### A. Chrome das páginas "compute" → `/assets/compute-page.css` (maior ganho)

**Evidência de identidade** (LOC totais de `<style>` inline e md5 do bloco):
- `oci-compute/index.html` e `ovh-instances/index.html`: `<style>` inline = **902 LOC, md5 idêntico** (`0ea7bbc8…`).
- `azure-vm/index.html`: 902 LOC, difere de ovh em **1 linha** (`.chip[data-cat="confidential"]` vs `.chip[data-cat="baremetal"]`).
- `gcp-compute/index.html` (931 LOC) partilha **877** linhas (sorted-comm) com ovh; `ec2/index.html` (939 LOC) partilha **894**.
- O bloco base `:root … ::selection` é byte-idêntico entre azure/gcp/oci/ovh (74 LOC, md5 `153fe562…`); ec2 difere só por faltar `--teal` (subconjunto puro).

**Precedente já no repo:** `assets/compute-table.css:1-9` comenta literalmente *"Linked by ec2 / azure-vm / gcp-compute / oci-compute / ovh-instances … Uses the shared design tokens already defined on every observatory page."* Ou seja, a tabela já foi extraída; falta extrair o **chrome de página** que continua inline nas 5+regions.

**Atenção (per-page-divergent a NÃO mexer):**
- Tokens `--yes`/`--no`/`--part` divergem por página (ex.: `egress` usa `--yes:#F4EFE6`, `apim-matrix` usa `--yes:#6FE7B5`) — manter por página.
- A linha `.chip[data-cat=…]` (confidential/baremetal/…) é específica por vendor — manter inline ou parametrizar com seletor que cubra ambas.
- `regions/` é "compute-shaped" mas tem 997 LOC de style (mais do que os outros) e **não** carrega `compute-table.js`; partilha ~894 linhas mas precisa de validação extra.

**Como verificar que nada partiu:** para cada página, extrair o `<style>` antes/depois e fazer `diff` do **rendered DOM** (mesmo HTML + nav.js) num browser headless; confirmar pixel-diff zero do masthead, filtros, drawer de comparação e colophon em viewport desktop + mobile; confirmar que `scripts/check_matrix_chrome.py` e os restantes `check_*.py` continuam verdes. **Risco médio:** mover `<style>` inline para `<link>` externo adiciona um request e muda o *timing* de carregamento (possível FOUC se o CSS não estiver no `<head>` antes do primeiro paint) — colocar o `<link>` no `<head>` como os já existentes, **não** `defer`.

### B. Chrome das páginas "matrix" → estender `matrix.css`

As 11 páginas carregam `assets/matrix.css` (tabela + foco) mas **todas inline-am também** masthead/colophon/status-line/filters/chips/legend: confirmado por `.masthead {` presente nas 11 páginas que carregam `matrix.css`. Linhas comuns (sorted-comm): apim∩iam = **205**, iam∩networking = **220**. As classes comuns são `.colophon`(6), `.filter-search`(5), `.chip`(4), `.status-counts`(3), `.masthead__eyebrow`(3), `.masthead`/`.legend`/`.status-line`/`.scroll-hint`, etc.

**Atenção:** o chrome difere **entre famílias** (compute vs matrix) em valores reais, não só whitespace: `.colophon margin-top: 80px` (compute) vs `64px` (matrix); `.masthead margin-bottom: 40px` vs `32px`. Logo **não** se deve criar um único `chrome.css` global — a granularidade correta é **por família** (compute-page.css e matrix-chrome.css), coerente com a forma como `compute-table.css`/`matrix.css` já estão separados. Dentro de cada família o bloco é byte-idêntico (md5 igual após normalização).

**Como verificar:** mesmo método de A (diff do DOM renderizado por página); validar que `--matrix-accent` por página continua a aplicar o tint de hover correto; correr `scripts/check_matrix_chrome.py` (que valida que cada página matrix "ships its chrome").

### C. `/assets/base.css` global para as páginas "soltas"

Páginas fora de compute/matrix que ainda inline-am o bloco base (`:root`+reset+grain+scanlines+selection, ~73 LOC byte-idênticos por cluster): about, api, support, privacy, changelog, atlas, `index.html`, confidential-computing, mulesoft, apigee, aws-api-gateway, self-hosted-apim. Conjunto core de 23 tokens é **byte-idêntico (md5 `1b9fa12b…`) em 21 páginas**; as restantes são subconjuntos puros (só faltam tokens, sem valores divergentes) ou diferem apenas em whitespace dentro de `rgba(...)` (ex.: `about` usa `rgba(244,239,230,…)` sem espaços).

**Atenção:** `tools/shared.css` usa `line-height: 1.55` e `decisions/decision.css` usa `line-height: 1.5` no `html, body`. Um `base.css` único teria de escolher um valor; aplicá-lo às páginas tools/decisions **mudaria** o line-height de uma delas → **não** unificar tools/decisions neste passo, só consolidar as páginas soltas (que usam `1.5`). Verificar valor por cluster antes de extrair.

**Como verificar:** diff DOM renderizado; confirmar fundo/grão/scanlines/selection idênticos; medir line-height computado antes/depois.

### D. `esc()` / `escapeHtml()` triplicado

- `assets/compute-table.js:20-24` e `assets/feed.js:25-29`: corpo praticamente idêntico (feed.js faz `String(s)`, compute-table.js faz `String(s == null ? "" : s)`).
- `assets/matrix.js:18` expõe `IA.matrix.escapeHtml` com o mesmo mapa de substituição.

Poupança ~8 LOC. **Risco médio, baixo valor:** consolidar exigiria um util partilhado carregado antes dos três (ordem de scripts) e introduz um novo global; o ganho não compensa o risco de ordem de carregamento. **Recomendação: deixar como está** (ou consolidar só se já houver um util partilhado carregado por todas as páginas).

### E. `scripts/_common.py`

- `ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))` repetido **exatamente em 10 scripts** (build_og.py:33, build_search_index.py:30, build_sitemap.py:15, check_html_attrs.py:21, check_instrument_count.py:25, check_landing_stats.py:21, check_matrix_chrome.py:26, check_og_card.py:23, check_region_drift.py:33, check_sovereignty_freshness.py:23). Variante `HERE/ROOT` em backfill_feed.py:24-25 e build_feed_rss.py:17-18.
- `SKIP_DIRS = {".git", "node_modules", "__pycache__", ".github"}` + função `html_files()` com `os.walk` quase idênticas em `check_html_attrs.py:23-31` e `check_matrix_chrome.py:27-35` (única diferença: filtro `*.html` vs `index.html`).

Propor `scripts/_common.py` com `ROOT`, `SKIP_DIRS`, `html_files(only_index=False)`. Poupança ~25 LOC. **Risco baixo:** import puro, não toca em output do site.

**Como verificar:** correr todos os `scripts/*.py` (geradores `build_*` e guards `check_*`) e confirmar output byte-idêntico (`git diff` vazio nos artefactos gerados: og.png, sitemap, search index, feed.xml, decisions/*) e exit codes inalterados; `python scripts/test_diff_feed.py` verde.

### F. Boilerplate `<head>` — REJECT

Estrutura OG/Twitter/JSON-LD quase idêntica em ~61 páginas, mas com valores por página (title, description, canonical, og:url, JSON-LD `@type`/`name`/`keywords`/`distribution`). Linhas verdadeiramente constantes e o seu nº de páginas:
- `<meta name="color-scheme" content="dark">`: 62 · viewport: 62 · favicon `?v=2`: 62
- `preconnect` googleapis/gstatic: 63/63 · link de fonts css2 (idêntico): 61
- `og:image` `og.png?v=3`: 61 · `og:site_name`: 61 · `twitter:card summary_large_image`: 61 · `og:type website`: 61 · `<canonical>`: 61
- JSON-LD presente em 21 páginas.

**Sem build step / SSI, `<meta>` e JSON-LD têm de estar no documento antes do primeiro paint e não há include em runtime → não redutível. REJECT.** A única migração possível (mover o `<link>` de fonts para `@import` dentro de um CSS partilhado) **altera o timing de carregamento das fonts e arrisca FOUT/FOUC → também REJECT.** Introduzir um SSG/templating para DRY-ar o head está fora de âmbito (não-objetivo).

### G. Footer `.colophon` (markup) — REJECT no markup

`<footer class="colophon">` em 61 páginas, mas o conteúdo (About, Data source, Shortcuts) é específico por instrumento (texto, fonte de dados, atalhos). O **CSS** do `.colophon` é byte-idêntico (md5 `ac072f4d…` em ec2/gcp/azure/oci) e **já está coberto** por A/B/C. O markup em si não é DRY-able sem build step → REJECT.

---

## Total estimado LOC poupado

- A (compute chrome → compute-page.css): **~4 300**
- B (matrix chrome → matrix.css/matrix-chrome.css): **~2 000**
- C (base.css nas páginas soltas, sem dupla-contagem com A/B): **~700**
- E (scripts/_common.py): **~25**
- D (esc consolidado): **~8** (não recomendado)

**Total estimado (sem dupla-contagem): ~7 000 LOC** removidas do HTML/JS/Python, mantendo output, UX e API públicas idênticos. Realisticamente, A+B+E são os de melhor relação ganho/risco (**~6 300 LOC**, todos com precedente já existente no repo).

## Recomendação de prioridade

1. **A** — `compute-page.css` (maior ganho, precedente direto em `compute-table.css`).
2. **B** — chrome das páginas matrix para dentro de `matrix.css` (já carregado pelas 11 páginas; risco de timing menor porque o `<link>` já existe).
3. **E** — `scripts/_common.py` (risco baixo, trivial).
4. **C** — `base.css` para as páginas soltas (verificar `line-height` por cluster antes).
5. **D/F/G** — não fazer (D baixo valor, F/G impossíveis sem build step).

### Aviso transversal de preservação de comportamento
Toda a extração CSS muda 1 request inline → 1 request externo: colocar sempre o `<link rel="stylesheet">` no `<head>` (como `compute-table.css`/`matrix.css` já estão), **nunca** com `defer`/`media` que mude a ordem de aplicação, para evitar FOUC. Validar cada família com diff visual desktop+mobile e com os guards `scripts/check_*.py` verdes antes de fundir.
