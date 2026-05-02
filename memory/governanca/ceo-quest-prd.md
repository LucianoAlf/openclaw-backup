# PRD — CEO Quest

**Sistema de Governança Pessoal Gamificado**

---

## Metadados

| Campo | Valor |
|---|---|
| Nome do produto | CEO Quest |
| Versão do PRD | 1.0 |
| Data | 1 de maio de 2026 |
| Owner | Luciano Alf (CEO LA Music) |
| Stakeholders | Luciano Alf (único usuário) |
| Status | Aprovado para implementação |
| Repositório | github.com/LucianoAlf/ceo-quest *(a criar)* |

---

## 1. Visão do Produto

### 1.1 O que é

CEO Quest é um sistema de governança pessoal gamificado, single-user, criado para um perfil específico de CEO: empreendedor, dev, músico, alérgico a rotina formal, motivado por desafio.

O sistema transforma os comportamentos críticos de gestão (cobrança sistemática, revisitação de entregas, presença consistente com o time) em mecânicas de jogo (XP, streaks, ranks, Boss Battles, Campanhas) — preservando a alma criativa do empreendedor enquanto cultiva o administrador interno.

### 1.2 O que NÃO é

- Não é um sistema corporativo de gestão
- Não é módulo do LA Organizer (sistema voltado pra colaboradores da LA)
- Não é multi-tenant ou multi-usuário
- Não é um app de produtividade genérico
- Não é um substituto pra TickTick (é uma camada acima)

### 1.3 Por que existe (o problema)

O Luciano Alf construiu uma empresa de 14 anos, 3 unidades, 1.200+ alunos, 70+ funcionários, faturamento ~R$ 500k/mês. Mas opera ainda como CEO de garagem:

- Sabe tudo o que precisa ser feito, mas vive na cabeça
- Cobra apenas quando lembra
- Delega sem revisitar sistematicamente
- Tem aversão a rotina formal (já abriu mão de R$ 20k/mês de mentorias por isso)
- Vive 8-10h/dia em rotina natural quando o trabalho é game (codar, criar sistemas)

**Diagnóstico:** o problema não é capacidade, é interface. Sistemas tradicionais de gestão não funcionam para esse perfil. O empreendedor precisa ser provocado pelo jogo, não obrigado pela rotina.

### 1.4 Para quem é

**Usuário único e exclusivo:** Luciano Alf.

CEO Quest é projetado pra resolver os gaps específicos desse usuário, não pra ser produto comercial. Decisões de design devem priorizar adequação ao perfil dele sobre genericidade.

### 1.5 Princípios fundadores

1. **O jogo premia o que custa fazer** (cobrar, revisitar) — não o que dá prazer natural (criar)
2. **Alfredo é Game Master** — não é Chief of Staff que terceiriza cobrança, é provocador que mantém o jogo vivo
3. **Honestidade comigo mesmo é a base** — sem evidência concreta, ação não conta
4. **MVP enxuto, evolução em camadas** — coração primeiro (streak), decoração depois
5. **Sistema vira identidade** — o objetivo não é usar o sistema, é virar outro CEO

### 1.6 Visão de longo prazo

Em 12 meses, CEO Quest deve ter:

- Levado o Luciano Alf de Rank 1 (Garagem) até Rank 3 (Maestro)
- Tornado revisão semanal de entregas um hábito natural (não tarefa)
- Reduzido em 70% o número de combinados que morrem na cabeça
- Validado o modelo a ponto de poder ser eventualmente generalizado pra outros CEOs (decisão de produto a ser tomada no futuro)

---

## 2. Requisitos Funcionais

### 2.1 Streak (coração do sistema)

**RF-001 — Detector de ação CEO**
O sistema deve detectar automaticamente, nas mensagens trocadas entre Alf e Alfredo, quando há uma ação CEO sobre alguém do círculo de responsabilidade.

**RF-002 — Validação por evidência concreta**
Apenas ações com evidência registrada contam. Pensamentos, intenções e conversas não registradas não contam.

**RF-003 — Cinco tipos válidos de evidência**
- Áudio/mensagem ENVIADA com cobrança/verificação/direção
- Tarefa criada/atualizada no TickTick + cobrança comunicada
- Decisão registrada que destrava alguém
- Conversa presencial registrada (o que cobrou + com quem + prazo)
- Reunião 1:1 com pauta + saída concreta (bônus +2 XP)

**RF-004 — Círculo de responsabilidade**
Define quem conta como "alguém do time" para fins de streak:
- Funcionários diretos
- Líderes e gestão
- Sócios com função operacional (Anne)
- Coordenadora SonoraMente (Bianca)
- Mentor-fundadores em projetos pagos
- Mentorados em programa pago ativo

