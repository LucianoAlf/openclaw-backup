-- =============================================================================
-- VALIDACAO_REGLA_KPI_V5_FINANCEIRO_ALFREDO_SELECT_ONLY.sql
-- Autor: Alfredo / OpenClaw
-- Data: 2026-06-01
--
-- Objetivo:
--   V5_FINANCEIRO validation-first para Campo Grande / Maio 2026.
--   Este arquivo NÃO aplica migration. Ele compara fórmulas financeiras antes
--   de qualquer persistência em dados_mensais.
--
-- Princípios da V5_FINANCEIRO:
--   1. Ticket médio financeiro = MRR contratual / alunos_pagantes.
--      Motivo: dados_mensais.faturamento_estimado é coluna gerada como
--      alunos_pagantes * ticket_medio. Logo, ticket_medio precisa reconstruir MRR.
--   2. MRR contratual = soma de valor_parcela das linhas pagantes no snapshot.
--   3. Inadimplência para faturamento = percentual de VALOR inadimplente sobre MRR,
--      não percentual de pessoas inadimplentes.
--   4. Faturamento previsto = MRR contratual.
--   5. Faturamento realizado estimado = MRR contratual - MRR inadimplente.
--   6. valor_parcela NULL/0 em pagante é alerta bloqueante, não filtro global.
--   7. Não mexe em tempo_permanencia, taxa_renovacao, reajuste_parcelas.
--      Esses são domínios de retenção/renovação, não do patch financeiro.
--
-- Guardrails:
--   - SELECT-only.
--   - Sem CREATE/DROP/ALTER.
--   - Sem UPDATE/INSERT/DELETE.
--   - Sem \set, \echo ou :param.
--   - Não escreve em colunas geradas faturamento_estimado/saldo_liquido.
-- =============================================================================

-- =============================================================================
-- 0. Schema check: confirmar contrato de dados_mensais antes de qualquer migration.
-- =============================================================================
SELECT
  '00_SCHEMA_CHECK_DADOS_MENSAIS' AS secao,
  c.column_name,
  c.data_type,
  c.is_nullable,
  c.column_default,
  c.is_generated,
  c.generation_expression
FROM information_schema.columns c
WHERE c.table_schema = 'public'
  AND c.table_name = 'dados_mensais'
  AND c.column_name IN (
    'alunos_pagantes',
    'ticket_medio',
    'inadimplencia',
    'faturamento_estimado',
    'saldo_liquido',
    'tempo_permanencia',
    'taxa_renovacao',
    'reajuste_parcelas',
    'updated_at'
  )
ORDER BY c.ordinal_position;

-- =============================================================================
-- 1. Resumo financeiro V5 — Campo Grande / Maio 2026.
-- =============================================================================
WITH params AS (
  SELECT
    u.id AS unidade_id,
    u.nome AS unidade_nome,
    2026::integer AS ano,
    5::integer AS mes,
    DATE '2026-05-01' AS inicio_mes,
    DATE '2026-05-31' AS fim_mes,
    386::numeric AS ticket_card_esperado
  FROM unidades u
  WHERE LOWER(u.nome) LIKE '%campo%grande%'
  ORDER BY u.nome
  LIMIT 1
),

snapshot_base AS (
  SELECT
    a.unidade_id,
    a.id AS aluno_id,
    a.nome,
    LOWER(TRIM(BOTH FROM a.nome)) AS nome_norm,
    a.status,
    a.data_matricula,
    a.data_saida,
    a.valor_parcela,
    a.status_pagamento,
    a.tipo_matricula_id,
    tm.codigo AS tipo_matricula_codigo,
    tm.conta_como_pagante,
    tm.entra_ticket_medio,
    a.curso_id,
    c.nome AS curso_nome,
    c.is_projeto_banda,
    a.is_segundo_curso
  FROM alunos a
  LEFT JOIN tipos_matricula tm ON tm.id = a.tipo_matricula_id
  LEFT JOIN cursos c ON c.id = a.curso_id
  JOIN params p ON p.unidade_id = a.unidade_id
  WHERE a.status IN ('ativo', 'trancado')
    AND a.data_matricula <= p.fim_mes
    AND (a.data_saida IS NULL OR a.data_saida > p.fim_mes)
),

linhas_pagantes AS (
  SELECT *
  FROM snapshot_base
  WHERE conta_como_pagante = true
),

