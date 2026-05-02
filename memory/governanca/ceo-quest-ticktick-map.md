# CEO Quest × TickTick — Mapa Operacional Oficial

> Objetivo: definir com clareza o que do CEO Quest deve ser registrado no TickTick, o que deve ficar só na memória local e o que precisa sincronizar entre os dois.
> 
> Baseado em:
> - `ceo-quest-skill.md`
> - `ceo-quest-prd.md`
> - `ticktick-capacidades.md`
> - `ticktick-payload-patterns.md`
> - `ticktick-execution-rules.md`
>
> Regra central: **TickTick é backend operacional de tarefas e cadência. Memória é backend histórico, semântico e narrativo.**

---

## 1. Princípio-mãe

Não tentar colocar **tudo** no TickTick.
Isso seria erro.

### O papel de cada camada

#### TickTick
Serve para:
- execução
- cadência
- cobrança
- lembrete
- planejamento semanal
- prioridades
- projetos vivos
- checklists operacionais

#### Memória (`memory/governanca/*`)
Serve para:
- streak oficial
- evidência histórica
- narrativa da semana
- decisões do jogo
- score interpretativo
- contexto semântico
- auditoria e aprendizagem

### Conclusão
**TickTick = sistema operacional do jogo**  
**Memória = consciência histórica do jogo**

---

## 2. O que deve registrar no TickTick

## 2.1 Ritual de domingo
**Deve registrar no TickTick.**

Mas com formato próprio, fixo e recorrente.

### Formato recomendado
- 1 card recorrente semanal
- sempre no mesmo projeto/lista
- sempre com a mesma estrutura visual
- sempre com as mesmas tags base

### Estrutura recomendada
- `title`: nome fixo do ritual
- `desc`: bloco visual curto e consistente
- `content`: perguntas do ritual
- `repeatFlag`: semanal domingo
- `reminders`: domingo 20h anterior + domingo na hora ou 30 min antes
- `tags`: `CEO Quest`, `Ritual Semanal`, `Planejamento`, `Review`

### Regra
O ritual no TickTick não é só lembrete.
Ele é o **container operacional recorrente** da revisão semanal.

### O que NÃO fazer
- criar um card diferente a cada domingo sem padrão
- improvisar estrutura nova toda semana
- transformar o ritual em checklist quebrado sem validação visual

---

## 2.2 Briefing matinal diário
**Não precisa virar card diário no TickTick.**

### Motivo
O briefing é melhor como:
- mensagem de cockpit
- provocação diária
- leitura do estado do jogo

Se virar um card todo dia, polui o TickTick.

### Exceção
Se o briefing gerar ação concreta, aí sim nasce task.

---

## 2.3 Ações CEO que sustentam streak
**Devem registrar no TickTick quando forem tarefas reais.**

Principalmente:
- cobrança
- verificação
- destravamento
- direcionamento
- follow-up com prazo

### Pattern oficial
Usar card simples com:
- `title`
- `content`
- `priority`
- `tags`
- prazo quando houver

### Tags mínimas
- `CEO Quest`
- `Ação CEO`
- reino
- pessoa

### Exemplo
- `Cobrar Quintela sobre LA Educa`
- `Verificar Juliana sobre grade Kids`
- `Destravar Bianca no escopo clínico`

### Regra
Se existe execução futura, cobrança ou acompanhamento real:
**vai pro TickTick**.

Se foi só evidência narrativa do que já aconteceu:
**fica na memória**.

---

## 2.4 1:1 com líderes
**Deve registrar no TickTick.**

Porque é cadência recorrente, reunião e acompanhamento.

### Estrutura ideal
- card recorrente
- pauta no `content`
- tags por líder e reino
- reminders

---

## 2.5 Boss Battles
**Devem registrar no TickTick.**

Porque são projetos vivos, com execução e fase.

### Formato
- checklist nativo quando fizer sentido
- prioridade alta
- tags de Boss + reino + projeto

---

## 2.6 Campanhas
**Devem registrar no TickTick.**

Mas como âncora e cards filhos.

### Regra
- campanha-mãe = card âncora
- Boss internos = cards separados
- vínculo via tags compartilhadas

---

## 2.7 Planejamento semanal
**Deve registrar no TickTick.**

Esse é um ponto central.

O ritual de domingo não termina no texto.
Ele precisa produzir desdobramento operacional.

### O que entra no TickTick após o ritual
- prioridades da semana
- tarefas que precisam de dia definido
- cobranças que saem de você
- compromissos e blocos críticos
- follow-ups com dono ou prazo

### Regra
Ritual sem desdobramento no TickTick vira reflexão sem execução.

---

## 2.8 Hábitos / pessoal
**Pode registrar no TickTick, mas com parcimônia.**

### Entra quando
- existe cadência real
- existe ritual fixo
- existe hábito monitorado

Exemplos:
- academia
- meditação
- leitura

### Não precisa entrar quando
- foi só observação da semana
- foi reflexão pessoal solta

---

## 3. O que deve ficar só na memória

## 3.1 Streak oficial
**Fica na memória.**

Arquivos:
- `streak.md`
- `daily-log.md`