**RF-005 — Cobrança real**
Para contar como ação CEO, a interação precisa ter pelo menos 1 destes 3 elementos:
- Verbo de exigência/verificação direto
- Prazo explícito comunicado à pessoa
- Verificação objetiva de status

**RF-006 — Verificação noturna**
Diariamente às 20h, o sistema deve verificar se houve ação CEO no dia e atualizar a streak.

**RF-007 — Alerta de risco**
Diariamente às 19h, se nenhuma ação CEO foi registrada, o sistema deve enviar alerta com 3 opções:
- Mandar áudio agora
- Registrar ação que aconteceu offline
- Aceitar pausa (com motivo)

**RF-008 — Pausa vs Quebra**
- **Pausa:** comunicada antes ou no dia, motivo extraordinário, máx 5 dias por trimestre, streak congela
- **Quebra:** silêncio, esquecimento, escolha sem aviso, streak zera

**RF-009 — Fim de semana**
- **Sábado:** streak congela. Não pontua e não quebra.
- **Domingo:** ritual de domingo conta como ação CEO se realizado.

**RF-010 — Marcos de streak**
Sistema deve celebrar marcos: 7, 14, 30, 60, 100 dias com mensagem dedicada e bônus de XP.

### 2.2 Briefing matinal

**RF-011 — Briefing diário (seg-quinta)**
Diariamente às 8h da manhã (segunda a quinta), o sistema deve enviar mensagem no tópico CEO Quest com:
- Streak atual em destaque
- Resumo de 3 reinos prioritários (Pessoal, Pedagógico, Comercial+Marketing) — 1 linha cada
- Ação concreta sugerida (de 30 segundos)
- Convite "Bora?" no final

**RF-012 — Quick check de sexta**
Sexta-feira, formato diferenciado:
- Resumo da semana
- Pendência crítica única
- Pergunta de honestidade: "foi CEO presente essa semana?"
- Ação de fim de semana

**RF-013 — Convite de domingo**
Domingo 8h, convite para Ritual da Virada com tempo estimado e camadas.

**RF-014 — Sábado silencioso**
Sábado não envia briefing. Descanso é parte do jogo.

### 2.3 Ritual de domingo

**RF-015 — Estrutura em 3 camadas**
- **8h-9h** — Pessoal (corpo + mente): academia, meditação, leitura
- **9h-9h30** — Fechamento: 5 perguntas pessoais + 5 perguntas CEO (versão completa: 7+7)
- **9h30-10h** — Planejamento: hábitos da semana + 3 prioridades por frente

**RF-016 — Condução por áudio**
Alfredo conduz o ritual uma pergunta por vez. Alf responde por áudio. Sistema registra.

**RF-017 — Geração de weekly review**
Ao final do ritual, sistema gera arquivo `weekly-review-YYYY-MM-DD.md` com todas as respostas + métricas + 3 prioridades.

### 2.4 Feedback diário e acompanhamento

**RF-018 — Fechamento diário oficial**
Diariamente às 20h, o sistema deve entregar um fechamento do dia com:
- quest principal do dia
- status da quest
- progresso percentual por checklist
- o que avançou
- o que travou ou ficou pendente
- status das campanhas
- próxima ação obrigatória
- provocação final
- validação ou não da presença CEO

**RF-019 — Consulta sob demanda**
Quando Alf perguntar sobre uma tarefa, frente, Boss ou Campanha, o sistema deve responder com:
- status atual
- barra de progresso
- itens concluídos
- itens pendentes
- leitura objetiva do prazo
- próxima ação concreta

**RF-020 — Regra oficial de percentual**
O percentual oficial do CEO Quest deve ser calculado por checklist simples:
- itens concluídos / itens totais = progresso

**RF-021 — Status oficiais de andamento**
O sistema deve usar 5 status oficiais:
- ON FIRE
- ON TRACK
- EM RISCO
- ATRASADA
- TRAVADA

### 2.5 Sistema de XP e Ranks

**RF-022 — XP por categoria**
Cada ação gera XP em uma categoria específica:
- 🎓 XP Pedagógico
- 💰 XP Comercial
- 🌱 XP Pessoal
- 🐉 XP Boss Battle
- ⚡ XP CEO Geral

**RF-023 — Faixas de pontuação**
- Pontos fáceis (manutenção): 1-3 XP
- Pontos médios (cobrança): 5-10 XP
- Pontos pesados (governança real): 15-25 XP
- Pontos raros (level up): 50+ XP
- Penalidades: -5 a -15 XP

