# Lições Aprendidas

> 🔒 Estratégicas = permanentes (padrões que sempre valem)
> ⏳ Táticas = expiram em 30 dias (workarounds, bugs, configs temporárias)

---

## 🔒 Estratégicas

### LAHQ School — design system não é checklist
2026-05-13: Alf corrigiu que a queda de qualidade veio também de não consultar de verdade o Design System visual/interativo da School para puxar componentes e elementos. Não basta usar cores, Prompt, logo e halftone. Antes de criar peças School, abrir as refs ouro + DS completo e extrair componentes concretos: grids, selos, barras, shapes, labels, diagonais, máscaras, ritmos, variações de card e regras de composição. Se a peça parece template genérico, é porque o DS não foi usado como biblioteca visual.


### Antes de qualquer mudança de DNS/nameservers
Checar todos os subdomínios e registros ativos. Perguntar ao Alf quais serviços dependem do domínio. Ter plano de rollback. **Origem:** incidente Cloudflare 01/04/2026 — derrubou n8n, NocoDB, webhooks críticos por horas.

### Credenciais nunca em chat
Se o usuário mandar token/senha no chat: salvar imediatamente no `.env`, alertar para revogar/trocar o token exposto, nunca deixar no histórico de mensagem.

### Alf é o piloto — a LA não voa sem ele
Aprendido da forma difícil em 2017. Não sugerir delegação total de gestão da LA para terceiros. Ele precisa estar no centro.

### A separação é feature, não bug
Cada sistema tem um domínio único. Não sugerir fusão de sistemas distintos. A fragmentação é intencional e estratégica.

### Nunca presumir o que Alf quer com ideia solta
Quando ele joga uma ideia no ar — perguntar: "Quer capturar pra depois ou já puxo o fio agora?" Nunca presumir que quer execução imediata.

### LAHQ School: skill não é enfeite, é processo obrigatório
Erro de 13/05/2026: Alfredo leu as skills, mas bypassou o workflow criativo e gerou carrossel técnico/E2E com qualidade baixa. Para LAHQ School, antes de registrar/publicar qualquer output: consultar runbook + DS canônico + refs ouro, montar direção Nina, copy Theo, composição Diego, e reprovar internamente se o QA não bater pelo menos 8,5. Teste E2E técnico não pode ser apresentado como peça criativa final.

### Mike/LAHQ: habilidade carregada não garante execução correta
2026-05-20/21: Mike tinha skills instaladas/ready, mas nem sempre elas entravam no prompt ou viravam método real. Em agente especializado, validar três camadas: skill existe, skill é carregada no contexto e o agente segue a ordem operacional. Para conteúdo School: carregar skill/runbook/DS/brand guide/refs, fazer preflight, montar HTML/CSS, renderizar e olhar preview grid antes de chamar de final.

### LAHQ School técnico: imagem precisa provar o assunto
2026-05-20: Em conteúdo técnico de guitarra/palhetada, Mike usou imagem com leitura de cantora/performance genérica. Isso destrói credibilidade. Foto bonita mas errada reprova. Palhetada precisa mostrar mão, palheta, cordas, braço do instrumento, gesto técnico, professor corrigindo ou recurso visual equivalente. Se não houver asset certo, dizer que não há asset certo e pedir/buscar/gerar dirigido.

### LAHQ carrossel: copy precisa ter arco, não cards soltos
2026-05-21: Alf rejeitou carrossel voz/palco por parecer template, com textos ruins e frases soltas. Antes de renderizar, a copy precisa formar campanha com tese → tensão → progressão → resolução → CTA. Se as lâminas parecem dicas independentes sem ligação narrativa, reprovar no preflight.

### LAHQ visual pesado bloqueia conversa se rodar no chat principal
2026-05-21: `image_generate`/render pesado deixou Mike em `blocked_tool_call` e travou o Telegram. Para agentes conversacionais, render/imagem/Chrome devem ir para worker assíncrono, subtarefa ou fila com status, nunca várias gerações pesadas diretas no chat principal.

---

## ⏳ Táticas (revisar/deletar após 30 dias)

### [2026-04-03] memory_search funciona nativamente
Desde março 2026, busca semântica não precisa de chave externa. A OpenAI configurada no `.env` deixa os embeddings mais precisos, mas não é obrigatória.

---


### LAHQ School: Research Gate antes de copy técnica
2026-05-23: Feedback recorrente do Alf/Mike mostrou que copy técnica genérica nasce de falta de pesquisa, não só de escrita fraca. Para conteúdo School técnico (guitarra, canto, palco, performance, estudo), a ordem obrigatória é: pesquisar/reunir base técnica validável → transformar em brief técnico → escrever copy com arco → preflight → render. Se o tema envolver técnica específica e não houver repertório/fonte/asset que prove o assunto, não improvisar frase bonita: pesquisar mais, declarar lacuna ou pedir direção.

### LAHQ entrega visual: validar em alta, não por screenshot
2026-05-23: Preview grid serve para visão geral, não para validar qualidade final. Carrosséis/render LAHQ precisam entregar PNGs individuais em alta resolução + pacote `.tar.gz`/`.zip`; screenshot comprimido de Telegram/WhatsApp não prova nitidez, legibilidade mobile ou acabamento. QA final deve olhar arquivos exportados reais.

