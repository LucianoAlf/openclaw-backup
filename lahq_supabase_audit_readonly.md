# Auditoria read-only — Supabase LAHQ

- Data UTC: 2026-05-13T11:59:11.561874Z
- Project ref: `tmslaunhmjifsjvbizje`
- Método: PostgREST OpenAPI + contagem por REST + Storage API com service_role.
- Limitação: Management API SQL retornou 403/code 1010; sem acesso direto a `pg_catalog`, policies, triggers e functions não expostas.

## Tabelas/views expostas

### `agent_costs` — rows: 100
`id`:uuid not_null, `agent_id`:uuid not_null, `provider`:text not_null, `model`:text, `tokens_input`:integer, `tokens_output`:integer, `images_generated`:integer, `cost_usd`:numeric, `period`:date not_null, `operation_type`:text, `task_id`:uuid, `created_at`:timestamp with time zone

### `agent_integrations` — rows: 5
`id`:uuid not_null, `agent_id`:uuid not_null, `integration_type`:text not_null, `integration_name`:text not_null, `config`:jsonb, `active`:boolean, `created_at`:timestamp with time zone, `updated_at`:timestamp with time zone

### `agent_skills` — rows: 34
`id`:uuid not_null, `agent_id`:uuid not_null, `skill_name`:text not_null, `skill_md_path`:text not_null, `description`:text, `version`:text, `active`:boolean, `created_at`:timestamp with time zone, `updated_at`:timestamp with time zone

### `agents` — rows: 8
`id`:uuid not_null, `squad_id`:uuid not_null, `name`:text not_null, `role`:text not_null, `icon`:text, `model`:text not_null, `personality_config`:jsonb, `avatar_url`:text, `equation_of_value`:text, `soul_md_path`:text, `archetype`:text, `tone`:text, `greeting`:text, `status`:text, `active`:boolean, `created_at`:timestamp with time zone, `updated_at`:timestamp with time zone

### `bio_links` — rows: 0
`id`:uuid not_null, `office_id`:uuid not_null, `brand`:text not_null, `label`:text not_null, `url`:text not_null, `icon`:text, `position`:integer not_null, `is_highlight`:boolean, `is_active`:boolean, `utm_campaign`:text, `clicks`:integer, `created_at`:timestamp with time zone, `updated_at`:timestamp with time zone

### `boosts` — rows: 0
`id`:uuid not_null, `office_id`:uuid not_null, `brand`:text not_null, `ig_media_id`:text not_null, `post_caption`:text, `organic_engagement`:numeric, `organic_avg_engagement`:numeric, `multiplier`:numeric, `decision`:text not_null, `decision_reason`:text, `budget_daily`:numeric, `duration_days`:integer, `budget_total`:numeric, `objective`:text, `targeting`:jsonb, `ad_campaign_id`:text, `ad_adset_id`:text, `ad_id`:text, `started_at`:timestamp with time zone, `ends_at`:timestamp with time zone, `total_spend`:numeric, `boost_impressions`:integer, `boost_reach`:integer, `boost_engagement`:integer, `boost_clicks`:integer, `boost_leads`:integer, `roas`:numeric, `result_notes`:text, `completed_at`:timestamp with time zone, `created_by`:text, `created_at`:timestamp with time zone

### `budget_decisions` — rows: 0
`id`:uuid not_null, `office_id`:uuid not_null, `brand`:text not_null, `campaign_id`:uuid, `campaign_name`:text, `decision_type`:text not_null, `reason`:text not_null, `metric_before`:jsonb, `metric_after`:jsonb, `budget_before`:numeric, `budget_after`:numeric, `decided_by`:text, `decided_at`:timestamp with time zone, `created_at`:timestamp with time zone

### `calendar_entries` — rows: 14
`id`:uuid not_null, `office_id`:uuid not_null, `brand`:text not_null, `title`:text not_null, `content_type`:text not_null, `scheduled_date`:timestamp with time zone not_null, `scheduled_at`:timestamp with time zone, `status`:text, `output_id`:uuid, `campaign_id`:uuid, `ig_media_id`:text, `published_at`:timestamp with time zone, `notes`:text, `created_by`:text, `created_at`:timestamp with time zone, `updated_at`:timestamp with time zone