por_pessoa_pagante AS (
  SELECT
    unidade_id,
    nome_norm,
    MIN(nome) AS nome_exemplo,
    COUNT(*) AS linhas_pagantes,
    SUM(COALESCE(valor_parcela, 0)) FILTER (
      WHERE COALESCE(status_pagamento, '') <> 'sem_parcela'
    ) AS valor_total_pagante,
    SUM(COALESCE(valor_parcela, 0)) FILTER (
      WHERE status_pagamento = 'inadimplente'
        AND COALESCE(status_pagamento, '') <> 'sem_parcela'
    ) AS valor_inadimplente_estrito,
    SUM(COALESCE(valor_parcela, 0)) FILTER (
      WHERE status_pagamento IN ('atrasado', 'inadimplente')
        AND COALESCE(status_pagamento, '') <> 'sem_parcela'
    ) AS valor_atrasado_ou_inadimplente,
    BOOL_OR(valor_parcela IS NULL OR valor_parcela = 0) AS tem_valor_zero_ou_null,
    ARRAY_AGG(DISTINCT COALESCE(status_pagamento, 'NULL')) AS status_pagamento_encontrados,
    ARRAY_AGG(DISTINCT COALESCE(tipo_matricula_codigo, 'NULL')) AS tipos_matricula_encontrados,
    ARRAY_AGG(DISTINCT COALESCE(curso_nome, 'NULL')) AS cursos_encontrados
  FROM linhas_pagantes
  GROUP BY unidade_id, nome_norm
),

metricas AS (
  SELECT
    p.unidade_id,
    p.unidade_nome,
    p.ano,
    p.mes,
    COUNT(*)::integer AS alunos_pagantes,
    COALESCE(SUM(valor_total_pagante), 0)::numeric(12,2) AS mrr_contratual,
    COALESCE(SUM(valor_inadimplente_estrito), 0)::numeric(12,2) AS mrr_inadimplente_estrito,
    COALESCE(SUM(valor_atrasado_ou_inadimplente), 0)::numeric(12,2) AS mrr_atrasado_ou_inadimplente,
    ROUND(COALESCE(SUM(valor_total_pagante), 0) / NULLIF(COUNT(*), 0), 2)::numeric(10,2) AS ticket_medio_v5_mrr_por_pagante,
    ROUND(AVG(valor_total_pagante), 2)::numeric(10,2) AS ticket_medio_v5_media_por_pessoa,
    ROUND(
      COALESCE(SUM(valor_inadimplente_estrito), 0) / NULLIF(COALESCE(SUM(valor_total_pagante), 0), 0) * 100,
      2
    )::numeric(5,2) AS inadimplencia_valor_pct_estrita,
    ROUND(
      COALESCE(SUM(valor_atrasado_ou_inadimplente), 0) / NULLIF(COALESCE(SUM(valor_total_pagante), 0), 0) * 100,
      2
    )::numeric(5,2) AS inadimplencia_valor_pct_expandida,
    COUNT(*) FILTER (WHERE tem_valor_zero_ou_null)::integer AS alunos_pagantes_com_valor_zero_ou_null,
    p.ticket_card_esperado
  FROM params p
  LEFT JOIN por_pessoa_pagante pp ON pp.unidade_id = p.unidade_id
  GROUP BY p.unidade_id, p.unidade_nome, p.ano, p.mes, p.ticket_card_esperado
),

dados_mensais_atual AS (
  SELECT dm.*
  FROM dados_mensais dm
  JOIN params p ON p.unidade_id = dm.unidade_id
   AND p.ano = dm.ano
   AND p.mes = dm.mes
)

SELECT
  '01_RESUMO_FINANCEIRO_V5' AS secao,
  m.unidade_nome,
  m.ano,
  m.mes,
  m.alunos_pagantes,
  m.mrr_contratual,
  m.ticket_medio_v5_mrr_por_pagante,
  m.ticket_medio_v5_media_por_pessoa,
  m.ticket_card_esperado,
  (m.ticket_medio_v5_mrr_por_pagante - m.ticket_card_esperado)::numeric(10,2) AS diferenca_vs_card_386,
  m.mrr_inadimplente_estrito,
  m.inadimplencia_valor_pct_estrita,
  (m.mrr_contratual - m.mrr_inadimplente_estrito)::numeric(12,2) AS faturamento_realizado_estimado_estrito,
  m.mrr_atrasado_ou_inadimplente,
  m.inadimplencia_valor_pct_expandida,
  (m.mrr_contratual - m.mrr_atrasado_ou_inadimplente)::numeric(12,2) AS faturamento_realizado_estimado_expandido,
  m.alunos_pagantes_com_valor_zero_ou_null,
  dm.ticket_medio AS ticket_medio_atual_dados_mensais,
  dm.inadimplencia AS inadimplencia_atual_dados_mensais,
  dm.faturamento_estimado AS faturamento_estimado_atual_gerado,
  dm.saldo_liquido AS saldo_liquido_atual_gerado,
  CASE
    WHEN m.alunos_pagantes_com_valor_zero_ou_null > 0
      THEN 'BLOQUEAR_MIGRATION: existem pagantes com valor_parcela NULL/0'
    WHEN ABS(m.ticket_medio_v5_mrr_por_pagante - m.ticket_card_esperado) > 1
      THEN 'VALIDAR_NOMINALMENTE: ticket difere do card esperado'
    ELSE 'OK_PARA_REVISAO_HUMANA'
  END AS status_validacao
