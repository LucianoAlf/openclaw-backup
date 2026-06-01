# Auditoria — MIGRACAO_REGLA_KPI_V5_ALUNOS 5683b0d0

Data: 2026-06-01
Arquivo: `/root/.openclaw/media/inbound/MIGRACAO_REGLA_KPI_V5_ALUNOS---5683b0d0-2d1d-49f0-abd8-705381c1e8a5.sql`

## Veredito

**Aprovada como candidata técnica da V5_ALUNOS.**

Ainda não significa autorização de execução em produção. O próximo passo seguro é:

1. rodar primeiro `VALIDACAO_KPI_CG_MAIO2026_V5` SELECT-only;
2. confirmar retorno `496 / 470 / 561 / 41 / 27 / 23 / 13 / 2,77%`;
3. só depois pedir aprovação explícita do Alf para aplicar migration/RPC.

## Comparação com versão aprovada do Alfredo

Comparei com:

`outputs/sol-business-rules-audit/MIGRACAO_REGLA_KPI_V5_ALUNOS_ALFREDO_APROVAVEL.sql`

Diferença real, ignorando quebra de linha/CRLF:

```diff
-- Renovação/reajuste preservados como estavam no contrato atual.
--- ATENÇÃO: V5_ALUNOS não deve trocar a fonte de renovação/reajuste.
--- A correção de reajuste via movimentacoes_admin deve ficar em patch separado.
+-- Fora de escopo da V5_ALUNOS — não alterar.
```

Ou seja: **mudou só comentário**. O SQL efetivo está alinhado.

## Checagem estática

- Sem `DROP VIEW`.
- Sem `\set`, `\echo`, `:param`.
- Não grava `faturamento_estimado` / `saldo_liquido`.
- Não grava `ticket_medio`.
- Não grava `inadimplencia`.
- Mantém `renovacoes_mes` usando tabela `renovacoes`, sem trocar para `movimentacoes_admin`.
- Mantém financeiro legado isolado.
- Função grava apenas:
  - `alunos_ativos`
  - `alunos_pagantes`
  - `matriculas_ativas`
  - `matriculas_banda`
  - `matriculas_2_curso`
  - `novas_matriculas`
  - `evasoes`
  - `churn_rate`
  - `updated_at`

## Ressalva operacional

A migration contém DDL e DML:

- `CREATE OR REPLACE VIEW`
- `CREATE OR REPLACE FUNCTION`
- `INSERT INTO ... ON CONFLICT DO UPDATE` dentro da função

Portanto **não é read-only** e não deve ser rodada sem aprovação explícita.

## Resposta recomendada ao Windsurf

```text
Agora sim. Esta V5_ALUNOS está alinhada com a versão aprovada conceitualmente.

Ela removeu o problema anterior da CTE renovacoes_mes e manteve renovação/reajuste fora do escopo.

A validação SELECT-only deve rodar primeiro. Se retornar:
496 ativos, 470 pagantes, 561 matrículas, 41 banda, 27 segundo curso, 23 novas, 13 evasões e 2,77% churn,
esta migration fica aprovada como candidata técnica.

Não executar em produção nem rodar recalcular_dados_mensais ainda sem aprovação explícita do Alf.
```