### `campaigns` — rows: 0
`id`:uuid not_null, `office_id`:uuid not_null, `brand`:text not_null, `platform`:text not_null, `name`:text not_null, `objective`:text, `budget_daily`:numeric, `budget_total`:numeric, `status`:text, `ad_account_id`:text, `campaign_ext_id`:text, `targeting`:jsonb, `creative_ids`:uuid[], `start_date`:date, `end_date`:date, `impressions`:integer, `clicks`:integer, `spend_brl`:numeric, `leads_count`:integer, `cpa_brl`:numeric, `roas`:numeric, `created_by`:text, `created_at`:timestamp with time zone, `updated_at`:timestamp with time zone

### `contacts` — rows: 0
`id`:uuid not_null, `office_id`:uuid not_null, `brand`:text not_null, `name`:text not_null, `email`:text, `whatsapp`:text, `status`:text, `source`:text, `tags`:text[], `created_at`:timestamp with time zone, `updated_at`:timestamp with time zone

### `dispatches` — rows: 0
`id`:uuid not_null, `office_id`:uuid not_null, `brand`:text not_null, `channel`:text not_null, `type`:text, `subject`:text, `content_preview`:text, `total_recipients`:integer, `sent`:integer, `failed`:integer, `opened`:integer, `clicked`:integer, `unsubscribed`:integer, `errors`:jsonb, `campaign_id`:uuid, `output_id`:uuid, `dispatched_by`:text, `dispatched_at`:timestamp with time zone, `created_at`:timestamp with time zone

### `email_bounces` — rows: 0
`id`:uuid not_null, `office_id`:uuid not_null, `dispatch_id`:uuid, `email`:text not_null, `error_message`:text, `bounce_type`:text, `created_at`:timestamp with time zone

### `ig_blocked_users` — rows: 0
`id`:uuid not_null, `office_id`:uuid not_null, `sender_ig_id`:text not_null, `sender_username`:text, `reason`:text not_null, `blocked_by`:text not_null, `events_count`:integer not_null, `created_at`:timestamp with time zone not_null

### `instagram_events` — rows: 0
`id`:uuid not_null, `office_id`:uuid not_null, `meta_event_id`:text not_null, `ig_account_id`:text not_null, `brand`:public.ig_brand not_null, `event_type`:public.ig_event_type not_null, `sender_ig_id`:text, `sender_username`:text, `content`:text, `media_id`:text, `media_caption`:text, `raw_payload`:jsonb not_null, `classification`:public.ig_classification, `confidence`:numeric, `reasoning`:text, `unit_hint`:text, `requires_human_review`:boolean not_null, `escalation_reason`:text, `responded`:boolean not_null, `responded_at`:timestamp with time zone, `response_sent`:text, `response_meta_id`:text, `response_error`:text, `whatsapp_dispatched`:boolean not_null, `whatsapp_to`:text, `lead_id`:uuid, `spam_score`:numeric, `is_minor_account`:boolean not_null, `is_business_account`:boolean not_null, `processed_by`:text, `processing_attempts`:integer not_null, `created_at`:timestamp with time zone not_null, `updated_at`:timestamp with time zone not_null

