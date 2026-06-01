# Supabase LA Report — inventário inicial via PostgREST OpenAPI

- Definitions total: 251
- Views `vw_*`: 60
- Tabelas/outros expostos: 191

## Views candidatas

### `vw_alertas`
- colunas (5): tipo_alerta, unidade, descricao, valor, data_referencia
### `vw_alertas_inteligentes`
- colunas (10): tipo_alerta, severidade, unidade_id, unidade_nome, quantidade, descricao, detalhe, valor_atual, valor_meta, data_referencia
### `vw_aluno_sucesso_lista`
- colunas (32): id, nome, unidade_id, unidade_codigo, unidade_nome, professor_atual_id, professor_nome, curso_id, curso_nome, tempo_permanencia_meses, status_pagamento, valor_parcela, percentual_presenca, data_matricula, dia_aula, horario_aula, modalidade, status, fase_jornada, health_score_numerico, health_status, health_score_updated_at, ultimo_feedback, ultimo_feedback_obs, ultimo_feedback_data, ultimo_feedback_professor_id, total_acoes, metas_ativas, responsavel_nome, responsavel_telefone, ...
### `vw_aluno_sucesso_resumo`
- colunas (23): unidade_id, unidade_codigo, unidade_nome, total_alunos, saudaveis, atencao, criticos, sem_score, onboarding, consolidacao, encantamento, renovacao, pagamento_em_dia, pagamento_atrasado, pagamento_inadimplente, feedback_verde, feedback_amarelo, feedback_vermelho, sem_feedback, media_tempo_permanencia, ticket_medio, health_score_medio, presenca_media
### `vw_alunos_ativos`
- colunas (16): id, nome, classificacao, idade_atual, unidade, unidade_codigo, professor, curso, tipo_matricula, entra_ticket_medio, conta_como_pagante, valor_parcela, tempo_permanencia_meses, data_matricula, data_fim_contrato, status
### `vw_consolidado_anual`
- colunas (10): ano, alunos_dezembro, total_matriculas, total_evasoes, churn_medio, ticket_medio, renovacao_media, permanencia_media, inadimplencia_media, faturamento_total
### `vw_contagem_alunos`
- colunas (8): unidade, unidade_codigo, classificacao, status, total, pagantes, ticket_medio, tempo_medio_meses
### `vw_dashboard_unidade`
- colunas (14): unidade_id, unidade_nome, codigo, alunos_ativos, alunos_pagantes, ticket_medio, mrr, matriculas_mes, evasoes_mes, churn_rate, taxa_renovacao, inadimplencia_pct, tempo_permanencia, reajuste_medio
### `vw_distribuicao_permanencia`
- colunas (3): faixa, quantidade, percentual
### `vw_evasao_por_motivo`
- colunas (4): unidade, motivo, quantidade, percentual
### `vw_evasao_por_tipo`
- colunas (4): unidade, tipo_saida, quantidade, percentual
### `vw_evasoes_motivos`
- colunas (5): motivo_categoria, unidade, quantidade, mrr_perdido, percentual
### `vw_evasoes_professores`
- colunas (6): unidade, professor, total_evasoes, mrr_perdido, ticket_medio, motivo_principal
### `vw_evasoes_resumo`
- colunas (12): competencia, unidade, total_evasoes, interrompidos, nao_renovacoes, mrr_perdido, ticket_medio_evasao, motivo_financeiro, motivo_horario, motivo_mudanca, motivo_desinteresse, motivo_inadimplencia
### `vw_evolucao_alunos`
- colunas (5): unidade, ano_mes, entradas, saidas, saldo
### `vw_farmer_aniversariantes_hoje`
- colunas (10): aluno_id, aluno_nome, whatsapp, data_nascimento, unidade_id, idade, classificacao, professor_id, professor_nome, instrumento
### `vw_farmer_checklist_alertas`
- colunas (17): checklist_id, titulo, descricao, data_prazo, prioridade, alerta_dias_antes, lembrete_whatsapp, colaborador_id, unidade_id, colaborador_nome, colaborador_apelido, colaborador_whatsapp, total_items, items_concluidos, percentual_progresso, dias_restantes, urgencia
### `vw_farmer_inadimplentes`
- colunas (10): aluno_id, aluno_nome, whatsapp, unidade_id, valor_parcela, status_pagamento, professor_id, professor_nome, instrumento, dias_atraso
### `vw_farmer_novos_matriculados`
- colunas (13): aluno_id, aluno_nome, whatsapp, unidade_id, data_matricula, valor_parcela, classificacao, idade, professor_id, professor_nome, instrumento, dia_aula, horario_aula
### `vw_farmer_renovacoes_proximas`
- colunas (11): aluno_id, aluno_nome, whatsapp, unidade_id, data_fim_contrato, valor_parcela, professor_id, professor_nome, instrumento, dias_para_vencer, urgencia
### `vw_farmer_resumo_alertas`
- colunas (8): unidade_id, unidade_nome, aniversariantes_hoje, inadimplentes, novos_matriculados, renovacoes_vencidas, renovacoes_urgentes, renovacoes_atencao
### `vw_fator_demanda_professor`
- colunas (6): professor_id, professor_nome, unidade_id, total_alunos, fator_demanda_ponderado, detalhamento_cursos
### `vw_funil_conversao_mensal`
- colunas (13): unidade, ano, mes, ano_mes, total_leads, leads_arquivados, experimentais_agendadas, experimentais_realizadas, faltaram, matriculas, taxa_lead_experimental, taxa_experimental_matricula, taxa_lead_matricula
### `vw_kpis_comercial_historico`
- colunas (17): id, competencia, unidade_nome, unidade_id, ano, mes, total_leads, experimentais_realizadas, novas_matriculas_total, novas_matriculas_lamk, novas_matriculas_emla, ticket_medio_parcelas, ticket_medio_passaporte, faturamento_passaporte, taxa_lead_exp, taxa_exp_mat, taxa_lead_mat
### `vw_kpis_comercial_mensal`
- colunas (16): unidade_id, unidade_nome, ano, mes, total_leads, leads_arquivados, experimentais_agendadas, experimentais_realizadas, faltaram, taxa_showup, novas_matriculas, taxa_conversao_lead_exp, taxa_conversao_exp_mat, taxa_conversao_geral, faturamento_novos, ticket_medio_novos
### `vw_kpis_gestao_mensal`
- colunas (27): unidade_id, unidade_nome, ano, mes, total_alunos_ativos, total_alunos_pagantes, total_bolsistas_integrais, total_bolsistas_parciais, total_banda, total_segundo_curso, ticket_medio, mrr, arr, tempo_permanencia_medio, ltv_medio, inadimplencia_pct, faturamento_previsto, faturamento_realizado, total_leads, experimentais_agendadas, experimentais_realizadas, novas_matriculas, total_evasoes, churn_rate, renovacoes, taxa_renovacao, reajuste_medio
### `vw_kpis_mensais`
- colunas (6): unidade, ano_mes, matriculas, renovacoes, evasoes, transferencias
### `vw_kpis_professor_completo`
- colunas (9): professor_id, professor_nome, carteira_alunos, ticket_medio, media_presenca, taxa_faltas, mrr_carteira, nps_medio, media_alunos_turma
### `vw_kpis_professor_historico`
- colunas (13): professor_id, professor_nome, unidade_id, ano, mes, matriculas, ticket_medio, experimentais, total_experimentais_unidade, total_matriculas_unidade, taxa_conversao, nps_medio, media_alunos_turma
### `vw_kpis_professor_mensal`
- colunas (26): professor_id, professor_nome, unidade_id, ano, mes, carteira_alunos, ticket_medio, media_presenca, taxa_faltas, mrr_carteira, nps_medio, media_alunos_turma, experimentais, matriculas, matriculas_pos_exp, matriculas_diretas, taxa_conversao, renovacoes, nao_renovacoes, taxa_renovacao, evasoes, mrr_perdido, taxa_cancelamento, ranking_matriculador, ranking_renovador, ranking_churn
### `vw_kpis_professor_por_unidade`
- colunas (10): professor_id, professor_nome, unidade_id, carteira_alunos, ticket_medio, media_presenca, taxa_faltas, mrr_carteira, nps_medio, media_alunos_turma
### `vw_kpis_retencao_mensal`
- colunas (17): unidade_id, unidade_nome, ano, mes, total_evasoes, evasoes_interrompidas, avisos_previos, transferencias, taxa_evasao, mrr_perdido, renovacoes_previstas, renovacoes_realizadas, nao_renovacoes, renovacoes_pendentes, renovacoes_atrasadas, taxa_renovacao, taxa_nao_renovacao
### `vw_leads_comercial`
- colunas (50): id, unidade_id, data, tipo, canal_origem_id, curso_id, quantidade, observacoes, aluno_nome, aluno_idade, professor_experimental_id, professor_fixo_id, agente_comercial, valor_passaporte, valor_parcela, forma_pagamento_id, tipo_matricula, aluno_novo_retorno, created_at, updated_at, created_by, arquivado, data_arquivamento, motivo_arquivamento_id, motivo_nao_matricula_id, forma_pagamento_passaporte_id, dia_vencimento, tipo_aluno, sabia_preco, lead_status, ...
### `vw_leads_por_canal`
- colunas (6): unidade, ano_mes, canal, total_leads, matriculas, taxa_conversao
### `vw_ltv_por_categoria`
- colunas (3): categoria_saida, total_alunos, ltv_meses
### `vw_ltv_por_unidade`
- colunas (5): unidade, total_alunos, soma_meses, ltv_meses, ltv_anos
### `vw_ltv_rede`
- colunas (4): total_alunos, soma_meses, ltv_meses, ltv_anos
### `vw_ltv_unidade`
- colunas (6): unidade, unidade_codigo, total_alunos_saidos, tempo_medio_meses, ticket_medio, ltv_medio
### `vw_matriculas_por_canal`
- colunas (4): unidade, ano_mes, canal_origem, quantidade
### `vw_metas_vs_realizado`
- colunas (19): unidade, ano, mes, ano_mes, meta_matriculas, matriculas_realizadas, pct_matriculas, meta_renovacoes, renovacoes_realizadas, pct_renovacoes, meta_churn_maximo, churn_realizado, status_churn, meta_faturamento_parcelas, faturamento_realizado, pct_faturamento, meta_alunos_ativos, alunos_ativos, pct_alunos
### `vw_motivos_nao_matricula`
- colunas (4): unidade, ano_mes, motivo_nao_matricula, quantidade
### `vw_movimentacoes_mensal`
- colunas (6): unidade, ano, mes, ano_mes, tipo, quantidade
### `vw_movimentacoes_recentes`
- colunas (9): id, aluno, unidade, curso, tipo, data_movimentacao, motivo_saida, observacoes, created_by
### `vw_performance_professor_experimental`
- colunas (6): unidade, ano_mes, professor, experimentais_realizadas, matriculas, taxa_conversao
### `vw_professores_carteira_resumo`
- colunas (9): professor_id, professor_nome, telefone_whatsapp, unidade_id, total_alunos, alunos_verdes, alunos_amarelos, alunos_vermelhos, alunos_sem_avaliacao
### `vw_professores_performance_atual`
- colunas (13): professor_id, professor, unidade, ano, total_alunos, ticket_medio, mrr, tempo_permanencia_medio, presenca_media, experimentais, matriculas, taxa_conversao, evasoes
### `vw_projecao_metas`
- colunas (13): unidade, ano, mes, dias_passados, dias_no_mes, meta_matriculas, matriculas_ate_agora, matriculas_projetadas, status_matriculas, meta_faturamento_parcelas, faturamento_ate_agora, faturamento_projetado, status_faturamento
### `vw_ranking_professores_evasoes`
- colunas (9): professor, unidade, ano, evasoes, matriculas, taxa_conversao, renovacoes, taxa_renovacao, nivel_risco
### `vw_ranking_professores_retencao`
- colunas (8): unidade, professor, total_alunos, alunos_ativos, alunos_perdidos, tempo_medio_permanencia, presenca_media, ticket_medio
### `vw_ranking_unidades`
- colunas (9): unidade, codigo, ano, alunos_dezembro, churn_medio, renovacao_media, inadimplencia_media, ticket_medio, permanencia
### `vw_renovacoes_mensal`
- colunas (10): unidade, ano, mes, ano_mes, renovacoes, nao_renovacoes, pendentes, negociando, reajuste_medio, taxa_renovacao
### `vw_renovacoes_pendentes`
- colunas (8): unidade_id, unidade_nome, mes_vencimento, total_vencendo, renovadas, nao_renovadas, pendentes, atrasadas
### `vw_renovacoes_proximas`
- colunas (17): aluno_id, aluno_nome, unidade_id, unidade_nome, professor_atual_id, professor_nome, curso_nome, valor_parcela, data_inicio_contrato, data_fim_contrato, tempo_permanencia_meses, classificacao, telefone, whatsapp, email, dias_ate_vencimento, status_renovacao
### `vw_sazonalidade`
- colunas (8): unidade, codigo, ano, mes, novas_matriculas, evasoes, churn_rate, saldo_liquido
### `vw_taxa_crescimento_professor`
- colunas (13): professor_id, professor_nome, unidade_id, ano, mes, alunos_iniciais, matriculas_mes, evasoes_mes, nao_renovacoes_mes, fator_demanda_ponderado, taxa_crescimento_bruta, taxa_crescimento_ajustada, pontos_crescimento
### `vw_totais_unidade_performance`
- colunas (10): unidade, ano, total_professores, total_experimentais, total_matriculas, taxa_conversao_media, total_evasoes, total_contratos, total_renovacoes, taxa_renovacao_media
### `vw_turmas_completa`
- colunas (18): id, unidade_id, unidade_nome, professor_id, professor_nome, sala_id, sala_nome, curso_id, curso_nome, dia_semana, horario_inicio, horario_fim, capacidade_maxima, turma_nome, ativo, total_alunos, nomes_alunos, ids_alunos
### `vw_turmas_implicitas`
- colunas (17): unidade_id, unidade_nome, professor_id, professor_nome, curso_id, curso_nome, dia_semana, horario_inicio, total_alunos, nomes_alunos, ids_alunos, ticket_medio_turma, tempo_medio_turma, turma_explicita_id, sala_id, sala_nome, capacidade_maxima
### `vw_turmas_professor_periodo`
- colunas (14): aula_id, professor_id, unidade_id, data_aula, turma_nome, turma_chave, curso_nome, sala_nome, dia_semana_iso, horario_inicio, aluno_id, status_presenca, aluno_nome, aluno_status
### `vw_unidade_anual`
- colunas (12): unidade, codigo, ano, alunos_dezembro, alunos_janeiro, total_matriculas, total_evasoes, churn_medio, ticket_medio, renovacao_media, permanencia_atual, inadimplencia_media

