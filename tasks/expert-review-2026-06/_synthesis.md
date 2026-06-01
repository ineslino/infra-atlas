# Infra Atlas — Revisão por Painel de Experts

**Data:** 2026-06-01 · **HEAD:** `1f3d70e` · **Painel:** 12 experts (6 de domínio + 6 de construção web), em paralelo.
**Método:** inspeção real do repositório e do site live (`infraatlas.dev`); cada claim ancorado em `ficheiro:linha`/snippet ou URL; claims de domínio (preços, regiões, regulação, features de vendor) verificados contra a fonte upstream e citados. Relatórios individuais em anexo.

---

## 1. Veredito global

**Aprovado com ressalvas — unânime (12/12).** Nenhum expert pediu "trabalho sério"; nenhum deu aprovação limpa.

**Pronto para divulgação mais agressiva? Ainda não — mas falta pouco, e o que falta é barato.** A fundação é genuinamente forte e *verificada* (ver §2). O que bloqueia a promoção não é qualidade de fundo; é um punhado de incoerências de baixo esforço que vivem precisamente nos primeiros 5 segundos de credibilidade e no único loop de distribuição (a API). Quase todas são fixes de tamanho **S**.

**Itens que gateiam a promoção (todos Quick Wins):**
1. A contagem de instrumentos está errada em 8+ superfícies, com **três** números diferentes (README "nineteen", hero/prose/chip/nav/atlas/dispatches "21", **22** cards reais). É a primeira coisa que um cético verifica num site cuja tese é "accurate, sourced".
2. O hero promete "updated daily from the source" para *todo* o Atlas, mas só 4 de 22 instrumentos são live-diários — e a própria `data-policy.md` **proíbe** explicitamente esta frase.
3. A API (o maior vetor de adoção orgânica) é desencorajada pela própria mensagem ("shape can change without notice") e **não tem licença de dados** — bloqueio jurídico real para uso empresarial.
4. Erros de precisão pontuais mas detetáveis no conteúdo de maior risco (soberania/compliance e a decomposição OCI da data-policy).

Feitos os Quick Wins (§5), o site **está** pronto: a precisão de dados foi confirmada à fonte (à vírgula, em vários casos), a voz editorial funciona para seniores, a segurança e a IA são fortes, e a infra da API é um diferenciador real. Os *Investimentos* (§5) não bloqueiam a promoção — convertem o site de "referência editorial superior" em "a ferramenta que o sénior mantém aberta".

---

## 2. O que está forte (consenso, verificado upstream)

Importa registar, porque o veredito unânime assenta nisto:

- **Precisão de dados de compute/regiões confirmada à fonte.** AWS 39 (= 34+2+2+1), GCP 43, Azure 67 batem com as páginas autoritárias dos vendors; `m7i.large` = `$0.1008/h` bate com o Vantage ao cêntimo; o refresh diário 06:00 UTC está *vivo* (`generated 2026-06-01T11:50Z`). *(expert 1)*
- **Egress preciso ao cêntimo** em todas as ~7 taxas verificadas, e editorialmente superior à Vantage (route-cards com a escada de tiers, condicionais explícitas). *(expert 5)*
- **APIM credível para produção** — quotas numéricas verbatim contra docs (AWS 50ms–29s/10MB/10k RPS, Apigee 30MB, Kong 60s default), REST-vs-HTTP correto linha-a-linha com fonte inline. *(expert 3)*
- **Regulação de fundo correta e bem-sourçada** — CLOUD Act, DPF (CELEX 32023D1795), Schrems II (C-311/18), EUCS contestado, Data Act (12-09-2025), AI Act, AWS ESC GA 15-01-2026 — todos verificados. *(expert 4)*
- **`data-policy.md` é governação de dados a sério** — reconcilia contagens por partição com as manchetes dos vendors, proíbe descrever curados como "daily", tem guards reais (region-drift, self-healing OG/chips). *(experts 1, 6, 12)*
- **Acessibilidade acima da média** — todos os tokens de *texto* passam AA com folga, glifos com `aria-label`, focus-trap e reduced-motion sólidos. *(expert 9)*
- **Base estática + Cloudflare excelente** — Brotli em tudo, cache HIT, TTFB 124–233ms; o "peso" do data-in-HTML é um falso problema sobre o fio (transfers reais 19–42KB). *(expert 8)*
- **SEO técnico limpo** (canonicals 100%, sitemap 59=59, 404 noindex, ld+json nos decisions) e **IA madura** (cmd-K com dupla afordância, 3 eixos de browse, RELATED curado com fonte única `window.IA.nav`). *(experts 10, 7)*
- **Segurança forte** — HSTS preload, CSP real, `x-frame-options: DENY`, CORS na API verificado. *(Step 0 + expert 8)*