### `kpi_snapshots` — rows: 0
`id`:uuid not_null, `office_id`:uuid not_null, `brand`:text, `period_start`:date not_null, `period_end`:date not_null, `period_type`:text, `platform`:text, `metric_type`:text, `value`:numeric, `organic_reach`:integer, `organic_impressions`:integer, `engagement_rate`:numeric, `followers_gained`:integer, `saves_total`:integer, `shares_total`:integer, `best_post_id`:text, `best_post_engagement`:numeric, `ad_spend_brl`:numeric, `ad_impressions`:integer, `ad_clicks`:integer, `ad_ctr`:numeric, `ad_cpc_brl`:numeric, `ad_leads`:integer, `ad_cpa_brl`:numeric, `ad_roas`:numeric, `ad_frequency`:numeric, `best_campaign_id`:text, `site_visits`:integer, `site_bounce_rate`:numeric, `lp_conversion_rate`:numeric, `total_leads`:integer, `total_contacted`:integer, `total_matriculas`:integer, `total_pieces`:integer, `by_brand`:jsonb, `by_type`:jsonb, `by_agent`:jsonb, `total_cost`:numeric, `cost_by_agent`:jsonb, `cost_by_provider`:jsonb, `avg_production_time`:numeric, `first_pass_rate`:numeric, `engagement_avg`:numeric, `best_piece`:jsonb, `alerts`:jsonb, `created_by`:text, `created_at`:timestamp with time zone

### `leads` — rows: 0
`id`:uuid not_null, `office_id`:uuid not_null, `brand`:text not_null, `name`:text not_null, `whatsapp`:text, `email`:text, `interest`:text, `unit`:text, `age_range`:text, `source`:text, `campaign_id`:uuid, `utm_source`:text, `utm_medium`:text, `utm_campaign`:text, `status`:text, `contacted`:boolean, `converted`:boolean, `conversion_date`:timestamp with time zone, `notes`:text, `created_at`:timestamp with time zone, `updated_at`:timestamp with time zone, `ig_username`:text, `ig_event_id`:uuid

### `media_assets` — rows: 46
`id`:uuid not_null, `office_id`:uuid not_null, `brand`:text, `type`:text not_null, `file_url`:text not_null, `thumbnail_url`:text, `source`:text, `prompt`:text, `model_used`:text, `tags`:text[], `width`:integer, `height`:integer, `aspect_ratio`:text, `file_size`:integer, `instrument`:text, `mood`:text, `scenario`:text, `treatment`:text, `status`:text, `original_asset_id`:uuid, `output_ids`:uuid[], `briefing_id`:uuid, `created_by`:text, `created_at`:timestamp with time zone, `updated_at`:timestamp with time zone

### `meetings` — rows: 0
`id`:uuid not_null, `office_id`:uuid not_null, `title`:text not_null, `type`:text, `participants`:text[], `agenda`:text, `notes`:text, `decisions`:jsonb, `scheduled_at`:timestamp with time zone, `completed_at`:timestamp with time zone, `created_by`:text, `created_at`:timestamp with time zone, `updated_at`:timestamp with time zone

### `offices` — rows: 1
`id`:uuid not_null, `name`:text not_null, `slug`:text not_null, `brand`:text, `floor_number`:integer, `wall_phrase`:text, `design_config`:jsonb, `active`:boolean, `created_at`:timestamp with time zone, `updated_at`:timestamp with time zone

### `outputs` — rows: 29
`id`:uuid not_null, `task_id`:uuid, `office_id`:uuid not_null, `type`:text not_null, `format`:text, `brand`:text, `title`:text, `theme`:text, `file_urls`:text[], `file_sizes`:integer[], `preview_url`:text, `total_slides`:integer, `duration_seconds`:integer, `published`:boolean, `published_at`:timestamp with time zone, `platform`:text, `ig_media_id`:text, `approval_status`:text, `approval_feedback`:text, `dispatched`:boolean, `dispatch_id`:uuid, `dispatched_at`:timestamp with time zone, `engagement_rate`:numeric, `rendered_by`:text, `render_time_ms`:integer, `status`:text, `asset_ids`:uuid[], `created_at`:timestamp with time zone, `updated_at`:timestamp with time zone

### `post_metrics` — rows: 0
`id`:uuid not_null, `office_id`:uuid not_null, `brand`:text not_null, `ig_media_id`:text not_null, `output_id`:uuid, `media_type`:text, `impressions`:integer, `reach`:integer, `engagement_rate`:numeric, `likes`:integer, `comments`:integer, `saves`:integer, `shares`:integer, `clicks`:integer, `follows`:integer, `published_at`:timestamp with time zone, `collected_at`:timestamp with time zone, `created_at`:timestamp with time zone

