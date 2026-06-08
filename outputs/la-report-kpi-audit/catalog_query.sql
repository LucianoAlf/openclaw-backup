WITH objs AS (
  SELECT n.nspname AS schema, c.relname AS name,
    CASE c.relkind WHEN 'r' THEN 'table' WHEN 'v' THEN 'view' WHEN 'm' THEN 'matview' WHEN 'p' THEN 'partitioned_table' ELSE c.relkind::text END AS kind
  FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
  WHERE n.nspname='public'
), funcs AS (
  SELECT n.nspname AS schema, p.proname AS name, 'function' AS kind,
    pg_get_function_identity_arguments(p.oid) AS args
  FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
  WHERE n.nspname='public'
)
SELECT jsonb_build_object(
  'objects', (SELECT jsonb_agg(to_jsonb(objs) ORDER BY name) FROM objs),
  'functions', (SELECT jsonb_agg(to_jsonb(funcs) ORDER BY name,args) FROM funcs),
  'dados_mensais_cols', (
    SELECT jsonb_agg(jsonb_build_object('column',column_name,'type',data_type,'nullable',is_nullable,'default',column_default) ORDER BY ordinal_position)
    FROM information_schema.columns WHERE table_schema='public' AND table_name='dados_mensais'
  ),
  'dados_mensais_constraints', (
    SELECT jsonb_agg(jsonb_build_object('name',con.conname,'type',con.contype,'def',pg_get_constraintdef(con.oid)) ORDER BY con.conname)
    FROM pg_constraint con JOIN pg_class rel ON rel.oid=con.conrelid JOIN pg_namespace n ON n.oid=rel.relnamespace
    WHERE n.nspname='public' AND rel.relname='dados_mensais'
  )
) AS result;