---

## 3. Temas transversais (levantados por ≥2 experts)

### T1 — Deriva da contagem de instrumentos (12/12 experts) — **o tema dominante**
O número que o site reporta sobre si próprio está errado e inconsistente. Confirmado: 22 cards `is-live`; `README.md:6` "nineteen"; `index.html:1050/1076/1081/1105` "21"; `nav.js:454` "twenty-one" (em **todas** as páginas de instrumento); `atlas/index.html:9` meta "21" (indexável); `dispatches.json:5` "21". O self-heal JS (`index.html:1923-1941`) só recalcula 2 superfícies (`#stat-instruments` + `.section-head__meta`) e nem isso de forma fiável (ver C1).
**Porque importa:** para a audiência (arquitetos séniores), errar a contagem trivialmente verificável dos *próprios* instrumentos é o sinal que contamina a confiança em tudo o que *não* é verificável de relance (as 67 regiões Azure, as ~200 células APIM). É o oposto exato da promessa "accurate, sourced".

### T2 — "Updated daily" sobre-promete frescura, contra a própria política (experts 5, 6, 11, 12)
O hero (`index.html:1030`) diz "updated daily from the source"; só `ec2/azure-vm/oci-compute/ovh-instances` (4 de 22) são live. `data-policy.md:96-98` escreve textualmente: *"Do not describe regions or gcp-compute as refreshed daily... Site copy must distinguish live-API from curated"*. O long-form (manifesto, colophon) acerta; o headline contradiz-se. Agrava: "What Changed" mostra "0 recent" e o feed mais novo tem 16 dias (`feed.json` 2026-05-16), parecendo abandonado num site que se diz "daily".
**Porque importa:** a frescura é o argumento central contra os snapshots estáticos da concorrência; sobre-prometê-la no primeiro ecrã inverte o argumento e gasta a credibilidade que os verdicts rigorosos constroem.

### T3 — Lacunas de enforcement de frescura (experts 3, 6, e 5)
7 de 22 instrumentos não têm *qualquer* guard de staleness: todo o **Dept II API Management** (usa texto plano sem `<time datetime>`, invisível ao `verify-freshness.yml`) + `observability` + `observability-stacks`. As páginas de vendor APIM não têm fonte por-linha (só um parágrafo "Sources"), ao contrário dos decisions. A `data-policy.md` §4 omite `networking-matrix`/`observability`(-stacks) da lista de curados e os thresholds divergem do guard real.
**Porque importa:** Dept II é um terço da superfície e o diferenciador editorial — e é a parte sem proteção contra apodrecimento, num domínio onde as features de gateway mudam todo o trimestre.

### T4 — Confirma decisões, mas não as *fecha* (experts 1, 2, 5)
`equivalent-sku` é shape-only (sem eixo de preço/performance); não há matriz de equivalência da **camada de dados** (DBs/storage/messaging); não há conteúdo de **commitment/discount** (RIs/Savings Plans/CUDs — a maior alavanca de TCO, 60–80% da fatura, vs egress 5–15%); os 10 decisions são compute-cêntricos e intra-cloud (não há "EKS vs AKS vs GKE" cross-cloud, apesar de os dados já existirem).
**Porque importa:** o workflow do arquiteto pára na borda onde a decisão é mesmo feita (custo + dados + escolha de provider), limitando o site a consulta em vez de ferramenta de decisão — e cedendo o terreno que mais o diferenciaria.

### T5 — A API: diferenciador real, mas mensagem + licença travam a adoção (experts 10, 12, 6)
CORS/free/no-key verificado *true* (ótimo). Mas o CTA "Build on it" colide com "best-effort, not a product / shape can change without notice", sem versionamento e **sem licença de dados** (`data.json` não tem campo `license`; o MIT cobre só o código). Os `data.json` não têm `Dataset` schema → invisíveis ao Google Dataset Search. E o EC2 deriva do dataset da Vantage sem crédito *on-page* (só no campo `source`).
**Porque importa:** a API é o maior loop de aquisição orgânica (devs integram e creditam); "shape can change" + zero licença reduzem-na a um `curl` pontual e levantam a pergunta fatal "porque não usar diretamente a Vantage?".

