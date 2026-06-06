# Auditoria inicial SELECT-only — LA Report schema

> Gerado por Alfredo. Somente leitura: inventário via `executar_query_auditoria` + cruzamento com repo local. Não houve DDL/DML.

## Resumo

- Objetos públicos: **253** (table: 193, view: 60).
- Views: **60**.
- Funções/RPCs: **194**.
- Crons ativos/listados: **17**.

## Primeiros achados importantes

- Existem objetos legados/suspeitos que ainda aparecem no banco real, incluindo `evasoes_v2`, objetos `*_v2`, tabelas/logs/debugs e snapshots.
- Algumas views ainda contêm padrões de risco para regra de negócio: `evasoes_v2`, `COUNT(*)`, `data_contato`, `renovacoes`, `dados_mensais`, `classificacao`, filtros por nome como `canto coral`.
- Há crons ativos com comandos SQL/HTTP; antes de mudar qualquer regra de snapshot ou sync, eles precisam entrar no mapa de dependências.
- O objetivo NÃO é apagar: é classificar em **ativo**, **legado congelado**, **legado usado por compatibilidade**, **suspeito**, **candidato a deprecar**.

## Maiores tabelas por tamanho

| Objeto | Tipo | Linhas estimadas | Tamanho | Refs código | Consumida por views |
|---|---:|---:|---:|---:|---|
| `audit_log` | table | 41434 | 108 MB | 39 |  |
| `aulas_emusys` | table | 26717 | 10224 kB | 71 | vw_turmas_professor_periodo |
| `leads_automacao_log` | table | 28205 | 9568 kB | 27 |  |
| `aluno_presenca` | table | 30160 | 9080 kB | 61 | vw_turmas_professor_periodo |
| `leads` | table | 7047 | 4456 kB | 1422 | vw_funil_conversao_mensal, vw_kpis_comercial_mensal, vw_kpis_gestao_mensal, vw_kpis_professor_historico, vw_kpis_professor_mensal |
| `alunos` | table | 1505 | 3040 kB | 3960 | vw_alertas_inteligentes, vw_aluno_sucesso_lista, vw_alunos_ativos, vw_contagem_alunos, vw_dashboard_unidade |
| `automacao_log` | table | 3540 | 2808 kB | 97 |  |
| `mensagens_campanha` | table | 2060 | 2296 kB | 32 |  |
| `conversas_campanha` | table | 1067 | 880 kB | 28 |  |
| `movimentacoes_admin` | table | 1332 | 744 kB | 263 | vw_alertas_inteligentes, vw_dashboard_unidade, vw_evasoes_motivos, vw_evasoes_professores, vw_evasoes_resumo |
| `campanha_contatos` | table | 1349 | 608 kB | 17 |  |
| `webhook_debug_log` | table | 317 | 536 kB | 1 |  |
| `alunos_historico` | table | 1421 | 528 kB | 96 | vw_dashboard_unidade, vw_distribuicao_permanencia, vw_ltv_por_categoria, vw_ltv_por_unidade, vw_ltv_rede |
| `dados_comerciais` | table | 92 | 472 kB | 93 | vw_alertas_inteligentes, vw_kpis_comercial_historico |
| `automacao_invariantes` | table | 621 | 384 kB | 73 |  |

## Views com sinais de risco de regra de negócio

