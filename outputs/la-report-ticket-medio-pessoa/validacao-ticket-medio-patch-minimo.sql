WITH atual_financeiro AS (
  SELECT
    u.nome AS unidade_nome,
    avg(a.valor_parcela) FILTER (WHERE tm.entra_ticket_medio = true) AS ticket_atual_linha,
    sum(a.valor_parcela) FILTER (WHERE tm.conta_como_pagante = true) AS mrr_atual
  FROM alunos a
  JOIN unidades u ON u.id = a.unidade_id
  LEFT JOIN tipos_matricula tm ON tm.id = a.tipo_matricula_id
  WHERE a.status::text = 'ativo'::text
  GROUP BY u.nome
), pessoas_ticket AS (
  SELECT
    u.nome AS unidade_nome,
    (lower(trim(both from a.nome)) || '-'::text) || a.unidade_id::text AS chave_pessoa,
    sum(a.valor_parcela) AS valor_total_pessoa
  FROM alunos a
  JOIN unidades u ON u.id = a.unidade_id
  LEFT JOIN tipos_matricula tm ON tm.id = a.tipo_matricula_id
  LEFT JOIN cursos c ON c.id = a.curso_id
  WHERE a.status::text = 'ativo'::text
    AND tm.entra_ticket_medio = true
    AND COALESCE(a.valor_parcela, 0::numeric) > 0::numeric
    AND (tm.codigo IS NULL OR tm.codigo::text <> ALL (ARRAY['BOLSISTA_INT'::character varying::text, 'BOLSISTA_PARC'::character varying::text]))
    AND COALESCE(c.is_projeto_banda, false) = false
    AND (c.nome IS NULL OR c.nome::text !~~* '%canto coral%'::text)
  GROUP BY u.nome, (lower(trim(both from a.nome)) || '-'::text) || a.unidade_id::text
  HAVING sum(a.valor_parcela) > 0::numeric
), novo_ticket AS (
  SELECT
    unidade_nome,
    avg(valor_total_pessoa) AS ticket_novo_pessoa,
    sum(valor_total_pessoa) AS soma_parcelas_ticket,
    count(*) AS pessoas_ticket
  FROM pessoas_ticket
  GROUP BY unidade_nome
), view_atual AS (
  SELECT
    unidade_nome,
    ticket_medio AS ticket_view_atual,
    mrr AS mrr_view_atual,
    novas_matriculas,
    total_alunos_pagantes,
    total_alunos_ativos,
    total_segundo_curso,
    matriculas_ativas,
    total_evasoes,
    churn_rate
  FROM vw_kpis_gestao_mensal
)
SELECT
  v.unidade_nome,
  v.ticket_view_atual,
  nt.ticket_novo_pessoa::numeric(10,2) AS ticket_novo_pessoa,
  (nt.ticket_novo_pessoa - v.ticket_view_atual)::numeric(10,2) AS diff_ticket,
  v.mrr_view_atual,
  af.mrr_atual::numeric(12,2) AS mrr_bloco_atual_recalculado,
  (af.mrr_atual - v.mrr_view_atual)::numeric(12,2) AS diff_mrr_view_vs_bloco,
  v.novas_matriculas,
  v.total_alunos_pagantes,
  v.total_alunos_ativos,
  v.total_segundo_curso,
  v.matriculas_ativas,
  v.total_evasoes,
  v.churn_rate,
  nt.pessoas_ticket,
  nt.soma_parcelas_ticket::numeric(12,2) AS soma_parcelas_ticket
FROM view_atual v
JOIN atual_financeiro af USING (unidade_nome)
JOIN novo_ticket nt USING (unidade_nome)
ORDER BY v.unidade_nome