## Tabelas/outros expostos (nomes)

- `admin_conversas`
- `admin_mensagens`
- `agente_conversas`
- `agente_fila_mensagens`
- `agentes`
- `aluno_acoes`
- `aluno_contatos`
- `aluno_feedback_professor`
- `aluno_feedback_sessoes`
- `aluno_metas`
- `aluno_presenca`
- `alunos`
- `alunos_arquivados`
- `alunos_health_score_historico`
- `alunos_historico`
- `alunos_turmas`
- `anamnese_respostas_perfil`
- `anamneses`
- `anotacoes`
- `anotacoes_alunos`
- `assistente_ia_config`
- `audit_log`
- `auditoria_acesso`
- `aulas_emusys`
- `automacao_invariantes`
- `automacao_log`
- `bi_agent_config_lamusic`
- `bi_ai_query_playbooks`
- `bi_conversations_lamusic`
- `bi_messages_lamusic`
- `bi_query_cache_lamusic`
- `bi_query_templates_lamusic`
- `campanha_contatos`
- `campanhas`
- `campanhas_config`
- `canais_origem`
- `catalogo_treinamentos`
- `colaboradores`
- `config_health_score`
- `config_health_score_aluno`
- `config_health_score_professor`
- `contatos_bloqueados_campanha`
- `conversa_estado_whatsapp`
- `conversas_campanha`
- `crm_conversas`
- `crm_etiquetas`
- `crm_followups`
- `crm_lead_etiquetas`
- `crm_lead_historico`
- `crm_mensagens`
- `crm_mensagens_agendadas`
- `crm_metas_andreza`
- `crm_motivos_nao_comparecimento`
- `crm_pipeline_etapas`
- `crm_templates_whatsapp`
- `cursos`
- `cursos_matriculados`
- `dados_comerciais`
- `dados_mensais`
- `dashboard_config`
- `emusys_sync_log`
- `evasoes_backup_20260215`
- `evasoes_legacy_backup`
- `evasoes_v2`
- `evasoes_v2_backup`
- `experimentais_mensal_unidade`
- `experimentais_professor_mensal`
- `farmer_checklist_contatos`
- `farmer_checklist_items`
- `farmer_checklist_templates`
- `farmer_checklists`
- `farmer_recados`
- `farmer_recados_campanhas`
- `farmer_recados_destinatarios`
- `farmer_rotinas`
- `farmer_rotinas_execucao`
- `farmer_tarefas`
- `farmer_templates`
- `feriados`
- `fila_relatorios_whatsapp`
- `formas_pagamento`
- `historico_pagamentos`
- `horarios`
- `insights_salvos`
- `inventario`
- `inventario_manutencoes`
- `inventario_movimentacoes`
- `inventario_pendencias`
- `lead_experimentais`
- `leads`
- `leads_automacao_log`
- `leads_diarios_backup`
- `loja_carteira`
- `loja_carteira_movimentacoes`
- `loja_categorias`
- `loja_configuracoes`
- `loja_estoque`
- `loja_movimentacoes_estoque`
- `loja_optin_novidades`
- `loja_produtos`
- `loja_reservas`
- `loja_responsaveis_reposicao`
- `loja_variacoes`
- `loja_vendas`
- `loja_vendas_itens`
- `mensagens_campanha`
- `metas`
- `metas_comerciais`
- `metas_kpi`
- `metas_legado`
- `metas_professor_turma`
- `mila_config`
- `mila_message_buffer`
- `motivos_arquivamento`
- `motivos_nao_matricula`
- `motivos_saida`
- `motivos_trancamento`
- `movimentacoes`
- `movimentacoes_admin`
- `notificacao_config`
- `notificacao_destinatarios`
- `notificacao_log`
- `numeros_meta`
- `origem_leads`
- `perfil_permissoes`
- `perfis`
- `permissoes`
- `pesquisa_evasao`
- `planos_acao`
- `professor_360_avaliacoes`
- `professor_360_config`
- `professor_360_criterios`
- `professor_360_ocorrencias`
- `professor_360_ocorrencias_log`
- `professor_acoes`
- `professor_acoes_participantes`
- `professor_checkpoints`
- `professor_metas`
- `professor_videos`
- `professores`
- `professores_cursos`
- `professores_experimentais`
- `professores_performance`
- `professores_sync_log`
- `professores_unidades`
- `programa_fideliza_config`
- `programa_fideliza_experiencias`
- `programa_fideliza_historico`
- `programa_fideliza_penalidades`
- `programa_matriculador_config`
- `programa_matriculador_historico`
- `programa_matriculador_penalidades`
- `projeto_anexos`
- `projeto_comentarios`
- `projeto_config_permissoes`
- `projeto_equipe`
- `projeto_equipe_membros`
- `projeto_fases`
- `projeto_log_alteracoes`
- `projeto_tarefas`
- `projeto_tipo_fases_template`
- `projeto_tipo_tarefas_template`
- `projeto_tipos`
- `projetos`
- `relatorios_diarios`
- `renovacoes`
- `respostas_rapidas_campanha`
- `salas`
- `simulacoes_metas`
- `simulacoes_turma`
- `templates_cenario`
- `templates_cenario_unidade`
- `templates_meta`
- `tipos_matricula`
- `tipos_saida`
- `transferencias_mila`
- `turmas`
- `turmas_alunos`
- `turmas_explicitas`
- `turmas_historico`
- `unidades`
- `unidades_cursos`
- `usuario_onboarding`
- `usuario_perfis`
- `usuarios`
- `visitas`
- `visitas_config`
- `webhook_debug_log`
- `whatsapp_caixas`
- `whatsapp_config`
- `whatsapp_destinatarios_relatorio`
