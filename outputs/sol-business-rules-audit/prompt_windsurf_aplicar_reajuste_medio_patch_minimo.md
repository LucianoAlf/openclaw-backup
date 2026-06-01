```md
Diagnóstico aprovado. Agora vamos aplicar uma correção mínima e segura no KPI “Reajuste Médio” do LA Report.

IMPORTANTE:
- O LA Report está em produção.
- Fazer patch mínimo.
- Não recriar a view inteira a partir de migration antiga.
- Usar a definição real atual da view em produção como base.
- Não mexer agora em taxa de renovação, contagem de renovações, evasões, segundo curso ou qualquer outro KPI.

## Regra de negócio validada pelo Alf
Reajuste Médio = média percentual somente das renovações com aumento positivo.

Não considerar:
- reajuste 0;
- registros sem `valor_parcela_anterior`;
- registros sem `valor_parcela_novo`;
- registros com `valor_parcela_anterior <= 0`;
- registros em que `valor_parcela_novo <= valor_parcela_anterior`.

Fonte operacional validada para este KPI:
- `movimentacoes_admin`
- `tipo = 'renovacao'`
- `data` como competência da renovação
- `valor_parcela_anterior`
- `valor_parcela_novo`

Valores esperados para Maio/2026 após correção:
- Campo Grande: 12,95%
- Recreio: 10,41%
- Barra: 8,70%

## Cuidado com a proposta anterior
Não substitua a CTE `renovacoes_mes` inteira de forma ampla, porque ela também alimenta:
- `renovacoes`
- `total_contratos`
- `taxa_renovacao`

Esses pontos ainda terão auditoria própria.

A correção mais segura agora é criar uma CTE separada, por exemplo `reajuste_mes`, usando `movimentacoes_admin`, e trocar somente o campo final `reajuste_medio` para vir dela.

## Patch SQL sugerido conceitualmente
Na definição da `vw_kpis_gestao_mensal`, adicionar uma CTE separada:

```sql
reajuste_mes AS (
  SELECT
    ma.unidade_id,
    EXTRACT(YEAR FROM ma.data)::integer AS ano,
    EXTRACT(MONTH FROM ma.data)::integer AS mes,
    ROUND(
      AVG(
        ((ma.valor_parcela_novo - ma.valor_parcela_anterior) / NULLIF(ma.valor_parcela_anterior, 0)) * 100
      ) FILTER (
        WHERE ma.tipo = 'renovacao'
          AND ma.valor_parcela_anterior IS NOT NULL
          AND ma.valor_parcela_novo IS NOT NULL
          AND ma.valor_parcela_anterior > 0
          AND ma.valor_parcela_novo > ma.valor_parcela_anterior
      ),
      2
    ) AS reajuste_medio
  FROM movimentacoes_admin ma
  WHERE ma.tipo = 'renovacao'
  GROUP BY ma.unidade_id, EXTRACT(YEAR FROM ma.data), EXTRACT(MONTH FROM ma.data)
)
```

Depois, no SELECT final da view, trocar somente o campo final de reajuste:

```sql
COALESCE(rjm.reajuste_medio, 0)::numeric(5,2) AS reajuste_medio
```

E adicionar o join correspondente:

```sql
LEFT JOIN reajuste_mes rjm
  ON rjm.unidade_id = u.id
 AND rjm.ano = COALESCE(lm.ano, am.ano, rm.ano)
 AND rjm.mes = COALESCE(lm.mes, am.mes, rm.mes)
```

Ajuste os aliases conforme a definição real atual da view. Não force esses nomes se a view atual estiver diferente.

## Validação obrigatória depois do patch
Rodar:

```sql
SELECT u.nome, v.ano, v.mes, v.reajuste_medio
FROM vw_kpis_gestao_mensal v
JOIN unidades u ON u.id = v.unidade_id
WHERE v.ano = 2026
  AND v.mes = 5
ORDER BY u.nome;
```

Esperado:
- Barra: 8,70
- Campo Grande: 12,95
- Recreio: 10,41

Também confirmar que estes campos não mudaram por causa do patch:
- total_alunos_ativos
- total_alunos_pagantes
- novas_matriculas
- total_evasoes
- renovacoes
- taxa_renovacao

## Retorno esperado
Depois de aplicar, me envie:
1. SQL exato aplicado.
2. Resultado da query de validação por unidade.
3. Comparação antes/depois apenas do `reajuste_medio`.
4. Confirmação de que nenhum outro KPI mudou.
```
