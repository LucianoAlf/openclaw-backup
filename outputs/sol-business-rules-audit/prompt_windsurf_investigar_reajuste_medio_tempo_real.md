```md
Vamos investigar um possível bug no KPI “Reajuste Médio” do LA Report antes de corrigir qualquer coisa.

IMPORTANTE:
- O LA Report está em produção.
- Não aplicar alteração ainda.
- Primeiro quero diagnóstico, evidências, queries e confirmação da causa.
- Só depois da investigação validada a gente corrige.

## Contexto observado
Tela: Analytics > Gestão > Campo Grande > Maio/2026.

O card “Reajuste Médio” mostra `0.0%`.

Tooltip do card:
> “Percentual médio de aumento aplicado nas renovações do mês. Indica o poder de precificação.”

Mas no detalhamento/listagem de renovações aparecem várias renovações com aumento positivo, tipo +11%, +12%, etc.

## Regra de negócio já validada pelo Alf
Para “Reajuste Médio”:
- Considerar somente renovações com aumento positivo.
- Registros com reajuste 0 não entram na média.
- Registros sem valor anterior/novo também não entram.
- A métrica deve representar o percentual médio de aumento efetivamente aplicado.

Ou seja, o cálculo esperado é algo como:

```sql
AVG(
  ((valor_parcela_novo - valor_parcela_anterior) / NULLIF(valor_parcela_anterior, 0)) * 100
)
```

com filtros:

```sql
valor_parcela_anterior IS NOT NULL
AND valor_parcela_novo IS NOT NULL
AND valor_parcela_anterior > 0
AND valor_parcela_novo > valor_parcela_anterior
```

## Hipótese a investigar
A suspeita é que a view/card esteja usando a tabela/campo errado para o reajuste médio.

Possível cenário:
- `vw_kpis_gestao_mensal.reajuste_medio` está vindo de `renovacoes.percentual_reajuste`.
- Mas a tabela operacional que aparece no detalhamento pode ser `movimentacoes_admin`, com `tipo = 'renovacao'`, `valor_parcela_anterior` e `valor_parcela_novo`.

## O que investigar

### 1. Frontend
Localizar no repo onde o card “Reajuste Médio” é alimentado.

Pontos prováveis:
- `src/components/GestaoMensal/TabGestao.tsx`
- campos como `reajuste_medio`, `reajuste_pct`, `reajusteMedio`

Responder:
- Qual componente renderiza o card?
- Qual campo ele usa?
- Esse campo vem de qual query/view/tabela?

### 2. View em produção
Inspecionar a definição real no banco da view:

```sql
SELECT pg_get_viewdef('public.vw_kpis_gestao_mensal'::regclass, true);
```

Responder:
- Como `reajuste_medio` é calculado hoje?
- Ele usa `renovacoes`, `movimentacoes_admin`, `dados_mensais` ou outra fonte?
- A definição real do banco bate com as migrations do repo ou está diferente?

### 3. Conferir dados das fontes — Campo Grande / Maio 2026
Rodar queries separadas para comparar as fontes.

#### 3.1 View atual
```sql
SELECT unidade_id, ano, mes, reajuste_medio
FROM vw_kpis_gestao_mensal
WHERE ano = 2026
  AND mes = 5
  AND unidade_id = '<ID_CAMPO_GRANDE>';
```

#### 3.2 `renovacoes`
```sql
SELECT
  COUNT(*) AS total_linhas,
  COUNT(*) FILTER (WHERE status = 'renovado') AS renovadas,
  COUNT(*) FILTER (WHERE percentual_reajuste IS NOT NULL) AS com_percentual,
  AVG(percentual_reajuste) FILTER (WHERE status = 'renovado' AND percentual_reajuste > 0) AS media_percentual_positivo
FROM renovacoes
WHERE data_renovacao >= '2026-05-01'
  AND data_renovacao < '2026-06-01'
  AND unidade_id = '<ID_CAMPO_GRANDE>';
```

Também listar amostra:

```sql
SELECT id, aluno_id, status, data_renovacao, valor_parcela_anterior, valor_parcela_novo, percentual_reajuste
FROM renovacoes
WHERE data_renovacao >= '2026-05-01'
  AND data_renovacao < '2026-06-01'
  AND unidade_id = '<ID_CAMPO_GRANDE>'
ORDER BY data_renovacao
LIMIT 30;
```

#### 3.3 `movimentacoes_admin`
```sql
SELECT
  COUNT(*) AS total_renovacoes,
  COUNT(*) FILTER (
    WHERE valor_parcela_anterior IS NOT NULL
      AND valor_parcela_novo IS NOT NULL
      AND valor_parcela_anterior > 0
      AND valor_parcela_novo > valor_parcela_anterior
  ) AS renovacoes_com_aumento,
  ROUND(AVG(
    ((valor_parcela_novo - valor_parcela_anterior) / NULLIF(valor_parcela_anterior, 0)) * 100
  ) FILTER (
    WHERE valor_parcela_anterior IS NOT NULL
      AND valor_parcela_novo IS NOT NULL
      AND valor_parcela_anterior > 0
      AND valor_parcela_novo > valor_parcela_anterior
  ), 2) AS reajuste_medio_positivo
FROM movimentacoes_admin
WHERE tipo = 'renovacao'
  AND data >= '2026-05-01'
  AND data < '2026-06-01'
  AND unidade_id = '<ID_CAMPO_GRANDE>';
```

Também listar amostra:

```sql
SELECT id, aluno_id, aluno_nome, data, valor_parcela_anterior, valor_parcela_novo,
  ROUND(((valor_parcela_novo - valor_parcela_anterior) / NULLIF(valor_parcela_anterior, 0)) * 100, 2) AS reajuste_calc
FROM movimentacoes_admin
WHERE tipo = 'renovacao'
  AND data >= '2026-05-01'
  AND data < '2026-06-01'
  AND unidade_id = '<ID_CAMPO_GRANDE>'
  AND valor_parcela_anterior IS NOT NULL
  AND valor_parcela_novo IS NOT NULL
  AND valor_parcela_anterior > 0
  AND valor_parcela_novo > valor_parcela_anterior
ORDER BY data
LIMIT 30;
```

### 4. Conferir por unidade
Depois de Campo Grande, rodar a mesma lógica para:
- Recreio
- Barra

Responder se o problema é geral ou só Campo Grande/Maio.

## Saída esperada da investigação
Antes de qualquer correção, me retorne:

1. Fonte atual do card no frontend.
2. Definição real da `vw_kpis_gestao_mensal` para `reajuste_medio`.
3. Resultado das queries em:
   - `vw_kpis_gestao_mensal`
   - `renovacoes`
   - `movimentacoes_admin`
4. Valor esperado do reajuste médio usando a regra validada:
   - somente renovações com aumento positivo
   - ignorar reajuste 0
   - ignorar registros sem valor anterior/novo
5. Confirmação da causa raiz.
6. Proposta de correção mínima, mas sem aplicar ainda.

## Regra de segurança
Não recriar view inteira usando migration antiga.
Se a correção for na view, ela deve partir da definição real em produção e alterar somente o trecho necessário para `reajuste_medio`.
```
