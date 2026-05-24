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