**RF-024 — Progressão de ranks (musical)**
1. 🎸 Garagem (0-500 XP)
2. 🎤 Bandleader (501-1.500)
3. 🎹 Maestro (1.501-3.500)
4. 🏗️ Arquiteto (3.501-6.000)
5. 👑 Fundador-CEO (6.001-10.000)
6. 🌍 Visionário (10.001-15.000)
7. 🚀 Legado (15.001+)

**RF-025 — Critério de subida de rank**
Subir de rank exige 3 critérios juntos:
- XP mínimo do rank
- Streak mínimo de CEO Quest
- Pelo menos 1 Boss Battle concluído

### 2.6 Boss Battles e Campanhas

**RF-026 — Critério de Boss Battle**
Algo só vira Boss se bater os 4 critérios:
1. Muda o patamar da empresa
2. Dura 4+ semanas
3. Tem 3+ fases sequenciais
4. Tem risco real se não acontecer

**RF-027 — Limite de Boss Battles ativos**
Máximo 3 Boss Battles ativos simultaneamente.

**RF-028 — Critério de Campanha**
Algo vira Campanha se bater os 4 critérios:
1. Dura 3+ meses
2. Contém 3+ Boss Battles internos
3. Tem múltiplas frentes paralelas
4. Muda identidade ou modelo de negócio

**RF-029 — Limite de Campanha ativa**
Máximo 1 Campanha ativa por vez.

**RF-030 — Cerimônia de ativação**
Boss/Campanha novo gera mensagem cerimonial com nome, fases, dono, XP, badge previsto.

**RF-031 — Cerimônia de pausa/cancelamento**
Boss/Campanha pode ser pausado ou cancelado sem culpa, com mensagem cerimonial registrando motivo + aprendizado.

### 2.7 Conquistas (Badges)

**RF-032 — Sistema de badges**
Sistema deve desbloquear conquistas ao bater marcos específicos:
- 🎯 Primeira semana completa
- 🔥 Streak de 4, 8, 12, 30 semanas
- 💪 Centurião (100 tarefas no prazo)
- 🎯 Sniper (20 tarefas seguidas no prazo)
- 🐉 First Blood (1º Boss concluído)
- ⚔️ Boss Rush (2 Boss no mesmo mês)
- 🏰 Dungeon Master (5 Boss no total)
- 👑 Fundador-CEO (chegou no Nível 5)

### 2.8 Loots Reais

**RF-033 — Definição de Loot Real**
Alf define recompensa concreta no início de cada quest/Boss/marco:
- Equipamento musical
- Jantar especial
- Final de semana fora
- Tempo livre sem culpa

**RF-034 — Cobrança de Loot**
Quando marco é atingido, sistema lembra do Loot definido e provoca a auto-cobrança.

### 2.9 Painel Visual (Web App)

**RF-035 — Dashboard principal**
Tela inicial mostra:
- Streak grande no centro
- Rank atual com identidade visual
- XP total e por categoria
- Boss Battles ativos com barras de progresso
- Campanha atual com cronograma
- Conquistas recentes
- Loot pendente

**RF-036 — Histórico**
Visualização de evolução temporal:
- Streak ao longo dos meses
- XP por semana
- Boss Battles concluídos
- Conquistas desbloqueadas

**RF-037 — Detalhe por reino**
Drill-down em cada um dos 8 reinos com:
- Tarefas pendentes
- Pessoas-chave do reino
- XP acumulado
- Próximas ações sugeridas

**RF-038 — Tabuleiro do jogo**
Visualização gamificada com mapa dos 8 reinos, Boss Battles como dragões, Campanha como expansão de território, ranks como classes.

**RF-039 — Integração com TickTick**
Painel deve refletir tarefas do TickTick em tempo real (read-only) — TickTick continua sendo fonte operacional de verdade.

**RF-040 — Health Check Mensal**
Primeira segunda do mês, painel apresenta diagnóstico do mês anterior e oferece ajustes de cadência.

---

## 3. Requisitos Não-Funcionais

### 3.1 Performance

**RNF-001 — Tempo de resposta**
- Briefing matinal deve ser entregue dentro de 30 segundos do horário programado
- Detector de ação CEO deve processar mensagem em <5 segundos
- Painel web deve carregar em <2 segundos

### 3.2 Disponibilidade

**RNF-002 — Uptime**
Sistema deve operar 99% do tempo (downtime máximo de ~7h/mês). Manutenções programadas podem ocorrer aos sábados.

### 3.3 Segurança

