# Learnings — Alfredo

Correções, insights, lacunas de conhecimento e boas práticas.

Categorias: correction | insight | knowledge_gap | best_practice | workflow
Status: pending | resolved | promoted | wont_fix

---

## [LRN-20260522-001] workflow

**Logged**: 2026-05-22T13:29:45Z
**Priority**: high
**Status**: promoted
**Area**: workflow

### Summary
Copy técnica genérica não se resolve só com skill de escrita; precisa de pesquisa/conhecimento antes da copy.

### Details
Alf apontou que Mike e Alfredo falharam em copy por falta de conteúdo validável sobre o tema. A etapa correta é Research Gate → brief técnico → copy, especialmente para LA Music School.

### Suggested Action
Promovido em 2026-05-23 para `memory/context/lessons.md` e `skills/lahq-content-pipeline/SKILL.md`: Research Gate obrigatório antes de copy técnica LAHQ/School.

### Metadata
- Source: user_feedback
- Tags: lahq, copy, research-gate, mike, alfredo
---

## [LRN-20260529-001] workflow

**Logged**: 2026-05-29T06:30:00Z
**Priority**: high
**Status**: promoted
**Area**: sol-atendimento

### Summary
Sol deve traduzir regra administrativa/contratual em linguagem humana da LA, sem soar jurídica ou fria.

### Details
Alf refinou explicitamente que, mesmo quando a base for contrato/checklist, Sol não deve falar “pelo contrato” com cliente. Preferir: “nosso padrão de trabalho aqui é...”, “normalmente fazemos assim...” ou “a orientação da escola é...”, com proximidade, respeito, emoji moderado e escalação humana quando houver jogo de cintura.

### Suggested Action
Promovido em 2026-05-29 para `memory/context/lessons.md`: regra operacional de linguagem para atendimento Sol/LA Music.

### Metadata
- Source: user_feedback + Sol sync 2026-05-28/29
- Tags: sol, atendimento, contrato, linguagem-humana, la-music
---

## [LRN-20260530-001] workflow

**Logged**: 2026-05-30T06:30:00Z
**Priority**: high
**Status**: promoted
**Area**: sol-chatwoot-bridge

### Summary
Bridge Chatwoot/Sol precisa ser porteiro determinístico de segurança, não cérebro do atendimento nem porteira aberta baseada só em prompt.

### Details
Após teste real, a Sol respondeu externamente pelo WhatsApp com KPI interno da Barra (alunos/matrículas). Isso provou que decisão estruturada por LLM não basta para categorias críticas. O bridge deve bloquear por regra determinística dados internos/agregados, KPIs, faturamento, inadimplência, listas, rankings e assuntos sensíveis, criando nota interna/handoff em vez de resposta ao cliente.

### Suggested Action
Promovido em 2026-05-30 para `memory/context/lessons.md` e `memory/context/decisions.md`: guardrails determinísticos obrigatórios no bridge externo da Sol.

### Metadata
- Source: real Chatwoot/WhatsApp test + patch 2026-05-30
- Tags: sol, chatwoot, whatsapp, guardrails, internal-data, privacy, handoff
---

## [LRN-20260531-001] correction

**Logged**: 2026-05-31T06:30:00Z
**Priority**: medium
**Status**: pending
**Area**: la-organizer-positioning

### Summary
LA Organizer não deve ser interpretado como app pessoal do Alf; é um app de Governança e Organização Pessoal para colaboradores.

### Details
Alf corrigiu explicitamente a leitura quando foi mostrado o módulo de finanças pessoais. A feature de finanças pessoais deve ser entendida como benefício/camada de organização da vida do colaborador, não como financeiro da LA nem finanças pessoais do Alf. TOM já opera como camada conversacional/operacional dentro desse produto.

### Suggested Action
Manter como aprendizado de projeto por enquanto. Se aparecer de novo em PRD, pitch, UI ou arquitetura, promover para `memory/projects/la-organizer-*.md` como posicionamento canônico do produto.

### Metadata
- Source: user_correction + memory/sessions/2026-05-31.md
- Tags: la-organizer, tom, colaboradores, governanca, produto
---

## [LRN-20260601-001] workflow

**Logged**: 2026-06-01T06:30:00Z
**Priority**: high
**Status**: promoted
**Area**: communication-handoff

### Summary
Quando Alf envia prints/trechos em sequência ou pede prompt para Windsurf/Cascade/terceiros, Alfredo deve esperar o bloco, consolidar em uma mensagem única e separar destinatários.

### Details
Três feedbacks de 2026-05-31 apontaram o mesmo padrão: respostas picotadas atrapalham quando Alf precisa juntar contexto ou encaminhar instrução. Em auditorias e prompts técnicos, não misturar comunicação para ADMs/equipe com prompt para Cascade/Windsurf. Se ainda estiver chegando contexto, aguardar ou avisar curto que vai responder em bloco.

### Suggested Action
Promovido em 2026-06-01 para `memory/context/lessons.md`: consolidar mensagens encaminháveis e separar público operacional vs técnico.

### Metadata
- Source: memory/feedback/2026-05-31-*.md + sessão/auditoria LA Report
- Tags: comunicacao, handoff, windsurf, cascade, prints, contexto, mensagem-unica
---

