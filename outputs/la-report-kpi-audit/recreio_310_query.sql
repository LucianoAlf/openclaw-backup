SELECT jsonb_build_object(
 'live_vw_rows', (SELECT jsonb_agg(to_jsonb(x)) FROM (SELECT ano,mes,total_alunos_pagantes,ticket_medio,mrr,inadimplencia_pct,churn_rate FROM vw_kpis_gestao_mensal WHERE unidade_id='95553e96-971b-4590-a6eb-0201d013c14d' ORDER BY ano DESC, mes DESC LIMIT 5) x),
 'snapshot_jun2026', (SELECT jsonb_agg(to_jsonb(x)) FROM (SELECT ano,mes,alunos_pagantes,ticket_medio,faturamento_estimado,inadimplencia,churn_rate,evasoes FROM dados_mensais WHERE unidade_id='95553e96-971b-4590-a6eb-0201d013c14d' AND ano=2026 AND mes=6) x),
 'unidade', (SELECT nome FROM unidades WHERE id='95553e96-971b-4590-a6eb-0201d013c14d')
) AS result;
