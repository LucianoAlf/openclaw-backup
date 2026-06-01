# Auditoria — MIGRACAO_REGLA_KPI_V4_ALUNOS + V4_FINANCEIRO

Data: 2026-06-01

Arquivos:
- `/root/.openclaw/media/inbound/MIGRACAO_REGLA_KPI_V4_ALUNOS---c3352185-7f03-44ba-a440-c1d9784d22de.sql`
- `/root/.openclaw/media/inbound/MIGRACAO_REGLA_KPI_V4_FINANCEIRO---2c726f02-e840-4db5-882b-d5bff5f2b609.sql`

## Veredito curto

**Separar foi correto, mas ainda não aprovar execução.**

- **V4_ALUNOS:** regra de negócio está bem melhor e conceitualmente alinhada para alunos/matrículas, mas o arquivo ainda tem risco estrutural na view `vw_kpis_gestao_mensal`.
- **V4_FINANCEIRO:** segue bloqueado. Além de pendente validação nominal, tem erro estático de SQL (`am` não existe) e ainda persiste ticket provisório.

## V4_ALUNOS — pontos aprováveis conceitualmente

O arquivo acerta os pontos centrais da auditoria CG/Maio:

- Não tem `DROP VIEW`.
- `alunos_ativos = COUNT(DISTINCT nome)` pessoa-level, sem excluir segundo curso.
- `alunos_pagantes = COUNT(DISTINCT nome)` com `conta_como_pagante=true`.
- `matriculas_ativas = COUNT(*)` linha-level.
- `matriculas_banda` por `cursos.is_projeto_banda=true`.
- `matriculas_2_curso = is_segundo_curso=true` e `is_projeto_banda=false`.
- `novas_matriculas` agora filtra `status IN ('ativo','trancado')` e exclui banda/coral/bolsista.
- Não mexe em ticket, MRR, faturamento ou inadimplência na função.
- Não escreve em colunas geradas `faturamento_estimado` / `saldo_liquido`.

## V4_ALUNOS — bloqueador estrutural

O arquivo recria `vw_kpis_gestao_mensal` com **menos colunas** e com **ordem diferente** da view atual usada pelo frontend.

A view atual/repo tem colunas financeiras e comerciais consumidas pelo frontend, por exemplo:

- `ticket_medio`
- `mrr`
- `arr`
- `tempo_permanencia_medio`
- `ltv_medio`
- `inadimplencia_pct`
- `faturamento_previsto`
- `faturamento_realizado`
- `total_leads`
- `experimentais_agendadas`
- `experimentais_realizadas`
- `renovacoes`
- `taxa_renovacao`
- `reajuste_medio`

No PostgreSQL, `CREATE OR REPLACE VIEW` não pode remover/reordenar colunas existentes de uma view pública sem risco de erro ou quebra de contrato. Se a view atual tiver essas colunas, a V4_ALUNOS provavelmente falha ou quebra consumidores.

### Correção necessária

Escolher uma das opções:

1. **Preferida:** manter `vw_kpis_gestao_mensal` com o mesmo contrato de colunas atual, alterando apenas as expressões dos campos de alunos/matrículas/churn e deixando campos financeiros/comerciais como estavam.
2. Criar uma view nova de validação/dev, por exemplo `vw_kpis_gestao_mensal_alunos_v4`, sem tocar na view pública.
3. Só alterar a função `recalcular_dados_mensais` na parte de alunos/matrículas e deixar a view para uma migration completa posterior.

## V4_FINANCEIRO — bloqueios

### 1. Erro estático de SQL: alias `am` não existe

No SELECT final, o arquivo usa `am.ano` e `am.mes`, mas não existe CTE/alias `am`. A CTE se chama `at`.

Trecho problemático:

```sql
COALESCE(am.ano, EXTRACT(year FROM CURRENT_DATE)::int) AS ano,
COALESCE(am.mes, EXTRACT(month FROM CURRENT_DATE)::int) AS mes,
...
LEFT JOIN mm ON mm.unidade_id=u.id AND mm.ano=COALESCE(am.ano,...)
LEFT JOIN em ON em.unidade_id=u.id AND em.ano=COALESCE(am.ano,...)
LEFT JOIN rm ON rm.unidade_id=u.id AND rm.ano=COALESCE(am.ano,...)
```

Isso não compila.

### 2. Continua substituindo a view pública inteira

Mesmo sendo financeiro pendente, o arquivo faz `CREATE OR REPLACE VIEW vw_kpis_gestao_mensal`. Só pode acontecer quando o contrato completo da view estiver validado.

### 3. Ticket médio segue provisório, mas é persistido

O JSON retorna `ticket_medio_status = PROVISORIO_PENDENTE_VALIDACAO`, mas a função grava `ticket_medio` em `dados_mensais`.

Enquanto for provisório, não deve persistir.

### 4. Inadimplência é calculada, mas não persistida

A função calcula:

- `vip` = inadimplência percentual;
- `vi` = MRR inadimplente;

mas o INSERT/UPDATE de `dados_mensais` não grava `inadimplencia`.

### 5. Financeiro precisa validação nominal antes de virar regra

Ainda precisa comparar nominalmente:

- ticket médio atual do card R$386 vs nova fórmula;
- MRR/faturamento previsto;
- faturamento realizado;
- inadimplência;
- reajuste médio;
- tempo de permanência.

## Resposta recomendada ao Windsurf

```text
A separação da V4 foi correta, mas ainda não está aprovada para execução.

V4_ALUNOS:
- As regras de negócio estão alinhadas: ativos pessoa-level, pagantes pessoa-level por conta_como_pagante, matrículas linha-level, banda separada, segundo curso operacional excluindo banda, novas matrículas com status ativo/trancado.
- Porém o arquivo recria vw_kpis_gestao_mensal com menos colunas e ordem diferente. Isso pode falhar no PostgreSQL com CREATE OR REPLACE VIEW e/ou quebrar o frontend, porque a view pública atual expõe campos financeiros/comerciais como ticket_medio, mrr, arr, inadimplencia_pct, faturamento_previsto, faturamento_realizado, renovacoes, taxa_renovacao e reajuste_medio.
- Corrigir mantendo o contrato completo da view atual e alterando somente as expressões de alunos/matrículas/churn, ou criar uma view nova de dev (`vw_kpis_gestao_mensal_alunos_v4`) para validação.

V4_FINANCEIRO:
- Não executar.
- Tem erro estático: usa alias `am.ano`/`am.mes`, mas não existe alias `am` no SELECT final.
- Ticket médio segue marcado como provisório, mas é persistido em dados_mensais.
- Inadimplência é calculada, mas não é persistida em dados_mensais.
- Só deve avançar depois de validação nominal de ticket, MRR, faturamento, inadimplência, tempo de permanência e reajuste.

Gerar V5_ALUNOS mantendo contrato da view ou usando view dev separada. Não executar financeiro.
```

## Status

- **V4_ALUNOS:** não aprovado para execução ainda; aprovado conceitualmente com ajuste estrutural obrigatório.
- **V4_FINANCEIRO:** reprovado / não executar.
