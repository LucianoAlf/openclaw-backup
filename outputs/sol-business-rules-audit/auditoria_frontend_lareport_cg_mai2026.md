# Auditoria frontend LA Report — Analytics / Campo Grande / Mai 2026

Data da auditoria: 2026-05-31  
URL: `https://la-aperformance-report.vercel.app/app/gestao-mensal`  
Filtro: Unidade `Campo Grande`, ano `2026`, mês `Mai`, aba `Gestão`.

## Acesso
- Login funcionou via navegador headless.
- Tela auditada diretamente no frontend.
- Trace de chamadas capturado via `performance.getEntriesByType('resource')`.

## Fontes chamadas pelo frontend
Para Campo Grande/Mai 2026, o frontend chama principalmente:

- `vw_kpis_gestao_mensal?select=*&ano=eq.2026&mes=eq.5&unidade_id=...`
- `vw_kpis_retencao_mensal?select=*&ano=eq.2026&mes=gte.5&mes=lte.5&unidade_id=...`
- `dados_mensais?select=*&ano=eq.2026&mes=eq.4/5&unidade_id=...`
- `metas_kpi?ano=2026&mes=5&unidade_id=...`
- `alunos?...status=in.(ativo,trancado)` para distribuição Kids/School
- `movimentacoes_admin?...tipo=in.(evasao,nao_renovacao)` para detalhes de evasão

JSONs salvos em:
`outputs/sol-business-rules-audit/frontend_trace_cg_mai2026/`

## Números vistos no frontend

### Gestão > Alunos
- Total alunos ativos: 499
- Alunos pagantes: 475 / 479
- LA Music Kids: 214
- LA Music School: 351
- Banda: 41
- Novas matrículas: 23
- Evasões: 13
- Saldo líquido: 10
- Bolsistas integrais: 14
- Bolsistas parciais: 10

### Gestão > Financeiro
- Ticket médio: R$ 385 / R$ 387
- MRR: R$ 176.696
- ARR: R$ 2.120.349
- LTV médio: R$ 7.553
- Faturamento previsto: R$ 176.696
- Faturamento realizado: R$ 174.638
- Inadimplência: 1,3% / 1,5%
- Reajuste médio: 0,0%

### Gestão > Retenção
- Cancelamentos: 8
- Não renovações: 5
- Total evasões: 13
- Churn rate: 2,7% / 4,0%
- MRR perdido: R$ 1.719
- Renovações: 38
- Taxa renovação: 88,4% / 90,0%
- Aviso prévio: 8
- Tempo permanência: 19,6 meses
- NPS evasões: 0,0

## Cruzamento com Supabase

### `vw_kpis_gestao_mensal`
Retornou:
- `total_alunos_ativos = 499`
- `total_alunos_pagantes = 475`
- `total_bolsistas_integrais = 14`
- `total_bolsistas_parciais = 10`
- `total_banda = 41`
- `total_segundo_curso = 66`
- `ticket_medio = 385.35`
- `mrr = 176695.73`
- `arr = 2120348.76`
- `tempo_permanencia_medio = 19.6`
- `ltv_medio = 7552.82`
- `inadimplencia_pct = 1.26`
- `faturamento_previsto = 176695.73`
- `faturamento_realizado = 174637.73`
- `novas_matriculas = 23`
- `total_evasoes = 13`
- `churn_rate = 2.74`

Conclusão: boa parte dos cards do frontend está arredondando diretamente esta view.

### `metas_kpi`
Metas usadas nos denominadores dos cards:
- `alunos_pagantes = 479` → explica o `/479`.
- `ticket_medio = 387` ou `ticket_parcela = 387` → explica `/R$ 387`.
- `churn_rate = 4.0` → explica `/4.0%`.
- `inadimplencia = 1.5` → explica `/1.5%`.
- `taxa_renovacao = 90.0` → explica `/90.0%`.

Regra: denominador depois da barra é meta, não total/base operacional.

### `dados_mensais` está defasado em relação à view atual
Para Campo Grande/Mai 2026, `dados_mensais` retornou:
- `alunos_ativos = 511`
- `alunos_pagantes = 481`
- `novas_matriculas = 29`
- `matriculas_ativas = 579`
- `matriculas_banda = 46`
- `matriculas_2_curso = 68`
- `ticket_medio = 348.13`
- `faturamento_estimado = 167450.53`

Isso diverge da tela atual e da `vw_kpis_gestao_mensal`.

Regra candidata: para mês corrente, Sol deve priorizar `vw_kpis_gestao_mensal`; `dados_mensais` é snapshot/histórico e pode ficar defasado antes do fechamento/recalcular.

## Achados de regra