| View | Sinais | Fontes/dependências | Refs código |
|---|---|---|---:|
| `vw_alertas_inteligentes` | `count(*)`, `renovacoes`, `dados_mensais` | `alunos`, `dados_comerciais`, `dados_mensais`, `metas_kpi`, `movimentacoes_admin`, `professores_unidades`, `renovacoes`, `unidades` | 10 |
| `vw_aluno_sucesso_lista` | `count(*)` | `aluno_acoes`, `aluno_feedback_professor`, `aluno_metas`, `alunos`, `cursos`, `professores`, `unidades` | 8 |
| `vw_aluno_sucesso_resumo` | `count(*)` | `vw_aluno_sucesso_lista` | 6 |
| `vw_alunos_ativos` | `classificacao` | `alunos`, `cursos`, `professores`, `tipos_matricula`, `unidades` | 4 |
| `vw_consolidado_anual` | `dados_mensais` | `dados_mensais` | 14 |
| `vw_contagem_alunos` | `count(*)`, `classificacao` | `alunos`, `tipos_matricula`, `unidades` | 4 |
| `vw_dashboard_unidade` | `count(*)`, `renovacoes`, `dados_mensais` | `alunos`, `alunos_historico`, `dados_mensais`, `movimentacoes_admin`, `tipos_matricula`, `unidades` | 50 |
| `vw_distribuicao_permanencia` | `count(*)` | `alunos_historico` | 2 |
| `vw_evasao_por_motivo` | `count(*)` | `motivos_saida`, `movimentacoes`, `unidades` | 1 |
| `vw_evasao_por_tipo` | `count(*)` | `movimentacoes`, `tipos_saida`, `unidades` | 1 |
| `vw_evasoes_motivos` | `count(*)` | `motivos_saida`, `movimentacoes_admin`, `unidades` | 7 |
| `vw_evasoes_professores` | `count(*)` | `motivos_saida`, `movimentacoes_admin`, `professores`, `unidades` | 6 |
| `vw_evasoes_resumo` | `count(*)`, `renovacoes` | `motivos_saida`, `movimentacoes_admin`, `unidades` | 7 |
| `vw_farmer_aniversariantes_hoje` | `classificacao` | `alunos`, `cursos`, `professores` | 3 |
| `vw_farmer_novos_matriculados` | `classificacao` | `alunos`, `cursos`, `professores` | 3 |
| `vw_farmer_resumo_alertas` | `count(*)`, `renovacoes` | `unidades`, `vw_farmer_aniversariantes_hoje`, `vw_farmer_inadimplentes`, `vw_farmer_novos_matriculados`, `vw_farmer_renovacoes_proximas` | 2 |
| `vw_fator_demanda_professor` | `count(*)` | `alunos`, `cursos`, `professores` | 2 |
| `vw_funil_conversao_mensal` | `count(*)`, `data_contato` | `leads`, `unidades` | 5 |
| `vw_kpis_comercial_mensal` | `count(*)`, `data_contato` | `alunos`, `leads`, `unidades` | 32 |
| `vw_kpis_gestao_mensal` | `count(*)`, `data_contato`, `renovacoes`, `canto coral` | `alunos`, `cursos`, `leads`, `movimentacoes_admin`, `renovacoes`, `tipos_matricula`, `unidades` | 144 |
| `vw_kpis_mensais` | `renovacoes` | `movimentacoes`, `unidades` | 7 |
| `vw_kpis_professor_completo` | `count(*)` | `alunos`, `professores` | 33 |
| `vw_kpis_professor_historico` | `data_contato` | `experimentais_mensal_unidade`, `leads`, `professores` | 8 |
| `vw_kpis_professor_mensal` | `count(*)`, `data_contato`, `renovacoes` | `alunos`, `cursos`, `leads`, `movimentacoes_admin`, `professores`, `vw_turmas_implicitas` | 29 |
| `vw_kpis_professor_por_unidade` | `count(*)` | `alunos`, `professores` | 0 |
| `vw_kpis_retencao_mensal` | `count(*)`, `renovacoes` | `alunos`, `movimentacoes_admin`, `tipos_matricula`, `unidades` | 52 |
| `vw_leads_comercial` | `data_contato` | `canais_origem`, `cursos`, `leads`, `professores`, `unidades` | 0 |
| `vw_leads_por_canal` | `count(*)`, `data_contato` | `canais_origem`, `leads`, `unidades` | 4 |
| `vw_ltv_por_categoria` | `count(*)` | `alunos_historico` | 1 |
| `vw_ltv_por_unidade` | `count(*)` | `alunos_historico`, `unidades` | 5 |
| `vw_ltv_rede` | `count(*)` | `alunos_historico` | 2 |
| `vw_ltv_unidade` | `count(*)` | `alunos`, `tipos_matricula`, `unidades` | 3 |
| `vw_matriculas_por_canal` | `count(*)` | `canais_origem`, `movimentacoes`, `unidades` | 3 |
| `vw_metas_vs_realizado` | `renovacoes` | `metas`, `relatorios_diarios`, `unidades` | 5 |
| `vw_motivos_nao_matricula` | `count(*)`, `data_contato` | `leads`, `unidades` | 3 |
| `vw_movimentacoes_mensal` | `count(*)` | `movimentacoes`, `unidades` | 1 |
| `vw_performance_professor_experimental` | `count(*)`, `data_contato` | `leads`, `professores`, `unidades` | 7 |
| `vw_professores_performance_atual` | `count(*)`, `data_contato` | `alunos`, `experimentais_professor_mensal`, `leads`, `movimentacoes_admin`, `professores`, `professores_unidades`, `unidades` | 7 |
| `vw_ranking_professores_evasoes` | `renovacoes` | `professores_performance` | 8 |
| `vw_ranking_unidades` | `dados_mensais` | `dados_mensais`, `unidades` | 5 |
| `vw_renovacoes_mensal` | `count(*)`, `renovacoes` | `renovacoes`, `unidades` | 2 |
| `vw_renovacoes_pendentes` | `count(*)`, `renovacoes` | `alunos`, `renovacoes`, `unidades` | 6 |
| `vw_renovacoes_proximas` | `classificacao` | `alunos`, `cursos`, `professores`, `unidades` | 7 |
| `vw_sazonalidade` | `dados_mensais` | `dados_mensais`, `unidades` | 15 |
| `vw_taxa_crescimento_professor` | `count(*)`, `renovacoes` | `alunos`, `movimentacoes_admin`, `professores`, `vw_fator_demanda_professor` | 5 |
| `vw_totais_unidade_performance` | `renovacoes` | `professores_performance` | 5 |
| `vw_turmas_implicitas` | `count(*)` | `alunos`, `cursos`, `professores`, `salas`, `turmas_explicitas`, `unidades` | 33 |
| `vw_unidade_anual` | `dados_mensais` | `dados_mensais`, `unidades` | 15 |

