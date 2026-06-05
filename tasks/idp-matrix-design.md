# Design + dados: Matriz de IDPs (Internal Developer Portals)

Instrumento novo, decidido após `tasks/backstage-evaluation.md` (exceção condicional: só uma matriz neutra e travada). Output deste doc: âmbito validado + dados pesquisados com fonte + decisões editoriais + plano de build. Voz: seca, factual, sem "melhor".

## Âmbito (validado)

7 ferramentas (coluna), por natureza, não por preferência:
- `backstage` (oss, framework self-hosted, CNCF)
- `spotify-portal` (managed-backstage)
- `roadie` (managed-backstage)
- `port` (commercial-saas)
- `cortex` (commercial-saas)
- `opslevel` (commercial-saas)
- `compass` (commercial-saas, Atlassian)

10 eixos (linha), em 3 categorias:
- **Catálogo & docs**: catalog, scaffolder, techdocs
- **Standards & extensibilidade**: scorecards, plugins, integrations, auth_rbac
- **Modelo** (descritivo, neutro): deployment, license, pricing

**Travão de âmbito (no topo do instrumento):** só Internal Developer Portals. Fora: Platform Orchestrators (Humanitec), backend frameworks (Encore), CI/CD, IaC, observability SaaS.

## Decisão editorial chave: linhas descritivas são neutras

`deployment`, `license`, `pricing` **não são capacidades "boas/más"**. Renderizadas todas com `level: "info"` (símbolo ≈, cor neutra), facto em `value`. Colorir "proprietary" a vermelho ou "open-source" a verde seria editorializar, exatamente o que a avaliação proibiu. Só os eixos de capacidade real (catalog, scaffolder, techdocs, scorecards, plugins, integrations, auth_rbac) usam yes/part/no.

## Dados (pesquisados nas docs oficiais, jun 2026)

Legenda level: ✓ yes · ◐ part · ✗ no · ≈ info(neutro). Cada célula tem `src` (doc oficial) no `data` real; aqui resumo.

### catalog (todos ✓)
backstage ✓ Software Catalog (core) · spotify-portal ✓ pré-instalado · roadie ✓ catálogo Backstage · port ✓ blueprint-based · cortex ✓ catálogos (Services/Infra/Domains/Teams) · opslevel ✓ catálogo automático (Catalog Engine) · compass ✓ catálogo de componentes nativo

### scaffolder
backstage ✓ Software Templates · spotify-portal ✓ Scaffolder pré-instalado · roadie ✓ templates · port ✓ self-service actions · cortex ✓ Scaffolder (Cookiecutter) · opslevel ✓ Actions + Service Creation · **compass ✗ Templates removidos em 2025-12-01**

### techdocs
backstage ✓ TechDocs (built-in) · spotify-portal ✓ pré-instalado · roadie ✓ incluído · **port ◐ Markdown do Git (sem árvore MkDocs)** · **cortex ◐ docs do repo embebidos** · opslevel ✓ docs-as-code · **compass ◐ só links (ex. Confluence), sem render**

### scorecards
**backstage ◐ via plugin Tech Insights (não core)** · spotify-portal ✓ Soundcheck (plugin premium) · roadie ✓ Tech Insights · port ✓ built-in · cortex ✓ flagship · opslevel ✓ Rubric/Scorecards/Checks · compass ✓ nativo

### plugins
backstage ✓ modelo de plugins first-class · spotify-portal ✓ instalador no-code + bundle premium · roadie ✓ OSS + custom · **port ≈ Ocean integrations, não plugins Backstage** · cortex ✓ plugins iframe custom · **opslevel ◐ API/custom, sem framework de plugins** · compass ✓ Forge apps

### integrations (todos ✓)
backstage ✓ SCM/cloud/CI/identity · spotify-portal ✓ SCM/CI/auth (via wizards) · roadie ✓ 50+ (cloud/SCM/CI/obs/incident) · port ✓ broad (Ocean) · cortex ✓ nativas + webhook · opslevel ✓ 70+ nativas · compass ✓ ecossistema Atlassian + SCM/incident/obs

### auth_rbac
**backstage ◐ muitos providers; RBAC policy-as-code (em código)** · spotify-portal ✓ SSO + plugin RBAC · roadie ✓ RBAC + IdP SSO · port ✓ RBAC + SSO · cortex ✓ RBAC + SSO/SCIM · opslevel ✓ SSO/SAML/SCIM/RBAC · compass ✓ roles + permission policies

### deployment (≈ neutro)
backstage "Self-hosted (framework)" · spotify-portal "SaaS gerido (Spotify)" · roadie "SaaS gerido (+ Roadie Local)" · port "SaaS (sem self-host completo)" · cortex "SaaS + self-managed (Helm)" · opslevel "SaaS + self-hosted (Helm)" · compass "Cloud only"

### license (≈ neutro)
backstage "Apache-2.0" · spotify-portal "Proprietário sobre OSS" · roadie "Proprietário sobre OSS" · port "Proprietário; Ocean Apache-2.0" · cortex "Proprietário" · opslevel "Proprietário" · compass "Proprietário"

### pricing (≈ neutro)
backstage "Grátis (OSS, sem licença)" · spotify-portal "Custom (contacto)" · roadie "Por developer; custom" · port "Free tier + per-seat" · cortex "Custom (contacto)" · opslevel "Por developer; custom" · compass "Free tier + per-user"

## Plano de build
1. `idp-matrix/index.html` clonando a estrutura de uma página matrix (chrome inline `<style>` + masthead + filtros + `#matrix` + drawer + colophon), com `IA.matrix.filters` + `IA.matrix.renderTable` (mecanismo já existente). Dados inline `VENDORS/CATEGORIES/FEATURES`. `<time datetime>` na masthead.
2. `nav.js`: entrada na secção XCLOUD (cross-cloud) + `window.IA.nav`.
3. Regenerar `sitemap.xml` + `search-index.json` (`scripts/build_*.py`).
4. `verify-freshness.yml`: adicionar `idp-matrix:180` (curado, janela 180d).
5. **Verificação**: `check_matrix_chrome.py` (exige `.masthead` inline + drawer `.drawer__head/__body`), `check_html_attrs.py`, `check_instrument_count.py`; harness jsdom (render + chips + drawer); browser real (computed styles, sem erros).

## Reversão
Apagar `idp-matrix/`, a entrada em `nav.js`, regenerar sitemap+search-index, remover a linha de `verify-freshness.yml`. Isolado, sem estado.
