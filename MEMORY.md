# MEMORY.md — Índice Central do Alfredo 🎩

> Este é o único arquivo carregado automaticamente em toda sessão.
> Todos os outros são buscados sob demanda via `memory_search` + `memory_get`.

---

## Identidade

- **Eu:** Alfredo — assistente pessoal do Alf, parceiro, copiloto
- **Nascido:** 01/04/2026
- **Batizado por:** Luciano Alf na primeira conversa

## Quem é o Alf

- **Luciano Teixeira**, 48 anos, Rio de Janeiro (UTC-3)
- CEO e fundador da **LA Music** — 3 escolas de música no RJ
- 1.200+ alunos | 70+ colaboradores | 42 professores
- Músico, mentor, dev citizen, escritor, professor
- **Aniversário:** 25 de janeiro (1978)
- **Aniversário LA Music:** 23/07/2026 → 14 anos

## Canal Principal

- **Telegram:** @lucianoalf_bot (atual, mas pouco usado)
- **WhatsApp:** canal principal desejado — em configuração (5521981278047)
- **Anne** não usa Telegram — só WhatsApp

## Integrações Ativas

| Ferramenta | Status | Onde está |
|------------|--------|-----------|
| TickTick | ✅ Ativo | `.env` → `TICKTICK_TOKEN` | **Agenda principal do Alf** (não usa Google Calendar) |
| GitHub | ✅ Ativo | `.env` → `GITHUB_TOKEN` |
| OpenAI Embeddings | ✅ Ativo | `.env` → `OPENAI_API_KEY` |
| WhatsApp | ⏳ Pendente | Aguardando número dedicado |

## Regras Invioláveis

1. **Nunca subir `.env` pro GitHub**
2. **Nunca executar ação financeira** — só analisar e alertar
3. **Antes de compactação:** extrair lessons, decisions, people, projects, pending
4. **Decisões permanentes:** `memory/context/decisions.md`
5. **Se não está escrito, não existe**

## Projetos Ativos

| Projeto | Status | Arquivo |
|---------|--------|---------|
| LA Music Report | ✅ Produção | `memory/projects/la-music-report.md` |
| LA Studio Manager | 🔄 Dev ativo | `memory/projects/la-studio-manager.md` |
| SonoraMente LA | 🔄 Dev ativo | `memory/projects/sonoramaente-la.md` |
| LA DashFinance | 🔄 Dev ativo | `memory/projects/la-dashfinance.md` |
| LA MusicJourney | 🔄 Dev ativo | `memory/projects/la-music-journey.md` |
| Emusys Academy | 🔄 Pré-lançamento | `memory/projects/emusys-academy.md` |
| MusicFinance | ✅ Produção | `memory/projects/musicfinance.md` |
| LA Music Indica | 🔄 Dev ativo | `memory/projects/la-music-indica.md` |
| Ana Clara/Personal Finance | 🔄 Dev ativo | `memory/projects/ana-clara-personal-finance.md` |
| DriveCFO | ✅ Produção | `memory/projects/drive-cfo.md` |
| Backlog/Pausados | 💤 | `memory/projects/backlog.md` |

## Mapa de Memória (buscar sob demanda)

```
memory/
├── context/
│   ├── decisions.md        ← regras permanentes
│   ├── lessons.md          ← erros que não repetem
│   ├── people.md           ← equipe, família, parceiros
│   └── business-context.md ← LA Music, SonoraMente, Emusys
├── content/
│   ├── voice/
│   │   ├── instagram.md        ← tom de voz @lucianoalf.la
│   │   ├── emusys-academy.md   ← tom de voz mentoria
│   │   └── la-music.md         ← tom de voz LA Music
│   ├── ideas.md            ← ideias de conteúdo capturadas
│   └── drafts/             ← rascunhos de posts, scripts, newsletters
├── projects/             ← um arquivo por projeto ativo
├── sessions/             ← diário: YYYY-MM-DD.md
│   ├── 2026-04-01.md
│   ├── 2026-04-02.md
│   └── 2026-04-03.md
├── integrations/
│   ├── integrations-map.md ← ferramentas, IDs, endpoints
│   └── credentials-map.md  ← onde cada credencial fica
├── feedback/             ← approve/reject de sugestões
└── pending.md            ← aguardando ação
```

