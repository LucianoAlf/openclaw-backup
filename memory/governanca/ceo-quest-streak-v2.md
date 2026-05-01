# CEO Quest Streak — Revisão técnica v2

> Documento de revisão do coração do CEO Quest.
> Baseado na leitura do `ceo-quest-streak.py`, no feedback do Alf e nos achados da sessão longa sobre TickTick, cron, tópico dedicado e regra do jogo.
> Objetivo: consolidar o que o script atual já faz, o que está bom, o que está faltando e como evoluir sem perder o MVP.

---

## 1. O que o script atual faz bem

O `ceo-quest-streak.py` é um **MVP funcional de verdade**.
Não é enfeite. Não é documento morto. Já executa regra real.

### O que ele já faz hoje

#### 1. Detecta 4 tipos de sinal
- **ação CEO**
- **decisão**
- **ação pessoal**
- **pausa**

#### 2. Usa `game_date()` com virada às 7h
Esse é um acerto forte.
Antes de 7h, o jogo ainda considera o dia anterior.
Isso cola com a realidade do Alf melhor do que a virada civil da meia-noite.

#### 3. Mantém log diário por categoria
Escreve em `daily-log.md`:
- ações de cobrança/verificação com time
- decisões tomadas
- tarefas criadas/atualizadas
- ações pessoais
- skips/pausas

#### 4. Fecha o dia
No `close_day()`:
- sábado congela
- se teve ação CEO, soma streak
- se não teve, zera

#### 5. Faz check de risco
No `risk_check()`:
- se ainda não houve ação CEO no dia → `RISK`
- se houve → `SAFE`

---

## 2. Diagnóstico técnico do estado atual

## 2.1 O script é simples e isso é bom
Ele está curto, legível e direto.
Pra fase 1, isso é vantagem.

### Vantagens do design atual
- poucas dependências
- baixo risco operacional
- fácil de ler
- fácil de alterar
- fácil de debugar

### Conclusão
Como MVP, a simplicidade dele é uma força, não uma fraqueza.

---

## 2.2 O detector atual é heurístico
Hoje o detector funciona por listas simples:
- nomes do círculo de responsabilidade
- verbos de cobrança/ação
- palavras-chave pessoais
- palavras-chave de pausa

### Isso é suficiente pra fase 1?
**Sim.**

### Isso é suficiente pra fase 2/3?
**Não.**

Porque com uso real vão aparecer:
- conjugações novas
- expressões novas
- erros de transcrição
- mensagens mais implícitas
- áudios com português zoado

### Conclusão
O detector atual serve.
Mas precisa ser tratado como **vocabulário vivo**, não como lista fechada.

---

## 3. Os 3 pontos de atenção levantados pelo Alf

## 3.1 Domingo não conta automaticamente
### Estado atual
A skill do CEO Quest diz:
> domingo: ritual conta como ação CEO se realizado

### Problema
No script atual não existe lógica específica para isso.
Ou seja:
- se domingo rolar ritual,
- mas não houver mensagem capturada como `ação`,
- o streak pode não contar como deveria.

### Impacto
Esse é um desalinhamento real entre:
- a regra operacional da skill
- e o comportamento do código

### Evolução necessária
Adicionar lógica explícita de domingo, algo como:
- se houve marcação de ritual realizado no domingo → conta como ação CEO
- mesmo sem verbo de cobrança no texto

---

## 3.2 Pausa não congela ainda
### Estado atual
O script detecta `pausa`, registra no log, **mas não usa isso no `close_day()`**.

### Resultado
Se não houver ação CEO no dia:
- mesmo com pausa registrada,
- a streak zera.

### Isso conflita com a skill?
**Sim.**
A skill prevê:
- pausa comunicada = congela
- quebra = zera

### Evolução necessária
O `close_day()` precisa checar:
- existe pausa válida hoje?
- se sim, status = congelado
- e atualizar `Última pausa`

---

## 3.3 Detector ainda é só português-BR literal
### Estado atual
Os gatilhos são bons, mas estreitos.

### Exemplos de limite
Hoje ele pega:
- `cobrar`
- `verifica`
- `cadê`
- `fechei`
- `academia`
- `meditei`

Mas no uso real podem vir:
- “me lembra de apertar o Quintela”
- “preciso ver essa porra com a Juliana”
- “falei com ele ontem e dei o prazo”
- “treinei” em vez de `academia`
- “lição” ou “corrida” no pessoal

### Evolução necessária
Manter o detector como **vocabulário expansível**, não estático.

---

## 4. O que faltou perceber além dos 3 pontos