### Motivo
Streak é lógica do jogo, não tarefa.

TickTick ajuda com evidência operacional, mas o placar oficial fica no CEO Quest.

---

## 3.2 Evidência narrativa do dia
Exemplos:
- “mandei áudio cobrando o Quintela”
- “dei direção pra Juliana”
- “fiquei omisso no comercial”

Isso deve ficar na memória porque é:
- histórico semântico
- rastro de comportamento
- matéria-prima de auditoria

---

## 3.3 Weekly review consolidado
**A síntese final fica na memória.**

Mesmo que o ritual tenha card no TickTick, o arquivo final consolidado deve viver em:
- `weekly-review.md`

### Motivo
O TickTick guarda o ritual como execução recorrente.
A memória guarda o que foi aprendido e decidido.

---

## 3.4 Score interpretativo
- leitura da semana
- onde houve omissão
- análise do jogo
- aconselhamento do Alfredo
- alertas executivos

Isso é memória, não task.

---

## 3.5 Auditoria e lições
Tudo que for:
- inconsistência
- padrão percebido
- risco recorrente
- evolução de comportamento

fica na memória.

---

## 4. O que precisa sincronizar entre TickTick e memória

## 4.1 Ritual de domingo
### TickTick guarda
- card recorrente
- lembretes
- estrutura fixa
- eventual checklist/roteiro

### Memória guarda
- respostas
- síntese
- prioridades da semana
- análise do Alfredo

### Regra de sync
Ao final do ritual:
1. revisar o card do ritual
2. gerar/update `weekly-review.md`
3. criar no TickTick as prioridades derivadas da semana

---

## 4.2 Planejamento semanal
### TickTick guarda
- as tarefas da semana
- distribuição por dia
- follow-ups operacionais

### Memória guarda
- por que essas prioridades existem
- o que ficou da semana anterior
- a leitura estratégica

---

## 4.3 Scorecard expandido
### TickTick fornece
- tarefas criadas
- vencimentos
- prioridades
- cards de campanha/boss
- cadência de execução

### Memória consolida
- streak
- ritual
- leitura por reino
- progresso geral do jogo

---

## 4.4 Ação CEO
### TickTick guarda
- a task operacional, se houver

### Memória guarda
- a evidência de que você agiu como CEO

### Regra
Se uma ação CEO gerar task, os dois lados recebem registro.
Se não gerar task, só a memória registra.

---

## 5. Formato oficial aprovado para o Ritual de Domingo no TickTick

Com base no teste visual validado no app, o ritual tem padrão fixo.

## Estrutura visual aprovada

### `title`
`Ritual da Virada — Review + Planejamento da Semana`

### `desc`
O **texto inteiro do ritual** fica no `desc`, com:
- abertura
- blocos pessoais
- blocos CEO
- fechamento
- saída final do ritual

### `items[]`
Checklist leve apenas no final:
- revisar a semana anterior
- definir prioridades da nova semana
- distribuir a semana no TickTick

### `tags`
- `CEO Quest`
- `Ritual Semanal`
- `Review`
- `Planejamento`

### `priority`
- `5`

### `repeatFlag`
- semanal domingo

### `reminders`
Padrão aprovado:
- 30 minutos antes
- na hora

## Regra estrutural oficial
Para o Ritual da Virada, o padrão aprovado foi:
- **não usar `content` como corpo principal**
- usar o **texto completo no `desc`**
- manter apenas um checklist final leve em `items[]`

## Regra de operação
- o card é criado/garantido no TickTick
- a condução do ritual acontece no **tópico CEO Quest (218)**
- o que for aprendido e decidido vai para `weekly-review.md`
- as tarefas derivadas do ritual descem para o TickTick como execução da semana

---

## 6. Regras práticas de ouro

1. **Nem tudo vai pro TickTick.**
2. **Tudo que tiver execução real, prazo ou acompanhamento deve tender ao TickTick.**
3. **Tudo que for interpretação, memória, streak ou auditoria deve tender à memória.**
4. **Ritual de domingo precisa existir nos dois lados.**
5. **Planejamento da semana nasce no ritual e desce para o TickTick.**
6. **Streak oficial continua fora do TickTick.**
7. **Card aprovado não se reinterpreta — replica.**

---

## 7. Resumo executivo

### Vai pro TickTick
- ritual semanal (card recorrente oficial)
- ações CEO com prazo/acompanhamento
- 1:1s
- Boss Battles
- Campanhas
- prioridades da semana
- tarefas derivadas do ritual
- hábitos quando forem cadências reais

### Fica só na memória
- streak oficial
- evidências narrativas
- leitura da semana
- weekly review consolidado
- auditoria
- aconselhamento
- padrões de comportamento

### Sincroniza entre os dois
- ritual de domingo
- planejamento semanal
- scorecard expandido
- ações CEO que viram tarefa real

---

## 8. Próximo passo recomendado

Antes de automatizar em lote:
1. criar **1 card piloto oficial** do Ritual da Virada no TickTick
2. validar o visual no app
3. aprovar o padrão
4. só então usar esse formato como molde fixo de todo domingo

Essa é a forma certa de não transformar o backbone do CEO Quest em bagunça.