## Objetos suspeitos/legados por nome ou isolamento

| Objeto | Tipo | Linhas estimadas | Tamanho | Flags | Refs código | Consumidores view |
|---|---|---:|---:|---|---:|---|
| `aluno_acoes` | table | 0 | 32 kB | usado_por_views:1 | 12 | vw_aluno_sucesso_lista |
| `aluno_feedback_professor` | table | 0 | 48 kB | usado_por_views:1 | 20 | vw_aluno_sucesso_lista |
| `aluno_metas` | table | 0 | 24 kB | usado_por_views:1 | 12 | vw_aluno_sucesso_lista |
| `aluno_presenca` | table | 30160 | 9080 kB | usado_por_views:1 | 61 | vw_turmas_professor_periodo |
| `alunos` | table | 1505 | 3040 kB | usado_por_views:27 | 3960 | vw_alertas_inteligentes, vw_aluno_sucesso_lista, vw_alunos_ativos, vw_contagem_alunos, vw_dashboard_unidade |
| `alunos_health_score_historico` | table | 0 | 32 kB | nome_suspeito, sem_ref_codigo_sem_view | 0 |  |
| `alunos_historico` | table | 1421 | 528 kB | nome_suspeito, usado_por_views:5 | 96 | vw_dashboard_unidade, vw_distribuicao_permanencia, vw_ltv_por_categoria, vw_ltv_por_unidade, vw_ltv_rede |
| `alunos_turmas` | table | 0 | 48 kB | usado_por_views:1 | 0 | vw_turmas_completa |
| `audit_log` | table | 41434 | 108 MB | nome_suspeito | 39 |  |
| `aulas_emusys` | table | 26717 | 10224 kB | usado_por_views:1 | 71 | vw_turmas_professor_periodo |
| `automacao_log` | table | 3540 | 2808 kB | nome_suspeito | 97 |  |
| `bi_ai_query_playbooks` | table | 19 | 104 kB | sem_ref_codigo_sem_view | 0 |  |
| `bi_query_templates_lamusic` | table | 4 | 32 kB | nome_suspeito | 4 |  |
| `canais_origem` | table | 11 | 56 kB | usado_por_views:3 | 107 | vw_leads_comercial, vw_leads_por_canal, vw_matriculas_por_canal |
| `catalogo_treinamentos` | table | 6 | 32 kB | nome_suspeito | 14 |  |
| `colaboradores` | table | 12 | 96 kB | usado_por_views:1 | 140 | vw_farmer_checklist_alertas |
| `crm_lead_historico` | table | 86 | 96 kB | nome_suspeito | 11 |  |
| `crm_metas_andreza` | table | 3 | 64 kB | sem_ref_codigo_sem_view | 0 |  |
| `crm_templates_whatsapp` | table | 8 | 48 kB | nome_suspeito | 7 |  |
| `cursos` | table | 40 | 96 kB | usado_por_views:14 | 1052 | vw_aluno_sucesso_lista, vw_alunos_ativos, vw_farmer_aniversariantes_hoje, vw_farmer_inadimplentes, vw_farmer_novos_matriculados |
| `dados_comerciais` | table | 92 | 472 kB | usado_por_views:2 | 93 | vw_alertas_inteligentes, vw_kpis_comercial_historico |
| `dados_mensais` | table | 124 | 120 kB | objeto_critico/legado_conhecido, usado_por_views:6 | 351 | vw_alertas_inteligentes, vw_consolidado_anual, vw_dashboard_unidade, vw_ranking_unidades, vw_sazonalidade |
| `emusys_sync_log` | table | 745 | 368 kB | nome_suspeito | 17 |  |
| `evasoes_backup_20260215` | table | 677 | 136 kB | nome_suspeito, sem_ref_codigo_sem_view | 0 |  |
| `evasoes_legacy_backup` | table | 677 | 136 kB | nome_suspeito, sem_ref_codigo_sem_view | 0 |  |
| `evasoes_v2` | table | 740 | 360 kB | nome_suspeito, objeto_critico/legado_conhecido | 113 |  |
| `evasoes_v2_backup` | table | 740 | 136 kB | nome_suspeito, sem_ref_codigo_sem_view | 0 |  |
| `experimentais_mensal_unidade` | table | 67 | 72 kB | usado_por_views:1 | 12 | vw_kpis_professor_historico |
| `experimentais_professor_mensal` | table | 140 | 96 kB | usado_por_views:1 | 28 | vw_professores_performance_atual |
| `farmer_checklist_items` | table | 30 | 128 kB | usado_por_views:1 | 13 | vw_farmer_checklist_alertas |
| `farmer_checklist_templates` | table | 5 | 64 kB | nome_suspeito | 10 |  |
| `farmer_checklists` | table | 5 | 112 kB | usado_por_views:1 | 24 | vw_farmer_checklist_alertas |
| `farmer_templates` | table | 14 | 64 kB | nome_suspeito | 4 |  |
| `historico_pagamentos` | table | 0 | 48 kB | nome_suspeito | 1 |  |
| `leads` | table | 7047 | 4456 kB | usado_por_views:10 | 1422 | vw_funil_conversao_mensal, vw_kpis_comercial_mensal, vw_kpis_gestao_mensal, vw_kpis_professor_historico, vw_kpis_professor_mensal |
| `leads_automacao_log` | table | 28205 | 9568 kB | nome_suspeito | 27 |  |
| `leads_backup_flags_20260601` | table | 17 | 8192 bytes | nome_suspeito, sem_ref_codigo_sem_view | 0 |  |
| `leads_diarios_backup` | table | 100 | 40 kB | nome_suspeito | 2 |  |
| `loja_reservas` | table | 2 | 80 kB | sem_ref_codigo_sem_view | 0 |  |
| `metas` | table | 7 | 104 kB | usado_por_views:2 | 790 | vw_metas_vs_realizado, vw_projecao_metas |
| `metas_kpi` | table | 596 | 344 kB | usado_por_views:1 | 26 | vw_alertas_inteligentes |
| `metas_legado` | table | 6 | 72 kB | sem_ref_codigo_sem_view | 0 |  |
| `motivos_saida` | table | 15 | 72 kB | usado_por_views:5 | 68 | vw_evasao_por_motivo, vw_evasoes_motivos, vw_evasoes_professores, vw_evasoes_resumo, vw_movimentacoes_recentes |
| `movimentacoes` | table | 0 | 144 kB | usado_por_views:7 | 71 | vw_evasao_por_motivo, vw_evasao_por_tipo, vw_evolucao_alunos, vw_kpis_mensais, vw_matriculas_por_canal |
| `movimentacoes_admin` | table | 1332 | 744 kB | usado_por_views:10 | 263 | vw_alertas_inteligentes, vw_dashboard_unidade, vw_evasoes_motivos, vw_evasoes_professores, vw_evasoes_resumo |
| `notificacao_log` | table | 9 | 160 kB | nome_suspeito | 13 |  |
| `professor_360_ocorrencias_log` | table | 75 | 136 kB | nome_suspeito | 27 |  |
| `professores` | table | 57 | 144 kB | usado_por_views:21 | 1362 | vw_aluno_sucesso_lista, vw_alunos_ativos, vw_evasoes_professores, vw_farmer_aniversariantes_hoje, vw_farmer_inadimplentes |
| `professores_performance` | table | 125 | 120 kB | usado_por_views:2 | 40 | vw_ranking_professores_evasoes, vw_totais_unidade_performance |
| `professores_sync_log` | table | 8 | 80 kB | nome_suspeito | 12 |  |
| `professores_unidades` | table | 77 | 128 kB | usado_por_views:2 | 56 | vw_alertas_inteligentes, vw_professores_performance_atual |
| `programa_fideliza_historico` | table | 0 | 32 kB | nome_suspeito | 8 |  |
| `programa_matriculador_historico` | table | 0 | 40 kB | nome_suspeito | 4 |  |
| `projeto_log_alteracoes` | table | 67 | 136 kB | nome_suspeito | 1 |  |
| `projeto_tipo_fases_template` | table | 34 | 96 kB | nome_suspeito | 25 |  |
| `projeto_tipo_tarefas_template` | table | 80 | 64 kB | nome_suspeito | 8 |  |
| `relatorios_diarios` | table | 0 | 48 kB | usado_por_views:3 | 51 | vw_alertas, vw_metas_vs_realizado, vw_projecao_metas |
| `renovacoes` | table | 383 | 264 kB | objeto_critico/legado_conhecido, usado_por_views:4 | 386 | vw_alertas_inteligentes, vw_kpis_gestao_mensal, vw_renovacoes_mensal, vw_renovacoes_pendentes |
| `salas` | table | 53 | 112 kB | usado_por_views:2 | 200 | vw_turmas_completa, vw_turmas_implicitas |
| `templates_cenario` | table | 3 | 32 kB | nome_suspeito | 1 |  |
| `templates_cenario_unidade` | table | 6 | 48 kB | nome_suspeito | 2 |  |
| `templates_meta` | table | 30 | 336 kB | nome_suspeito | 10 |  |
| `tipos_matricula` | table | 5 | 64 kB | usado_por_views:6 | 184 | vw_alunos_ativos, vw_contagem_alunos, vw_dashboard_unidade, vw_kpis_gestao_mensal, vw_kpis_retencao_mensal |
| `tipos_saida` | table | 4 | 64 kB | usado_por_views:1 | 37 | vw_evasao_por_tipo |
| `transferencias_mila` | table | 0 | 32 kB | sem_ref_codigo_sem_view | 0 |  |
| `turmas` | table | 0 | 72 kB | usado_por_views:1 | 353 | vw_turmas_completa |
| `turmas_explicitas` | table | 404 | 224 kB | usado_por_views:1 | 26 | vw_turmas_implicitas |
| `turmas_historico` | table | 2 | 128 kB | nome_suspeito | 2 |  |
| `unidades` | table | 3 | 64 kB | usado_por_views:40 | 1029 | vw_alertas, vw_alertas_inteligentes, vw_aluno_sucesso_lista, vw_alunos_ativos, vw_contagem_alunos |
| `webhook_debug_log` | table | 317 | 536 kB | nome_suspeito | 1 |  |
| `vw_aluno_sucesso_lista` | view | 0 | 0 bytes | usado_por_views:1 | 8 | vw_aluno_sucesso_resumo |
| `vw_farmer_aniversariantes_hoje` | view | 0 | 0 bytes | usado_por_views:1 | 3 | vw_farmer_resumo_alertas |
| `vw_farmer_inadimplentes` | view | 0 | 0 bytes | usado_por_views:1 | 2 | vw_farmer_resumo_alertas |
| `vw_farmer_novos_matriculados` | view | 0 | 0 bytes | usado_por_views:1 | 3 | vw_farmer_resumo_alertas |
| `vw_farmer_renovacoes_proximas` | view | 0 | 0 bytes | usado_por_views:1 | 3 | vw_farmer_resumo_alertas |
| `vw_fator_demanda_professor` | view | 0 | 0 bytes | usado_por_views:1 | 2 | vw_taxa_crescimento_professor |
| `vw_kpis_comercial_historico` | view | 0 | 0 bytes | nome_suspeito | 25 |  |
| `vw_kpis_professor_historico` | view | 0 | 0 bytes | nome_suspeito | 8 |  |
| `vw_kpis_professor_por_unidade` | view | 0 | 0 bytes | view_sem_ref_codigo | 0 |  |
| `vw_leads_comercial` | view | 0 | 0 bytes | view_sem_ref_codigo | 0 |  |

