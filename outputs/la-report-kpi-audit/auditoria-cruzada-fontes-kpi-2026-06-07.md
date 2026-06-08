# Auditoria cruzada — fontes de KPI LA Report

Data: 2026-06-07
Executor: Alfredo / OpenClaw
Escopo: cruzar relatório arquitetural recebido com código do repo `repos/LAperformanceReport` e catálogo real do Supabase LA Report.
Modo: SELECT-only / leitura de código. Nenhum dado alterado. Nenhum snapshot recalculado.

---

## 1. Conclusão executiva

A auditoria do Cascade está correta na tese: o sistema mistura fontes para KPIs equivalentes.

A auditoria cruzada confirmou, no banco e no código, que há pelo menos 5 classes de fonte competindo:

1. views live (`vw_kpis_gestao_mensal`, `vw_kpis_retencao_mensal`, `vw_dashboard_unidade` etc.);
2. snapshots (`dados_mensais`, `dados_comerciais`);
3. tabelas brutas (`alunos`, `movimentacoes_admin`, `leads`, etc.);
4. RPCs/functions (`get_programa_fideliza_dados`, `get_kpis_professor_periodo`, etc.);
5. cálculos/fallbacks locais no frontend.

Portanto, a divergência Recreio 310/311 não é bug isolado. É sintoma de dívida arquitetural de fonte/regra.

---

## 2. Evidência banco — Recreio 310 vs 311

Consulta SELECT-only no Supabase real confirmou:

### `vw_kpis_gestao_mensal` — Recreio
- Jun/2026: `total_alunos_pagantes = 310`
- `ticket_medio = 438`
- `mrr = 132939.10`
- `inadimplencia_pct = 0.65`

### `dados_mensais` — Recreio Jun/2026
- `alunos_pagantes = 311`
- `ticket_medio = 0`
- `faturamento_estimado = 0`
- `inadimplencia = 0`
- `evasoes = 17`

Conclusão: snapshot de Jun/2026 está stale/incompleto em relação à live view.

Observação crítica: `vw_kpis_gestao_mensal` retorna linhas para vários meses, mas campos de alunos/MRR/ticket são baseados no estado vivo atual e aparecem repetidos nos meses retornados; o mês varia por joins de leads/evasões/renovações. Isso reforça que a view live não deve ser tratada como histórico mensal fechado.

---

## 3. Catálogo real do banco — objetos chave

### Confirmados existentes

Views/tabelas/funções confirmadas no catálogo real:

- `dados_mensais` — tabela, com `UNIQUE (unidade_id, ano, mes)`.
- `dados_comerciais` — tabela.
- `movimentacoes_admin` — tabela.
- `vw_kpis_gestao_mensal` — view existente.
- `vw_kpis_retencao_mensal` — view existente.
- `vw_dashboard_unidade` — view existente.
- `vw_kpis_comercial_mensal` — view existente.
- `vw_kpis_comercial_historico` — view existente.
- `vw_kpis_professor_mensal` — view existente.
- `vw_kpis_professor_completo` — view existente.
- `vw_fator_demanda_professor` — view existente.
- `vw_turmas_implicitas` — view existente.
- `get_programa_fideliza_dados(p_ano, p_trimestre, p_unidade_id)` — function existente.
- `get_kpis_professor_periodo(p_ano, p_mes, p_unidade_id, p_data_inicio, p_data_fim)` — function existente.
- `get_carteira_professores(p_unidade_id)` — function existente.
- `get_tempo_permanencia(p_unidade_id, p_ano, p_mes)` — function existente.
- `get_dados_relatorio_coordenacao(p_unidade_id, p_ano, p_mes)` — function existente.

### Referências do código que NÃO existem no catálogo real

Pontos que precisam validação antes de qualquer plano:

- `get_presenca_por_aluno_professor` — referenciada em `ModalDetalhesPresenca.tsx`, mas não existe como function pública no catálogo.
- `vw_leads_diarios` — aparece em migrations/código, mas não existe no catálogo público atual.
- `vw_professor_360_historico` — referenciada em migration antiga, não existe no catálogo público atual.
- `vw_professor_360_resumo` — referenciada em SQL, não existe no catálogo público atual.

Observação: algumas referências `get_unidades`, `get_resumo_unidade`, `get_movimentacoes`, `get_funil_leads`, `get_leads_hoje`, `get_dados_mensais` aparecem como nomes internos de tools/functions em Edge Function (`bi-agent-lamusic`), não necessariamente RPCs SQL públicas. Não tratar automaticamente como bug de banco.

---

## 4. `dados_mensais` — risco confirmado

A tabela tem:

- `PRIMARY KEY (id)`;
- `UNIQUE (unidade_id, ano, mes)`;
- triggers de audit:
  - `tr_audit_dados_mensais` → `audit_dados_mensais()`;
  - `trg_audit` → `fn_audit_log()`;
  - `tr_dados_mensais_updated_at`.

Isso prova que existe algum audit log, mas não resolve governança de fechamento: funções ainda podem sobrescrever a linha única por mês/unidade.

### Funções reais que escrevem/sobrescrevem `dados_mensais`

Confirmadas no catálogo:

