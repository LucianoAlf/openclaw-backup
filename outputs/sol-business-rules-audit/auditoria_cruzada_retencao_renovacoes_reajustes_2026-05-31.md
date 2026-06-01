# Auditoria cruzada — Retenção / Renovações / Reajustes / Não Renovações

Data: 2026-05-31  
Escopo: LA Report — repo local + Supabase produção, somente leitura.  
Período foco: Maio/2026 por unidade.

## 1. Conclusão curta

O domínio está dividido entre duas fontes:

1. `movimentacoes_admin` é a fonte operacional mais confiável para o mês corrente:
   - renovações (`tipo='renovacao'`)
   - não renovações (`tipo='nao_renovacao'`)
   - evasões/cancelamentos (`tipo='evasao'`)
   - avisos prévios (`tipo='aviso_previo'`), mas aviso prévio não deve entrar como evasão realizada.

2. `renovacoes` está sendo alimentada por fluxo automático/legado, especialmente Emusys, mas em Maio/2026 está incompleta para KPI:
   - registros com `valor_parcela_novo` nulo
   - `percentual_reajuste` nulo/zero
   - não renovações ausentes
   - contagem diferente de `movimentacoes_admin`

Portanto: corrigir só o card de Reajuste Médio usando `renovacoes` seria remendo ruim. A correção coerente para o mês atual deve mover o bloco de retenção corrente para `movimentacoes_admin`, preservando `renovacoes` como histórico/apoio até auditoria de legado.

## 2. Evidência — Supabase schema real

Tabelas relevantes existem:

- `movimentacoes_admin`: 1271 registros, período 2025-01-01 a 2026-06-27.
- `renovacoes`: 377 registros, período 2025-12-09 a 2026-05-30.
- `dados_mensais`: 121 registros, período 2023-01 a 2026-05.
- `evasoes_v2`: 740 registros, período 2025-01-01 a 2026-02-24.
- `evasoes` não aparece no schema real consultado via `information_schema.tables`.

Triggers reais:

- `movimentacoes_admin`:
  - auditoria genérica `fn_audit_log()`.
  - `trg_sync_evasao_dados_mensais` em INSERT/UPDATE/DELETE, função `sync_evasao_to_dados_mensais()`.
- `renovacoes`:
  - auditoria genérica `fn_audit_log()`.
  - `trigger_calcular_reajuste` em INSERT/UPDATE, função `calcular_reajuste_renovacao()`.
  - `update_renovacoes_updated_at`.

Não há trigger real em produção sincronizando `movimentacoes_admin.tipo='renovacao'` para `renovacoes`. A migration antiga `20260127_sync_movimentacoes_admin.sql` tem função `sync_renovacao_to_historico()`, mas ela não existe no DB real hoje.

## 3. Evidência — funções/views reais

### `calcular_reajuste_renovacao()`

Calcula `percentual_reajuste` em `renovacoes` apenas se `valor_parcela_anterior > 0`; usa `valor_parcela_novo`. Se `valor_parcela_novo` vem nulo, o percentual vira nulo/zero na prática e o KPI quebra.

### `sync_evasao_to_dados_mensais()`

Atualiza `dados_mensais.evasoes` e `churn_rate` a partir de `movimentacoes_admin`, contando somente:

- `tipo='evasao'`
- `tipo='nao_renovacao'`

A trigger é disparada também por `aviso_previo`, mas o count exclui aviso prévio. Isso está alinhado com a regra validada: aviso prévio não é evasão realizada.

### `vw_kpis_gestao_mensal`

Mistura fontes:

- Evasões: `movimentacoes_admin`, apenas `evasao` + `nao_renovacao`.
- Renovações/reajuste: `renovacoes`.

Problema: para Maio/2026, `renovacoes` está ruim para reajuste e taxa; logo a view retorna:

- renovação CG: 61 em vez de 38
- taxa CG: 100% em vez de 88,37%
- reajuste CG: 0,0% em vez de 12,95%

### `vw_kpis_retencao_mensal`

Também mistura fontes, mas de outro jeito:

- Renovações realizadas: `movimentacoes_admin.tipo='renovacao'`.
- Não renovações: vêm da CTE de evasões (`movimentacoes_admin.tipo='nao_renovacao'`).
- Porém `renovacoes_previstas = count(renovacao)` e `renovacoes_realizadas = count(renovacao)`, com `nao_renovacoes_renovacao = 0`.

Resultado: taxa de renovação fica 100% sempre que há renovações, porque o denominador ignora `nao_renovacao`.

Outro problema: `total_evasoes` desta view inclui `aviso_previo`, então em CG Maio/2026 retorna 21 (= 8 evasões + 5 não renovações + 8 avisos prévios), quando a regra operacional para evasões realizadas é 13 (= 8 + 5).

## 4. Evidência — repo/frontend

### `TabGestao.tsx`

- Período atual usa `vw_kpis_gestao_mensal` e `vw_kpis_retencao_mensal`.
- Reajuste médio vem de `vw_kpis_gestao_mensal.reajuste_medio`.
- Fallback ainda consulta `renovacoes.percentual_reajuste`.