**RNF-003 — Dados sensíveis**
- API keys nunca commitadas no Git
- Credenciais em `.env` com permissão 600
- Dados de cobrança e times em arquivo local, não em cloud público

**RNF-004 — Backup**
Backup diário automático no GitHub (já implementado via cron).

### 3.4 Privacidade

**RNF-005 — Single-user**
Sistema deve recusar interação de qualquer usuário que não seja Alf (ID Telegram 1668476586).

### 3.5 Manutenibilidade

**RNF-006 — Documentação**
Toda regra de negócio nova deve ser registrada em `ceo-quest-skill.md` antes de ser implementada.

**RNF-007 — Versionamento**
Mudanças em regras (XP, ranks, critérios) devem manter histórico no Git.

### 3.6 Escalabilidade

**RNF-008 — Limites do sistema**
Como é single-user, escalabilidade não é prioridade. Mas o sistema deve suportar:
- 10.000 ações registradas no histórico (5+ anos de uso)
- 50 Boss Battles concluídos
- 200 conquistas desbloqueadas

---

## 4. Arquitetura Técnica

### 4.1 Visão Geral

```
┌─────────────────────────────────────────────────┐
│         INTERFACES                              │
├─────────────────────────────────────────────────┤
│  Telegram (hub)  │  Painel Web  │  TickTick    │
└─────────────────────────────────────────────────┘
                     ↑    ↓
┌─────────────────────────────────────────────────┐
│         ALFREDO (Game Master)                   │
│   OpenClaw + GPT-5.4 + Skills + Memória         │
└─────────────────────────────────────────────────┘
                     ↑    ↓
┌─────────────────────────────────────────────────┐
│         CEO QUEST CORE                          │
├─────────────────────────────────────────────────┤
│  Detector  │  Streak  │  XP Engine  │  Crons   │
└─────────────────────────────────────────────────┘
                     ↑    ↓
┌─────────────────────────────────────────────────┐
│         DADOS (memory/governanca/)              │
├─────────────────────────────────────────────────┤
│  streak.md       │  daily-log.md                │
│  scorecard.md    │  weekly-review.md            │
│  cobrancas.md    │  ceo-quest-skill.md          │
└─────────────────────────────────────────────────┘
                     ↑
┌─────────────────────────────────────────────────┐
│         BACKUP (GitHub)                         │
│   github.com/LucianoAlf/ceo-quest               │
└─────────────────────────────────────────────────┘
```

### 4.2 Stack tecnológico

| Camada | Tecnologia | Decisão |
|---|---|---|
| Hub conversacional | Telegram (Bot API) | Já em uso |
| Agente | OpenClaw 2026.4.1 + GPT-5.4 (OAuth) | Estável |
| STT | Whisper local (faster-whisper, modelo tiny) | Custo zero |
| TTS | ElevenLabs (opcional) | Disponível, off por padrão |
| Embeddings | OpenAI text-embedding-3-small | Memória semântica |
| Banco operacional | TickTick (via API) | Fonte de verdade das tarefas |
| Storage local | Arquivos Markdown em `memory/governanca/` | Simples, versionável |
| Backend Web (Fase 3) | Node.js + Express OU Next.js API Routes | A definir |
| Banco de dados Web (Fase 3) | Supabase OU SQLite local + sync | A definir |
| Frontend Web (Fase 3) | React + TypeScript + Tailwind | Stack do Alf |
| Hospedagem Web (Fase 3) | Vercel (frontend) + VPS Hostinger (backend) | A definir |
| Versionamento | Git + GitHub | github.com/LucianoAlf/ceo-quest |
| CI/CD (Fase 3) | GitHub Actions | A definir |

### 4.3 Repositório

**Novo repositório dedicado:** `github.com/LucianoAlf/ceo-quest`

Estrutura:
```
ceo-quest/
├── docs/
│   ├── PRD.md (este documento)
│   ├── design-session.md
│   └── skill.md
├── core/
│   ├── streak/
│   │   ├── detector.py
│   │   ├── close_day.py
│   │   └── risk_check.py
│   ├── briefing/
│   │   ├── morning.py
│   │   └── friday.py
│   ├── ritual/
│   │   ├── sunday.py
│   │   └── weekly_review.py
│   └── xp_engine/
│       ├── calculator.py
│       └── ranks.py
├── data/
│   ├── streak.md
│   ├── daily-log.md
│   ├── scorecard.md
│   └── weekly-review/
├── web/  (Fase 3)
│   ├── frontend/
│   ├── backend/
│   └── shared/
├── crons/
│   └── jobs.json
└── README.md
```