FROM metricas m
LEFT JOIN dados_mensais_atual dm ON true;

-- =============================================================================
-- 2. Comparativo de fórmulas de ticket médio.
-- =============================================================================
WITH params AS (
  SELECT
    u.id AS unidade_id,
    u.nome AS unidade_nome,
    DATE '2026-05-01' AS inicio_mes,
    DATE '2026-05-31' AS fim_mes
  FROM unidades u
  WHERE LOWER(u.nome) LIKE '%campo%grande%'
  ORDER BY u.nome
  LIMIT 1
),

snapshot_base AS (
  SELECT
    a.unidade_id,
    a.nome,
    LOWER(TRIM(BOTH FROM a.nome)) AS nome_norm,
    a.valor_parcela,
    a.status_pagamento,
    tm.conta_como_pagante,
    tm.entra_ticket_medio
  FROM alunos a
  LEFT JOIN tipos_matricula tm ON tm.id = a.tipo_matricula_id
  JOIN params p ON p.unidade_id = a.unidade_id
  WHERE a.status IN ('ativo', 'trancado')
    AND a.data_matricula <= p.fim_mes
    AND (a.data_saida IS NULL OR a.data_saida > p.fim_mes)
),

por_pessoa AS (
  SELECT
    unidade_id,
    nome_norm,
    SUM(COALESCE(valor_parcela, 0)) FILTER (
      WHERE conta_como_pagante = true
        AND COALESCE(status_pagamento, '') <> 'sem_parcela'
    ) AS valor_pagante_total,
    BOOL_OR(conta_como_pagante = true) AS pessoa_pagante
  FROM snapshot_base
  GROUP BY unidade_id, nome_norm
)

SELECT
  '02_COMPARATIVO_FORMULAS_TICKET' AS secao,
  p.unidade_nome,
  COUNT(*) FILTER (WHERE pp.pessoa_pagante)::integer AS alunos_pagantes,
  SUM(pp.valor_pagante_total)::numeric(12,2) AS mrr_contratual,

  -- Fórmula recomendada para dados_mensais, pois reconstrói faturamento_estimado gerado.
  ROUND(
    SUM(pp.valor_pagante_total) / NULLIF(COUNT(*) FILTER (WHERE pp.pessoa_pagante), 0),
    2
  )::numeric(10,2) AS ticket_recomendado_mrr_dividido_por_pagantes,

  -- Fórmula pessoa-level média da soma por pessoa. Deve bater com a anterior quando
  -- o denominador também é pessoas pagantes; fica explícita para auditoria.
  ROUND(AVG(pp.valor_pagante_total) FILTER (WHERE pp.pessoa_pagante), 2)::numeric(10,2)
    AS ticket_media_soma_por_pessoa,

  -- Fórmula legada de linha. NÃO recomendada para fechamento, mas útil para comparar.
  (
    SELECT ROUND(AVG(sb.valor_parcela) FILTER (WHERE sb.entra_ticket_medio = true), 2)
    FROM snapshot_base sb
  )::numeric(10,2) AS ticket_legado_media_linha_entra_ticket
FROM params p
LEFT JOIN por_pessoa pp ON pp.unidade_id = p.unidade_id
GROUP BY p.unidade_nome;

-- =============================================================================
-- 3. Alertas bloqueantes: pagante sem valor financeiro confiável.
-- =============================================================================
WITH params AS (
  SELECT
    u.id AS unidade_id,
    u.nome AS unidade_nome,
    DATE '2026-05-01' AS inicio_mes,
    DATE '2026-05-31' AS fim_mes
  FROM unidades u
  WHERE LOWER(u.nome) LIKE '%campo%grande%'
  ORDER BY u.nome
  LIMIT 1
)
SELECT
  '03_ALERTA_BLOQUEANTE_PAGANTE_SEM_VALOR' AS secao,
  p.unidade_nome,
  a.id AS aluno_id,
  a.nome,
  a.status,
  a.data_matricula,
  a.data_saida,
  a.valor_parcela,
  a.status_pagamento,
  tm.codigo AS tipo_matricula_codigo,
  tm.conta_como_pagante,
  c.nome AS curso_nome,
  c.is_projeto_banda,
  a.is_segundo_curso,
  'Pagante contratual com valor_parcela NULL/0. Não excluir automaticamente; validar fatura/competência/passaporte/Gabi.' AS orientacao
