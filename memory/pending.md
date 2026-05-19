# Pendências

> Itens aguardando input, acesso ou decisão.

---

## Aguardando Alf

- [ ] **LAHQ segundo cérebro + rede de agentes** — retomar amanhã com revisão de arquitetura antes de executar. Pontos já corrigidos pelo Alf: Mike não pode ficar só com skills School; precisa contemplar também LA Music Kids e SonoraMente futuro; revisar catálogo completo de skills antes de migrar Mike/agents para OpenClaw; evitar arquitetura capenga que depois gere problema.
- [ ] **WhatsApp** — número dedicado (chip/eSIM) para conectar no OpenClaw. Número pessoal Alf: 5521981278047
- [x] **Agenda** — TickTick é a agenda do Alf (não Google Calendar)
- [x] **Crons TickTick (grupo HQ Alf)** — revisados e endurecidos para consulta real à API do TickTick, com timezone America/Sao_Paulo e regra explícita de não inventar resposta (2026-05-04)
- [ ] **Projetos ativos** — atualizar status de cada projeto em `memory/projects/` com detalhes mais precisos (roadmap, próximos passos reais)

## Aguardando Terceiros

- [ ] **Canva Connect API** — integração no LA Studio Manager aguardando Canva liberar acesso/documentação

---

## ✅ Resolvido Recentemente

- [x] TickTick integrado via API (2026-04-03)
- [x] Estrutura de memória em camadas implementada (2026-04-03)
- [x] Cloudflare Tunnel + dashboard configurado (2026-04-01)
- [x] Hardening VPS completo (2026-04-01)

---

*Última atualização: 2026-05-15*

## Rotação de credenciais pós-audit — 2026-05-18
Status: pendente, mas não bloquear Alf agora.
Contexto: Alf pediu para não deixar a rotação depender dele no fluxo atual; ele disse que faz depois. Manter como pendência visível e lembrar depois.
Credenciais/ações:
- Gerar novo GitHub PAT, atualizar `GITHUB_TOKEN`, `gh auth`, e fazer push force-with-lease do histórico limpo do repo `openclaw-backup`.
- Gerar nova OpenAI API key e atualizar `.env`/memory embedding provider.
- Rotacionar TickTick token via OAuth/app setup.
- Rotacionar Pluggy client secret/API key/items se aplicável.
- Rotacionar Supabase access tokens/service_role/anon keys dos projetos Alfredo e LAHQ.
- Após rotação: novo scan de secrets e `openclaw security audit`.


- [ ] **Mike/Hermes — primeiro agente LAHQ** — criar/planejar amanhã o Mike como agente OpenClaw/Hermes com as habilidades de marketing já desenvolvidas no Alfredo: carrosséis, artes, design systems, refs ouro, copy/publicação e conexão ao segundo cérebro LAHQ. Prioridade antes de Sol/Fábio/Tom/Maria. Alfredo deve coordenar a arquitetura.
- [ ] **Agente financeiro/Rose** — após Mike, preparar agente financeiro para apoiar conversa com Rose; escopo ainda a definir.
