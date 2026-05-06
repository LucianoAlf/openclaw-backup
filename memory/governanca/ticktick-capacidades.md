# TickTick — Capacidades confirmadas da API v1 para o CEO Quest

> Documento técnico vivo.
> Baseado em testes reais feitos pelo Alfredo + validação visual do Alf no app TickTick.
> Objetivo: registrar o que é confiável hoje na API oficial v1 para servir de substrato operacional do CEO Quest.

---

## 1. Conclusão executiva

A API oficial v1 do TickTick entrega **muito mais** do que parecia no começo.

Hoje está **confirmado em campo** que a API v1 consegue sustentar, para o CEO Quest:

- criação e atualização de tarefas
- conclusão de tarefas
- criação de listas/projetos
- prioridade/bandeira
- recorrência
- lembretes múltiplos
- conteúdo longo no corpo da tarefa
- descrição (`desc`)
- checklist/subtarefas via `items[]`
- tags/etiquetas
- hábitos e check-ins
- seções de hábitos
- leitura de comentários (mas não criação)

### Conclusão central
A API v1 oficial já resolve uma parte grande do backend operacional do CEO Quest sem depender de API não-oficial.

### Regra crítica para leitura da agenda (validada em 2026-05-06)
Para a agenda pessoal do Alf bater com o app do TickTick, a renderização precisa usar:
- `startDate` como início
- `dueDate` como fim
- conversão para `America/Sao_Paulo`
- inclusão de itens `TEXT` e `CHECKLIST`
- leitura de `items[]` quando o card tiver checklist interno

Usar `dueDate` como referência principal única quebra a agenda e omite/bloca itens recorrentes e blocos de checklist.

---

## 2. Capacidades confirmadas

## 2.1 Tarefas

### Criar tarefa
**Status:** ✅ Confirmado

**Endpoint:**
- `POST /open/v1/task`

**Capacidades confirmadas no create:**
- `title`
- `projectId`
- `content`
- `desc`
- `startDate`
- `dueDate`
- `timeZone`
- `priority`
- `reminders`
- `repeatFlag`
- `tags`
- `items[]`

---

### Atualizar tarefa
**Status:** ✅ Confirmado

**Endpoint:**
- `POST /open/v1/task/{taskId}`

**Observação importante:**
- updates simples funcionam bem para campos como título, conteúdo, prioridade, lembretes, tags, recorrência
- updates com `items[]` precisam muito cuidado, porque podem sobrescrever o estado do checklist

---

### Marcar tarefa como concluída
**Status:** ✅ Confirmado

**Forma que funcionou na prática:**
- `POST /open/v1/task/{taskId}` com `status: 2`

**Observação:**
- a rota intuitiva via projeto/tarefa não foi a que funcionou melhor nos testes iniciais
- padronizar conclusão via update de task com `status: 2`

---

### Apagar tarefa
**Status:** ✅ Confirmado

**Endpoint:**
- `DELETE /open/v1/project/{projectId}/task/{taskId}`

---

## 2.2 Listas / Projetos

### Criar lista/projeto
**Status:** ✅ Confirmado

**Endpoint:**
- `POST /open/v1/project`

**Observação:**
- útil para criar estruturas por domínio, frente ou ambiente de teste

---

### Ler listas/projetos
**Status:** ✅ Confirmado

**Endpoints:**
- `GET /open/v1/project`
- `GET /open/v1/project/{projectId}`
- `GET /open/v1/project/{projectId}/data`

**Observação:**
- `project/{id}/data` é a principal forma de inspecionar tarefas e sua estrutura real

---

## 2.3 Prioridade / Bandeiras / Eisenhower

### Campo técnico
- `priority`

### Mapeamento confirmado
- `0` = nenhuma
- `1` = azul / baixa
- `3` = amarela / média
- `5` = vermelha / alta

### Status
**Status:** ✅ Confirmado por API + validação visual

### Achado importante
As bandeirinhas alimentam a visualização da Matriz Eisenhower do TickTick.

**Conclusão:**
- `priority` é parte importante do jogo
- pode ser usado para representar urgência e ajudar a empurrar tarefas para quadrantes específicos da matriz

---

## 2.4 Recorrência

### Campo técnico correto
- `repeatFlag`

### Status
**Status:** ✅ Confirmado

### Exemplo confirmado
#### Mensal — dia 1
```json
"repeatFlag": "RRULE:FREQ=MONTHLY;BYMONTHDAY=1"
```

#### Semanal — domingo
```json
"repeatFlag": "RRULE:FREQ=WEEKLY;BYDAY=SU"
```

