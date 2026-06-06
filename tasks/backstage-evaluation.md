# Avaliação: adicionar "componentes Backstage" ao infra-atlas

Output: recomendação, não código. Aplicado critical review (sem justificar uma feature só por ter sido pedida).

Stack detetado: site estático (HTML servido tal-e-qual pela Cloudflare Workers), ~23 instrumentos em 3 departamentos (Cloud Compute, API Management, Cross-Cloud) + Decisions / Calculators / Toolbox. Instrumentos data-driven têm `data.json` + `refresh.sh` (cron diário, credential-free, fontes públicas); as matrizes curadas são mantidas à mão com guards de frescura (`verify-freshness.yml`, ex.: AI Atlas tem janela de 45 dias por mexer depressa). Voz: seca, literária, terse. Anti-patterns hard: sem contas, sem ads, sem tiers pagos, sem chatbots AI, sem SaaS drift.

---

## Passo 0 (bloqueante): desambiguar

"Componentes Backstage" é termo ambíguo, e em Backstage "Component" é literalmente uma entidade do software catalog, o que torna a leitura B plausível à letra. Duas interpretações:

- **A. Conteúdo NOVO sobre Backstage / platform engineering / IDPs** (matriz de Internal Developer Portals, comparação cross-tool). Encaixa no modelo de reference hub.
- **B. Construir/integrar o infra-atlas EM CIMA do Backstage** (catalog, plugins, backend stateful).

**Decisão: avalio A. B está REJEITADA à partida e não a desenho sem confirmação explícita.** Justificação: o Backstage é uma app Node com backend, base de dados/catalog e auth. Adotá-lo como base do infra-atlas traz contas, estado persistente e superfície SaaS, violando frontalmente três anti-patterns hard (sem contas, sem SaaS drift, e o site é estático sem backend). Não há versão "reduzida" de B que não colida. Se a intenção real era B, **pára aqui e confirma** — não é uma otimização, é trocar a natureza do projeto.

---

## A. Avaliação (conteúdo)

### 1. Problema concreto

Lacuna real? O hub cobre a camada de **infraestrutura cloud** (o que os clouds oferecem: compute, regiões, APIM, networking, IAM, observability, etc.) e um Toolbox de ferramentas de linha de comando. **Não cobre a camada de platform/devex que corre POR CIMA** (IDPs, developer portals, service catalogs, scorecards, golden paths).

Pergunta de utilizador que ficaria respondida: *"que Internal Developer Portal escolher: Backstage vs Port vs Cortex vs OpsLevel vs Spotify Portal vs Roadie?"*. É uma pergunta real e o espaço é confuso. **Mas** é uma pergunta de outra camada, não a promessa central do hub ("referência multi-cloud de infraestrutura"). A lacuna existe; a questão é se é *a lacuna deste* hub.

### 2. Opções

| Opção | O que é | Esforço | Encaixe editorial | Risco manutenção/drift |
|---|---|---|---|---|
| **(a) Matriz de IDPs dedicada** | Instrumento novo, grelha vendor×capacidade (Backstage, Port, Cortex, OpsLevel, Spotify Portal, Roadie, ...) | Médio (curar a matriz; reusa `matrix.js`) | Bom SE factual; mau se virar tier-list | **Alto** (espaço volátil, marketing-y, sem fonte canónica) |
| **(b) Secção no Toolbox** | Adicionar IDPs como categoria/nota curta no Toolbox existente | Baixo | Bom (Toolbox já é curadoria de ferramentas) | Médio |
| **(c) Deep-dive "Backstage Atlas"** | Artigo editorial single-tool (estilo Apigee/Mulesoft) | Médio | **Mau**: single-vendor quebra a neutralidade multi-vendor | Médio |
| **(d) Não fazer** | — | Zero | n/a | Zero |

### 3. Fit com o modelo de dados

**Mau.** Ao contrário de EC2 (dataset público da Vantage) ou preços Azure (API pública), **não há fonte canónica máquina-legível para features de IDPs**. A "fonte" seria a documentação de cada vendor, ou seja claims do próprio vendor, exatamente o risco de "opinião disfarçada de referência". Não encaixa no sync diário: seria **curadoria manual** com carimbo de frescura, como as matrizes curadas (compliance, iam-matrix, sovereignty) e com janela curta tipo AI Atlas (45 dias), porque o espaço muda depressa (re-verificação frequente contra docs que também mudam). Carga de manutenção real e recorrente.

### 4. Risco editorial

**Alto, o mais alto do hub.** Platform engineering é o canto mais saturado de marketing e hype-cycle da infra. Manter a voz seca (presença factual de capacidade + fonte, nunca "o melhor") é difícil. O formato matriz (célula = facto + fonte, como a APIM Matrix) é o antídoto, mas a tentação de tier-list/listicle é forte e o conteúdo dos vendors empurra para lá.

### 5. Trade-offs

