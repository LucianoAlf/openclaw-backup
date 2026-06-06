# Prompt para Cascade/Windsurf — Auditoria Cruzada de Schema LA Report

Você vai atuar como auditor técnico do LA Music Performance Report/Sol.

## Contexto

Foi gerado um inventário SELECT-only do banco real com:

- 193 tabelas;
- 60 views;
- 194 funções/RPCs;
- 17 crons;
- dependências entre views/tabelas;
- cruzamento com referências no código/migrations.

Arquivos de entrada:

- `relatorio-auditoria-inicial-schema-la-report.md`
- `schema-audit-raw.json`
- `objects.json`
- `views.json`
- `functions.json`
- `dependencies.json`
- `constraints.json`
- `triggers.json`
- `columns.json`
- `cron_jobs.json`

## Regra de segurança

NÃO execute nada no banco.

Proibido:

- `ALTER`
- `CREATE`
- `DROP`
- `UPDATE`
- `DELETE`
- `INSERT`
- migration
- backfill
- cron
- produção

Esta etapa é somente classificação documental e análise de risco.

## Regra de negócio

Use a skill/regras canônicas `sol-la-report-business-rules`.

Ordem de autoridade:

1. Regra validada pelo Alf;
2. regra canônica da skill;
3. SELECT-only no banco real;
4. código atual como evidência;
5. documento antigo = legado;
6. código divergente = possível bug.

## Objetivo

Classificar objetos do banco em grupos:

1. **ATIVO / CANÔNICO** — usado e alinhado às regras.
2. **ATIVO MAS SUSPEITO** — usado, mas contém regra potencialmente errada.
3. **LEGADO CONGELADO** — manter por histórico/compatibilidade, mas não usar em regra nova.
4. **LEGADO QUEBRANDO REGRA** — objeto ainda usado e causando divergência.
5. **CANDIDATO A DEPRECAR** — sem uso aparente, mas exige validação humana antes.
6. **LIXO TÉCNICO PROVÁVEL** — backup/debug/temp sem uso, mas ainda NÃO apagar.
7. **BLOQUEADO / PRECISA SELECT EXTRA** — não dá para concluir.

## Prioridade alta

Analise primeiro objetos ligados a:

- `evasoes_v2`
- `renovacoes`
- `dados_mensais`
- `movimentacoes`
- `movimentacoes_admin`
- `vw_kpis_gestao_mensal`
- `vw_dashboard_unidade`
- `vw_kpis_retencao_mensal`
- `vw_kpis_professor_mensal`
- `vw_kpis_comercial_mensal`
- funções `recalcular_dados_mensais` e `snapshot_dados_mensais`
- crons relacionados a sync/snapshot/relatórios

## Entrega esperada

Gerar um relatório em Markdown com:

1. Resumo executivo.
2. Tabela de objetos críticos.
3. Tabela de objetos suspeitos.
4. Tabela de candidatos a deprecar.
5. Views que provavelmente quebram regra de negócio.
6. RPCs/funções sensíveis.
7. Crons que podem contaminar dados.
8. SELECTs extras necessários para confirmar uso/risco.
9. Plano faseado:
   - Fase 1: documentação/flags;
   - Fase 2: SELECT-only por objeto crítico;
   - Fase 3: staging;
   - Fase 4: produção com aprovação.

## Restrições

Não proponha apagar nada agora.

Não proponha executar migration agora.

Quando recomendar deprecar, escreva:

> candidato a deprecar após validação, backup e aprovação explícita do Alf.

## Frase-guia

Documento antigo divergente = legado. Código divergente = possível bug. Regra validada pelo Alf = canônica.