### Observações
- o campo `repeat` não se mostrou confiável
- o campo que persistiu no retorno e apareceu corretamente no app foi `repeatFlag`
- recorrência foi validada visualmente no app do Alf

**Conclusão:**
- para a integração Alfredo ↔ TickTick, o padrão correto é usar `repeatFlag`

---

## 2.5 Lembretes

### Campo técnico
- `reminders`

### Status
**Status:** ✅ Confirmado

### Formato confirmado
```json
"reminders": ["TRIGGER:-PT30M", "TRIGGER:PT0S"]
```

### Casos confirmados
- lembrete 30 minutos antes
- lembrete na hora
- múltiplos lembretes na mesma task

### Conclusão
- os lembretes são confiáveis e podem ser usados em rituais, 1:1s, revisões e eventos do jogo

---

## 2.6 Conteúdo longo e descrição

### Campos técnicos
- `content`
- `desc`

### Status
**Status:** ✅ Confirmado

### Achado importante
A API v1 suporta tarefa com:
- `content` longo estruturado
- `desc`
- checklist (`items[]`)
- prioridade
- recorrência
- lembretes
- tags

Tudo isso **no mesmo create**.

### Exemplo validado em campo
Foi criado um card-laboratório completo com:
- 10 perguntas no `content`
- `desc`
- checklist com 3 itens
- recorrência semanal
- lembretes
- prioridade alta
- tags

A UI do app renderizou isso corretamente.

### Conclusão
A coexistência entre `content` e `items[]` é suportada.
O problema que tivemos antes era de modelagem/update, não limitação da API.

---

## 2.7 Checklist / subtarefas via `items[]`

### Campo técnico
- `items[]`

### Status
**Status:** ✅ Confirmado

### O que `items[]` representa
- checklist interno da tarefa
- subtarefas do tipo checklist

### Estrutura oficial do item
- `id`
- `title`
- `status`
- `completedTime`
- `isAllDay`
- `sortOrder`
- `startDate`
- `timeZone`

### Status do checklist item
- `0` = normal
- `1` = completo

### Pegadinha de status
**ATENÇÃO:** status do checklist item **não** segue o mesmo padrão da task pai.

- **Task pai:** `status 0 = pendente`, `2 = concluída`
- **Checklist item (`items[]`):** `status 0 = normal`, `1 = completed`

Usar `status 2` num checklist item **não funciona corretamente** como padrão oficial. Isso foi validado pela OpenAPI oficial.

### Achados importantes
- checklist funciona no create
- checklist funciona no retorno
- checklist aparece bem no app
- `items[]` coexistem com `content` quando modelado corretamente desde o nascimento da task

### Risco conhecido
Updates incrementais com `items[]` podem sobrescrever a lista inteira em vez de fazer append inteligente.

**Regra operacional:**
- checklist complexo deve preferencialmente nascer completo no `create`
- usar update incremental em `items[]` com cautela máxima

---

## 2.8 Tags / Etiquetas

### Campo técnico
- `tags[]`

### Status
**Status:** ✅ Confirmado

### Achado importante
Não foi necessário endpoint separado para criar tag.

A tag foi criada na prática ao atualizar/criar task com:
```json
"tags": ["CEO Quest"]
```

### Conclusão
- o TickTick aceita criação/aplicação de tag via próprio payload da task
- isso é excelente para o CEO Quest

### Usos sugeridos
- `CEO Quest`
- `#boss`
- `#campanha`
- `#sonoramente`
- `#pedagogico`
- `#comercial`
- `#pessoal`

---

## 2.9 Hábitos

### Endpoints confirmados
- `GET /open/v1/habit`
- `POST /open/v1/habit`
- `GET /open/v1/habit/{habitId}`
- `GET /open/v1/habit/sections`
- `POST /open/v1/habit/checkins`

### Status
**Status:** ✅ Confirmado

### O que foi validado
- criar hábito
- listar hábitos
- ler hábito específico
- ver seções de hábito
- fazer check-in
- ver no app:
  - total de check-ins
  - melhor sequência
  - sequência atual

### Achado importante
O reino **🌱 Pessoal Alf** pode usar o Habit Tracker nativo do TickTick.

### Conclusão
Hábitos não são mais hipótese. São capacidade real do stack.

---

## 2.10 Comentários / histórico / atividades

### Leitura de comentários
**Status:** ✅ Parcial

- `GET /open/v1/task/{id}/comments` respondeu
- mas normalmente veio `[]`

### Criação de comentários
**Status:** ❌ Não confirmada / falhou

### Task Activities (rodapé do app)
**Status:** ❌ Não exposto claramente na v1 oficial

### Achado importante
O rodapé de “Task Activities” do app **não é `items[]`**.

