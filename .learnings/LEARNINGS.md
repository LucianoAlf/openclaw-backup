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
