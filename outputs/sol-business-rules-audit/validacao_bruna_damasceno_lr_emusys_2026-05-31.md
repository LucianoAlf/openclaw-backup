# Validação — Bruna Damasceno / divergência LA Report x Emusys

Data: 2026-05-31
Contexto: auditoria CG/Maio 2026 — regra de KPIs por pessoa/pagantes.

## Evidência enviada pelo Alf

Prints analisados:
- `/root/.openclaw/media/inbound/file_1156---4b902637-51c7-4a99-be8e-e24199d58792.jpg`
- `/root/.openclaw/media/inbound/file_1157---c3600277-e223-40b0-ac92-7f6d9d4893b9.jpg`

Evidência visual:
- No Emusys/cadastro aparece **Bruna Damasceno De Castro**, número de aluno **1925**.
- No LA Report aparecem dois registros semelhantes/duplicados:
  1. **Bruna Damasceno Castro** — ativo, Guitarra, sexta 15:00, valor **R$367**.
  2. **Bruna Damasceno De Castro** — ativo, Guitarra, sexta 15:00, valor **R$0**.

## Conferência no Supabase/LA Report

Consulta read-only confirmou duas linhas ativas em Campo Grande:

| ID | Nome | Status | Data matrícula | Curso | Tipo | Valor | Conta como pagante |
|----|------|--------|----------------|-------|------|-------|--------------------|
| 1459 | Bruna Damasceno De Castro | ativo | 2026-02-27 | Guitarra | Regular | 0 | true |
| 1464 | Bruna Damasceno Castro | ativo | 2026-02-27 | Guitarra | Regular | 367 | true |

As duas linhas têm mesmo curso, mesma data de matrícula, mesmo status e nomes quase iguais. Forte indício de duplicidade/erro de cadastro/sincronização.

## Conferência no CSV Emusys ativo

No CSV ativo `relatorio_exportado_39`, não houve match exato para **Bruna Damasceno De Castro**.

Isso não significa necessariamente que não exista cadastro no Emusys; o print mostra cadastro. Significa que ela não apareceu no export ativo usado na reconciliação operacional.

## Impacto nos KPIs

Bruna é uma provável “pegadinha” da divergência:

- O agrupamento por `nome` exato trata **Bruna Damasceno Castro** e **Bruna Damasceno De Castro** como duas pessoas diferentes.
- A linha com R$367 já entra como pagante real no LA Report.
- A linha com R$0 entra como `conta_como_pagante=true`, mas não tem valor financeiro e não aparece no CSV ativo.
- Portanto, a linha R$0 pode inflar a contagem por flag (`conta_como_pagante=true`) e contaminar o 475.

## Conclusão operacional

Sim: esta é uma evidência forte de falha da equipe/processo.

Bruna deve ir para relatório de cobrança/saneamento porque há divergência entre:
- LA Report com duplicidade ativa;
- CSV ativo Emusys sem correspondência clara para a linha R$0;
- possível cadastro Emusys existente, mas não conciliado como ativo/pagante.

## Ação recomendada para equipe

Pedir validação nominal:

1. Bruna Damasceno Castro e Bruna Damasceno De Castro são a mesma pessoa?
2. Qual é o cadastro correto no Emusys? Número 1925?
3. Ela está ativa no Emusys ou só cadastrada?
4. Existe contrato ativo de Guitarra sexta 15:00?
5. A mensalidade correta é R$367 ou R$0?
6. Qual linha deve permanecer no LA Report?
7. A linha duplicada deve ser inativada, mesclada ou corrigida?

## Status

Não executar update ainda. Precisa validação da equipe/Alf antes de saneamento.

---

## Atualização do Alf — correção manual iniciada

Alf informou em 2026-05-31 23:12 UTC:

- A Bruna zerada está sendo apagada/corrigida no Windsurf/Emusys.
- O problema era diferença de nome: `Bruna Damasceno Castro` vs `Bruna Damasceno de Castro`.
- A orientação enviada foi apagar a entrada zerada e corrigir o nome da pagante.

## Implicação para auditoria

Após correção, validar:

1. existe apenas uma Bruna ativa no LA Report;
2. nome correto: Bruna Damasceno de Castro;
3. valor correto: R$367;
4. linha R$0 não aparece mais como ativa/pagante;
5. CSV Emusys passa a bater com LA Report.

Não assumir números finais antes dessa revalidação.
