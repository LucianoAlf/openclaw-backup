# Crítica da auditoria por KPI — TabGestao.tsx / dados_mensais

Data: 2026-05-31
Arquivo recebido: `Auditoria-READ-ONLYporKPI-TabGestaotsx---1f8b9c91-730e-4a04-8d62-ecd28300ba3c.md`

## Veredito

A segunda auditoria do Windsurf corrigiu bem o erro conceitual: separar KPIs de EVENTO vs ESTOQUE.

Mas o próximo passo sugerido — “adicionar colunas em dados_mensais” — ainda está prematuro e parcialmente incorreto.

## Achado do Alfredo no schema real

`dados_mensais` já tem algumas colunas que o Windsurf listou como se não existissem:

- `alunos_ativos`
- `matriculas_ativas`
- `matriculas_banda`
- `matriculas_2_curso`
- `ticket_medio_passaporte`
- `faturamento_passaporte`

A função real `recalcular_dados_mensais(p_ano, p_mes, p_unidade_id)` também já popula:

- `alunos_ativos`
- `alunos_pagantes`
- `matriculas_ativas`
- `matriculas_banda`
- `matriculas_2_curso`
- `novas_matriculas`
- `evasoes`
- `churn_rate`
- `ticket_medio`
- `tempo_permanencia`

Então não é correto sair criando `alunos_ativos` novamente. O problema é outro:

1. `TabGestao.tsx` ainda ignora algumas colunas existentes no histórico.
2. Alguns meses têm colunas nulas, especialmente janeiro/2026.
3. Maio/2026 só tem Campo Grande em `dados_mensais` no momento consultado.
4. A função `recalcular_dados_mensais` ainda não popula renovações, não renovações, avisos prévios, mrr_perdido, reajuste_medio e bolsistas/Kids/School.
5. Os critérios atuais da função talvez não batam com as regras canônicas recém-validadas (ex.: segundo curso, bolsista parcial, banda/projeto, data_saida vs status atual).

## Dados observados

Para 2026-05, `dados_mensais` tinha apenas Campo Grande:

- alunos_ativos: 511
- alunos_pagantes: 481
- matriculas_ativas: 579
- matriculas_banda: 46
- matriculas_2_curso: 68
- novas_matriculas: 29
- evasoes: 13
- taxa_renovacao: 0
- reajuste_parcelas: 0

Isso diverge do número live validado para Campo Grande/Maio em alguns KPIs:

- alunos ativos live validado: 499
- pagantes live validado: 475
- matrículas ativas live: 565
- segundo curso correto: 28

Conclusão: `dados_mensais` é necessário como snapshot histórico, mas ainda precisa reconciliação de regra e preenchimento, não apenas adição de coluna.

## O que está correto na auditoria Windsurf

- Separar EVENTO vs ESTOQUE.
- Não usar `vw_kpis_gestao_mensal` para estoque histórico.
- Não eliminar `dados_mensais` agora.
- Nunca usar `renovacoes` para KPI.
- Reconhecer que eventos novos de retenção sumiram do histórico/snapshot.

## O que precisa corrigir

Antes de criar migration de colunas:

1. Auditar schema real de `dados_mensais`.
2. Auditar `recalcular_dados_mensais`.
3. Auditar `TabGestao.tsx` para usar colunas existentes (`alunos_ativos`, `matriculas_ativas`, etc.) antes de propor novas.
4. Definir quais colunas realmente faltam.
5. Definir regras canônicas de cálculo para o snapshot de fechamento.
6. Validar backfill mês/unidade antes de atualizar histórico em massa.

## Próximo passo seguro

Pedir ao Windsurf uma auditoria READ-ONLY específica de `dados_mensais` + `recalcular_dados_mensais`, com foco em:

- colunas existentes;
- colunas realmente ausentes;
- colunas existentes mas não usadas pelo `TabGestao.tsx`;
- colunas populadas de forma divergente da regra canônica;
- meses/unidades incompletos;
- proposta de migration mínima futura, sem aplicar.