- **Esforço vs valor:** valor real (pergunta genuína) mas servida só com manutenção alta e risco editorial alto.
- **Mudança de camada / diluição de identidade:** IDPs são uma categoria de *software que se corre*, não algo que os *clouds oferecem*. Adicionar estica o hub de "referência de infra cloud" para "reviews de devtools".
- **Scope creep:** Backstage/IDPs é porta de entrada para "adicionar tudo o que é platform eng" (catálogos, scorecards, golden paths, mais CI/CD, mais observability SaaS). Difícil traçar a fronteira depois do primeiro passo.

---

## Recomendação

**Não fazer agora (lean no).** Com uma exceção condicional estreita.

Porquê não: é uma mudança de camada (devex/platform, não infra cloud) que dilui a identidade do hub; não tem fonte canónica sincronizável, logo é curadoria manual pura no canto mais hype-prone da infra; e abre scope creep difícil de fechar. O ganho (responder "que IDP?") é real mas não é a promessa central, e o custo (manutenção + risco editorial + erosão de foco) é desproporcionado.

**Exceção condicional:** se houver uma decisão *estratégica e deliberada* de expandir o hub para a camada de platform/devex (não uma feature avulsa), então a única forma aceitável é a **Opção (a) numa versão reduzida**: uma **Matriz de IDPs** neutra, factual, curada, com guard de frescura e com **âmbito travado por escrito** a "Internal Developer Portals / self-service developer portals". Nunca a (c) (deep-dive de Backstage quebra a neutralidade), nunca "componentes Backstage" no sentido literal.

### Se mesmo assim avançar: porquê (a) e não as outras
- **(c) rejeitada:** singularizar o Backstage trai a neutralidade multi-vendor que é a marca do hub. Se entra, entra como comparação, não como ode a uma ferramenta.
- **(b) insuficiente:** uma linha no Toolbox não responde à pergunta de comparação (a pergunta é "qual escolher entre N", precisa de grelha, não de lista).
- **(a) é a única que serve a pergunta no formato em que o hub é bom**, mas só com os travões abaixo.

### Esquema de dados proposto (se Opção a)
Reusa o padrão das matrizes curadas (`matrix.js` + dados inline + `<time datetime>` para o guard de frescura):
- `VENDORS`: `{ key, name, short, swatch, kind }` onde `kind ∈ {oss, managed-oss, commercial-saas}` (ex.: Backstage=oss, Spotify Portal/Roadie=managed-oss, Port/Cortex/OpsLevel=commercial-saas).
- `CATEGORIES`: eixos factuais, não opinativos. Ex.: Software Catalog, Scaffolder/Golden Paths, Plugins/Extensibilidade, Scorecards, TechDocs, Auth/RBAC, Self-host vs SaaS, Licença, Modelo de preço (presença, não valores).
- `FEATURES[].support[vendorKey] = { level: yes|part|no|info, value, note, src }`. `src` = **link para a doc oficial da capacidade** (obrigatório por célula não-trivial; sem fonte, não entra).
- **Cadência:** manual. Carimbo `<time datetime>` na masthead + entrada em `verify-freshness.yml` com janela ~90 dias.
- **Sem `refresh.sh`, sem `data.json`** (não há fonte sincronizável; seria honestidade fingida).

### Como reverter/remover (se não pegar)
A arquitetura torna a remoção trivial e isolada (como qualquer instrumento): apagar a pasta `idp-matrix/`, a entrada em `nav.js` (e `window.IA.nav`), regenerar `sitemap.xml` e `search-index.json` (`scripts/build_*.py`), e remover a linha do `verify-freshness.yml`. Zero acoplamento a outros instrumentos. Sem estado, sem migração, sem dados a limpar.

### Top 3 riscos + mitigação
1. **Vira tier-list opinativa / marketing-y.** Mitigação: célula = facto + fonte oficial obrigatória; proibir adjetivos de juízo ("melhor", "líder"); a coluna `kind` (oss/saas) dá o enquadramento sem opinar.
2. **Apodrece depressa (espaço volátil) e a fonte é o próprio vendor.** Mitigação: guard de frescura curto (~90 dias); marcar explicitamente que as células refletem docs do vendor numa data; preferir capacidades estruturais estáveis (tem catalog? tem scaffolder?) a detalhes que mudam todas as semanas.
3. **Scope creep para "todo o platform eng".** Mitigação: âmbito travado por escrito no topo do instrumento (só IDPs/portals); um `check_*.py` que falhe se forem adicionadas categorias fora do âmbito é exagero, mas a regra editorial deve ficar registada em `tasks/lessons.md`.

---

## Conclusão (uma linha)
B: rejeitar (viola anti-patterns hard). A: lean **não fazer**; só fazer como **Matriz de IDPs neutra e travada** se houver decisão estratégica de entrar na camada de platform/devex, nunca como "componentes Backstage" nem deep-dive single-vendor.