### `schedule_entries` — rows: 0
`id`:uuid not_null, `office_id`:uuid not_null, `calendar_entry_id`:uuid, `output_id`:uuid, `brand`:text not_null, `content_type`:text not_null, `platform`:text not_null, `scheduled_at`:timestamp with time zone not_null, `executed_at`:timestamp with time zone, `status`:text, `reschedule_reason`:text, `rescheduled_by`:text, `error_message`:text, `created_by`:text, `created_at`:timestamp with time zone, `updated_at`:timestamp with time zone

### `semantic_memory` — rows: 128
`id`:uuid not_null, `office_id`:uuid not_null, `agent_id`:uuid, `content`:text not_null, `embedding`:public.vector(1536), `category`:text, `metadata`:jsonb, `source`:text, `relevance_score`:numeric, `expires_at`:timestamp with time zone, `created_at`:timestamp with time zone

### `shared_memory` — rows: 0
`id`:uuid not_null, `source_office_id`:uuid not_null, `content`:text not_null, `category`:text, `visibility`:text, `visible_to_squads`:uuid[], `created_by`:text, `created_at`:timestamp with time zone, `updated_at`:timestamp with time zone

### `squads` — rows: 1
`id`:uuid not_null, `office_id`:uuid not_null, `name`:text not_null, `description`:text, `leader_agent_id`:uuid, `equation_of_value`:text, `active`:boolean, `created_at`:timestamp with time zone, `updated_at`:timestamp with time zone

### `staff_contacts` — rows: 5
`id`:uuid not_null, `office_id`:uuid not_null, `name`:text not_null, `role`:text not_null, `phone`:text not_null, `email`:text, `unit`:text, `is_lead_receiver`:boolean not_null, `whatsapp_enabled`:boolean not_null, `priority_order`:integer not_null, `active`:boolean not_null, `notes`:text, `created_at`:timestamp with time zone not_null, `updated_at`:timestamp with time zone not_null

### `tasks` — rows: 103
`id`:uuid not_null, `agent_id`:uuid, `squad_id`:uuid, `parent_task_id`:uuid, `type`:text not_null, `brand`:text, `input`:jsonb, `output`:jsonb, `status`:text, `approval_status`:text, `priority`:text, `model_used`:text, `tokens_consumed`:integer, `cost_usd`:numeric, `feedback`:text, `started_at`:timestamp with time zone, `completed_at`:timestamp with time zone, `created_at`:timestamp with time zone, `updated_at`:timestamp with time zone

### `v_ig_metrics_24h` — rows: 0
`office_id`:uuid, `brand`:public.ig_brand, `total_dms`:bigint, `total_comments`:bigint, `total_mentions`:bigint, `total_leads`:bigint, `total_alunos`:bigint, `total_eventos`:bigint, `total_engajamento`:bigint, `total_ruido`:bigint, `total_revisao_humana`:bigint, `total_respondidos`:bigint, `total_uazapi_disparado`:bigint, `avg_confidence`:numeric

### `v_ig_review_queue` — rows: 0
`id`:uuid, `office_id`:uuid, `brand`:public.ig_brand, `event_type`:public.ig_event_type, `sender_username`:text, `content`:text, `classification`:public.ig_classification, `confidence`:numeric, `escalation_reason`:text, `created_at`:timestamp with time zone, `minutos_aguardando`:numeric

### `v_lead_receivers` — rows: 5
`office_id`:uuid, `name`:text, `phone`:text, `unit`:text, `priority_order`:integer, `unit_label`:text

## RPC/functions expostas via PostgREST

- nenhuma RPC exposta no OpenAPI

## Storage buckets

- `media-assets` public=True created_at=2026-04-14T10:13:23.263Z
- `outputs` public=True created_at=2026-04-14T10:13:23.263Z
- `landing-pages` public=True created_at=2026-04-14T10:13:23.263Z
