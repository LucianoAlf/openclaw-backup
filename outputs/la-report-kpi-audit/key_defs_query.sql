WITH key_views(name) AS (VALUES
 ('vw_kpis_gestao_mensal'),('vw_kpis_retencao_mensal'),('vw_dashboard_unidade'),('vw_kpis_comercial_mensal'),('vw_kpis_comercial_historico'),('vw_kpis_professor_mensal'),('vw_kpis_professor_completo'),('vw_fator_demanda_professor'),('vw_turmas_implicitas')
), key_funcs(name) AS (VALUES
 ('get_programa_fideliza_dados'),('get_kpis_professor_periodo'),('get_presenca_por_aluno_professor'),('get_carteira_professores'),('get_tempo_permanencia'),('get_dados_relatorio_coordenacao')
)
SELECT jsonb_build_object(
 'views', (SELECT jsonb_agg(jsonb_build_object('name',v.name,'exists',c.oid IS NOT NULL,'def',CASE WHEN c.oid IS NOT NULL THEN pg_get_viewdef(c.oid,true) END) ORDER BY v.name)
           FROM key_views v LEFT JOIN pg_class c ON c.relname=v.name AND c.relnamespace='public'::regnamespace),
 'functions', (SELECT jsonb_agg(jsonb_build_object('name',f.name,'exists',p.oid IS NOT NULL,'args',pg_get_function_identity_arguments(p.oid),'def',CASE WHEN p.oid IS NOT NULL THEN pg_get_functiondef(p.oid) END) ORDER BY f.name)
           FROM key_funcs f LEFT JOIN pg_proc p ON p.proname=f.name AND p.pronamespace='public'::regnamespace)
) AS result;
