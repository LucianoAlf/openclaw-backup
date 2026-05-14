# LAHQ DB Refactor — plano seguro

## Resultado da análise

- `squads` **não deve ser removida agora**: tem 1 registro e é referenciada por `agents.squad_id` e `tasks.squad_id` no dado real.
- `instagram_events`, `ig_blocked_users`, `leads`, `v_lead_receivers` devem ficar: Tina monitor usa/consulta.
- Tabelas vazias de módulos futuros podem ficar, mas precisam ser **classificadas e bloqueadas contra uso acidental**, senão viram o problema que o Alf descreveu.

## Decisão recomendada

### Manter core
`tasks`, `outputs`, `semantic_memory`, `agents`, `agent_skills`, `agent_costs`, `media_assets`, `calendar_entries`, `staff_contacts`, `agent_integrations`, `offices`, `squads`.

### Manter futuro, mas documentar como não-operacional ainda
`bio_links`, `boosts`, `budget_decisions`, `campaigns`, `contacts`, `dispatches`, `email_bounces`, `kpi_snapshots`, `leads`, `post_metrics`, `schedule_entries`, `ig_blocked_users`.

### Deprecar primeiro
`shared_memory`, `meetings`.

## Script gerado

`/root/.openclaw/workspace/outputs/lahq-db-refactor/lahq_safe_deprecation_plan.sql`

Ele está com `ROLLBACK` no final por segurança. Não apaga nada.
