# Crítica da auditoria Windsurf — dados_mensais + recalcular_dados_mensais

Data: 2026-05-31
Arquivo recebido: `Auditoria_READ_ONLY_dados_mensais_recalcular_dados_mensais_T---c1c36a88-3abe-4afa-a099-d2033f3fb161.md`

## Veredito

A auditoria está muito boa e confirma o problema central: `dados_mensais` é necessário como snapshot histórico, mas está incompleto, parcialmente ignorado pelo `TabGestao.tsx`, e a função `recalcular_dados_mensais` não reflete todas as regras canônicas.

Mas há uma correção crítica:

## Correção do Alfredo — churn da função NÃO está correto

Windsurf marcou `churn_rate` como “fórmula correta”, mas a função usa:

```sql
v_evasoes / v_pagantes_anterior
```

Regra validada no caso Campo Grande/Maio 2026:

```text
churn = evasões realizadas / pagantes do mês corrente
13 / 475 = 2,74% (~2,7%)
```

A função `recalcular_dados_mensais` retornou/gravou para CG Maio:

```text
13 / 459 ou base anterior ≈ 2,83%
```

Isso diverge da view live validada (`vw_kpis_gestao_mensal.churn_rate = 2,74`).

Portanto, antes de corrigir a função, precisa confirmar a regra do denominador:

- Se o KPI de churn da LA for “perdas do mês / pagantes atuais”, a função está errada.
- Se for “perdas do mês / base inicial/mês anterior”, a view live está errada.

Até agora, a regra validada com Alf para Maio/2026 foi base pagante atual: 13/475.

## Pontos confirmados da auditoria Windsurf

### Colunas zombie

Existem, são usadas pelo frontend, mas não são populadas pela função:

- `taxa_renovacao`
- `inadimplencia`
- `reajuste_parcelas`
- `faturamento_estimado` (a função calcula no JSON, mas não grava)
- `saldo_liquido` (a função calcula no JSON, mas não grava)

### Colunas hidden/orphan

Existem e algumas são populadas, mas `TabGestao.tsx` não usa corretamente no histórico:

- `alunos_ativos`
- `matriculas_ativas`
- `matriculas_banda`
- `matriculas_2_curso`
- `ticket_medio_passaporte`
- `faturamento_passaporte`

### Divergência em novas matrículas

A função `recalcular_dados_mensais` conta novas matrículas sem aplicar os filtros validados:

- não exclui segundo curso
- não exclui banda/projeto
- não exclui canto coral
- não exclui bolsistas

Isso explica divergência em CG Maio:

- view/live validado: 23 novas matrículas
- dados_mensais/função: 29 novas matrículas

### Divergência em estoque

Para CG Maio:

- view/live validado: 499 ativos / 475 pagantes / 565 matrículas ativas / 28 segundo curso correto operacional
- `dados_mensais`: 511 ativos / 481 pagantes / 579 matrículas ativas / 68 segundo curso

Isso mostra que a função de snapshot ainda não está alinhada às regras operacionais canônicas.

## Próximo passo correto

Não criar migration ainda.

Antes, pedir ao Windsurf uma proposta de patch READ-ONLY/DESIGN para `recalcular_dados_mensais`, sem aplicar, incluindo:

1. Denominador do churn como decisão explícita.
2. Correção de novas matrículas com os mesmos filtros da view.
3. Cálculo/gravação de taxa_renovacao via `movimentacoes_admin`.
4. Cálculo/gravação de reajuste_medio/reajuste_parcelas via `movimentacoes_admin` com aumentos positivos.
5. Cálculo/gravação de `faturamento_estimado` e `saldo_liquido`, se a tabela deve armazenar essas colunas.
6. Uso no `TabGestao.tsx` das colunas já existentes (`alunos_ativos`, `matriculas_banda`, etc.) depois que a função estiver certa.
7. Estratégia de backfill por unidade/mês com validação antes/depois.

## Decisão operacional

Próxima etapa ainda é design/auditoria, não aplicação.
