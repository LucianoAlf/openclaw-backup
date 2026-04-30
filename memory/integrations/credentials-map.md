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

## Regras

- Nunca colocar valores reais aqui — só o nome da variável
- Valores ficam APENAS no `.env` (chmod 600)
- `.env` nunca vai pro GitHub (`.gitignore` cobre)
- Se token for exposto em chat: revogar imediatamente e gerar novo

---

*Última atualização: 2026-04-03*
