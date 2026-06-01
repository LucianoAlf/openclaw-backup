```md
Precisamos corrigir com cuidado o KPI “Reajuste Médio” do LA Report em produção. Não fazer alteração ampla sem antes confirmar a fonte e testar por unidade.

## Contexto operacional
O LA Report está em produção. A regra desejada pelo Alf é: métricas do mês atual não podem depender de snapshot/fechamento (`dados_mensais`). A cada movimento operacional — matrículas, renovações, reajustes, evasões etc. — o Analytics deve refletir em tempo real quando houver fonte operacional viva.

`dados_mensais` pode continuar existindo como snapshot/histórico/fechamento, mas não deve ser a fonte viva do mês corrente.

## Problema observado
Tela: Analytics > Gestão > Campo Grande > Maio/2026.

O card “Reajuste Médio” mostra `0.0%`, mas a listagem/detalhamento de renovações mostra várias renovações com aumento de mensalidade, como +12%, +11% etc.

Tooltip do card:
> “Percentual médio de aumento aplicado nas renovações do mês. Indica o poder de precificação.”

## Evidência técnica levantada

### 1. `vw_kpis_gestao_mensal`
Para Campo Grande / Maio 2026:
- `total_alunos_ativos`: 499
- `total_alunos_pagantes`: 475
- `novas_matriculas`: 23
- `reajuste_medio`: 0.0
- `taxa_renovacao`: 100.0 — também suspeita, mas NÃO corrigir agora sem auditoria própria.

### 2. `dados_mensais`
Para Campo Grande / Maio 2026:
- `alunos_pagantes`: 481 — defasado
- `novas_matriculas`: 29 — defasado
- `reajuste_parcelas`: 0.0
- `taxa_renovacao`: 0.0

Conclusão: `dados_mensais` não pode ser a fonte viva do mês atual.

### 3. Tabela `renovacoes`
Para Campo Grande / Maio 2026:
- 61 linhas com `status = renovado`.
- Porém `valor_parcela_novo` está majoritariamente `null`.
- `percentual_reajuste` está `null` ou `0.0`.
- Média por `percentual_reajuste` = 0.

Essa tabela NÃO está refletindo corretamente os reajustes operacionais visíveis na tela.

### 4. Tabela `movimentacoes_admin`
Para Campo Grande / Maio 2026:
- 38 linhas com `tipo = renovacao`.
- Esse total bate com o relatório operacional de renovações.
- 25 linhas têm `valor_parcela_anterior` e `valor_parcela_novo` preenchidos.
- Média calculada com todos os registros que têm valor anterior/novo: ~12,44%.
- Média considerando apenas aumentos positivos: ~12,95%.
- Se diluir aumentos positivos por todas as 38 renovações, dá ~8,18%.

Exemplos reais:
- 375 → 417 = +11,20%
- 414 → 467 = +12,80%
- 327 → 367 = +12,23%
- 334 → 407 = +21,86%

Além disso, o modal/listagem de retenção no frontend já usa `movimentacoes_admin` e calcula o reajuste por linha a partir de `valor_parcela_anterior` e `valor_parcela_novo`.

## Hipótese principal
A view `vw_kpis_gestao_mensal` está calculando `reajuste_medio` a partir da tabela `renovacoes.percentual_reajuste`, mas a fonte operacional correta para o que aparece na tela é `movimentacoes_admin`.

No repo existe uma migration com CTE parecida com:

```sql
renovacoes_mes AS (
  SELECT 
    renovacoes.unidade_id,
    EXTRACT(YEAR FROM renovacoes.data_renovacao)::INTEGER AS ano,
    EXTRACT(MONTH FROM renovacoes.data_renovacao)::INTEGER AS mes,
    COUNT(*) FILTER (WHERE renovacoes.status = 'renovado') AS renovacoes,
    COUNT(*) AS total_contratos,
    AVG(renovacoes.percentual_reajuste) FILTER (WHERE renovacoes.status = 'renovado') AS reajuste_medio
  FROM renovacoes
  GROUP BY renovacoes.unidade_id, EXTRACT(YEAR FROM renovacoes.data_renovacao), EXTRACT(MONTH FROM renovacoes.data_renovacao)
)
```

Mas cuidado: antes de substituir a view, consultar a definição real em produção (`pg_get_viewdef`/Supabase SQL editor), porque migrations antigas podem não representar 100% a view atual.

## Correção solicitada — segura

1. Inspecionar no banco a definição atual de `vw_kpis_gestao_mensal`.
2. Identificar exatamente como `reajuste_medio` está sendo calculado hoje.
3. Corrigir somente o cálculo de `reajuste_medio`, sem alterar os outros KPIs da view.
4. Usar `movimentacoes_admin` como fonte viva de renovações/reajuste, pelo menos para `reajuste_medio`, com:
   - `tipo = 'renovacao'`
   - agrupamento por `unidade_id`, ano e mês de `data`
   - cálculo a partir de `valor_parcela_anterior` e `valor_parcela_novo`
   - ignorar registros sem valor anterior/novo ou com valor anterior <= 0

Sugestão de expressão para o KPI, a validar:

```sql
ROUND(
  AVG(
    ((valor_parcela_novo - valor_parcela_anterior) / NULLIF(valor_parcela_anterior, 0)) * 100
  ) FILTER (
    WHERE tipo = 'renovacao'
      AND valor_parcela_anterior IS NOT NULL
      AND valor_parcela_novo IS NOT NULL
      AND valor_parcela_anterior > 0
      AND valor_parcela_novo > valor_parcela_anterior
  ),
  2
) AS reajuste_medio
```

Observação de regra:
- Como o tooltip fala “percentual médio de aumento aplicado”, minha recomendação é calcular a média apenas dos aumentos positivos aplicados.
- Se o objetivo for “média de reajuste considerando todas as renovações, inclusive sem aumento”, aí registros sem aumento devem entrar como 0. Mas isso precisa ser validado com Alf antes.

5. Validar especificamente Campo Grande / Maio 2026 antes e depois:
   - Antes: `reajuste_medio = 0.0`
   - Esperado aproximado se usar apenas aumentos positivos: ~12,95%
   - Esperado aproximado se usar todos com valor anterior/novo: ~12,44%
   - Esperado se diluir por todas as 38 renovações: ~8,18%

6. Não mexer agora em `taxa_renovacao`, `evasoes`, `segundo_curso` ou outros KPIs. Eles têm auditorias separadas.

7. Depois da correção, retornar:
   - definição exata alterada
   - diff SQL
   - query de validação antes/depois
   - resultado por unidade para Maio/2026: Campo Grande, Recreio e Barra
   - confirmação de que os outros campos da view continuaram iguais

## Regra de segurança
Se a view atual em produção for diferente da migration do repo, NÃO recriar a view usando arquivo antigo inteiro. Fazer patch mínimo baseado na definição real do banco.
```
