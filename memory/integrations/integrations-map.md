# integrations-map.md — Mapa de Ferramentas, IDs e Acessos

---

## TickTick

- **Token:** `TICKTICK_TOKEN` no `.env`
- **API base:** `https://api.ticktick.com/open/v1`
- **Permissão:** leitura + escrita (tasks:read, tasks:write)
- **Listas:**
  | ID | Nome |
  |----|------|
  | `643c0518525047536b6594cf` | 📝 Notas Alf |
  | `643c0518525047536b6594d0` | 🏠 Pessoal Alf |
  | `643c0518525047536b6594d1` | 💼 Trabalho Alf |
  | `67158c51db647de6536f46dc` | 💸 Contas Pessoais |
  | `67fbc6398f08b12415f506c4` | 💡 Mentorias |

- **Operações disponíveis:**
  - GET `/project` → listar projetos
  - GET `/project/{id}/data` → listar tarefas de uma lista
  - POST `/task` → criar tarefa
  - POST `/task/{id}` → editar tarefa
  - POST `/project/{id}/task/{taskId}/complete` → marcar como concluída
  - DELETE `/project/{id}/task/{taskId}` → deletar (requer confirmação)

- **Limitações:** sem webhook, sem busca por texto, sem tags via API

---

## GitHub

- **Token:** `GITHUB_TOKEN` no `.env`
- **Repositório backup:** `https://github.com/LucianoAlf/openclaw-backup`
- **Permissão:** repo (leitura + escrita)
- **Push:** somente quando Alf solicitar explicitamente

---

## Telegram

- **Bot:** @lucianoalf_bot
- **Chat DM:** `telegram:1668476586`
- **Grupo HQ Alf:** ID `-1003663543711` (fórum com tópicos)
  - Tópico 2: sessão separada — contas pessoais/TickTick

---

## WhatsApp

- **Status:** ⏳ em configuração — aguardando número dedicado
- **Número Alf:** 5521981278047
- **Método:** OpenClaw plugin nativo (Baileys/WhatsApp Web)

---

## OpenAI (Embeddings)

- **Key:** `OPENAI_API_KEY` no `.env`
- **Modelo:** `text-embedding-3-small`
- **Uso:** memory_search (busca semântica nos arquivos de memória)
- **Custo:** ~$0,02/milhão de tokens — desprezível

---

## Instagram Graph API — LAHQ

- **Status:** ✅ credenciais disponíveis na VPS LAHQ
- **Arquivo:** `/home/lahq/.env`
- **School:** `IG_USER_ID_SCHOOL = 17841401761485758` + `IG_TOKEN_SCHOOL`
- **Kids:** `IG_USER_ID_KIDS = 17841404041835860` + `IG_TOKEN_KIDS`
- **App Meta:** `META_APP_ID` + `META_APP_SECRET`
- **Fluxo:**
  1. Upload da imagem → `POST /{ig-user-id}/media`
  2. Publicar → `POST /{ig-user-id}/media_publish`
- **Referência:** `scripts/tina.js` já implementa esse fluxo.
- **Regra:** publicação pública no Instagram sempre exige aprovação explícita do Alf antes de executar.

---

## Supabase LAHQ

- **Status:** ✅ fonte da verdade para LAHQ/Instagram/assets/outputs
- **Project ID:** `tmslaunhmjifsjvbizje`
- **URL:** `https://tmslaunhmjifsjvbizje.supabase.co`
- **Credenciais locais:** `.env` → `SUPABASE_LAHQ_URL`, `SUPABASE_LAHQ_PROJECT_ID`, `SUPABASE_LAHQ_ANON_KEY`, `SUPABASE_LAHQ_SERVICE_ROLE`, `SUPABASE_LAHQ_ACCESS_TOKEN`
- **Regra:** não salvar valores reais de keys/tokens em memória ou Git.
- **Decisão:** centralizar a frente LAHQ no Supabase LAHQ; o Supabase “Agente Alfredo” fica deprecated para esse domínio até migração/validação final.

---

## Infraestrutura VPS

- **Cloudflare Tunnel ID:** `2de0fe7b`
- **Domínio ativo:** `maestrosdagestao.com.br`
- **Dashboard:** `https://agent.maestrosdagestao.com.br`
- **⚠️ NÃO usar `latecnology.com.br`** — serviços críticos lá (n8n, NocoDB, webhooks)

---

_Atualizado: 2026-05-13_