## O que Carregar em Cada Sessão

| Sempre carregado | Buscado sob demanda |
|-----------------|---------------------|
| SOUL.md | memory/context/*.md |
| USER.md | memory/projects/*.md |
| AGENTS.md | memory/sessions/ (hoje + ontem) |
| MEMORY.md (este) | memory/integrations/*.md |
| HEARTBEAT.md | memory/pending.md |

---

_Atualizado: 2026-04-03_

## Promoted From Short-Term Memory (2026-05-22)

<!-- openclaw-memory-promotion:memory:memory/2026-05-10.md:39:46 -->
- - **Repo `la-hq-agents` deve virar segundo cérebro operacional/skill da LA** — O repositório `https://github.com/LucianoAlf/la-hq-agents` contém design systems, brand guides, agentes e skills suficientes para virar uma skill OpenClaw (`la-hq-marketing` ou `la-design-system`) usada em carrosséis, posts, vídeos e pipelines de marketing. Data: 2026-05-10. - **Para produção visual premium, usar pipeline HTML/CSS + renderização, não imagem IA com texto final** — O teste mostrou que GPT Image 2 sozinho gera imagem bonita mas com cara de IA; melhor fluxo é Luna gerar assets/fotos e Diego montar texto/design em HTML/CSS seguindo Design System, renderizando PNG. Data: 2026-05-10. ### Lições aprendidas - NotebookLM MCP funciona no OpenClaw após autenticação: `notebooklm__notebook_list` retornou 66 notebooks (63 próprios, 3 compartilhados), validando acesso real. - OpenClaw/Alfredo consegue operar o fluxo NotebookLM → leitura/estruturação → copy/prompt → geração visual → entrega de imagens por Telegram/WhatsApp. - Para LA Music School, o DS principal usa: Pink `#E91E63`, Black `#0A0A0A`, Cream `#F5F1EC`, fonte display Bebas Neue uppercase, corpo Montserrat, faixa diagonal pink -8°, alternância Dark/Cream/Pink e CTA final. - O fluxo multiagente do repo pode ser simulado pelo Alfredo como papéis internos: Nina (direção/QA), Theo (copy), Luna (assets), Diego (HTML/render), Tina (publicação/preparo). Agentes separados só são necessários para escala/paralelismo/calendário. [score=0.857 recalls=7 avg=0.397 source=memory/2026-05-10.md:39-46]
<!-- openclaw-memory-promotion:memory:memory/sessions/2026-05-10.md:63:74 -->
- - Inclui `LAHQ_PIPELINE.md` com briefing, copy slide-a-slide, legenda Instagram e responsabilidades. - PNGs finais: `png/la-school-respiracao-rock-carousel-01.png` até `08.png`. - Preview grid: `preview-grid.jpg`. - Pacote completo: `/root/.openclaw/workspace/outputs/la-school-respiracao-rock-v3-LAHQ-carousel.tar.gz`. - QA final: PASS após ajuste no slide 06 (“Controle o ar antes do volume” / “Controle o ar no tempo”). ## Pacote oficial LA Music School DS/logos recebido - Alf enviou DS HTML v2 com Prompt embedada, 6 logos oficiais em XML/SVG e 3 artes oficiais de referência. - Arquivos salvos em `repos/la-hq-agents/shared/design-systems/la-music-school-v2/`. - Atualizado canônico: proibido usar logo fake em texto/box; próximos outputs devem usar SVG oficial da LA Music. - Regra extraída das 3 refs: logo oficial no topo; título grande sólido+outline; fundo musical escuro com overlay; halftone magenta; footer cápsula magenta com `@lamusicschool`. [score=0.842 recalls=6 avg=0.422 source=memory/sessions/2026-05-10.md:63-74]

## Promoted From Short-Term Memory (2026-05-22)

<!-- openclaw-memory-promotion:memory:memory/sessions/2026-05-04.md:1:46 -->
- # Sessão — 2026-05-04 ## CEO Quest — auditoria e hotfix do briefing matinal ### Problema identificado - o CEO Quest não tinha briefing matinal real próprio no tópico 218 - o que existia era um briefing operacional/pessoal (agenda + contas + semana) no tópico 2 + WhatsApp - isso criava desalinhamento entre a documentação do CEO Quest e o runtime da manhã ### Auditoria realizada Foram auditados: - `memory/governanca/ceo-quest-prd.md` - `memory/governanca/ceo-quest-skill.md` - `memory/governanca/ceo-quest-ticktick-map.md` - `memory/governanca/ticktick-execution-rules.md` - `memory/governanca/ticktick-capacidades.md` - `memory/governanca/ticktick-payload-patterns.md` - `memory/governanca/scorecard.md` - `memory/governanca/weekly-review.md` - crons ativos do OpenClaw ### Correções executadas - criado arquivo de auditoria: `memory/governanca/ceo-quest-auditoria-briefing-matinal-2026-05-04.md` - criado novo cron: `CEO Quest — Briefing matinal` - job configurado para: - seg–qui - 8h BRT - `sessionTarget: isolated` - entrega em `Telegram -1003663543711:topic:218` - sem WhatsApp - sem tópico 2 - prompt do cron reforçado para consultar explicitamente: - `ceo-quest-skill.md` - `streak.md` - `daily-log.md` - `weekly-review.md` - `ceo-quest-ticktick-map.md` - `ticktick-execution-rules.md` - `scorecard.md` - prompt do cron atualizado para consultar explicitamente projetos/listas do TickTick: - `🔥 CEO Quest` - `💼 Trabalho Operacional` - `💡 Mentorias` - `🏠 Pessoal Alf` - `💸 Contas Pessoais` - `🎬 Emusys Academy` [score=0.806 recalls=4 avg=0.559 source=memory/sessions/2026-05-04.md:1-46]
<!-- openclaw-memory-promotion:memory:memory/2026-05-11.md:565:580 -->
- - School logos oficiais: `shared/brand-assets/logos/school/`; nunca reconstruir logo digitando `LA`. - School refs ouro: `shared/design-systems/references/la-music-school-v2-gold/`. - Kids refs ouro: `shared/design-systems/references/la-music-kids-v2-gold/`. - Skill OpenClaw LAHQ deve apontar para arquivos canônicos e runbooks, não virar documentação duplicada. - Logo School deve entrar como composição variável, não watermark fixo/template: variar posição, escala, corte, opacidade, versão e função; QA reprova LA no mesmo lado/tamanho em vários cards. - Imagens não têm quantidade fixa: usar quantas a direção pedir, sem repetir fórmula visual. - Capa precisa vender o swipe; se tema pedir, usar foto hero forte. - Carrossel contínuo/emendado é recurso premium opcional, não padrão obrigatório. - QA final obrigatório: olhar preview grid como direção criativa e perguntar se parece campanha ou template, se capa dá vontade de passar e se faz o olho brilhar. ## LAHQ — Teste posture singer v6 - Alf pediu refazer o carrossel “postura de palco para cantor” para buscar nota 10. - Foram tentadas versões intermediárias v3/v4 e reprovadas internamente por ainda parecerem carimbo/template: rodapé repetido, setas/assinatura demais e marca pouco premium. - Versão entregue ao Alf: `/root/.openclaw/workspace/outputs/la-school-stage-posture-singer-test-v6/`. - Pacote entregue: `/root/.openclaw/workspace/outputs/la-school-stage-posture-singer-test-v6-carousel.tar.gz`. - Preview entregue: `/root/.openclaw/workspace/outputs/la-school-stage-posture-singer-test-v6/preview-grid.jpg`. [score=0.803 recalls=5 avg=0.410 source=memory/2026-05-11.md:565-580]

## Promoted From Short-Term Memory (2026-05-23)

<!-- openclaw-memory-promotion:memory:memory/sessions/2026-05-05.md:1:43 -->
- # Sessão — 2026-05-05 ## CEO Quest — refatoração do briefing matinal ### Decisão de produto O briefing matinal do CEO Quest foi refatorado para sair do modelo de 3 reinos fixos e migrar para um modelo mais aderente ao uso real do Alf. ### Novo modelo matinal - Streak - Hoje no tabuleiro - Pendência viva - Ação CEO do dia - Próxima ação - Performance ### Motivos - a vida do Alf é dinâmica demais para forçar 3 reinos toda manhã - os reinos continuavam bonitos como lore e leitura estratégica, mas pouco funcionais como molde diário obrigatório - o briefing precisava nascer do TickTick real, não de interpretação simbólica demais ### Documentação atualizada - `memory/governanca/ceo-quest-prd.md` - `memory/governanca/ceo-quest-skill.md` - `memory/governanca/ceo-quest-ticktick-map.md` - `memory/governanca/ceo-quest-refatoracao-plano-2026-05-05.md` - `memory/governanca/ceo-quest-arquitetura-runtime-whatsapp-2026-05-05.md` ### Runtime atualizado - cron `CEO Quest — Briefing matinal` passou a entregar no WhatsApp `5521981278047` - briefing matinal deixa de usar reinos fixos - briefing passa a consultar explicitamente docs centrais + TickTick ### Reorganização completa dos crons - trilha operacional pessoal formalmente separada da trilha CEO Quest - 7h = briefing operacional pessoal - 7h30 = pendências do dia anterior - 19h30 = fechamento operacional pessoal - 8h = briefing CEO Quest - 20h = fechamento CEO Quest - domingo 8h = ritual CEO Quest no WhatsApp - risk-check 19h do CEO Quest desativado para não competir com a noite operacional ### Documentação complementar criada [score=0.812 recalls=5 avg=0.407 source=memory/sessions/2026-05-05.md:1-43]

## Promoted From Short-Term Memory (2026-05-28)

<!-- openclaw-memory-promotion:memory:memory/2026-05-21.md:7:7 -->
- Decisão operacional aplicada: [score=0.894 recalls=0 avg=0.620 source=memory/2026-05-21.md:7-7]
<!-- openclaw-memory-promotion:memory:memory/2026-05-21.md:17:17 -->
- Correções aplicadas: [score=0.894 recalls=0 avg=0.620 source=memory/2026-05-21.md:17-17]
<!-- openclaw-memory-promotion:memory:memory/2026-05-21.md:22:22 -->
- Próximo teste correto: [score=0.894 recalls=0 avg=0.620 source=memory/2026-05-21.md:22-22]
<!-- openclaw-memory-promotion:memory:memory/2026-05-22.md:5:5 -->
- Alf avaliou o card/imagem do carrossel School respiração/canto V2 como “nota 10”. Este é marco importante após a crise do Mike: [score=0.894 recalls=0 avg=0.620 source=memory/2026-05-22.md:5-5]
<!-- openclaw-memory-promotion:memory:memory/2026-05-22.md:11:11 -->
- Lição: a melhoria veio menos de “mais prompt” e mais de processo criativo correto com veto antes do render. Guardar como evidência de que o pipeline por modos é o caminho oficial para Mike. [score=0.894 recalls=0 avg=0.620 source=memory/2026-05-22.md:11-11]

## Promoted From Short-Term Memory (2026-06-02)

<!-- openclaw-memory-promotion:memory:memory/sessions/2026-05-04.md:36:76 -->
- - `weekly-review.md` - `ceo-quest-ticktick-map.md` - `ticktick-execution-rules.md` - `scorecard.md` - prompt do cron atualizado para consultar explicitamente projetos/listas do TickTick: - `🔥 CEO Quest` - `💼 Trabalho Operacional` - `💡 Mentorias` - `🏠 Pessoal Alf` - `💸 Contas Pessoais` - `🎬 Emusys Academy` - disparo manual do cron feito para validação inicial - corrigido o bloco noturno do CEO Quest conforme regra oficial do Alf: - **19h BRT** = risk-check - **20h BRT** = close-day - criado arquivo de auditoria: `memory/governanca/ceo-quest-auditoria-ri[REDACTED_OPENAI_KEY].md` - risk-check reescrito para tom curto, natural e contextualizado no tópico 218 - close-day já alinhado para entregar fechamento visual do dia no tópico 218 ### Ajuste de expectativa - o hotfix principal do runtime foi aplicado - ainda será necessário observar a qualidade fina da saída nas próximas manhãs reais - o sistema ficou mais correto arquiteturalmente: briefing operacional pessoal continua separado do briefing CEO Quest ## TickTick — ajustes feitos hoje ### Reagendamento - `Fechamento do Q1 e premiação do programa Fideliza +` - movido de 2026-05-04 14h para 2026-05-05 14h ### Nova reunião criada - `Reunião com Anne Krissya — sucesso do cliente + retorno da Jéssica` - quinta-feira, 14h - checklist incluído - lembrete 30 min antes + na hora - nome corrigido de Anne Crícia para Anne Krissya ## Estado final da sessão - principal buraco do CEO Quest matinal corrigido no runtime - documentação da auditoria registrada - sessão registrada para memória futura [score=0.888 recalls=6 avg=0.435 source=memory/sessions/2026-05-04.md:36-76]
<!-- openclaw-memory-promotion:memory:memory/2026-05-01.md:1:20 -->
- ## 2026-05-01 18:59 UTC — CEO Quest / SonoraMente / TickTick ### Decisões permanentes - **CEO Quest deve respeitar estritamente a documentação e memória existente antes de propor qualquer estrutura nova.** - Por que: houve erro ao reinventar um sistema já desenhado e documentado em `memory/governanca/ceo-quest-*`, causando retrabalho e perda de confiança. - Data: 2026-05-01 - **Para cards TickTick com checklist, o padrão operacional é criar do zero via `POST /task` com estrutura completa, evitando remendos por update.** - Por que: updates/reaproveitamento causaram sobrescrita, perda de descrição e comportamento inconsistente; o padrão validado é recriar com `title + desc + items[]` e `content` só se necessário. - Data: 2026-05-01 - **Para cards operacionais do TickTick, o `desc` deve ser curto e visual (ex.: responsável + objetivo), e `items[]` deve carregar o checklist nativo.** - Por que: esse foi o formato que o app renderizou corretamente no caso validado pelo Alf. - Data: 2026-05-01 - **SonoraMente é uma Campanha do CEO Quest, não um projeto solto nem um Boss único.** - Por que: envolve múltiplas frentes paralelas e continuará após o MVP de 30/05. - Data: 2026-05-01 - **O marco de 30/05/2026 para SonoraMente é lançamento de MVP operacional validável, não operação clínica plena.** - Por que: evita misturar fase de validação com estrutura final multiprofissional e jurídica expandida. - Data: 2026-05-01 - **A operação inicial do SonoraMente dentro da LA Music Campo Grande é decisão estratégica de ecossistema, não improviso.** [score=0.866 recalls=5 avg=0.412 source=memory/2026-05-01.md:1-20]
<!-- openclaw-memory-promotion:memory:memory/2026-05-21.md:1:25 -->
- ## 2026-05-21 23:45 UTC — Mike piorou após tentativa: bloqueio emergencial Alf enviou novos prints/resultado do Mike e avaliou como “ainda pior, nota -1”. Concordância: as tentativas visuais do Mike entraram em loop de baixa qualidade; ele reconhece erros no texto, mas ainda não consegue transformar em peça visual School boa de forma autônoma. Decisão operacional aplicada: - Suspender entrega visual final autônoma do Mike para LA Music School até liberação explícita do Alf/Alfredo. - Mike não pode mais responder “feito” com PNGs/cards School renderizados sem preflight aprovado. - Novo fluxo obrigatório para School: 1. carregar skills/refs; 2. entregar somente preflight textual: tese criativa, copy card a card, direção de asset/foto/ilustração, wireframe/layout, riscos de reprovação; 3. aguardar aprovação explícita; 4. só então HTML/CSS/render; 5. se render < 9, não enviar como final. Correções aplicadas: - Commit `e307cb4 fix: suspende entrega visual School sem preflight`. - Atualizados `mike/AGENTS.md`, `skills/lahq-school-content/SKILL.md`, `docs/runbooks/LAHQ_SCHOOL_CARROSSEL.md`. - Mike sincronizado para `origin/main`; AGENTS live e skill live atualizados. Próximo teste correto: - Em sessão nova do Mike, pedir um carrossel School. - Esperado: Mike NÃO renderiza; entrega preflight textual e diz que não vai renderizar antes da aprovação da direção/copy porque o fluxo visual está em bloqueio de qualidade. [score=0.860 recalls=3 avg=0.784 source=memory/2026-05-21.md:1-25]

## Promoted From Short-Term Memory (2026-06-05)

<!-- openclaw-memory-promotion:memory:memory/2026-05-30.md:9:9 -->
- Manter o bridge, mas corrigir seu papel: ele deve ser porteiro/validador de segurança, não cérebro do atendimento nem porteira aberta. Arquitetura desejada: Chatwoot → bridge seguro → Sol decide intenção/risco → bridge envia ou cria nota interna. [score=0.874 recalls=0 avg=0.620 source=memory/2026-05-30.md:9-9]

## Promoted From Short-Term Memory (2026-06-06)

<!-- openclaw-memory-promotion:memory:memory/2026-05-30.md:12:14 -->
- Arquivo alterado no host da Sol: `/home/sol/.openclaw/workspace/scripts/chatwoot-sol-bridge.js`. Backup criado: `/home/sol/.openclaw/workspace/backups/chatwoot-sol-bridge.20260530-020625.js`. [score=0.893 recalls=0 avg=0.620 source=memory/2026-05-30.md:12-13]
<!-- openclaw-memory-promotion:memory:memory/2026-05-30.md:32:32 -->
- Testar em conversa pendente controlada: [score=0.893 recalls=0 avg=0.620 source=memory/2026-05-30.md:32-32]

## Promoted From Short-Term Memory (2026-06-07)

<!-- openclaw-memory-promotion:memory:memory/2026-06-01.md:3:3 -->
- > Registro criado no flush pré-compactação. Por instrução do runtime, tudo foi salvo somente neste arquivo, em vez de distribuir entre `memory/context`, `memory/projects`, `memory/pending` e `memory/sessions`. [score=0.879 recalls=0 avg=0.620 source=memory/2026-06-01.md:3-3]
<!-- openclaw-memory-promotion:memory:memory/2026-06-01.md:10:10 -->
- Construir uma base canônica de regras de negócio para LA Report/Sol, começando por Campo Grande/Maio 2026, reconciliando LA Report, Supabase, frontend, Emusys, CSVs, prints, Windsurf/Cascade e validação do Alf. [score=0.879 recalls=0 avg=0.620 source=memory/2026-06-01.md:10-10]
<!-- openclaw-memory-promotion:memory:memory/2026-06-01.md:23:23 -->
- Sistemas, CSVs, Supabase, LA Report, Emusys, prints e Cascade são evidências, mas a validação final de regra de negócio é do Alf. [score=0.873 recalls=0 avg=0.620 source=memory/2026-06-01.md:23-23]
<!-- openclaw-memory-promotion:memory:memory/2026-06-01.md:26:26 -->
- Durante auditoria: [score=0.873 recalls=0 avg=0.620 source=memory/2026-06-01.md:26-26]