Arquivos/linhas relevantes:

- `src/components/GestaoMensal/TabGestao.tsx`: current path usa views em tempo real.
- `src/components/GestaoMensal/TabGestao.tsx`: fallback histórico ainda usa `renovacoes` para reajuste/taxa.

### `AdministrativoPage.tsx`

- Tela administrativa usa `movimentacoes_admin` como base operacional.
- Também consulta `vw_kpis_retencao_mensal` e combina com `Math.max`, o que mascara algumas divergências.
- A taxa exibida no modal administrativo é calculada corretamente no frontend como:
  `renovacoes_realizadas / (renovacoes_realizadas + nao_renovacoes)`.

### `relatorio-admin-whatsapp`

O relatório diário administrativo usa `movimentacoes_admin` para renovações e não renovações, depois calcula:

`renovacoes_realizadas / (renovacoes_realizadas + nao_renovacoes + pendentes)`

No caso atual, sem pendentes, bate com a regra de taxa de renovação.

### `DashboardPage.tsx`

Tem comentário explícito: “Buscar renovações e não renovações de movimentacoes_admin (fonte de verdade)”. Calcula taxa de renovação como:

`renovacao / (renovacao + nao_renovacao)`

Isso reforça que o próprio repo já trata `movimentacoes_admin` como fonte operacional em alguns lugares.

### `PlanilhaRetencao.tsx`

Mistura duas tabelas:

- Evasões/não renovações/avisos: `movimentacoes_admin`.
- Renovações: `renovacoes`.

Ela também salva novos registros conforme o tipo/tabela da linha. Isso perpetua a bifurcação.

### `FormRenovacao.tsx`

Parece defasado/perigoso:

- insere em `renovacoes` usando colunas antigas `valor_anterior`, `valor_novo`, `duracao_contrato_meses`, `motivo_reajuste`.
- essas colunas não existem no schema real atual, que usa `valor_parcela_anterior` e `valor_parcela_novo`.

Se essa rota estiver ativa, tende a falhar ou já está fora do fluxo real.

### `processar-matricula-emusys`

No repo, o fluxo automático insere em `renovacoes` com:

- `valor_parcela_anterior`
- `status='renovado'`
- observação “Automático via Emusys”
- sem `valor_parcela_novo`

Isso explica por que `renovacoes` de Maio/2026 tem registros automáticos sem valor novo e reajuste zerado/nulo.

Observação: os registros reais de `movimentacoes_admin` vindos do Emusys têm valores anterior/novo em muitos casos; isso pode indicar código deployado diferente do repo, update posterior, ou outro processo. Mesmo assim, a evidência do DB real favorece `movimentacoes_admin` para KPI atual.

## 5. Comparativo Maio/2026 por unidade

### Campo Grande

Fonte operacional `movimentacoes_admin`:

- Renovações: 38
- Não renovações: 5
- Taxa: 88,37%
- Reajustes positivos: 24
- Reajuste médio positivo: 12,95%
- Evasões/cancelamentos: 8
- Avisos prévios: 8
- Evasões realizadas: 13 (= 8 + 5)

Tabela/view divergente:

- `renovacoes`: 61 registros, todos `status='renovado'`, `valor_parcela_novo` ausente, reajuste 0/nulo.
- `vw_kpis_gestao_mensal`: renovações 61, taxa 100%, reajuste 0,0%.
- `vw_kpis_retencao_mensal`: renovações 38, não renovações 5, mas taxa 100% porque denominador ignora não renovações; total_evasoes 21 porque inclui avisos.
- `dados_mensais`: taxa 0,0%, reajuste 0,0%, snapshot defasado para KPI corrente.

### Recreio

Fonte operacional `movimentacoes_admin`:

- Renovações: 16
- Não renovações: 0
- Taxa: 100%
- Reajustes positivos: 15
- Reajuste médio positivo: 10,41%
- Evasões/cancelamentos: 19

Tabela/view divergente:

- `renovacoes`: 26 registros, valor novo ausente, reajuste 0/nulo.
- `vw_kpis_gestao_mensal`: renovações 26, taxa 100%, reajuste 0,0%.
- `vw_kpis_retencao_mensal`: renovações 16, taxa 100%.

### Barra

Fonte operacional `movimentacoes_admin`:

- Renovações: 9
- Não renovações: 1
- Taxa: 90,00%
- Reajustes positivos: 8
- Reajuste médio positivo: 8,70%
- Evasões/cancelamentos: 12

Tabela/view divergente:

- `renovacoes`: 10 registros, valor novo ausente, reajuste 0/nulo.
- `vw_kpis_gestao_mensal`: renovações 10, taxa 100%, reajuste 0,0%.
- `vw_kpis_retencao_mensal`: renovações 9, não renovações 1, mas taxa 100% porque denominador ignora não renovações.

## 6. Histórico Jan–Mai/2026

Comparação resumida:

- Jan–Mar/2026: `renovacoes` às vezes ainda tem valores úteis e alguns meses batem parcialmente com `movimentacoes_admin`.
- Abr–Mai/2026: `renovacoes` degrada fortemente; reajuste vira 0,0% em todas as unidades e não renovações somem.
- `dados_mensais` tem campos `taxa_renovacao` e `reajuste_parcelas`, mas vários meses de 2026 estão zerados/nulos ou defasados.

Conclusão histórica: não dá para deletar/demover `renovacoes` sem migração/auditoria. Mas para KPI corrente, ela não é fonte confiável.

## 7. Diagnóstico técnico

### Problema central

A arquitetura está com dupla escrita e dupla leitura:

- Algumas telas/views leem `renovacoes`.
- Outras leem `movimentacoes_admin`.
- O relatório administrativo já se comporta como se `movimentacoes_admin` fosse a verdade operacional.
- O card de Gestão Mensal ainda lê `renovacoes` via `vw_kpis_gestao_mensal`.

### Por que Reajuste Médio está 0,0%

Porque `vw_kpis_gestao_mensal.reajuste_medio` calcula:

`avg(renovacoes.percentual_reajuste) filter (where status='renovado')`

Mas em Maio/2026 os registros de `renovacoes` são automáticos/Emusys, sem `valor_parcela_novo`, então `percentual_reajuste` fica nulo/zero.

### Por que Taxa de Renovação está errada

Há dois erros diferentes:

1. Em `vw_kpis_gestao_mensal`, `renovacoes` não tem não-renovações para Maio/2026, então taxa vira 100%.
2. Em `vw_kpis_retencao_mensal`, as não-renovações aparecem, mas não entram no denominador da taxa.

## 8. Recomendação arquitetural

### Para mês atual / operação viva

Fonte canônica recomendada:

- `movimentacoes_admin`

Regras:

- Renovações realizadas: count `tipo='renovacao'`.
- Não renovações: count `tipo='nao_renovacao'`.
- Taxa renovação: `renovacao / (renovacao + nao_renovacao)`.
- Reajuste médio: média apenas de `tipo='renovacao'` com:
  - `valor_parcela_anterior > 0`
  - `valor_parcela_novo > valor_parcela_anterior`
- Reajuste 0 não entra.
- Valor anterior/novo ausente não entra.
- Evasões realizadas: `evasao + nao_renovacao`.
- Aviso prévio fica separado; não entra em evasões realizadas/churn até virar saída efetiva.

### Para histórico/fechamento

- `dados_mensais` pode continuar como snapshot/fechamento, mas precisa ser preenchido corretamente no fechamento.
- `renovacoes` deve ser preservada enquanto histórico/legado/apoio; não deletar.
- Antes de decidir o destino de `renovacoes`, fazer migração/normalização:
  - mapear origem dos registros
  - reconciliar com `movimentacoes_admin`
  - decidir se vira tabela de contratos/renovações previstas ou se será legada.

## 9. Patch recomendado, sem aplicar ainda

Não recomendo patch mínimo isolado só no Reajuste Médio se a tela vai continuar exibindo taxa e renovações divergentes.

Recomendo patch coerente em duas views:

1. `vw_kpis_gestao_mensal`
   - manter demais KPIs como estão.
   - substituir CTE `renovacoes_mes` por base em `movimentacoes_admin`, ou adicionar CTEs separadas para:
     - `renovacoes_realizadas`
     - `nao_renovacoes`
     - `reajuste_medio`
   - calcular `taxa_renovacao` com denominador `renovacao + nao_renovacao`.

2. `vw_kpis_retencao_mensal`
   - corrigir `renovacoes_previstas = renovacao + nao_renovacao + pendentes` se pendentes existirem.
   - corrigir `taxa_renovacao = renovacao / (renovacao + nao_renovacao + pendentes)` ou, se pendentes não fazem parte da taxa realizada, validar com Alf.
   - corrigir `total_evasoes` para não incluir `aviso_previo` quando o campo significa evasões realizadas.
   - manter `avisos_previos` como campo próprio.

## 10. Pendências de validação com Alf/equipe

1. Confirmar se, para taxa de renovação mensal, pendentes entram no denominador ou só vencimentos resolvidos entram.
   - Regra já usada no relatório administrativo atual: realizadas / (realizadas + não renovações + pendentes).
   - Regra validada parcialmente no caso CG: 38 / (38 + 5) = 88,4%.

2. Confirmar se `movimentacoes_admin` vira oficialmente a fonte canônica operacional de retenção.

3. Confirmar destino de `renovacoes`:
   - legado/histórico
   - apoio de contrato
   - tabela a ser reestruturada/sincronizada

4. Auditar `evasoes_v2`, porque tem histórico até 2026-02-24 e não deve ser abandonada sem reconciliação.

## 11. Arquivos de evidência gerados

- `supabase_retencao_schema_dump_partial.json`
- `supabase_retencao_data_comparison_2026-05.json`
- `retencao_comparativo_2026_jan-mai.json`