### 4.4 Integração com Alfredo (OpenClaw)

CEO Quest **não substitui** o Alfredo. Ele é um sistema operado pelo Alfredo:

- Alfredo lê arquivos do CEO Quest no workspace
- Alfredo aplica regras definidas em `ceo-quest-skill.md`
- Alfredo dispara crons que executam scripts do CEO Quest
- Alfredo envia mensagens no tópico 218 do Telegram

Isso significa que **mudanças no CEO Quest não exigem mexer no OpenClaw** — só nos arquivos do workspace e nos scripts.

### 4.5 Integração com TickTick

CEO Quest lê o TickTick (read-only para fins de scorecard). Lê:

- Tarefas criadas/atualizadas/concluídas
- Tags `#sonoramente`, `#la-educa`, `#jornada-aluno` etc
- Vencimentos e responsáveis

CEO Quest **não duplica tarefas** — TickTick é a fonte de verdade operacional. CEO Quest é a camada de gamificação acima.

---

## 5. Roadmap em 3 Fases

### FASE 1 — Coração (já implementado, em validação)

**Objetivo:** Validar streak em uso real durante 4-6 semanas.

**Status:** ✅ Implementado em 30/04/2026

**Entregas:**
- ✅ Skill operacional (`ceo-quest-skill.md`)
- ✅ Design session salvo
- ✅ Detector heurístico de ação CEO
- ✅ Arquivo `daily-log.md` registrando evidências
- ✅ Cron de risk-check (21h)
- ✅ Cron de close-day (22h)
- ✅ Cron de marco zero (7h do dia 1)
- ✅ Tópico Telegram dedicado (218)
- ✅ Backup no GitHub

**Critérios de saída da Fase 1:**
- Streak médio ≥ 4 dias antes de cada quebra
- Falsos-positivos do detector < 10% das detecções
- Falsos-negativos relatados < 5% das ações reais
- Pelo menos 1 streak histórico de 7+ dias atingido
- Alf reporta sentir o jogo "puxar" pra ação

**Duração estimada:** 4-6 semanas (1 maio - 15 junho)

**Validação:**
- Reunião semanal de 15 min entre Alf e Alfredo (no domingo) pra ajustar detector
- Métricas reportadas no scorecard semanalmente

### FASE 2 — Tração operacional

**Objetivo:** Tornar o jogo proativo, cíclico e visível.

**Status:** 🟢 Ativado

**Entregas ativas:**

**2.1 Ritual de domingo automatizado**
- Cron de 8h domingo no tópico 218
- Convite oficial do Ritual da Virada
- Condução em formato 5+5 (pessoal + CEO)
- Revisão da semana anterior
- Planejamento da semana seguinte
- Atualização do `weekly-review.md`

**2.2 Briefing matinal automatizado**
- Cron de 8h da manhã (seg-sex) no tópico 218
- Template padrão (3 reinos + ação sugerida)
- Variação de sexta (quick check)
- Sábado: silêncio
- Mensagens condicionais: streak em risco, marco atingido, Boss caído

**2.3 Scorecard expandido**
- consolidação semanal de streak, ritual, prioridades e KPIs principais
- leitura de progresso por reino
- base para auditoria e feedback executivo

**2.4 XP, ranks e painéis**
- sistema de progressão ativo como camada motivacional do jogo
- marcos, badges e ranks documentados
- painel visual previsto no ecossistema LA Organizer / Supabase

**2.3 Health Check Mensal**
- Primeira segunda do mês
- Diagnóstico do mês anterior
- Sugestão de ajustes de cadência

**2.4 Sistema de marcos**
- Mensagens de comemoração nos marcos 7, 14, 30, 60, 100 dias
- Bônus de XP automático
- Conquista desbloqueada

**Duração estimada:** 3-4 semanas (16 junho - 15 julho)

**Critérios de saída da Fase 2:**
- Briefing matinal lido em ≥80% das manhãs úteis
- Ritual de domingo realizado em ≥10 das 12 últimas semanas
- Pelo menos 1 marco de streak (7, 14 ou 30 dias) atingido
- Health check mensal gerou ajuste útil de cadência

### FASE 3 — Tabuleiro (Painel Web próprio)

**Objetivo:** Sistema próprio com identidade visual, dashboard interativo e capacidades avançadas.

**Status:** 🔲 Não iniciado

**Trigger pra iniciar:** Fase 2 estabilizada por pelo menos 4 semanas.

**Decisão arquitetural-chave:** **Sistema próprio, não módulo do LA Organizer.**