Também não encontramos endpoint oficial/documentado v1 para:
- history
- activity log
- task timeline

### Conclusão
- o log de atividade existe na UI
- é alimentado automaticamente por ações na task
- mas não está exposto claramente na v1 oficial que mapeamos

---

## 3. Capacidades que o CEO Quest já pode usar com segurança

## 3.1 Rituais recorrentes
Exemplo:
- revisão semanal de domingo
- avaliação mensal
- 1:1s recorrentes

Estrutura segura:
- `content`
- `repeatFlag`
- `reminders`
- `priority`
- `tags`

---

## 3.2 Boss Battles
Estrutura possível:
- card com título do Boss
- descrição/critério no `content`
- fases em `items[]`
- urgência em `priority`
- tag `#boss`

### Observação
Para Boss com checklist, preferir criar o card já com a estrutura final em vez de ir acrescentando `items[]` aos poucos.

---

## 3.3 Campanhas
Estrutura possível:
- tags: `#campanha`, `#sonoramente`
- tarefas principais por frente
- recorrências de revisão
- lembretes
- bandeiras

---

## 3.4 Reino Pessoal Alf
Estrutura possível:
- hábitos nativos
- check-ins
- streak visual do próprio app
- separação por sections (manhã/tarde/noite)

---

## 4. Limitações reais hoje

## 4.1 Append incremental confiável de checklist
**Status:** risco alto

### Problema
Quando a task já existe e recebe update com `items[]`, a API pode tratar isso como substituição do estado do checklist.

### Regra
- checklist complexo deve nascer pronto no `create`
- updates incrementais precisam de extremo cuidado

---

## 4.2 Task Activities / histórico de mudanças
**Status:** não resolvido na v1 oficial

### Situação
A UI mostra histórico como:
- created the task
- edited the content

Mas a v1 oficial não revelou endpoint claro para leitura/escrita disso.

---

## 4.3 Pomodoro / foco / Eisenhower endpoint nativo
**Status:** não resolvido na v1 oficial mapeada

### Observação
A matriz Eisenhower existe visualmente a partir de `priority`, mas endpoint formal específico não foi mapeado.

---

## 5. Payload de referência — card completo oficial

Este payload foi validado em campo como combinação funcional do combo completo:

```json
{
  "title": "LAB TICKTICK — combo completo oficial",
  "projectId": "643c0518525047536b6594cf",
  "content": "10 perguntas...",
  "desc": "Laboratório TickTick: content + desc + checklist + prioridade + lembretes + recorrência.",
  "startDate": "2026-05-04T11:00:00+0000",
  "dueDate": "2026-05-04T13:00:00+0000",
  "timeZone": "America/Sao_Paulo",
  "isAllDay": false,
  "priority": 5,
  "reminders": ["TRIGGER:-PT30M", "TRIGGER:PT0S"],
  "repeatFlag": "RRULE:FREQ=WEEKLY;BYDAY=SU",
  "tags": ["CEO Quest", "Lab"],
  "items": [
    {"title": "Checklist 1", "status": 0, "isAllDay": false, "timeZone": "America/Sao_Paulo"},
    {"title": "Checklist 2", "status": 0, "isAllDay": false, "timeZone": "America/Sao_Paulo"},
    {"title": "Checklist 3", "status": 0, "isAllDay": false, "timeZone": "America/Sao_Paulo"}
  ]
}
```

**Validado visualmente no app em 01/05/2026:** `content` + `desc` + `checklist` + `recorrência` + `tags` + `reminders` + `priority` coexistem renderizando corretamente.

---

## 6. Regras operacionais finais

1. **Usar `repeatFlag`, não `repeat`.**
2. **Usar `priority` = 0/1/3/5.**
3. **Tratar `items[]` como checklist oficial.**
4. **Para coexistência content + checklist, preferir create completo do zero.**
5. **Evitar update incremental de checklist em card sensível.**
6. **Usar `content` para perguntas/rituais longos.**
7. **Usar `tags[]` como camada de taxonomia do jogo.**
8. **Usar Habit Tracker nativo para o reino pessoal sempre que fizer sentido.**

---

## 7. Conclusão final

Sem resiliência a gente não chega a lugar nenhum.

O que parecia limitação da API era, em boa parte, problema de modelagem de payload e de ordem de experimento.

Hoje está documentado que a API v1 oficial do TickTick é robusta o bastante para ser o backend operacional de boa parte do CEO Quest.

Não resolve tudo.
Mas resolve **muito mais** do que parecia no início.

E agora isso deixou de ser achismo.
Virou referência técnica confirmada em campo.
