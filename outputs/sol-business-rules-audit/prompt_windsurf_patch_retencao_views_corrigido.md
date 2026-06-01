Windsurf, comparei sua auditoria com a auditoria independente do Alfredo. O diagnóstico central está aprovado, mas NÃO aplique literalmente o SQL sugerido na Etapa 1, porque `COUNT(*) AS total_contratos` em `movimentacoes_admin` sem filtro conta evasão, aviso prévio, trancamento etc. e pode quebrar o denominador da taxa de renovação.

Objetivo: aplicar patch seguro, sem alteração de dados, corrigindo as views de KPI de retenção para Maio/2026 e meses correntes.

REGRAS VALIDADAS:
- Fonte canônica operacional/live para retenção: `movimentacoes_admin`.
- Renovações: `tipo = 'renovacao'`.
- Não renovações: `tipo = 'nao_renovacao'`.
- Taxa de renovação: `renovacoes / (renovacoes + nao_renovacoes)`.
- Reajuste médio: média apenas das renovações com aumento positivo:
  - `tipo = 'renovacao'`
  - `valor_parcela_anterior > 0`
  - `valor_parcela_novo > valor_parcela_anterior`
  - ignorar reajuste 0 e valores ausentes.
- Evasões realizadas/churn: `tipo IN ('evasao','nao_renovacao')`.
- `aviso_previo` deve ficar separado; não entra em total de evasões realizadas.
- Não usar `renovacoes` para KPI live de quantidade de renovações, taxa ou reajuste médio.
- Não alterar dados existentes.
- Não apagar ou aposentar `renovacoes` ainda.
- Não criar trigger de sync ainda.

PATCH 1 — `vw_kpis_gestao_mensal`:
- Localizar CTE `renovacoes_mes`.
- Trocar a fonte de `renovacoes` para `movimentacoes_admin`.
- Garantir que `total_contratos` conte somente `renovacao + nao_renovacao`, NÃO todas as movimentações administrativas.

A lógica correta da CTE deve ser equivalente a:

```sql
renovacoes_mes AS (
  SELECT
    unidade_id,
    EXTRACT(year FROM data)::integer AS ano,
    EXTRACT(month FROM data)::integer AS mes,
    COUNT(*) FILTER (WHERE tipo = 'renovacao') AS renovacoes,
    COUNT(*) FILTER (WHERE tipo = 'nao_renovacao') AS nao_renovacoes,
    COUNT(*) FILTER (WHERE tipo IN ('renovacao', 'nao_renovacao')) AS total_contratos,
    ROUND(AVG(
      ((valor_parcela_novo - valor_parcela_anterior) / NULLIF(valor_parcela_anterior, 0)) * 100
    ) FILTER (
      WHERE tipo = 'renovacao'
        AND valor_parcela_anterior IS NOT NULL
        AND valor_parcela_novo IS NOT NULL
        AND valor_parcela_anterior > 0
        AND valor_parcela_novo > valor_parcela_anterior
    ), 2) AS reajuste_medio
  FROM movimentacoes_admin
  WHERE tipo IN ('renovacao', 'nao_renovacao')
  GROUP BY unidade_id, EXTRACT(year FROM data), EXTRACT(month FROM data)
)
```

- Ajustar o cálculo final de `taxa_renovacao` da view para usar:

```sql
ROUND((renovacoes::numeric / NULLIF(total_contratos, 0)) * 100, 2)
```

ou equivalente.

PATCH 2 — `vw_kpis_retencao_mensal`:
- Corrigir total de evasões realizadas para excluir `aviso_previo`.
- Manter `avisos_previos` como campo separado.
- Corrigir taxa de renovação para considerar `nao_renovacao` no denominador.
- Remover/ajustar qualquer `nao_renovacoes_renovacao` hardcoded 0 se ele estiver impedindo a taxa correta.

VALIDAÇÃO OBRIGATÓRIA ANTES/DEPOIS:

Para Maio/2026, após patch, as views devem refletir:

Campo Grande:
- renovações: 38
- não renovações: 5
- taxa renovação: 88.37% / 88.4%
- reajuste médio: 12.95%
- total evasões realizadas: 13
- avisos prévios separados: 8

Recreio:
- renovações: 16
- não renovações: 0
- taxa renovação: 100%
- reajuste médio: 10.41%

Barra:
- renovações: 9
- não renovações: 1
- taxa renovação: 90.00%
- reajuste médio: 8.70%

ENTREGA:
- Gere migration SQL ou patch equivalente.
- Mostre o diff antes de aplicar.
- Rode validação SQL antes/depois.
- Não mexa em frontend nesta etapa, a menos que a mudança de view quebre contrato existente.
- Se encontrar dependência que impeça trocar a view com segurança, pare e explique antes de aplicar.