### T6 — Precisão de domínio: forte, com erros pontuais detetáveis (experts 1, 3, 4)
Apesar de §2, há erros específicos que um leitor sénior apanha — e numa página "asterisks intact" cada um custa desproporcionadamente:
- **OCI**: `data-policy.md:32` "45+8+2=55" não reconcilia com `region-reference.json` (real ≈ 47 comercial + 7 gov + 1 sovereign); e 55 fica acima do "50+" público da Oracle sem reconciliação. *(expert 1)*
- **Soberania (com carimbo "Verified 2026-05-31")**: S3NS marcado "SecNumCloud (target)" quando a PREMI3NS foi qualificada 3.2 em 2025-12-17; Scaleway "Gaia-X confirm membership" quando **saiu** em nov-2021; IONOS por resolver. Células "confirm current" são admissões de não-verificação que contradizem o carimbo. *(expert 4)*
- **CLOUD Act**: cita `18 USC §2703` 6×; a extraterritorialidade foi adicionada no `§2713`. *(expert 4)*
- **Imunidade ao CLOUD Act sobrestimada** para providers UE com presença nos EUA (OVHcloud US assinou o CLOUD Act): é o asterisco que a página critica nos hyperscalers e omite aqui. *(expert 4)*
- **Kong OAuth2**: matrix marca o plugin `oauth2` (OSS+Enterprise) para flows de OIDC, mas a validação de IdP externo é o `openid-connect` = Enterprise-only — contradiz a página irmã `self-hosted-apim`. *(expert 3)*

---

## 4. Conflitos entre experts + recomendação ponderada

**C1 — O site renderizado mostra 21 ou 22?**
Frontend (expert 7) afirma que pós-JS o DOM mostra 22 (self-heal funciona) e que "21" é só o estado pré-JS. Mas Acessibilidade (expert 9) **verificou live, com JS, e viu 21** no hero/header/chip; Positioning (expert 12) e o meu WebFetch também viram 21; Platform (expert 2) atribui a deploy-lag/cache. **Recomendação ponderada:** o próprio desacordo entre dois experts que dizem ter testado o site live *é* o veredito — depender de JS de cliente para o número-âncora produz resultados inconsistentes entre clientes/deploys/crawlers. A correção é idêntica em qualquer das leituras: **tornar a fonte estática correta (22), corrigir todas as superfícies não-auto-curadas, e adicionar um guard de CI**. Trato C1 como reforço do P0, não como dúvida sobre ele. (Leitura conservadora: assumir 21 live, como 9/12/Step-0 observaram.)

**C2 — O peso das páginas é problema? (o meu Step 0 vs expert 8)**
O Step 0 sinalizou data-in-HTML pesado (ec2 138KB, regions 142KB). Performance (expert 8) **corrige-me, e tem razão**: com Brotli + cache HIT os transfers reais são 19–42KB; o data-in-HTML é um falso problema. Os verdadeiros custos são **`three.min.js` (166KB Brotli, decorativo, em toda a 1ª visita)** e a **lacuna de cache no `_headers`** (og.png/nav.js/favicon/brand caem em `max-age=0`). Adoto a leitura do expert 8; o Step 0 estava enganado neste ponto.

**C3 — Severidade da staleness (FinOps expert 5 vs Data Quality expert 6)**
FinOps aceita staleness *se* sinalizada (a página já diz "snapshot, not a live feed"); Data Quality vê a ausência de guards em 7 instrumentos como gap real. **Ambos certos em camadas diferentes:** a honestidade per-página mitiga o risco para o utilizador; o guard em falta é um risco de manutenção. O fix (trazer os 7 para o `verify-freshness.yml` + badge de frescura) satisfaz os dois.

**C4 — Profundidade dos decisions (SEO expert 10) vs brevidade editorial (NON-GOAL + expert 11)**
SEO nota conteúdo fino (~404 palavras) vs concorrentes long-form. Resolvido pelo próprio expert 10: priorizar **intent-match no título ("vs") + structured data** (que respeitam o tom) acima de volume de texto. Sem conflito real — não se mexe no tom.

---

## 5. Top 10 ações priorizadas (impacto × esforço)

### Quick Wins — alto impacto / baixo esforço (fazer já, quase todos `S`)

