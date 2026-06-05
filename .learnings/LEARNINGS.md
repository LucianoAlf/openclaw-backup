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


## [LRN-20260602-001] workflow

**Logged**: 2026-06-02T06:30:00Z
**Priority**: high
**Status**: promoted
**Area**: la-report-kpi-governance

### Summary
LA Report não pode recalcular mês fechado com tabela viva; fechamento mensal é snapshot histórico/forense e retificação exige controle explícito.

### Details
Auditoria CG/Maio mostrou que cron legado sobrescreveu `dados_mensais` usando estado atual/cadastro vivo, contaminando histórico. A restauração correta veio do `audit_log`/old_record, com retificação escopada, transação, exatamente 1 linha afetada, registro de auditoria, rollback e preservação financeira. Também ficou consolidado que métricas de alunos ativos/pagantes são por pessoa, enquanto matrículas/banda/segundo curso são por linha, e banda/projeto não é segundo curso financeiro.

### Suggested Action
Promovido em 2026-06-02 para `memory/context/decisions.md` e `memory/context/lessons.md`: governança permanente de snapshot histórico, retificação controlada e separação pessoa vs matrícula no LA Report/Sol.

### Metadata
- Source: memory/2026-06-01.md + memory/2026-06-02.md + Dreaming 2026-06-02
- Tags: la-report, sol, dados-mensais, snapshot, kpi, retificacao, cascade, windsurf
---

## [LRN-20260603-001] workflow

**Logged**: 2026-06-03T06:30:00Z
**Priority**: high
**Status**: promoted
**Area**: la-report-financial-competence

### Summary
LA Report/Sol precisa separar ativo operacional, pagante contratual e pagante financeiro da competência antes de migrar MRR/ticket/faturamento.

### Details
Auditorias CG/Maio e Junho mostraram que `conta_como_pagante`, `valor_parcela`, faturas Emusys, passaporte, início real, bolsistas/permutas/professores/estagiários e alunos com pagamento adiado podem divergir. Um aluno pode estar ativo e contratualmente pagante, mas não compor o financeiro daquela competência; também pode haver fatura paga mesmo com `valor_parcela` zerado no LA Report. Financeiro não deve virar migration/backfill enquanto houver lista nominal sem classificação.

### Suggested Action
Promovido em 2026-06-03 para `memory/context/decisions.md` e `memory/context/lessons.md`: separar KPIs operacionais/contratuais/financeiros e bloquear migration financeira sem reconciliação nominal por competência.

### Metadata
- Source: memory/2026-05-31.md + memory/2026-06-02.md + Dreaming 2026-06-03
- Tags: la-report, sol, financeiro, competencia, mrr, ticket-medio, faturas, emusys
---

## [LRN-20260604-001] workflow

**Logged**: 2026-06-04T06:30:00Z
**Priority**: high
**Status**: promoted
**Area**: la-report-evasoes-competencia

### Summary
LA Report/Sol não pode contar evasão pela data em que o registro caiu no sistema; precisa distinguir data de lançamento/importação, data real da saída e natureza da saída.

### Details
Auditoria Junho/CG mostrou 22 movimentações lançadas em 01/06 como `evasao`. Validação nominal da Gabi mostrou que só 5 eram saídas reais de junho; 16 já tinham saído antes, 1 caiu agora mas saiu em outro mês, e Rayane não saiu da escola — era finalização de segundo curso. Gabi removeu as 22 inválidas; a correção segura exige reinserir/registrar só as 5 reais, classificando 3 evasões e 2 não renovações.

### Suggested Action
Promovido em 2026-06-04 para `memory/context/decisions.md` e `memory/context/lessons.md`: data de lançamento/importação não define competência de evasão; finalização de segundo curso não é evasão da escola; mês corrente usa corte operacional `CURRENT_DATE` quando o modo for tempo real.

### Metadata
- Source: memory/.dreams/session-corpus/2026-06-02.txt + DREAMS 2026-06-04 + validação Gabi/Cascade
- Tags: la-report, sol, evasao, nao-renovacao, competencia, data-real-saida, segundo-curso
---

## [LRN-20260604-002] correction

**Logged**: 2026-06-04T06:30:00Z
**Priority**: high
**Status**: promoted
**Area**: communication-handoff

### Summary
Não inventar destinatário/pessoa em prompt encaminhável. Se Alf pede Cascade/Windsurf, endereçar apenas ao Cascade/Windsurf.

### Details
Alf corrigiu com força quando Alfredo escreveu “Hugo” num texto que deveria ser prompt para Cascade/Windsurf. Esse erro repete a classe já consolidada em 2026-06-01: misturar destinatário e tornar a mensagem não encaminhável. A regra agora fica mais explícita: nunca introduzir nome de pessoa/dev/equipe que não veio do pedido atual ou da fonte confirmada.

### Suggested Action
Promovido em 2026-06-04 para `memory/context/lessons.md`, reforçando a lição de comunicação/handoff e a regra “LA Report + Cascade”.

### Metadata
- Source: memory/.dreams/session-corpus/2026-06-02.txt
- Tags: cascade, windsurf, comunicacao, destinatario, prompt-encaminhavel, erro
---

