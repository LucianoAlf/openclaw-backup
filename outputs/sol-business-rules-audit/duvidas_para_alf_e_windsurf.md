# Dúvidas para validação — Sol / LA Report

## Perguntas para o Alf

1. Quando você fala “bolsista não conta”, é para excluir:
   - só bolsista integral?
   - bolsista parcial também?
   - não pagante?
   - banda/projeto?
   - segundo curso?

2. Para “total de alunos ativos” usado em dashboard principal, conta matrícula ou pessoa?
   - Ex: aluno faz guitarra + canto. Conta 1 ou 2?

3. Para “alunos pagantes”, segundo curso conta como aluno pagante separado ou como aumento de ticket da mesma pessoa?

4. Churn/evasão deve considerar:
   - saída de matrícula individual?
   - ou só saída total da pessoa da LA?
   - essa regra muda entre KPI de gestão e KPI de professor?

5. Conversão de professor acima de 100%:
   - aceitamos como reflexo operacional?
   - ou corrigimos fórmula para nunca passar de 100%?

6. Trancado entra em algum KPI como ativo? Ou sempre sai de carteira/base ativa?

7. Aviso prévio entra como evasão já no mês do aviso ou só no mês da saída prevista?

8. LTV deve ser por unidade ou rede?
   - Se aluno sai de Campo Grande e entra no Recreio, é saída + entrada, transferência, ou continuidade?

## Prompt para mandar no Windsurf / agente do LA Report

Você é o agente que desenvolveu o LA Music Performance Report. Preciso auditar e extrair as regras de negócio reais usadas nos KPIs para criar uma skill canônica da Sol.

Não responda genérico. Liste regras com fonte no código/SQL quando possível.

Foque nestes pontos:

1. Quais arquivos/RPCs/views são fontes canônicas para KPIs de:
   - LTV / tempo de permanência
   - churn / evasão
   - alunos ativos
   - alunos pagantes
   - bolsistas / não pagantes
   - segundo curso
   - banda/projeto
   - conversão comercial
   - conversão de professor
   - ticket médio
   - renovação / não renovação / aviso prévio
   - inadimplência

2. Para cada KPI, diga:
   - fórmula exata
   - tabela/view/RPC usada
   - filtros obrigatórios
   - exclusões obrigatórias
   - divergências conhecidas entre banco, frontend e documentação
   - se a regra está em produção ou só documentada

3. Procure especialmente por divergências envolvendo:
   - bolsistas incluídos indevidamente
   - `status = ativo` ausente
   - `is_segundo_curso`
   - `is_projeto_banda`
   - aluno pessoa vs matrícula
   - views `vw_*`
   - RPCs como `get_historico_ltv`, `get_kpis_professor_periodo`, `get_dados_relatorio_*`

4. Responda em formato auditável:
```md
## KPI: nome
- Status: produção/documentado/divergente/dúvida
- Fórmula:
- Fonte executável:
- Arquivos:
- Filtros:
- Exclusões:
- Observações:
- Dúvidas:
```

## Prompt específico após auditoria frontend — Campo Grande Mai/2026

Auditei o LA Report logado no frontend em Analytics > Gestão > Campo Grande > Mai/2026 e encontrei divergências específicas. Preciso que você, agente do Windsurf/LA Report, valide no código e SQL.

Contexto observado:
- Frontend mostra alunos ativos 499, pagantes 475/479, Kids 214, School 351, Banda 41, matrículas 23, evasões 13, saldo 10.
- `vw_kpis_gestao_mensal` retorna `total_alunos_ativos=499`, `total_alunos_pagantes=475`, `total_banda=41`, `total_segundo_curso=66`, `churn_rate=2.74`.
- Query direta em `alunos` com `status in ('ativo','trancado')` retorna 565 linhas.
- Relatório administrativo da equipe diz matrículas ativas 565, banda 41, 2º curso 28, trancados 2.
- `dados_mensais` para o mesmo mês está defasado: alunos_ativos 511, pagantes 481, matrículas_ativas 579, 2º curso 68.
- `vw_kpis_retencao_mensal` retorna `total_evasoes=21`, `evasoes_interrompidas=8`, `avisos_previos=8`, `nao_renovacoes=5`, `taxa_renovacao=100`, mas frontend exibe total evasões 13 e taxa renovação 88,4%.

Perguntas objetivas:

1. Onde está o SQL atual de `vw_kpis_gestao_mensal` e qual é a fórmula exata de:
   - `total_alunos_ativos`
   - `total_alunos_pagantes`
   - `total_bolsistas_integrais`
   - `total_bolsistas_parciais`
   - `total_banda`
   - `total_segundo_curso`
   - `ticket_medio`
   - `mrr`
   - `churn_rate`

2. Por que o relatório administrativo conta `matrículas de 2º curso = 28`, mas banco/view mostram `66/68`?
   - Existe filtro de pagante?
   - Exclui banda/coral/bolsista?
   - Há registros `is_segundo_curso=true` marcados indevidamente?

3. Por que relatório administrativo conta `trancados=2`, mas query direta mostra `5`?
   - Qual filtro correto?

4. Em `vw_kpis_retencao_mensal`, por que `total_evasoes=21` se `evasoes_interrompidas=8` e `nao_renovacoes=5`?
   - A view está somando aviso prévio?
   - Isso está errado para regra de negócio?

5. A regra canônica de evasões deve ser:
   `total_evasoes = cancelamentos + não renovações`, excluindo aviso prévio?

6. A regra canônica de renovação deve ser:
   `renovacoes / (renovacoes + nao_renovacoes)`?
   Ou deve incluir pendentes/avisos?

7. Para mês atual, a Sol deve usar `vw_kpis_gestao_mensal` e ignorar `dados_mensais` até fechamento/recalcular?

8. A contagem Kids/School no frontend está usando matrículas, mas o rótulo diz “% do total” usando total de alunos/pessoas 499. Isso é bug de UI/regra ou intencional?

Responda com fonte por arquivo/linha/SQL quando possível e marque cada item como:
- regra correta
- bug conhecido
- decisão pendente
- dado sujo no banco