Justificativa:
- LA Organizer é pra colaboradores da LA Music (operacional, multi-user)
- CEO Quest é exclusivo do Alf (estratégico, single-user)
- Públicos, objetivos e estéticas diferentes
- Manutenção independente facilita evolução

**Entregas:**

**3.1 Frontend Web**
- Stack: React + TypeScript + Tailwind + Vite
- Design system próprio (não LA Music) com tema "RPG/cockpit pessoal"
- Hospedagem: Vercel
- PWA (mobile-first)
- Domínio: `ceoquest.lucianoalf.dev` ou similar

**3.2 Backend Web**
- Stack: Node.js + Express OU Next.js API Routes
- Hospedagem: VPS Hostinger (mesma do Alfredo) OU Vercel Functions
- Autenticação: SSO via Google OU Telegram Login OU JWT simples (single-user)
- Endpoints REST pra ler/atualizar dados

**3.3 Banco de dados**
- Decisão: SQLite local + sync com GitHub (mantém abordagem "memory" atual) OU Supabase
- Recomendação: começar com SQLite + sync (zero custo, simples)
- Migrar pra Supabase se precisar de queries complexas no futuro

**3.4 Dashboard principal**
- Streak grande no centro com animação
- Rank atual com identidade visual (ícone musical animado)
- XP por categoria com gráficos de evolução
- Boss Battles com barras de progresso e arte temática
- Campanha SonoraMente com mapa de fases
- Conquistas como cards
- Loot pendente em destaque

**3.5 Tabuleiro do jogo**
- Visualização gamificada do mapa dos 8 reinos
- Boss Battles representados como dragões
- Campanha como expansão de território
- Animações de transição quando algo é concluído

**3.6 Histórico**
- Timeline de streak (calendário tipo GitHub contributions)
- Gráficos de XP por semana/mês
- Lista de Boss Battles concluídos
- Conquistas desbloqueadas com data

**3.7 Detalhe por reino**
- Drill-down em cada reino
- Tarefas pendentes do TickTick (read-only)
- Pessoas-chave do reino
- XP acumulado e tendência
- Próximas ações sugeridas

**3.8 Integração com Alfredo**
- Alfredo continua sendo a interface principal de input (Telegram)
- Painel é só pra visualização e contemplação
- Mudanças importantes (definir Loot, ativar Boss) podem ser feitas em ambos

**3.9 Modo "fim de fase"**
- Ao completar Boss Battle, animação cinematográfica
- Ao subir de rank, level up screen estilo RPG
- Ao bater marco, celebração visual

**Duração estimada:** 6-8 semanas (16 julho - 15 setembro)

**Critérios de saída da Fase 3:**
- Painel acessível em web e mobile
- Sincronização automática com Alfredo a cada 15 min
- Alf abrir o painel pelo menos 3x por semana
- Animações e visual evocando "jogo de verdade", não dashboard corporativo

### FASE 4+ — Evolução contínua (pós-MVP)

Após Fase 3, possibilidades:
- IA generativa de conquistas personalizadas baseadas no histórico
- Modo "lições do mês" com análise de padrões
- Integração com WhatsApp do time pra cobranças automáticas
- Modo desafio: setar metas trimestrais com Loots maiores
- Dashboard pra Anne (única pessoa além do Alf que pode ter acesso, se ela quiser acompanhar)

---

## 6. Decisões de Produto

### DP-001 — Single-user, não SaaS
CEO Quest é feito sob medida pro Alf. Não há intenção de virar produto comercial agora. Decisões priorizam adequação ao usuário sobre genericidade.

### DP-002 — Sistema próprio, não módulo
CEO Quest é repositório próprio (`github.com/LucianoAlf/ceo-quest`), não submódulo do LA Organizer. Stack independente, evolução independente.

### DP-003 — TickTick como fonte de verdade operacional
Tarefas continuam no TickTick. CEO Quest é camada de gamificação acima — não duplica gestão de tarefas.

### DP-004 — Telegram como hub conversacional
Toda interação ativa do jogo (briefing, ritual, marcos) acontece no Telegram, tópico 218. Painel Web é pra visualização contemplativa, não pra operação.

### DP-005 — Markdown como storage primário
Dados ficam em arquivos `.md` no workspace do Alfredo. Versionáveis, legíveis, sem dependência de banco.

### DP-006 — MVP enxuto, evolução em camadas
Coração (streak) primeiro. Briefing/Ritual depois. Painel Web por último. Não construir decoração antes de validar valor.

### DP-007 — Honestidade como base
Sistema falha de propósito quando Alf mente. Não há mecanismo automático de "te dar uma força" — autoengano destrói o jogo.