FROM alunos a
LEFT JOIN tipos_matricula tm ON tm.id = a.tipo_matricula_id
LEFT JOIN cursos c ON c.id = a.curso_id
JOIN params p ON p.unidade_id = a.unidade_id
WHERE a.status IN ('ativo', 'trancado')
  AND a.data_matricula <= p.fim_mes
  AND (a.data_saida IS NULL OR a.data_saida > p.fim_mes)
  AND tm.conta_como_pagante = true
  AND (a.valor_parcela IS NULL OR a.valor_parcela = 0)
ORDER BY a.nome, a.id;

-- =============================================================================
-- 4. Nominal financeiro por pessoa pagante para validação humana.
-- =============================================================================
WITH params AS (
  SELECT
    u.id AS unidade_id,
    u.nome AS unidade_nome,
    DATE '2026-05-01' AS inicio_mes,
    DATE '2026-05-31' AS fim_mes
  FROM unidades u
  WHERE LOWER(u.nome) LIKE '%campo%grande%'
  ORDER BY u.nome
  LIMIT 1
),

snapshot_base AS (
  SELECT
    a.unidade_id,
    a.id AS aluno_id,
    a.nome,
    LOWER(TRIM(BOTH FROM a.nome)) AS nome_norm,
    a.valor_parcela,
    a.status_pagamento,
    tm.codigo AS tipo_matricula_codigo,
    tm.conta_como_pagante,
    c.nome AS curso_nome,
    c.is_projeto_banda,
    a.is_segundo_curso
  FROM alunos a
  LEFT JOIN tipos_matricula tm ON tm.id = a.tipo_matricula_id
  LEFT JOIN cursos c ON c.id = a.curso_id
  JOIN params p ON p.unidade_id = a.unidade_id
  WHERE a.status IN ('ativo', 'trancado')
    AND a.data_matricula <= p.fim_mes
    AND (a.data_saida IS NULL OR a.data_saida > p.fim_mes)
    AND tm.conta_como_pagante = true
),

por_pessoa AS (
  SELECT
    unidade_id,
    nome_norm,
    MIN(nome) AS nome_exemplo,
    COUNT(*) AS linhas_pagantes,
    SUM(COALESCE(valor_parcela, 0)) FILTER (
      WHERE COALESCE(status_pagamento, '') <> 'sem_parcela'
    ) AS valor_total_pagante,
    SUM(COALESCE(valor_parcela, 0)) FILTER (
      WHERE status_pagamento = 'inadimplente'
    ) AS valor_inadimplente_estrito,
    ARRAY_AGG(
      aluno_id || ' | ' || COALESCE(curso_nome, 'SEM_CURSO') || ' | R$ ' || COALESCE(valor_parcela::text, 'NULL') || ' | ' || COALESCE(status_pagamento, 'NULL') || ' | ' || COALESCE(tipo_matricula_codigo, 'NULL')
      ORDER BY aluno_id
    ) AS linhas_detalhe
  FROM snapshot_base
  GROUP BY unidade_id, nome_norm
)

SELECT
  '04_NOMINAL_POR_PESSOA_PAGANTE' AS secao,
  p.unidade_nome,
  pp.nome_exemplo AS aluno,
  pp.linhas_pagantes,
  pp.valor_total_pagante::numeric(12,2) AS valor_total_pagante,
  pp.valor_inadimplente_estrito::numeric(12,2) AS valor_inadimplente_estrito,
  pp.linhas_detalhe
FROM params p
JOIN por_pessoa pp ON pp.unidade_id = p.unidade_id
ORDER BY pp.valor_total_pagante DESC, pp.nome_exemplo;

-- =============================================================================
-- 5. Migration futura — NÃO EXECUTAR AGORA.
--
-- Depois da validação nominal, a migration de verdade deveria persistir APENAS:
--   - dados_mensais.ticket_medio
--   - dados_mensais.inadimplencia
--
-- Não persistir faturamento_estimado/saldo_liquido porque são generated columns.
-- Não persistir MRR porque não existe coluna MRR em dados_mensais; ele é reconstruído
-- por alunos_pagantes * ticket_medio.
--
-- Esqueleto conceitual, propositalmente comentado:
--
-- WITH metricas AS (...mesmas CTEs validadas acima...)
-- UPDATE dados_mensais dm
-- SET
--   ticket_medio = metricas.ticket_medio_v5_mrr_por_pagante,
--   inadimplencia = metricas.inadimplencia_valor_pct_estrita,
--   updated_at = NOW()
-- FROM metricas
-- WHERE dm.unidade_id = metricas.unidade_id
--   AND dm.ano = metricas.ano
--   AND dm.mes = metricas.mes;
-- =============================================================================
