SELECT jsonb_build_object(
 'functions_touching_dados_mensais', (
   SELECT jsonb_agg(jsonb_build_object('name',p.proname,'args',pg_get_function_identity_arguments(p.oid),'contains_write', pg_get_functiondef(p.oid) ~* '\\b(insert|update|delete|upsert)\\b','snippet', left(pg_get_functiondef(p.oid),1000)) ORDER BY p.proname)
   FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
   WHERE n.nspname='public' AND p.prokind='f' AND pg_get_functiondef(p.oid) ILIKE '%dados_mensais%'
 ),
 'triggers_touching_dados_mensais', (
   SELECT jsonb_agg(jsonb_build_object('trigger',t.tgname,'table',c.relname,'function',p.proname,'def',pg_get_triggerdef(t.oid)) ORDER BY t.tgname)
   FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid JOIN pg_proc p ON p.oid=t.tgfoid JOIN pg_namespace n ON n.oid=c.relnamespace
   WHERE NOT t.tgisinternal AND n.nspname='public' AND p.prokind='f' AND (pg_get_triggerdef(t.oid) ILIKE '%dados_mensais%' OR pg_get_functiondef(p.oid) ILIKE '%dados_mensais%')
 ),
 'cron_jobs', (
   SELECT CASE WHEN to_regclass('cron.job') IS NULL THEN to_jsonb('cron.job not available'::text) ELSE (
     SELECT jsonb_agg(to_jsonb(j) ORDER BY j.jobname) FROM cron.job j WHERE j.command ILIKE '%dados_mensais%' OR j.jobname ILIKE '%dados_mensais%'
   ) END
 )
) AS result;