- `fechar_dados_mensais(p_ano, p_mes)` — faz `INSERT INTO dados_mensais ... ON CONFLICT (unidade_id, ano, mes) DO UPDATE`.
- `recalcular_dados_mensais(p_ano, p_mes, p_unidade_id)` — faz `INSERT INTO dados_mensais ... ON CONFLICT ... DO UPDATE`.
- `snapshot_dados_mensais(p_ano, p_mes)` — faz `INSERT INTO dados_mensais ... ON CONFLICT ... DO UPDATE`.
- `upsert_dados_mensais(...)` — faz `INSERT INTO dados_mensais ... ON CONFLICT ... DO UPDATE`, com atualização parcial por `COALESCE`.
- `sync_evasao_to_dados_mensais()` — trigger em `movimentacoes_admin`; faz `UPDATE dados_mensais SET evasoes = ..., churn_rate = ...`.

Trigger confirmado:

- `trg_sync_evasao_dados_mensais AFTER INSERT OR DELETE OR UPDATE ON movimentacoes_admin EXECUTE FUNCTION sync_evasao_to_dados_mensais()`.

Cron Supabase: nenhum job `cron.job` contendo `dados_mensais` retornou na consulta feita.

Conclusão: mês fechado ainda pode ser sobrescrito por função/botão/trigger. Isso é P0 de governança de snapshot.

---

## 5. Validação do relatório recebido

### Correto / confirmado

- Dashboard mistura fontes live/snapshot/fallback.
- Analytics/Gestão Mensal separa mês atual via view live e histórico via `dados_mensais`, mas ainda há fallback e inconsistência de agregação.
- Alunos recalcula cards localmente em frontend a partir de tabela bruta.
- Comercial mistura `vw_kpis_comercial_mensal` e `dados_comerciais`.
- Administrativo mistura cards gerenciais via views e tabelas operacionais brutas.
- Professores é área frágil por RPC + views + fallback.
- Fideliza+ usa `get_programa_fideliza_dados()` e herda staleness de `dados_mensais`.

### Precisa ajuste

- Nem todo objeto citado é view/RPC real no banco; alguns são nomes de tools de Edge Function ou legados em migration.
- Professores precisa ser separado entre:
  - funções/views reais existentes;
  - fallback frontend;
  - referências inexistentes (`get_presenca_por_aluno_professor`).
- `vw_kpis_gestao_mensal` deve ser marcada como fonte live atual, não fonte histórica, porque campos vivos repetem nos meses.

---

## 6. Matriz operacional inicial — P0

| KPI | Live atual provável | Histórico atual | Problema | Fonte-alvo recomendada |
|---|---|---|---|---|
| Alunos Pagantes | `vw_kpis_gestao_mensal.total_alunos_pagantes` + cálculos locais em Alunos/Dashboard | `dados_mensais.alunos_pagantes` | mesmo KPI em view, snapshot e frontend | Live: fonte canônica única; Histórico: `dados_mensais` fechado |
| Alunos Ativos | `vw_kpis_gestao_mensal.total_alunos_ativos` + cálculos locais | `dados_mensais.alunos_ativos` | pessoa vs linha e fallback local | Live: fonte canônica única; Histórico: `dados_mensais` fechado |
| Ticket Médio | `vw_kpis_gestao_mensal.ticket_medio` + cálculo frontend | `dados_mensais.ticket_medio` | regra por pessoa não centralizada em todos os cards | Live: fonte canônica única; Histórico: snapshot |
| MRR | `vw_kpis_gestao_mensal.mrr` | `dados_mensais.faturamento_estimado`/campos financeiros | nomenclatura e competência financeira ainda frágeis | Live: canônica; Histórico: snapshot com definição explícita |
| Inadimplência | `vw_kpis_gestao_mensal.inadimplencia_pct` | `dados_mensais.inadimplencia` | snapshot zerado/stale já visto | Live: canônica; Histórico: snapshot protegido |
| Churn | `vw_kpis_gestao_mensal.churn_rate`/`vw_kpis_retencao_mensal` | `dados_mensais.churn_rate`/`evasoes` | transferência interna ainda não aplicada; trigger pode sobrescrever snapshot | Live: canônica com regra; Histórico: snapshot protegido |

---

## 7. Próximas ações recomendadas

### Não fazer ainda

- Não corrigir card por card no improviso.
- Não recalcular `dados_mensais`.
- Não rodar backfill.
- Não aplicar UPDATE em transferências históricas.
- Não transformar todas as views em RPC sem desenho.

### Fazer agora

1. Transformar esta auditoria em matriz operacional final:
   - KPI;
   - tela;
   - arquivo;
   - fonte atual;
   - objeto confirmado no banco;
   - live/histórico;
   - regra atual;
   - risco;
   - fonte-alvo;
   - prioridade.

2. Criar uma camada/fonte canônica live para P0 ou eleger explicitamente a view/RPC canônica existente após revisão da `vw_kpis_gestao_mensal`.

3. Separar snapshot como frente própria e urgente:
   - impedir overwrite de mês fechado;
   - criar retificação com motivo/diff/aprovador;
   - bloquear trigger/function que altera mês fechado sem fluxo formal;
   - manter audit log e rollback.

4. Primeiro patch futuro deve ser pequeno:
   - exemplo: card `Pagantes` da tela Alunos usar fonte canônica live quando está mostrando KPI executivo, sem mexer na lista operacional.

---

## 8. Arquivos de evidência gerados

- `outputs/la-report-kpi-audit/code-refs.raw.txt`
- `outputs/la-report-kpi-audit/code-objects.json`
- `outputs/la-report-kpi-audit/catalog.json`
- `outputs/la-report-kpi-audit/catalog-crosscheck.md`
- `outputs/la-report-kpi-audit/key-defs.json`
- `outputs/la-report-kpi-audit/dados-mensais-writers.json`
- `outputs/la-report-kpi-audit/writer-defs.md`
- `outputs/la-report-kpi-audit/recreio-live-vs-snapshot.json`
