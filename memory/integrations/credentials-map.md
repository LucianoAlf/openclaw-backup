# credentials-map.md — Onde Cada Credencial Fica

> Mapa de ONDE estão as credenciais — não os valores. Valores ficam no `.env`.

---

| Credencial | Variável no .env | Onde conseguir |
|------------|-----------------|----------------|
| Anthropic API Key | `ANTHROPIC_API_KEY` | console.anthropic.com |
| OpenAI API Key (embeddings) | `OPENAI_API_KEY` | platform.openai.com |
| TickTick Token | `TICKTICK_TOKEN` | developer.ticktick.com |
| GitHub Token | `GITHUB_TOKEN` | github.com → Settings → Developer settings |
| Gateway Token | (no openclaw.json) | `openclaw config get gateway.auth.token` |
| Instagram School User ID | `IG_USER_ID_SCHOOL` | `/home/lahq/.env` na VPS LAHQ |
| Instagram Kids User ID | `IG_USER_ID_KIDS` | `/home/lahq/.env` na VPS LAHQ |
| Instagram School Token | `IG_TOKEN_SCHOOL` | `/home/lahq/.env` na VPS LAHQ |
| Instagram Kids Token | `IG_TOKEN_KIDS` | `/home/lahq/.env` na VPS LAHQ |
| Meta App ID/Secret | `META_APP_ID`, `META_APP_SECRET` | `/home/lahq/.env` na VPS LAHQ |
| Supabase LAHQ URL/Project | `SUPABASE_LAHQ_URL`, `SUPABASE_LAHQ_PROJECT_ID` | `.env` local / painel Supabase LAHQ |
| Supabase LAHQ Keys | `SUPABASE_LAHQ_ANON_KEY`, `SUPABASE_LAHQ_SERVICE_ROLE`, `SUPABASE_LAHQ_ACCESS_TOKEN` | `.env` local / painel Supabase LAHQ |

## Regras

- Nunca colocar valores reais aqui — só o nome da variável
- Valores ficam APENAS no `.env` (chmod 600)
- `.env` nunca vai pro GitHub (`.gitignore` cobre)
- Se token for exposto em chat: revogar imediatamente e gerar novo

---

*Última atualização: 2026-05-13*
