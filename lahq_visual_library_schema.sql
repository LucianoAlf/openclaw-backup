-- LAHQ Visual Library — Supabase Agente Alfredo
-- Safe initial schema: creates only new schema/tables/buckets/indexes/policies.

create extension if not exists pgcrypto;

create schema if not exists lahq;

grant usage on schema lahq to service_role;

create table if not exists lahq.visual_assets (
  id uuid primary key default gen_random_uuid(),
  brand text not null check (brand in ('school','kids','sonoramente','la-music','other')),
  asset_type text not null default 'photo' check (asset_type in ('photo','reference','output','logo','texture','video','other')),
  title text,
  description text,
  people_names text[] default '{}',
  instrument text,
  location text,
  event_name text,
  vibe_tags text[] default '{}',
  content_tags text[] default '{}',
  quality_score numeric check (quality_score is null or (quality_score >= 0 and quality_score <= 11)),
  consent_status text default 'unknown' check (consent_status in ('unknown','ok','restricted','do_not_use')),
  usage_notes text,
  safe_zones jsonb default '{}'::jsonb,
  visual_analysis jsonb default '{}'::jsonb,
  storage_bucket text,
  storage_path text,
  external_url text,
  local_source_path text,
  width integer,
  height integer,
  checksum text,
  approved_reference boolean default false,
  approved_by text,
  approved_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists lahq.content_references (
  id uuid primary key default gen_random_uuid(),
  brand text not null check (brand in ('school','kids','sonoramente','la-music','other')),
  title text not null,
  score numeric check (score is null or (score >= 0 and score <= 11)),
  status text not null default 'gold' check (status in ('draft','approved','gold','deprecated')),
  output_path text,
  preview_path text,
  repo_path text,
  storage_bucket text,
  storage_path text,
  notes text,
  principles jsonb default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (brand, title)
);

create table if not exists lahq.asset_usage (
  id uuid primary key default gen_random_uuid(),
  asset_id uuid references lahq.visual_assets(id) on delete cascade,
  reference_id uuid references lahq.content_references(id) on delete set null,
  usage_type text default 'carousel',
  card_number integer,
  role text,
  notes text,
  created_at timestamptz not null default now()
);

grant all on lahq.visual_assets to service_role;
grant all on lahq.content_references to service_role;
grant all on lahq.asset_usage to service_role;

create index if not exists visual_assets_brand_idx on lahq.visual_assets(brand);
create index if not exists visual_assets_asset_type_idx on lahq.visual_assets(asset_type);
create index if not exists visual_assets_people_gin on lahq.visual_assets using gin(people_names);
create index if not exists visual_assets_vibe_tags_gin on lahq.visual_assets using gin(vibe_tags);
create index if not exists visual_assets_content_tags_gin on lahq.visual_assets using gin(content_tags);
create index if not exists visual_assets_approved_idx on lahq.visual_assets(approved_reference);
create index if not exists content_references_brand_status_idx on lahq.content_references(brand,status);

create or replace function lahq.touch_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end $$;

drop trigger if exists visual_assets_touch_updated_at on lahq.visual_assets;
create trigger visual_assets_touch_updated_at
before update on lahq.visual_assets
for each row execute function lahq.touch_updated_at();

drop trigger if exists content_references_touch_updated_at on lahq.content_references;
create trigger content_references_touch_updated_at
before update on lahq.content_references
for each row execute function lahq.touch_updated_at();

-- RLS: internal/private by default. No anon/authenticated table access unless we add policies later.
alter table lahq.visual_assets enable row level security;
alter table lahq.content_references enable row level security;
alter table lahq.asset_usage enable row level security;

drop policy if exists service_role_all_visual_assets on lahq.visual_assets;
create policy service_role_all_visual_assets on lahq.visual_assets
  for all to service_role using (true) with check (true);

drop policy if exists service_role_all_content_references on lahq.content_references;
create policy service_role_all_content_references on lahq.content_references
  for all to service_role using (true) with check (true);

drop policy if exists service_role_all_asset_usage on lahq.asset_usage;
create policy service_role_all_asset_usage on lahq.asset_usage
  for all to service_role using (true) with check (true);

-- Storage buckets (private by default)
insert into storage.buckets (id, name, public)
values
  ('lahq-visual-assets', 'lahq-visual-assets', false),
  ('lahq-reference-outputs', 'lahq-reference-outputs', false)
on conflict (id) do nothing;

-- Seed approved V4 reference metadata
insert into lahq.content_references (
  brand, title, score, status, output_path, preview_path, repo_path, storage_bucket, storage_path, notes, principles
) values (
  'school',
  'O que é ser aluno da LA? — V4 Manifesto',
  11,
  'gold',
  '/root/.openclaw/workspace/outputs/la-school-what-is-student-carousel-v4/',
  '/root/.openclaw/workspace/outputs/la-school-what-is-student-carousel-v4/preview-grid.jpg',
  'shared/design-systems/references/la-music-school-v2-gold/v4-manifesto-ser-aluno-la/',
  'lahq-reference-outputs',
  'school/gold/v4-manifesto-ser-aluno-la/preview-grid.jpg',
  'Aprovado por Alf como referência 11/11: design V3 preservado + copy bebendo no Manifesto LA Music.',
  jsonb_build_object(
    'copy', jsonb_build_array('música não é só aula','sonho aceso','identidade','paixão vira prática vira palco','empatia sem moleza','excelência sem frieza'),
    'visual', jsonb_build_array('foto real de aluno','dark/pink premium','Prompt gigante','halftone orgânico','logo oficial topo','texto fora do rosto'),
    'rule', 'manter a alma, não copiar a forma'
  )
)
on conflict (brand, title) do update set
  score = excluded.score,
  status = excluded.status,
  output_path = excluded.output_path,
  preview_path = excluded.preview_path,
  repo_path = excluded.repo_path,
  storage_bucket = excluded.storage_bucket,
  storage_path = excluded.storage_path,
  notes = excluded.notes,
  principles = excluded.principles,
  updated_at = now();