### DP-008 — Identidade musical
Ranks (Garagem → Bandleader → Maestro → Arquiteto → Fundador-CEO → Visionário → Legado) refletem a história musical do Alf, não progressão genérica de RPG.

### DP-009 — Game Master, não Chief of Staff
Alfredo provoca, registra, celebra. Mas não substitui o Alf no papel de CEO. Cobrança automática pelo Alfredo direto pro time NÃO faz parte do CEO Quest.

### DP-010 — Hábitos pessoais valem ponto
Academia, meditação, leitura, sono valem XP igual a cobrança do time. CEO de verdade cuida das duas dimensões.

---

## 7. Métricas de Sucesso

### 7.1 Métricas de produto (3 meses)

| Métrica | Meta |
|---|---|
| Streak médio | ≥ 20 dias antes de cada quebra |
| Streak máximo histórico | ≥ 45 dias |
| Briefing matinal lido | ≥ 80% das manhãs úteis |
| Ritual de domingo realizado | ≥ 10 das 12 semanas |
| Subida de rank | Garagem → Bandleader (501+ XP) |
| SonoraMente | Fase 3 (Operação Clínica) iniciada |
| Painel web aberto por vontade | ≥ 3x/semana após Fase 3 |

### 7.2 Métricas comportamentais (subjetivas, reportadas pelo Alf no ritual)

- Sentir que "abriu o tópico CEO Quest por vontade própria"
- Notar diminuição de "combinados que morrem na cabeça"
- Sentir que time tá sendo acompanhado de verdade
- Não sentir o jogo como obrigação corporativa

### 7.3 Métricas de saúde (12 meses)

| Métrica | Meta |
|---|---|
| Faturamento LA Music | Crescimento ≥ 20% vs ano anterior |
| Churn LA Music | < 2% (bate meta Fideliza+) |
| Boss Battles concluídos | ≥ 3 (LA Educa, Jornada Aluno, SonoraMente Fase 1) |
| Rank atingido | Maestro (1.501+ XP) |
| Tempo livre do Alf | Reportar 10h+/semana de trabalho criativo (não operacional) |

---

## 8. Riscos e Mitigações

### Risco 1 — Detector heurístico v1 com qualidade insuficiente
**Probabilidade:** Alta
**Impacto:** Médio
**Mitigação:** Refinar em 4-6 semanas de uso. Reportar falso-positivos/negativos diariamente nos primeiros 14 dias.

### Risco 2 — Alf não responder ao marco zero/primeiro briefing
**Probabilidade:** Baixa
**Impacto:** Crítico
**Mitigação:** Marco zero foi negociado com Alf. Compromisso claro. Se acontecer, revisar timing e formato.

### Risco 3 — Inflação artificial do streak
**Probabilidade:** Média
**Impacto:** Alto (destrói credibilidade do jogo)
**Mitigação:** Regra de evidência concreta + auto-honestidade no quick check + pergunta "mão na consciência".

### Risco 4 — Atualização do OpenClaw quebrar o sistema
**Probabilidade:** Média (já aconteceu com 2026.4.2)
**Impacto:** Alto
**Mitigação:** Manter 2026.4.1 estável. Testar atualizações em ambiente isolado antes.

### Risco 5 — Custo da OpenAI escalar
**Probabilidade:** Baixa
**Impacto:** Baixo
**Mitigação:** Embeddings via text-embedding-3-small são baratos. Monitorar via skill `model-usage`.

### Risco 6 — Painel Web atrasar ou não sair
**Probabilidade:** Média
**Impacto:** Baixo (Fase 1 e 2 já entregam valor sozinhas)
**Mitigação:** Fase 3 é evolução, não pré-requisito. Se atrasar, sistema continua funcionando via Telegram.

### Risco 7 — Sobrecarga do Alfredo (contexto cheio)
**Probabilidade:** Alta
**Impacto:** Médio
**Mitigação:** Memória semântica funcionando. Skills consultáveis. Quando contexto resetar, ele reconstroi via memória.

### Risco 8 — Conflito de tempo com SonoraMente (Campanha #1)
**Probabilidade:** Alta
**Impacto:** Médio
**Mitigação:** SonoraMente é Boss Battle dentro do CEO Quest, não competidor. Tempo gasto em SonoraMente gera XP.

---

## 9. Critérios de Aceite por Fase

### Fase 1 (em curso)
- [✅] Skill operacional escrita e indexada
- [✅] Detector funcional v1
- [✅] 3 crons configurados e testados
- [✅] Tópico Telegram dedicado
- [✅] Backup no GitHub
- [ ] 4 semanas de uso sem queda de sistema
- [ ] Alf reporta "o jogo me puxa pra ação"