## Tabelas sem referência no código nem em views — NÃO apagar, só investigar

| Tabela | Linhas estimadas | Tamanho | Comentário |
|---|---:|---:|---|
| `alunos_health_score_historico` | 0 | 32 kB |  |
| `bi_ai_query_playbooks` | 19 | 104 kB |  |
| `crm_metas_andreza` | 3 | 64 kB |  |
| `evasoes_backup_20260215` | 677 | 136 kB |  |
| `evasoes_legacy_backup` | 677 | 136 kB |  |
| `evasoes_v2_backup` | 740 | 136 kB |  |
| `leads_backup_flags_20260601` | 17 | 8192 bytes |  |
| `loja_reservas` | 2 | 80 kB |  |
| `metas_legado` | 6 | 72 kB | BACKUP: Tabela metas original (estrutura anual). Dados migrados para nova tabela metas em 2026-01-16. Pode ser removida após 30 dias de validação. |
| `transferencias_mila` | 0 | 32 kB |  |

## Views sem referência direta no código — podem ser API/legado, investigar

| View | Fontes |
|---|---|
| `vw_kpis_professor_por_unidade` | `alunos`, `professores` |
| `vw_leads_comercial` | `canais_origem`, `cursos`, `leads`, `professores`, `unidades` |
| `vw_professores_carteira_resumo` | `alunos`, `professores` |
| `vw_turmas_professor_periodo` | `aluno_presenca`, `alunos`, `aulas_emusys` |

## Próxima etapa recomendada

1. Enviar este relatório ao Cascade/Windsurf e pedir classificação **sem DDL/DML**.
2. Para cada objeto suspeito, preencher: dono funcional, uso atual, dependências, risco, proposta (`manter`, `legado congelado`, `deprecar depois`, `corrigir regra`, `remover só após backup/aprovação`).
3. Priorizar objetos que quebram regra de negócio: `evasoes_v2`, `renovacoes`, `dados_mensais`, views de gestão/retencão/professor/comercial, funções de snapshot/recalculo.
4. Só depois desenhar migrations em staging. Produção segue travada.

## Arquivos brutos

- `schema-audit-raw.json`
- `objects.json`, `views.json`, `functions.json`, `dependencies.json`, `constraints.json`, `triggers.json`, `columns.json`, `cron_jobs.json`