*Revisão mensal: deletar táticas vencidas.*
*Última atualização: 2026-05-23*

## 2026-05-24 — Nubank vence dia 21
- Não repetir o erro: Cartão Nubank do Alf vence todo dia **21**. O TickTick estava cadastrado como dia 22 e isso induziu resposta errada. Corrigido no TickTick para recorrência mensal no dia 21.

## 2026-05-24 — Não chamar vencimento futuro de aberto/vencido
- Regra operacional: em contas do TickTick, item com vencimento futuro é **próximo vencimento**, não “aberto”, “pendente de ontem” nem “vencido”. Só classificar como atrasado depois da data/hora de vencimento no timezone `America/Sao_Paulo`.

## 2026-05-29 — Sol: contrato duro, linguagem humana
- Não repetir linguagem jurídica/fria no atendimento da LA. Mesmo quando a base for contrato/checklist, Sol deve evitar “pelo contrato”. Preferir “nosso padrão de trabalho aqui é...”, “normalmente fazemos assim...” ou “a orientação da escola é...”, com proximidade, respeito, emoji moderado e escalação humana quando houver jogo de cintura.

## 2026-05-30 — Sol/Chatwoot: prompt não é guardrail suficiente para dado interno
- Não repetir o erro: em teste real, a Sol respondeu externamente no WhatsApp com KPI interno da unidade Barra. Para canais externos, decisão estruturada da LLM ajuda, mas não pode ser a única barreira. O bridge precisa bloquear por regra determinística pedidos de alunos/matrículas/pagantes/ativos, KPIs, faturamento, inadimplência, listas, rankings, scores e dados internos/agregados, forçando nota interna/handoff humano.

## LA Report — cuidado com banco legado e fonte canônica

- O LA Report nasceu com dados históricos normalizados/importados para comparação de início de ano e evoluiu para sistema central; por isso o banco mistura legado, snapshots e dados atuais.
- Nunca assumir que uma tabela/view é fonte canônica só porque existe no Supabase.
- `dados_mensais`, `evasoes_v2` e migrations antigas podem estar defasadas ou parcialmente abandonadas.
- Para regras de negócio da Sol/LA Report, Alf é a fonte final; banco/frontend/Windsurf/equipe são evidências a cruzar.
- Antes de criar skill canônica, validar regra por unidade e marcar status: canônica, dúvida, divergente ou legado.

## 2026-06-01 — Sol precisa auditar inconsistências, não só responder consulta

Auditoria CG/Maio provou que números oficiais da equipe podem estar contaminados por duplicidade, bolsista/professor marcado como pagante, faturas removidas, aluno novo com passaporte e pagamento no mês seguinte, curso divergente e aluno ativo sem frequência/pagamento. Alf perdeu tempo de CEO fazendo auditoria manual. Regra: projetos da Sol/LA Report devem priorizar cruzamento automático de Emusys + LA Report + faturas + presença + tipo de matrícula, gerando alertas nominais para equipe corrigir. Não confiar cegamente em `valor_parcela`, `conta_como_pagante` ou número informado por equipe.

## 2026-06-01 — Não responder picotado quando o Alf está agrupando contexto

Quando Alf enviar sequência de prints, SQLs, relatórios ou trechos para análise, não responder cada fragmento isolado. Aguardar o bloco, integrar do começo ao fim e responder consolidado. Se parecer que ainda vem mais coisa, avisar curto: “vou juntar tudo e responder em bloco”. Para prompts ao Windsurf/Cascade/Claude Code ou mensagens que o Alf precisa encaminhar, entregar uma única mensagem limpa e copiável. Separar sempre o destinatário: prompt técnico para ferramenta/dev não deve misturar justificativa operacional para ADMs/equipe.

## 2026-06-01 — Nomes corretos: LA Report e Cascade

Correção do Alf: não chamar o sistema de “LAHQ” neste contexto. O sistema correto é **LA Report**. O agente/dev no Windsurf é **Cascade**, não “Mutsaf”. Ao preparar mensagem técnica sobre investigação de aluno/ticket/migração financeira, endereçar para o Cascade do Windsurf e citar LA Report.

## 2026-06-02 — LA Report: não recalcular histórico com cadastro vivo

Não repetir o erro arquitetural que contaminou CG/Maio: mês fechado é fotografia histórica, não espelho do cadastro atual. Cron/função que recalcula `dados_mensais` com `alunos.status` vivo pode mudar números passados quando alunos são ajustados depois. Para restaurar mês fechado, usar fonte forense confiável (`audit_log`/snapshot anterior), retificação controlada, rollback e auditoria nominal. Não rodar backfill ou Barra/Recreio antes de fechar uma unidade/mês com SELECT-only.

## 2026-06-02 — LA Report: separar pessoa, matrícula, banda e segundo curso

Não misturar domínios: alunos ativos/pagantes são pessoas; matrículas/banda/segundo curso são linhas. Banda/projeto não é segundo curso financeiro. `valor_parcela > 0` não pode ser filtro global de pagante, porque há passaporte, mensalidade futura, fatura movida e bugs de sincronização; `conta_como_pagante=true` também exige classificação correta de bolsista/professor/estagiário/permuta. Duplicidades e sujeiras devem virar alertas nominais, não hardcode por nome.