### Fase 2
- [ ] Briefing matinal entregue diariamente sem falha por 2 semanas
- [ ] Ritual de domingo realizado por 4 semanas seguidas
- [ ] Pelo menos 1 marco de streak celebrado
- [ ] Health check mensal gerou ajuste útil

### Fase 3
- [ ] Painel acessível em web e mobile
- [ ] Sync com Alfredo funcionando
- [ ] Animações de level up e Boss down implementadas
- [ ] Histórico de 3+ meses visualizável
- [ ] Alf reporta "dá prazer abrir o painel"

---

## 10. Cronograma Macro

```
ABRIL 2026          MAIO          JUNHO         JULHO         AGOSTO        SETEMBRO
   │                  │             │             │             │             │
   │  ┌────────────FASE 1───────────┐                                        │
   │  │ Validação do streak         │                                        │
   │  │ Refinamento detector        │                                        │
   │  │ 4-6 semanas                 │                                        │
   │  └─────────────────────────────┘                                        │
   │                                ┌────FASE 2─────┐                        │
   │                                │ Briefing+Ritual                        │
   │                                │ 3-4 semanas    │                        │
   │                                └────────────────┘                        │
   │                                                ┌─────────FASE 3────────┐│
   │                                                │ Painel Web próprio    ││
   │                                                │ 6-8 semanas           ││
   │                                                └───────────────────────┘│
```

**Marcos:**
- 30/04 — Skill aprovada, Fase 1 iniciada
- 01/05 — Marco zero (CEO Quest ON)
- 15/06 — Critérios de saída Fase 1 atingidos
- 16/06 — Início Fase 2
- 15/07 — Fase 2 estabilizada
- 16/07 — Início Fase 3
- 15/09 — Painel Web em produção

---

## 11. Stakeholders e Responsabilidades

### Alf (CEO, único usuário)
- Joga
- Reporta falhas e sucessos
- Decide ajustes de regras
- Define Loots Reais

### Alfredo (Game Master, agente)
- Detecta ações CEO
- Atualiza streak diariamente
- Envia briefings e provocações
- Conduz ritual de domingo
- Celebra marcos e Boss caídos
- Mantém honestidade do jogo

### Hugo (Tech Coordenador, suporte futuro)
- Pode ajudar na construção do Painel Web (Fase 3) se Alf delegar
- Manutenção da VPS e backups

### Anne (cofundadora, observadora opcional)
- Pode ter acesso de visualização ao painel se Alf quiser compartilhar evolução
- Não tem responsabilidades operacionais no sistema

---

## 12. Glossário

| Termo | Definição |
|---|---|
| **Streak** | Sequência de dias consecutivos com pelo menos 1 ação CEO registrada |
| **Ação CEO** | Cobrança/verificação/direção real sobre alguém do círculo de responsabilidade, com evidência concreta |
| **Reino** | Uma das 8 frentes de governança do jogo |
| **Quest** | Projeto médio de 1-3 semanas |
| **Boss Battle** | Projeto estratégico de 4+ semanas com 4 critérios |
| **Campanha** | Transformação de 3+ meses com 3+ Boss internos |
| **Loot Real** | Recompensa concreta auto-definida pelo Alf |
| **Game Master** | Papel do Alfredo no sistema |
| **Marco zero** | Mensagem inicial do dia 1 ("CEO Quest ON. Streak: 0") |
| **Risk-check** | Verificação automática às 19h se houve ação no dia |
| **Close-day** | Fechamento automático do dia às 20h |
| **Ritual da Virada** | Ritual de domingo manhã com 3 camadas |
| **Pause vs Quebra** | Pausa = comunicada antes, congela streak. Quebra = silêncio, zera. |

---

## 13. Aprovações

| Stakeholder | Status | Data |
|---|---|---|
| Luciano Alf (Owner) | ⏳ Aguardando | — |

---

## Anexos

- **Anexo A:** `ceo-quest-skill.md` — Bíblia operacional completa
- **Anexo B:** `ceo-quest-design-session.md` — Transcrição das 22 perguntas e respostas
- **Anexo C:** `relatorio-executivo-sessao.md` — Relatório da sessão de 30/04 que originou o sistema

---

**Documento gerado em:** 1 de maio de 2026, 01:00 BRT
**Próxima revisão:** Após critérios de saída da Fase 1 (estimado 15/06/2026)
**Versionado em:** github.com/LucianoAlf/ceo-quest *(repositório a criar)*

🎩🎮🚀
