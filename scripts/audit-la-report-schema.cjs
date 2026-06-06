const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: '/root/.openclaw/workspace/.env' });

const url = process.env.LAREPORT_SUPABASE_URL || process.env.SUPABASE_URL;
const key = process.env.LAREPORT_SUPABASE_SERVICE_ROLE || process.env.SUPABASE_SERVICE_ROLE;
if (!url || !key) throw new Error('Missing LAREPORT_SUPABASE_URL/SERVICE_ROLE');
const supabase = createClient(url, key, { auth: { persistSession: false } });

async function q(name, sql) {
  const { data, error } = await supabase.rpc('executar_query_auditoria', { p_sql: sql });
  if (error) {
    console.error(`ERROR ${name}:`, error);
    return { name, error };
  }
  return { name, data };
}

(async () => {
  const queries = [
    ['objects', `
      SELECT n.nspname AS schema,
             c.relname AS name,
             CASE c.relkind WHEN 'r' THEN 'table' WHEN 'v' THEN 'view' WHEN 'm' THEN 'materialized_view' WHEN 'p' THEN 'partitioned_table' ELSE c.relkind::text END AS kind,
             COALESCE(s.n_live_tup, 0) AS estimated_rows,
             pg_total_relation_size(c.oid) AS total_bytes,
             pg_size_pretty(pg_total_relation_size(c.oid)) AS total_size,
             obj_description(c.oid) AS comment
      FROM pg_class c
      JOIN pg_namespace n ON n.oid = c.relnamespace
      LEFT JOIN pg_stat_user_tables s ON s.relid = c.oid
      WHERE n.nspname = 'public'
        AND c.relkind IN ('r','p','v','m')
      ORDER BY kind, name
    `],
    ['views', `
      SELECT schemaname AS schema, viewname AS name, definition
      FROM pg_views
      WHERE schemaname = 'public'
      ORDER BY viewname
    `],
    ['matviews', `
      SELECT schemaname AS schema, matviewname AS name, definition
      FROM pg_matviews
      WHERE schemaname = 'public'
      ORDER BY matviewname
    `],
    ['functions', `
      SELECT n.nspname AS schema,
             p.proname AS name,
             pg_get_function_identity_arguments(p.oid) AS args,
             pg_get_function_result(p.oid) AS returns,
             l.lanname AS language,
             p.prosecdef AS security_definer,
             pg_get_functiondef(p.oid) AS definition
      FROM pg_proc p
      JOIN pg_namespace n ON n.oid = p.pronamespace
      JOIN pg_language l ON l.oid = p.prolang
      WHERE n.nspname = 'public'
      ORDER BY p.proname, args
    `],
    ['dependencies', `
      SELECT dependent_ns.nspname AS dependent_schema,
             dependent_view.relname AS dependent_object,
             CASE dependent_view.relkind WHEN 'v' THEN 'view' WHEN 'm' THEN 'materialized_view' ELSE dependent_view.relkind::text END AS dependent_kind,
             source_ns.nspname AS source_schema,
             source_table.relname AS source_object,
             CASE source_table.relkind WHEN 'r' THEN 'table' WHEN 'v' THEN 'view' WHEN 'm' THEN 'materialized_view' ELSE source_table.relkind::text END AS source_kind
      FROM pg_depend d
      JOIN pg_rewrite r ON r.oid = d.objid
      JOIN pg_class dependent_view ON dependent_view.oid = r.ev_class
      JOIN pg_namespace dependent_ns ON dependent_ns.oid = dependent_view.relnamespace
      JOIN pg_class source_table ON source_table.oid = d.refobjid
      JOIN pg_namespace source_ns ON source_ns.oid = source_table.relnamespace
      WHERE dependent_ns.nspname = 'public'
        AND source_ns.nspname = 'public'
        AND dependent_view.oid <> source_table.oid
        AND dependent_view.relkind IN ('v','m')
        AND source_table.relkind IN ('r','v','m')
      GROUP BY 1,2,3,4,5,6
      ORDER BY dependent_object, source_object
    `],
    ['constraints', `
      SELECT c.relname AS table_name,
             con.conname AS constraint_name,
             con.contype AS constraint_type,
             pg_get_constraintdef(con.oid) AS definition
      FROM pg_constraint con
      JOIN pg_class c ON c.oid = con.conrelid
      JOIN pg_namespace n ON n.oid = c.relnamespace
      WHERE n.nspname = 'public'
      ORDER BY c.relname, con.contype, con.conname
    `],
    ['rls_policies', `
      SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual, with_check
      FROM pg_policies
      WHERE schemaname = 'public'
      ORDER BY tablename, policyname
    `],
    ['triggers', `
      SELECT event_object_table AS table_name,
             trigger_name,
             action_timing,
             event_manipulation,
             action_statement
      FROM information_schema.triggers
      WHERE trigger_schema = 'public'
      ORDER BY event_object_table, trigger_name
    `],
    ['columns', `
      SELECT table_name, column_name, data_type, is_nullable, column_default, generation_expression
      FROM information_schema.columns
      WHERE table_schema = 'public'
      ORDER BY table_name, ordinal_position
    `],
    ['cron_jobs', `
      SELECT jobid, jobname, schedule, command, active
      FROM cron.job
      ORDER BY jobname
    `],
  ];

  const results = {};
  for (const [name, sql] of queries) {
    console.error('Running', name);
    results[name] = await q(name, sql);
  }

  const outDir = '/root/.openclaw/workspace/outputs/la-report-schema-audit';
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, 'schema-audit-raw.json'), JSON.stringify(results, null, 2));
  for (const [name] of queries) {
    const r = results[name];
    if (!r || r.error) continue;
    fs.writeFileSync(path.join(outDir, `${name}.json`), JSON.stringify(r.data, null, 2));
  }
  console.log(outDir);
})();