| # | Ação | Prio | Esf | Quem | Âncora |
|---|------|------|-----|------|--------|
| 1 | **Corrigir a contagem em todas as superfícies + guard de CI.** `index.html:1050/1076/1081/1105`, `README.md:6` ("nineteen"), `nav.js:454` ("twenty-one"), `atlas/index.html:9`, `dispatches.json:5`. Tornar a fonte estática correta (não depender de JS) e estender `check_og_card.py`/`check_landing_stats.py` para falhar quando *qualquer* literal de contagem diverge dos cards `is-live`. | P0 | S | 1,2,4,6,7,8,9,10,11,12 | 8+ superfícies confirmadas |
| 2 | **Alinhar a copy de frescura do hero com a `data-policy`.** Trocar "updated daily from the source" por "cloud-compute refreshed daily; API + cross-cloud as dated snapshots" (reusar a frase já correta do colophon `index.html:1732`). | P0 | S | 5,6,11,12 | `index.html:1030` vs `data-policy.md:96-98` |
| 3 | **Destravar a API.** Publicar licença de dados explícita (ex. CC-BY-4.0) em `/api/` + campo `license` nos `data.json`; suavizar "shape can change without notice" para um compromisso mínimo de estabilidade dos campos de topo; creditar `ec2instances.info`/Vantage *on-page* em `/ec2/`. | P0 | S | 12,10,(6) | `api/index.html:139-140,173`; `ec2/data.json source` |
| 4 | **Corrigir a decomposição OCI** em `data-policy.md:32` (≈47+7+1) e reconciliar o total 55 com o "50+" público da Oracle. | P0 | S | 1 | `data-policy.md:32` vs `region-reference.json` |
| 5 | **Precisão de soberania** (manter o carimbo "Verified" honesto): S3NS → SecNumCloud 3.2 (2025-12-17); Scaleway → saída do Gaia-X (2021); IONOS resolver; citar `18 USC §2713`; nota do *control test* na imunidade dos providers UE com presença US (OVHcloud). | P1 | S | 4 | `sovereignty/index.html:294-298,334-347,462` |
| 6 | **Bundle de 4 fixes estáticos de alta confiança:** (a) lacuna de cache no `_headers` (og.png/nav.js/favicon/brand); (b) `--paper-4` como cor de *texto* → ≥4.5:1 (`.cmp-cell.is-zero`, falha AA 1.68:1); (c) `vs` literal nos `<title>`+meta dos 10 decisions (manter H1 "or"); (d) célula Kong OAuth2 (distinguir `oauth2` OSS de `openid-connect` Enterprise). | P1 | S | 8,9,10,3 | `_headers`; `index.html:57`; `decisions/*`; `apim-matrix:382/394` |
| 7 | **"What Changed" honesto:** janela real (ex. 30 dias) ou renomear "recent"→"entries"; mostrar "last data change 16 May · sources re-verified daily" para não parecer abandonado. | P1 | S | 6,11,12 | `index.html:1670,1758-1759` |

### Investimentos — alto impacto / esforço M–L (sequenciar após a promoção)

| # | Ação | Prio | Esf | Quem |
|---|------|------|-----|------|
| 8 | **Lazy-load / substituir o globe `three.js`** (166KB Brotli em toda a 1ª visita): injetar só se `!reduced-motion` + desktop + idle, ou trocar por SVG/canvas 2D estático. | P1 | M | 8 |
| 9 | **Fechar a frescura + descoberta:** trazer os 7 instrumentos sem guard (Dept II APIM + observability) para o `verify-freshness.yml` (normalizar para `<time datetime>`); + `Dataset`/`SearchAction`/`BreadcrumbList`/`FAQPage` structured data (22 de 32 páginas têm zero). | P1 | M | 6,3,10 |
| 10 | **Fechar a decisão:** eixo de preço no `equivalent-sku` + 1ª matriz de equivalência da camada de dados (DBs/storage); e/ou 1–2 decisions cross-cloud reusando os dados de `kubernetes`/`confidential-computing`. | P1 | L | 2,1 |
| (11) | **Substituir a prova social inexistente:** página `/about` de metodologia (transforma "como uma claim entra" no argumento) + primeiro empurrão de tração (HN/lobste.rs/r/devops com um instrumento cross-cloud forte). Adiar o destaque ao `/support/` enquanto a adoção é ~0. | P1 | M | 12 |

---

## 6. Prontidão para divulgação — recomendação

**Sequência:** fazer os **Quick Wins 1–7** (essencialmente uma tarde de fixes `S`, com 4 deles a tocarem o ponto exato — "accurate, sourced" — em que esta audiência decide se volta) → **então** promover. Os erros não são de competência; são de *acabamento*, e estão concentrados nos primeiros 5 segundos de credibilidade e no loop da API. Corrigidos, o produto é defensavelmente superior à Vantage no cross-cloud, com dados verificados e uma voz que os seniores respeitam.

**Risco de promover antes:** o resultado mais provável não é rejeição — é indiferença. O sénior chega via link, vê "21 vs 22 cards" e "0 recent" num site "daily", conclui "projeto solo, talvez abandonado, números que não batem", e fecha a aba sem partilhar — exatamente o público que o Atlas precisa de converter. E a API, o vetor de distribuição mais potente, fica neutralizada por mensagem + zero licença. Tudo isto por detalhes de esforço `S`.

Os **Investimentos (8–11)** são o caminho de "referência respeitada" → "ferramenta indispensável": peso, frescura/descoberta, e o fecho da decisão (custo + dados). Não bloqueiam a promoção; maximizam o seu retorno.
