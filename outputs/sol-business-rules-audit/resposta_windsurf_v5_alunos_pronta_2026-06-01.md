# Resposta ao Windsurf — V5_ALUNOS pronta por Alfredo

Use como base o arquivo:

`outputs/sol-business-rules-audit/MIGRACAO_REGLA_KPI_V5_ALUNOS_ALFREDO_DRAFT.sql`

## Direção

A V4 separou corretamente alunos de financeiro, mas ainda errou ao recriar `vw_kpis_gestao_mensal` com menos colunas e ordem diferente. Isso pode quebrar o contrato público da view.

A V5 correta deve:

1. manter o contrato público atual de `vw_kpis_gestao_mensal`;
2. alterar somente as expressões de:
   - `total_alunos_ativos`;
   - `total_alunos_pagantes`;
   - `total_banda`;
   - `total_segundo_curso`;
   - `novas_matriculas`;
   - `total_evasoes`;
   - `churn_rate`;
   - `matriculas_ativas` se for adicionada, apenas no final da view;
3. preservar ticket/MRR/faturamento/inadimplência/renovação/reajuste para migration financeira separada;
4. não usar `DROP VIEW`;
5. não escrever em colunas geradas;
6. não persistir ticket provisório.

## Status

Arquivo pronto como **draft técnico para revisão**. Ainda não executar em produção sem aprovação do Alf.
