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
| TickTick | ✅ Ativo | `.env` → `TICKTICK_TOKEN` |
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
│   └── voice/
│       ├── instagram.md        ← tom de voz @lucianoalf.la
│       ├── emusys-academy.md   ← tom de voz mentoria
│       └── la-music.md         ← tom de voz LA Music
├── projects/             ← um arquivo por projeto ativo
├── sessions/             ← diário: YYYY-MM-DD.md
│   ├── 2026-04-01.md
│   ├── 2026-04-02.md
│   └── 2026-04-03.md
├── integrations/
│   └── integrations-map.md ← IDs, tokens, endpoints
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
