# Backlog — Compositions & pipeline Terraform (plataforma Backstage)

Contexto: recursos criados pelo Backstage geram um repo no Azure DevOps com um
`main.tf` que consome a Composition como módulo Terraform via `source = "git::...?ref=..."`.
Hoje a Composition vive em `main`, sem tags. Quando se altera a Composition,
recursos já deployed **não** recebem as mudanças só por correr a pipeline outra
vez — o Terraform usa o módulo em cache porque a string do `source` (`?ref=main`)
não muda.

---

## 1. Versionamento da Composition com tags

**Problema:** o módulo aponta para `?ref=main`. Como a string nunca muda, o
Terraform não re-descarrega o módulo e o `plan` dá "No changes" mesmo havendo
alterações na Composition.

**Proposta:**
- Adotar tags semânticas na Composition (`v1.2.0`, …) em vez de apontar para `main`.
- Recurso passa a referenciar `?ref=v1.2.0`; bump explícito do ref quando se quer
  a nova versão.
- Como a string do `source` muda, o Terraform re-puxa o módulo no `init` normal —
  **sem precisar de `-upgrade`** e sem mexer na pipeline.

**Benefício:** mudanças controladas e reproduzíveis; resolve a causa-raiz em vez
do sintoma. Este é o estado-alvo — quando existir, o tema do `-upgrade` (abaixo)
deixa de ser necessário.

**Esforço:** M (tagging na Composition + atualizar template do scaffolder para
gerar `?ref=<versão>` em vez de `main`).

---

## 2. Opção no run da pipeline para `terraform init -upgrade`

**Problema:** enquanto tudo vive em `main` (sem versionamento), a única forma de
forçar o re-download do módulo é `terraform init -upgrade` (ou limpar `.terraform/`).
Pôr o `-upgrade` sempre, em todos os runs, é indesejável (mais lento, re-resolve
providers desnecessariamente).

**Proposta:** parâmetro de runtime na pipeline — à semelhança do que já existe
para escolher `plan` vs `apply` — um toggle tipo `forceModuleUpgrade` (default
`false`) que, quando ligado, corre `terraform init -upgrade` em vez do `init`
normal. Usa-se pontualmente quando se sabe que a Composition em `main` mudou.

**Benefício:** desbloqueia o cenário atual sem editar a pipeline a cada vez e sem
penalizar todos os runs.

**Esforço:** S (parâmetro + condição no step de `init`).

**Nota:** medida-ponte. Quando o item #1 (versionamento) estiver implementado,
reavaliar se ainda é preciso.
