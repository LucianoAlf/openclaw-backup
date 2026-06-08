SELECT jsonb_agg(jsonb_build_object('name',p.proname,'args',pg_get_function_identity_arguments(p.oid),'def',pg_get_functiondef(p.oid)) ORDER BY p.proname) AS result
FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
WHERE n.nspname='public' AND p.prokind='f' AND p.proname IN ('fechar_dados_mensais','recalcular_dados_mensais','snapshot_dados_mensais','sync_evasao_to_dados_mensais','upsert_dados_mensais');
