-- LAHQ — Deprecar shared_memory sem apagar dados
-- Seguro/reversível. Revisar no Supabase SQL Editor antes de COMMIT.

begin;

-- 1) Confirmar que está vazia
select 'shared_memory' as table_name, count(*) as rows from public.shared_memory;

-- 2) Criar registry de governança do schema
create table if not exists public.schema_deprecation_registry (
  object_schema text not null default 'public',
  object_name text not null,
  object_type text not null default 'table',
  status text not null check (status in ('active','keep_future','deprecated','archive_candidate','drop_candidate')),
  reason text,
  replacement text,
  decision_by text default 'Alf + Alfredo',
  decided_at timestamptz not null default now(),
  review_after timestamptz,
  primary key (object_schema, object_name, object_type)
);

-- 3) Registrar decisão: não usar shared_memory
insert into public.schema_deprecation_registry
  (object_schema, object_name, object_type, status, reason, replacement, review_after)
values
  (
    'public',
    'shared_memory',
    'table',
    'deprecated',
    'Tabela vazia e sem uso operacional. Alfredo usa memória OpenClaw; LAHQ usa semantic_memory para aprendizados dos agentes/pipeline.',
    'OpenClaw memory para Alfredo; public.semantic_memory para LAHQ agents/pipeline',
    now() + interval '30 days'
  )
on conflict (object_schema, object_name, object_type) do update
set status = excluded.status,
    reason = excluded.reason,
    replacement = excluded.replacement,
    review_after = excluded.review_after,
    decided_at = now();

-- 4) Bloquear escrita acidental via clients sujeitos a RLS.
-- Observação: service_role bypassa RLS; por isso scripts também devem parar de usar shared_memory.
alter table public.shared_memory enable row level security;

drop policy if exists deprecated_no_select_shared_memory on public.shared_memory;
create policy deprecated_no_select_shared_memory
on public.shared_memory
for select
using (false);

drop policy if exists deprecated_no_insert_shared_memory on public.shared_memory;
create policy deprecated_no_insert_shared_memory
on public.shared_memory
for insert
with check (false);

drop policy if exists deprecated_no_update_shared_memory on public.shared_memory;
create policy deprecated_no_update_shared_memory
on public.shared_memory
for update
using (false)
with check (false);

drop policy if exists deprecated_no_delete_shared_memory on public.shared_memory;
create policy deprecated_no_delete_shared_memory
on public.shared_memory
for delete
using (false);

-- 5) Verificar registro
select *
from public.schema_deprecation_registry
where object_schema = 'public'
  and object_name = 'shared_memory'
  and object_type = 'table';

rollback;
-- Trocar ROLLBACK por COMMIT somente quando o Alf aprovar execução no SQL Editor.
