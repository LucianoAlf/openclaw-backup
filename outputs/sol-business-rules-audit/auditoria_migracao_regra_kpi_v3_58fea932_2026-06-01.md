# Auditoria — MIGRACAO_REGLA_KPI_V3 58fea932

Data: 2026-06-01
Arquivo: `/root/.openclaw/media/inbound/MIGRACAO_REGLA_KPI_V3---58fea932-6039-464d-ae1b-5bf1f8acea5a.sql`

## Veredito

**Ainda não aprovar para execução.**

A V3 melhorou bastante, mas ainda tem bloqueios de produto/dados antes de rodar em produção.

## Melhorias confirmadas

- Removeu `DROP VIEW IF EXISTS vw_kpis_gestao_mensal`.
- Padronizou `alunos_ativos` entre view e função como `COUNT(DISTINCT nome)` sem filtrar segundo curso.
- Documentou que `vw_kpis_gestao_mensal` é snapshot vivo/mês corrente, não histórico fechado.
- Documentou `ticket_medio` como provisório.
- Documentou `novas_matriculas` como snapshot operacional com semântica final pendente.
- Incluiu `v_inadimplencia` e nota sobre schema de `dados_mensais`.
- Preserva assinatura da função e `SECURITY DEFINER`.
- Não tenta escrever `faturamento_estimado` / `saldo_liquido`.

## Bloqueadores restantes

### 1. Ticket médio continua sendo persistido como provisório

A migration calcula e grava `ticket_medio` em `dados_mensais`, mas o próprio arquivo diz que a fórmula é provisória e pendente de validação nominal.

Se é provisório, não deve entrar em migration de produção nem ser persistido em fechamento.

Opções:
- manter fórmula atual de ticket até validação nominal; ou
- separar ticket médio em outra migration após comparação antiga vs nova; ou
- entregar SQL comparativo nominal antes de aplicar.

### 2. `novas_matriculas` continua pendente de decisão semântica

O arquivo diz que a definição final evento comercial vs snapshot operacional está pendente, mas a função já grava `novas_matriculas` em `dados_mensais`.

Se está pendente, não deve ir para backfill/fechamento ainda.

Além disso, a query de novas matrículas não filtra `status IN ('ativo','trancado')`. Se for snapshot operacional, deveria filtrar status. Se for evento comercial, deveria estar documentado como evento e talvez vir de fonte/evento apropriado.

### 3. `inadimplencia` segue como TODO perigoso

A função declara `v_inadimplencia := 0`, mas não persiste `inadimplencia` em `dados_mensais`.

O próprio comentário diz:
> Se a coluna dados_mensais.inadimplencia for NOT NULL sem default, adicione-a aqui...

Isso não pode ficar como hipótese em migration executável. Antes de aplicar, Cascade precisa confirmar schema e ajustar o INSERT/UPDATE.

### 4. View altera ticket/MRR/financeiro junto com correção de alunos/matrículas

O escopo principal era corrigir alunos/matrículas/segundo curso/banda. A migration ainda mexe em fórmulas financeiras (`ticket_medio`, `mrr`, `faturamento_previsto`, `faturamento_realizado`) sem fechamento completo da regra financeira por competência.

Recomendação: separar patch estrutural de KPI de alunos/matrículas do patch financeiro.

## O que pode ser aprovado conceitualmente

- Regra de `alunos_ativos` pessoa-level.
- Regra de `alunos_pagantes` pessoa-level por `conta_como_pagante` no snapshot.
- `matriculas_ativas` linha-level.
- `matriculas_banda` linha-level.
- `matriculas_2_curso` excluindo banda/projeto.
- `evasoes` deduplicadas por nome no mês.
- `churn_rate = evasoes / alunos_pagantes`.

## Resposta recomendada ao Windsurf

Pedir V4 ou split da migration:

1. `MIGRACAO_KPI_ALUNOS_MATRICULAS_V4.sql`
   - Corrige apenas ativos, pagantes, matrículas, banda, segundo curso, evasões/churn.
   - Não altera ticket médio/fórmulas financeiras.

2. `MIGRACAO_FINANCEIRO_TICKET_VX.sql`
   - Só depois de validação nominal do ticket, MRR, faturamento previsto/realizado e inadimplência.

3. Confirmar schema de `dados_mensais.inadimplencia` antes de qualquer execução.
