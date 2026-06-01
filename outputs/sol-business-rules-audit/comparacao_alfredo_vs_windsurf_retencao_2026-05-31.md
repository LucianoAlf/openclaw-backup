# Comparação — Auditoria Alfredo vs Windsurf — Retenção / Renovações / Reajustes

Data: 2026-05-31
Arquivo Windsurf recebido: `/root/.openclaw/media/inbound/auditoria_do_domínio_renovações_reajustes_não_renovações---327295ca-3cdd-4151-a495-2a68cc94df6f.md`

## Veredito

As auditorias batem no ponto central:

- `movimentacoes_admin` deve ser a fonte canônica operacional/live para retenção no mês corrente.
- `renovacoes` não deve ser usada como fonte de KPI de quantidade de renovações, taxa de renovação ou reajuste médio.
- `vw_kpis_gestao_mensal` está errada porque usa `renovacoes` para renovações/reajuste.
- `vw_kpis_retencao_mensal` tem bugs: taxa ignora não renovações e total de evasões inclui aviso prévio.
- Corrigir só `reajuste_medio` seria remendo ruim.

## Confirmações cruzadas

### Maio/2026 — números iguais nas duas auditorias

Campo Grande:
- `movimentacoes_admin`: 38 renovações, 5 não renovações, 24 aumentos positivos, reajuste médio 12,95%.
- `renovacoes`: 61 renovados, 0 não renovados, 0 aumentos, reajuste 0,00%.

Recreio:
- `movimentacoes_admin`: 16 renovações, 0 não renovações, 15 aumentos positivos, reajuste médio 10,41%.
- `renovacoes`: 26 renovados, reajuste 0,00%.

Barra:
- `movimentacoes_admin`: 9 renovações, 1 não renovação, 8 aumentos positivos, reajuste médio 8,70%.
- `renovacoes`: 10 renovados, reajuste 0,00%.

## Ressalvas importantes na auditoria Windsurf

### 1. SQL sugerido para Etapa 1 não deve ser aplicado literalmente

O trecho proposto:

```sql
COUNT(*) AS total_contratos
FROM movimentacoes_admin
GROUP BY unidade_id, EXTRACT(year FROM data), EXTRACT(month FROM data)
```

sem filtro por tipo conta todas as movimentações administrativas do mês: renovação, não renovação, evasão, aviso prévio, trancamento etc.

Se `total_contratos` for usado como denominador da taxa de renovação, a taxa fica errada.

Correção: limitar a CTE a `tipo IN ('renovacao','nao_renovacao')` ou calcular `total_contratos` com filtro:

```sql
COUNT(*) FILTER (WHERE tipo IN ('renovacao','nao_renovacao')) AS total_contratos
```

Regra validada para Campo Grande/Maio:

```text
38 / (38 + 5) = 88,37%
```

### 2. Causa exata de escrita em `renovacoes` ainda precisa cautela

Windsurf atribui principalmente ao `FormRenovacao.tsx`. Minha auditoria encontrou também indício forte no fluxo `processar-matricula-emusys`, que insere em `renovacoes` sem `valor_parcela_novo` no repo local.

Além disso, `FormRenovacao.tsx` parece usar colunas antigas (`valor_anterior`, `valor_novo`) que não batem com schema real (`valor_parcela_anterior`, `valor_parcela_novo`).

Conclusão: isso não bloqueia patch de KPI, mas impede afirmar com 100% de segurança que só o `FormRenovacao` é a causa.

### 3. Relatório Diário

Windsurf lista `renovacoes` como fonte do Relatório Diário. Minha leitura do arquivo `supabase/functions/relatorio-admin-whatsapp/index.ts` indicou uso de `movimentacoes_admin` para o relatório administrativo. Precisa confirmar versão deployada, mas não muda a decisão sobre a view.

## Recomendação final

Aprovar o conceito da Etapa 1, mas não o SQL literal.

Patch imediato seguro:

1. Corrigir `vw_kpis_gestao_mensal` usando `movimentacoes_admin` para:
   - renovações
   - não renovações
   - taxa renovação
   - reajuste médio positivo
2. Corrigir `vw_kpis_retencao_mensal` no mesmo ciclo se for baixo risco:
   - retirar `aviso_previo` de `total_evasoes`
   - taxa = `renovacao / (renovacao + nao_renovacao)` ou regra com pendentes, se validada
3. Não alterar dados.
4. Não apagar/aposentar `renovacoes` ainda.
5. Não criar trigger de sync ainda.
6. Validar com queries antes/depois nas 3 unidades.

## Valores esperados para validação pós-patch

Campo Grande/Maio 2026:
- renovações: 38
- não renovações: 5
- taxa renovação: 88,37% / 88,4%
- reajuste médio: 12,95%
- total evasões realizadas: 13
- avisos prévios separados: 8

Recreio/Maio 2026:
- renovações: 16
- não renovações: 0
- taxa renovação: 100%
- reajuste médio: 10,41%

Barra/Maio 2026:
- renovações: 9
- não renovações: 1
- taxa renovação: 90,00%
- reajuste médio: 8,70%
