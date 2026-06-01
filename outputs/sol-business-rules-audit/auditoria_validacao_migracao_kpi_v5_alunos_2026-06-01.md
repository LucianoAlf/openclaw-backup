# Auditoria — V5_ALUNOS + validação CG/Maio 2026

Data: 2026-06-01

Arquivos recebidos:
- `/root/.openclaw/media/inbound/MIGRACAO_REGLA_KPI_V5_ALUNOS---e926fa0d-8544-4ed8-814d-111c1eebeada.sql`
- `/root/.openclaw/media/inbound/VALIDACAO_KPI_CG_MAIO2026_V5---055e4380-5fe1-406c-ab30-1905539fa507.sql`

Arquivo corrigido pelo Alfredo para versão aprovável:
- `/root/.openclaw/workspace/outputs/sol-business-rules-audit/MIGRACAO_REGLA_KPI_V5_ALUNOS_ALFREDO_APROVAVEL.sql`

## Veredito curto

- **VALIDACAO_KPI_CG_MAIO2026_V5:** aprovado como SELECT-only para rodar no SQL Editor.
- **MIGRACAO_REGLA_KPI_V5_ALUNOS recebida:** quase aprovada, mas **não executar como está** por um detalhe fora de escopo.
- **MIGRACAO_REGLA_KPI_V5_ALUNOS_ALFREDO_APROVAVEL:** versão que eu aceitaria como candidata técnica, mantendo renovação/reajuste fora do escopo.

## Checagem estática

### Validação V5

- Sem DDL.
- Sem DML.
- Sem `DROP VIEW`.
- Sem `CREATE OR REPLACE`.
- Sem `\set`, `\echo`, `:param`.
- Espera os números corretos de CG/Maio:
  - 496 ativos
  - 470 pagantes
  - 561 matrículas
  - 41 banda
  - 27 segundo curso
  - 23 novas
  - 13 evasões
  - 2,77% churn

**Status:** pode rodar como validação read-only.

### Migration V5 recebida

Pontos corretos:

- Sem `DROP VIEW`.
- Mantém contrato público da view na ordem original.
- Adiciona `matriculas_ativas` no final.
- Não grava `faturamento_estimado` / `saldo_liquido`.
- Não grava `ticket_medio` / `inadimplencia` / `taxa_renovacao` / `reajuste_parcelas`.
- Corrige alunos/matrículas/churn conforme regra canônica.
- Função retorna escopo `ALUNOS_MATRICULAS_ONLY` e `financeiro_alterado=false`.

Bloqueador:

A migration recebeu uma alteração na CTE `renovacoes_mes`, trocando a fonte para `movimentacoes_admin` e recalculando:

- `renovacoes`
- `total_contratos`
- `taxa_renovacao`
- `reajuste_medio`

Isso sai do escopo declarado da V5_ALUNOS, que deveria corrigir apenas alunos/matrículas/evasões/churn.

Além disso, guardrail anterior já dizia: a fonte operacional correta para **reajuste médio** pode ser `movimentacoes_admin`, mas não se deve substituir a CTE inteira de `renovacoes_mes` sem auditar `renovacoes`, `total_contratos` e `taxa_renovacao`. O patch mínimo deveria alterar só `reajuste_medio` em migration separada.

## Correção feita

Criei a versão:

`MIGRACAO_REGLA_KPI_V5_ALUNOS_ALFREDO_APROVAVEL.sql`

Diferença principal:

- mantém `renovacoes_mes` preservado como contrato atual/legado;
- deixa correção de `reajuste_medio` via `movimentacoes_admin` para patch separado;
- mantém V5_ALUNOS estritamente dentro do escopo alunos/matrículas/evasões/churn.

## Resposta recomendada ao Windsurf

```text
A validação V5 está aprovada como SELECT-only e pode ser rodada no SQL Editor.

A migration V5_ALUNOS ficou quase correta, mas ainda não deve ser executada como está.

Motivo: ela trocou a CTE renovacoes_mes para usar movimentacoes_admin e passou a recalcular renovacoes, total_contratos, taxa_renovacao e reajuste_medio. Isso está fora do escopo da V5_ALUNOS.

A V5_ALUNOS deve corrigir somente ativos, pagantes, matrículas, banda, segundo curso, novas, evasões e churn. Renovação/reajuste fica para patch separado.

Use a versão corrigida mantendo renovacoes_mes como contrato atual/legado, ou crie uma V5.1_ALUNOS sem mexer em renovação/reajuste.

Depois de rodar a validação SELECT-only e confirmar 496/470/561/41/27/23/13/2,77%, podemos aprovar a migration de alunos como candidata técnica. Ainda assim, execução em produção só com aprovação explícita do Alf.
```

## Status final

- `VALIDACAO_KPI_CG_MAIO2026_V5`: **APROVADO PARA RODAR READ-ONLY**.
- `MIGRACAO_REGLA_KPI_V5_ALUNOS` recebida: **NÃO EXECUTAR COMO ESTÁ**.
- `MIGRACAO_REGLA_KPI_V5_ALUNOS_ALFREDO_APROVAVEL`: **candidata técnica aprovada, pendente validação SELECT-only e aprovação explícita do Alf antes de execução**.
