# Auditoria — MIGRACAO_REGLA_KPI_V2 bab6c927

Data: 2026-06-01
Arquivo: `/root/.openclaw/media/inbound/MIGRACAO_REGLA_KPI_V2---bab6c927-0a99-43ae-83f6-dab634dda7aa.sql`

## Veredito

**Não aprovar / não executar ainda.**

A migration acerta parte importante das regras de matrícula, mas ainda mexe em pontos não fechados e mantém riscos estruturais.

## Pontos corretos

- `matriculas_banda` por linha com `cursos.is_projeto_banda=true`.
- `matriculas_2_curso` por linha com `is_segundo_curso=true AND COALESCE(is_projeto_banda,false)=false`.
- `recalcular_dados_mensais` preserva assinatura e `SECURITY DEFINER`.
- Não tenta inserir/atualizar `faturamento_estimado` e `saldo_liquido` em `dados_mensais`.
- Snapshot base usa status + data matrícula + data saída.

## Bloqueadores

1. `DROP VIEW IF EXISTS vw_kpis_gestao_mensal` continua na migration. Preferir `CREATE OR REPLACE VIEW` sem drop, salvo justificativa com dependências.

2. Regra de `alunos_ativos` está diferente entre view e função:
   - View: `COUNT(DISTINCT sb.nome) FILTER (WHERE is_segundo_curso IS NULL OR is_segundo_curso=false)`.
   - Função: `COUNT(DISTINCT a.nome)`.
   Padronizar.

3. Ticket médio ainda não está validado. A migration muda para média da soma por pessoa, mas esse KPI não foi fechado nominalmente contra o card atual (`385.59`/`386`). Não mexer em ticket médio nesse patch ou entregar comparação nominal.

4. `novas_matriculas` segue sem decisão semântica final: evento comercial vs snapshot operacional. Para CG/Maio fecha 23, mas precisa documentar e decidir antes de backfill.

5. A view calcula apenas snapshot vivo/mês corrente para alunos. Isso precisa estar explícito: `vw_kpis_gestao_mensal` não deve ser usada como verdade histórica de meses fechados.

6. Conferir schema de `dados_mensais`: a função omite `inadimplencia`. Se a coluna for `NOT NULL` sem default, o insert/upsert falha. Confirmar antes.

## Recomendação

Pedir V3 da migration:
- sem `DROP VIEW`;
- padronizando `alunos_ativos` entre view e função;
- sem alterar ticket médio ainda, ou com comparação nominal aprovada;
- mantendo `matriculas_banda=41` e `matriculas_2_curso=27`;
- documentando explicitamente mês corrente vs histórico;
- validando schema de `dados_mensais` antes de executar.