## 4.1 Falta normalização explícita do tópico CEO Quest
Hoje a conversa mostrou uma mudança importante:
- o CEO Quest tem **tópico próprio** no HQ Alf
- topic ID **218**

### Impacto
O coração do sistema não deveria ficar cego ao contexto do canal/tópico.

### Evolução futura
Idealmente:
- registrar quando a ação veio do tópico CEO Quest
- separar sinais do jogo das conversas gerais
- reduzir ruído e falso positivo fora do contexto

---

## 4.2 Falta integração conceitual com o TickTick como backend
O script atual funciona por texto e log.
Isso é suficiente pro MVP de streak.

Mas depois da sessão longa, ficou claro que o TickTick já provou muito mais capacidade:
- recorrência
- reminders
- tags
- priority/Eisenhower
- content
- checklist
- hábitos

### O que isso muda
O `ceo-quest-streak.py` hoje ainda não usa esse poder como fonte complementar.

### Exemplo futuro
Poderia reconhecer como ação CEO também:
- criação de task com tag `Ação CEO`
- tarefa de cobrança com pessoa + reino + prazo
- update de tarefa de 1:1

### Conclusão
Não precisa entrar agora.
Mas é uma evolução natural e importante.

---

## 4.3 Falta uma camada explícita de evidência
Hoje a evidência do dia é inferida do texto da ação.
Funciona, mas é frágil.

### Evolução possível
Guardar no `daily-log.md` ou em estrutura própria:
- tipo da evidência
- origem (mensagem / tarefa / ritual / manual)
- pessoa envolvida
- reino
- prazo, se houver

### Benefício
Isso facilitaria:
- auditoria
- scorecard futuro
- streak explicável
- transição para Fase 2/3

---

## 4.4 Falta distinção entre ação CEO e decisão estratégica com peso diferente
Hoje o script detecta:
- `ação`
- `decisão`

Mas a streak depende só de `ação` no bloco atual.

### Pergunta importante
Uma decisão estratégica que destrava alguém conta ou não conta como presença CEO no dia?

Pela filosofia do jogo, **deveria contar em alguns casos**.

### Exemplo
- “defini com Bianca o modelo de abertura da SonoraMente”
- isso é ação de CEO real, mesmo sem linguagem clássica de cobrança

### Evolução futura
Ou:
- decisão destravadora passa a contar como ação
ou
- ganha regra própria dentro do close-day

---

## 5. O que o script ainda não precisa fazer agora

Pra não encher de complexidade cedo demais, **não precisa entrar ainda**:
- XP por categoria
- rank automático
- Boss Battle scoring
- integração profunda com hábitos do TickTick
- briefing matinal completo
- análise de campanha
- leitura de activity log do TickTick

Essas camadas são reais, mas vêm **depois**.

---

## 6. Leitura do coração do sistema hoje

Hoje o coração do CEO Quest é isso:

- detectar presença CEO mínima
- registrar sem ruído
- somar ou quebrar streak
- manter simplicidade
- funcionar em silêncio

### E isso já é suficiente?
**Sim, como fase 1.**

### E o que mais importa agora?
Não é sofisticar. É:
- usar por 1 semana
- ver falso positivo
- ver falso negativo
- refinar vocabulário
- corrigir domingo
- corrigir pausa

---

## 7. Proposta objetiva de evolução (sem quebrar o MVP)

## v1.1 — ajustes mínimos importantes
1. domingo conta ritual como ação CEO
2. pausa congela em vez de zerar
3. ampliar vocabulário de detecção
4. registrar `Última pausa` corretamente

## v1.2 — robustez de evidência
1. guardar origem da evidência
2. marcar pessoa/reino se possível
3. separar melhor `ação` de `decisão destravadora`

## v2 — integração com backend operacional
1. usar tags do TickTick como sinais do jogo
2. integrar tarefas `Ação CEO`
3. usar hábitos do TickTick no reino pessoal
4. preparar scorecard futuro

---

## 8. Recomendação final

O script atual **não está errado**.
Ele está **certo para a fase em que está**.

O que existe são 3 desalinhamentos naturais entre:
- a ambição da skill
- e a implementação mínima do MVP

### Os 3 consertos prioritários são:
1. domingo contar ritual
2. pausa congelar
3. vocabulário vivo

Se fizer isso, o coração fica bem mais alinhado com o desenho do jogo sem perder simplicidade.

---

## 9. Frase síntese

> O `ceo-quest-streak.py` já é um coração que bate.  
> Agora o trabalho não é trocar o coração — é calibrar o ritmo, proteger contra falso disparo e alinhar com a regra real do jogo.
