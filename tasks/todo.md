# Quick wins — UX/organização (audit 2026-05-21)

Derivados de `docs/backlog.md` + audit Parte 1.
Verificação: coluna "Como confirmar" diz o que deve aparecer no browser ou test.

---

## Estado actual (após commit `6d4ead6`)

### ✅ Já feito

| # | Item | Ficheiro(s) | Como confirmar |
|---|------|-------------|----------------|
| 1 | `scope="row"` em todos os row headers das matrizes | networking-matrix, iam-matrix, apim-matrix, kubernetes `/index.html` | Inspecionar DOM → `<th scope="row" class="feature-col">` nas linhas do tbody |
| 2 | `aria-label` no `<table>` | networking-matrix, apim-matrix, kubernetes (iam já tinha) | DevTools → `<table aria-label="...">` |
| 3 | `scope="col"` nos `<th>` de cabeçalho do apim-matrix | `apim-matrix/index.html` | Inspecionar thead → todos os `<th>` têm `scope="col"` |
| 4 | Filter deep-link em toolbox pages | `toolbox/filter.js` | Activar chips TUI + Go → URL muda para `?tags=TUI,Go`; reload → chips restaurados |
| 5 | search-index: instance types indexados | `scripts/build_search_index.py` + `search-index.json` | ⌘K → pesquisar "m5.xlarge" → aparece "EC2 Observatory — matched: m5.xlarge" |
| 6 | search-index: tool names do toolbox indexados | idem | ⌘K → pesquisar "k9s" → aparece Kubernetes Toolbox |
| 7 | feed.json | — | Feed funciona; 0 entries significa que não houve mudanças nos dados ontem↔hoje. Auto-popula no próximo refresh com alterações reais. |

---

## 🔲 Por confirmar — candidatos a quick wins adicionais

Não estavam na lista explícita do audit mas têm esforço S (< 1 dia).
**Aguardo OK antes de tocar.**

| # | Item | Ficheiro(s) | O que muda | Como confirmar |
|---|------|-------------|------------|----------------|
| A | Cross-link Decisions ↔ Instruments | `nav.js` (RELATED map) | Adicionar Decisions ao RELATED de instrumentos relevantes (EC2→Fargate vs EC2, Networking Matrix→NAT gateway vs…) e instrumentos ao RELATED de cada Decision | Related pills no EC2 Observatory mostram "Fargate vs EC2"; Related pills no Fargate vs EC2 decision mostram "EC2 Observatory" |
| B | Contagem de resultados visíveis pós-filtro nos compute instruments | `ec2/index.html` (+ azure-vm, gcp-compute, etc.) | Mostrar "X de Y tipos" quando há filtros activos | Activar filtro "arm64" no EC2 → header ou label diz "147 de 623 instâncias" |
| C | Corrigir fallback `--paper-3` em `nav.js` (0.42 → 0.55) | `nav.js` | A nav injected CSS usa `rgba(244,239,230,0.42)` como fallback. Se uma página futura não definir `--paper-3`, os labels do palette rendem a 3.64:1 (abaixo AA). Alinhar fallback com o valor definido em todos os pages (0.55 = 5.56:1) | `nav.js` hardcoded fallbacks todos a 0.42 → mudados para 0.55 |
| D | Indicador de scroll horizontal em matrizes mobile | `tools/shared.css` ou por instrumento | Gradiente lateral "shadow" que aparece quando a tabela tem mais colunas do que a viewport | Em 375px, networking-matrix mostra gradiente no lado direito da tabela |

---

## ❌ Não aplicar (violam "static, no build" ou foram descartados)

| Item | Razão |
|---|---|
| Busca global de conteúdo livre (full-text) | Exigiria index server ou build step; o search-index.json enriched já cobre os casos práticos |
| Split da taxonomy Cross-Cloud | Só faz sentido quando o grupo ultrapassar 10 items; agora tem 8 |
| Shared CSS para instrumentos individuais (`/ec2/index.html` etc.) | Cada instrumento tem CSS inline — extrair exigiria um include mechanism que viola "no build" |

---

## Notas

- Itens A–D aguardam OK explícito.
- Cada item tem um commit isolado.
- Nada disto toca na organização de grupos do nav (só RELATED, que é curado manualmente).