### `[CANONICA-CANDIDATA]` Denominador visual `/479`, `/387`, `/4.0%` é meta
Não é denominador de cálculo operacional. Vem da tabela `metas_kpi`.

### `[CANONICA-CANDIDATA]` Alunos vs matrículas
- `total_alunos_ativos = 499` vem da view.
- Query direta `alunos status in ativo,trancado` retornou 565 linhas, que corresponde a matrículas.
- Aproximação por nome único deu ~500 pessoas.
- Portanto, a LA opera com duas bases:
  - **alunos/pessoas** para base ativa;
  - **matrículas/linhas** para cursos/produtos.

### `[CANONICA-CANDIDATA]` Kids/School no frontend é contagem de matrículas, não pessoas
O código em `src/components/GestaoMensal/TabGestao.tsx` busca `alunos` com `status in ('ativo','trancado')` e conta por `idade_atual`.
Isso gera:
- Kids 214
- School 351
- Soma 565 = matrículas ativas/trancadas

Por isso passa de 499. O problema é mais de **rótulo/base visual** do que necessariamente cálculo errado.

### `[CANONICA-CANDIDATA]` Pagantes = ativos - bolsistas integrais - bolsistas parciais
- `499 - 14 - 10 = 475`.
- Relatório administrativo confirma: não pagantes 24 = 14 + 10.
- Bolsista parcial entra como não pagante nessa regra operacional.

### `[CANONICA-CANDIDATA]` ARR usa centavos antes do arredondamento
- `mrr = 176695.73`
- `arr = 2120348.76`
- `176695.73 * 12 = 2120348.76`
- Tela arredonda para R$ 2.120.349.
- A diferença de R$ 3 vs `176.696 x 12` é só arredondamento.

### `[CANONICA-CANDIDATA]` Churn usa pagantes como base
- `13 / 475 * 100 = 2,7368%`, arredonda para 2,7%.
- Não usa total ativo 499.

### `[CANONICA-CANDIDATA]` Taxa renovação exibida é recalculada no frontend
- View `vw_kpis_retencao_mensal` traz `taxa_renovacao = 100.0`, mas frontend mostra 88,4%.
- Código em `TabGestao.tsx` calcula:
  `renovacoes_realizadas / (renovacoes_realizadas + nao_renovacoes)`.
- Tela: `38 / (38 + 5) = 88,4%`.
- Logo, para a Sol, a regra correta da tela atual é a do frontend, não a coluna da view.

## Divergências abertas

### `[DIVERGENTE]` Aviso prévio: relatório diário 7 vs frontend 8
- Frontend usa `vw_kpis_retencao_mensal.avisos_previos = 8`.
- Relatório administrativo enviado pela equipe lista 7 avisos para junho.
- Edge function `relatorio-admin-whatsapp` busca aviso prévio por `mes_saida` no mês seguinte; frontend usa view mensal.
- Precisa auditar se há um aviso sem nome/listagem, diferença de data/hora ou filtro de status.

### `[DIVERGENTE]` Segundo curso: relatório diário 28 vs view/query 66/68
- Relatório diário enviado: matrículas de 2º curso = 28.
- `vw_kpis_gestao_mensal.total_segundo_curso = 66`.
- `dados_mensais.matriculas_2_curso = 68`.
- Query direta `is_segundo_curso_true = 66`.
- Grande divergência. Precisa validação urgente: talvez equipe conte só 2º curso pagante/passaporte, enquanto banco marca muito mais linhas como segundo curso.

### `[DIVERGENTE]` Trancados: relatório diário 2 vs query direta 5
- Relatório administrativo: trancados = 2.
- Query direta em `alunos status='trancado'` dentro de ativos/trancados retornou 5 para Campo Grande.
- Precisa validar se relatório exclui banda/2º curso/bolsistas ou filtra outra data.

### `[DIVERGENTE]` `vw_kpis_retencao_mensal.total_evasoes = 21`, tela mostra 13
- A view parece somar algo além de cancelamento + não renovação, possivelmente avisos prévios.
- Frontend exibe `r.evasoes_interrompidas + r.nao_renovacoes`, portanto 8 + 5 = 13.
- Regra correta para tela/relatório: evasões = cancelamentos + não renovações. Aviso prévio não entra como evasão.

## Próximo passo técnico
1. Auditar SQL da `vw_kpis_gestao_mensal`.
2. Auditar SQL da `vw_kpis_retencao_mensal`.
3. Auditar edge `relatorio-admin-whatsapp` vs `TabGestao.tsx`.
4. Resolver divergência crítica de `is_segundo_curso`.
5. Resolver divergência de aviso prévio 7 vs 8.
