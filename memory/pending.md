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


- [ ] **Mike OpenClaw — agente LAHQ** — Mike instalado na VPS LAHQ `srv1586784` como usuário `mike`, OpenClaw alinhado para `2026.5.4`, Telegram `@mike_lahq_bot`, runtime `openai-codex/gpt-5.5` via OAuth, repo/skills/memória/Supabase configurados. Allowlist Telegram de Alf/Yuri/John/Rayan aplicada. Em 2026-05-21 foi documentado e instalado o método técnico do Alfredo para carrosséis: `ALFREDO_CAROUSEL_METHOD.md`, `MIKE_DIVERGENCES_AND_FIXES.md`, `MIKE_VISUAL_WORKER.md`; worker visual assíncrono `mike-visual-worker.service` criado; `google-chrome-stable` instalado; teste `Respiração pra Rock` renderizou 8 PNGs + preview grid com match forte contra original. Pendências: testar uma criação nova ponta-a-ponta no Mike com prompt natural, preencher copy-ouro real e definir rotina segura para publicação/live.
- [ ] **LAHQ copy anti-IA / skill de copywriter** — Alf recebeu feedback de que a copy dos carrosséis está com “cara de IA”. Em 2026-05-20 foi instalada no Mike a skill consolidada `lahq-copywriting`, substituindo as duas skills antigas (`lahq-copy-redes-sociais` e `lahq-tom-de-voz`, arquivadas fora de `skills` em `/home/mike/.openclaw/workspace/archived-skills/copy-legacy-20260520T204132Z`). `lahq-copywriting` consolida copy visual + copy editorial + detector anti-IA + tom por marca. Pipeline/publication/school agora apontam para ela. Pastas `shared/copy-ouro/{school,kids,sonoramente}` criadas no repo LAHQ do Mike. Pendência: preencher banco real com 10–15 copies ouro publicadas, commitar `shared/copy-ouro` no repo LAHQ e testar se o Mike usa a nova skill antes de escrever carrossel.
- [ ] **Agente financeiro/Rose** — após Mike, preparar agente financeiro para apoiar conversa com Rose; escopo ainda a definir.

## LA Report / Sol — governança de snapshots mensais (2026-06-02)
- [ ] Classificar nominalmente pagantes financeiros por competência antes de aprovar MRR/ticket/faturamento: erro de cadastro, tipo_matrícula errado, fatura movida/removida, passaporte/início futuro, cortesia/bolsista/permuta/professor/estagiário ou pagante real.
- [ ] Revisar próximos entregáveis do Cascade/Windsurf sempre em modo SELECT-only antes de aprovar execution/migration.
- [ ] Fazer verificação leve dos meses anteriores antes de declarar histórico inteiro fechado.
- [ ] Auditar Barra/Recreio com SELECT-only antes de qualquer retificação.
- [ ] Corrigir/documentar bug Kids/School no frontend com regra temporal por competência.
- [ ] Desenhar Fase 3: snapshot imutável / fechamento mensal assinado para impedir nova contaminação.
- [ ] Junho/CG: após remoção das 22 movimentações inválidas, validar/reinserir apenas as 5 saídas reais com classificação correta (3 evasões + 2 não renovações), sem ressuscitar baixas antigas nem finalização de segundo curso.
- [ ] Junho/CG: auditar divergência entre `vw_kpis_gestao_mensal`, `dados_mensais` e cálculo frontend Kids/School antes de declarar painel correto.

## LA Report — não perder timing: auditoria `sem_parcela` + transferência Giane (2026-06-07)

Prioridade ativa. Não deixar sair do radar.

Estado atual:
- Zero UPDATEs de status/status_pagamento/tipo_matricula.
- Relatório v2 do Cascade melhorou e incorporou presenças, falsos positivos e foco em sync.
- Ajuste pendente importante: regra de **transferência interna não é evasão** precisa entrar antes de qualquer correção/modelagem.
- Caso Giane/Geane: matrícula 1026 CG teve saída/evasão lançada, mas ela continuou no Recreio matrícula 1723; isso é transferência CG → Recreio, não churn/evasão global LA.
- Próximo foco técnico: auditar edge function `processar-matricula-emusys`/sync para `status_pagamento`, contrato/renovação e vínculo por `emusys_matricula_id`/ID, não por nome.
- Próximo foco de regra: modelar `transferencia_unidade` separada de `evasao`/`nao_renovacao`, com impacto separado para unidade origem/destino e global LA.

## LA Report — sequência estratégica após sem_parcela/Fideliza (2026-06-07)

Alf reforçou que não quer se perder em bug pontual do Fideliza+ antes de resolver bases estruturais que alimentam o Fideliza e Report. Ordem estratégica acordada:
1. Governança `status_pagamento`: validação ADM dos casos, trava/aviso na UI, alerta de alteração em massa, dono do campo.
2. Transferência entre unidades: modelar categoria própria; não contar como evasão/churn global; auditar candidatos históricos.
3. Snapshot mensal `dados_mensais`: impedir overwrite de mês fechado, histórico/audit trail, P8/P11 SELECT-only antes de migration.
4. Financeiro por competência: separar ativo operacional, pagante contratual e pagante financeiro da competência.
5. Pendências de regra: taxa renovação com/sem aviso prévio, conversão geral, chave de pessoa.

Fideliza+ depende dessas bases: manter trimestral por regra, corrigir UI, mas adiar cálculo final enquanto transferência/snapshot/financeiro não estiverem alinhados.
