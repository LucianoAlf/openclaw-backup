# TickTick — Payload Patterns reutilizáveis para o CEO Quest

> Biblioteca operacional de payloads prontos para uso.
> Foco: reduzir improviso, reaproveitar padrões validados e acelerar a execução do CEO Quest.
> Baseado em testes reais na API oficial v1 do TickTick.

---

## 1. Regras gerais

### Campo de recorrência
Usar sempre:
- `repeatFlag`

Não confiar em:
- `repeat`

### Campo de bandeira / Eisenhower
Usar:
- `priority: 0` → sem bandeira
- `priority: 1` → baixa / azul
- `priority: 3` → média / amarela
- `priority: 5` → alta / vermelha

### Campo de lembretes
Exemplos válidos:
- `TRIGGER:-PT30M` → 30 minutos antes
- `TRIGGER:PT0S` → na hora

### Campo de checklist
Usar:
- `items[]`

Status correto do item:
- `0` = normal
- `1` = completed

### Regra de ouro
Se a tarefa vai combinar:
- `content`
- `desc`
- `items[]`
- `repeatFlag`
- `reminders`
- `priority`
- `tags`

**prefira criar o card completo no `POST /open/v1/task`**.
Evitar update incremental em tarefa sensível quando houver checklist.

---

## 2. Estrutura base da task

```json
{
  "title": "Título da tarefa",
  "projectId": "<PROJECT_ID>",
  "content": "Conteúdo longo opcional",
  "desc": "Descrição opcional",
  "startDate": "2026-05-04T11:00:00+0000",
  "dueDate": "2026-05-04T13:00:00+0000",
  "timeZone": "America/Sao_Paulo",
  "isAllDay": false,
  "priority": 5,
  "reminders": ["TRIGGER:-PT30M", "TRIGGER:PT0S"],
  "repeatFlag": "RRULE:FREQ=WEEKLY;BYDAY=SU",
  "tags": ["CEO Quest"],
  "items": [
    {"title": "Checklist 1", "status": 0},
    {"title": "Checklist 2", "status": 0}
  ]
}
```

---

## 3. Pattern — Ritual semanal CEO Quest (padrão aprovado)

### Uso
Revisão semanal pessoal + trabalho.

### Quando usar
- domingo de manhã
- ritual recorrente
- reflexão + planejamento
- card oficial recorrente do Ritual da Virada

### Status
**Aprovado visualmente no app do TickTick pelo Alf.**

### Estrutura aprovada
- `title` curto
- **todo o ritual no `desc`**
- checklist final leve em `items[]`
- recorrência semanal no domingo
- lembretes no próprio horário do ritual

### Payload
```json
{
  "title": "Ritual da Virada — Review + Planejamento da Semana",
  "projectId": "<PROJECT_ID>",
  "desc": "🌅 RITUAL DA VIRADA\n\nEste é o momento de fechar a semana anterior com honestidade e entrar na nova semana com direção.\n\n━━━━━━━━━━━━━━━━━━━━━━\n🌱 BLOCO 1 — PESSOAL\n━━━━━━━━━━━━━━━━━━━━━━\n\n1. Como me senti essa semana?\n\n2. O que conquistei?\n\n3. O que ficou faltando?\n\n4. Vivi alinhado com meus valores?\n\n5. O que espero da próxima semana?\n\n━━━━━━━━━━━━━━━━━━━━━━\n🎯 BLOCO 2 — CEO\n━━━━━━━━━━━━━━━━━━━━━━\n\n1. Como foi minha semana como CEO?\n\n2. Quais entregas saíram do time?\n\n3. Onde fui omisso?\n\n4. Os 3 projetos prioritários avançaram?\n\n5. O que precisa sair de mim na semana nova?\n\n━━━━━━━━━━━━━━━━━━━━━━\n📋 BLOCO 3 — FECHAMENTO E PLANEJAMENTO\n━━━━━━━━━━━━━━━━━━━━━━\n\nPendências da semana anterior\nO que ficou aberto e não pode sumir?\n\nTransbordo para a nova semana\nO que precisa entrar na próxima semana?\n\nDistribuição da semana\nO que vai acontecer em cada dia?\n\n━━━━━━━━━━━━━━━━━━━━━━\n✅ SAÍDA FINAL DO RITUAL\n━━━━━━━━━━━━━━━━━━━━━━\n\nAo terminar este ritual, eu preciso sair com:\n\n• clareza sobre a semana passada\n• pendências visíveis\n• prioridades definidas\n• semana distribuída no TickTick",
  "startDate": "2026-05-03T11:00:00+0000",
  "dueDate": "2026-05-03T13:00:00+0000",
  "timeZone": "America/Sao_Paulo",
  "priority": 5,
  "reminders": ["TRIGGER:-PT30M", "TRIGGER:PT0S"],
  "repeatFlag": "RRULE:FREQ=WEEKLY;BYDAY=SU",
  "tags": ["CEO Quest", "Ritual Semanal", "Review", "Planejamento"],
  "items": [
    {"title": "Revisar a semana anterior", "status": 0},
    {"title": "Definir prioridades da nova semana", "status": 0},
    {"title": "Distribuir a semana no TickTick", "status": 0}
  ]
}
```

### Observação
Para o Ritual da Virada, o padrão aprovado foi:
- **não usar `content` como corpo principal**
- usar o **texto completo no `desc`**
- manter apenas um checklist leve no fim

### Bloco pessoal oficial (conteúdo)
O conteúdo oficial do bloco pessoal do ritual passa a ser:
1. **Cumpri o que planejei pra semana ou ficou coisa importante de fora?**
2. **O que me fez bem de verdade essa semana?**
3. **O que me desgastou ou me tirou do eixo?**
4. **O que eu negligenciei no meu pessoal que não posso repetir?**
5. **O que eu não posso deixar de fazer nesta próxima semana?**

### Regra de segurança de formatação
Como o card do TickTick já foi validado visualmente no app, alterações nesse bloco devem ser feitas **com extremo cuidado** para não quebrar a renderização aprovada.
Se houver dúvida, o ajuste fino do texto dentro do card pode ser feito manualmente pelo Alf no TickTick, preservando a estrutura visual validada.

### Regra operacional
Esse card é criado/garantido no TickTick e o ritual é conduzido no **tópico CEO Quest (218)**.
A conversa acontece no tópico. O TickTick guarda o container recorrente oficial.

---

## 4. Pattern — Avaliação mensal

### Uso
Fechamento do mês anterior + projeção do novo mês.

### Payload
```json
{
  "title": "Avaliação do mês anterior + projeção do novo mês",
  "projectId": "<PROJECT_ID>",
  "content": "Revisar o mês que passou e projetar o novo mês.",
  "startDate": "2026-05-01T13:00:00+0000",
  "dueDate": "2026-05-01T13:00:00+0000",
  "timeZone": "America/Sao_Paulo",
  "priority": 5,
  "reminders": ["TRIGGER:-PT30M", "TRIGGER:PT0S"],
  "repeatFlag": "RRULE:FREQ=MONTHLY;BYMONTHDAY=1",
  "tags": ["CEO Quest", "Avaliação Mensal"]
}
```

### Observação
No fuso do Alf, 13:00 UTC = 10:00 BRT.

---

## 5. Pattern — 1:1 recorrente com líder

### Uso
Reunião recorrente de acompanhamento com líder específico.

### Payload
```json
{
  "title": "1:1 Quintela",
  "projectId": "<PROJECT_ID>",
  "content": "Pauta:\n- Avanços\n- Travamentos\n- Próximos passos\n- Cobranças\n- Decisões",
  "startDate": "2026-05-05T12:00:00+0000",
  "dueDate": "2026-05-05T13:00:00+0000",
  "timeZone": "America/Sao_Paulo",
  "priority": 5,
  "reminders": ["TRIGGER:-PT30M", "TRIGGER:PT0S"],
  "repeatFlag": "RRULE:FREQ=WEEKLY;BYDAY=MO",
  "tags": ["CEO Quest", "1:1", "Pedagógico", "Quintela"]
}
```

### Variações
- Juliana
- Krissya
- Rose
- Bianca
- Anne (contexto negócio)

---

## 6. Pattern — Boss Battle com fases

### Uso
Projetos estratégicos com fases visíveis.

### Quando usar
- Jornada do Aluno
- LA Educa
- Reforma Cultural
- LA Organizer

### Payload
```json
{
  "title": "Boss Battle — Jornada do Aluno",
  "projectId": "<PROJECT_ID>",
  "content": "Objetivo: concluir a Jornada do Aluno com fases por instrumento.",
  "desc": "Boss Battle CEO Quest",
  "startDate": "2026-05-06T12:00:00+0000",
  "dueDate": "2026-06-30T21:00:00+0000",
  "timeZone": "America/Sao_Paulo",
  "priority": 5,
  "reminders": ["TRIGGER:-PT30M"],
  "tags": ["CEO Quest", "Boss", "Pedagógico", "Jornada do Aluno"],
  "items": [
    {"title": "Fase 1 — Bateria", "status": 0},
    {"title": "Fase 2 — Canto", "status": 0},
    {"title": "Fase 3 — Cordas", "status": 0},
    {"title": "Fase 4 — Teclas", "status": 0},
    {"title": "Fase 5 — Musicalização", "status": 0}
  ]
}
```

### Observação
Boss com fases = ótimo caso de uso para checklist.

---

## 7. Pattern — Campanha com tag-mãe

### Uso
Quando a campanha é grande e o card serve como âncora central.

### Exemplo
SonoraMente.

### Payload
```json
{
  "title": "Campanha — SonoraMente",
  "projectId": "<PROJECT_ID>",
  "content": "Campanha estratégica com múltiplos Boss internos: jurídico, marca, operação clínica, ERP e lançamento comercial.",
  "desc": "Campanha CEO Quest",
  "startDate": "2026-05-01T12:00:00+0000",
  "dueDate": "2026-08-31T21:00:00+0000",
  "timeZone": "America/Sao_Paulo",
  "priority": 5,
  "tags": ["CEO Quest", "Campanha", "SonoraMente"]
}
```

### Observação
Em campanha, o ideal é usar vários cards filhos com a mesma tag, não um checklist gigante só.

---

## 8. Pattern — Tarefa CEO simples com Eisenhower

### Uso
Cobrança, decisão ou tarefa rápida do jogo.

### Payload
```json
{
  "title": "Cobrar Quintela sobre LA Educa",
  "projectId": "<PROJECT_ID>",
  "content": "Verificar status da grade e cobrar prazo.",
  "startDate": "2026-05-01T15:00:00+0000",
  "dueDate": "2026-05-01T15:00:00+0000",
  "timeZone": "America/Sao_Paulo",
  "priority": 5,
  "tags": ["CEO Quest", "Pedagógico", "Cobrança"]
}
```

### Observação
Ideal para ações que sustentam streak.

---

## 9. Pattern — Tarefa de apoio com prioridade média

### Uso
Acompanhamentos importantes mas não urgentes.

### Payload
```json
{
  "title": "Revisar proposta de campanha de julho",
  "projectId": "<PROJECT_ID>",
  "content": "Analisar campanha antes da aprovação final.",
  "startDate": "2026-05-02T16:00:00+0000",
  "dueDate": "2026-05-02T16:00:00+0000",
  "timeZone": "America/Sao_Paulo",
  "priority": 3,
  "tags": ["CEO Quest", "Comercial", "Marketing"]
}
```

---

## 10. Pattern — Tarefa sem urgência operacional

### Uso
Backlog útil, não urgente.

### Payload
```json
{
  "title": "Pensar melhorias na régua do CEO Quest",
  "projectId": "<PROJECT_ID>",
  "content": "Capturar ideias sem urgência imediata.",
  "startDate": "2026-05-03T17:00:00+0000",
  "dueDate": "2026-05-03T17:00:00+0000",
  "timeZone": "America/Sao_Paulo",
  "priority": 1,
  "tags": ["CEO Quest", "Meta", "Backlog"]
}
```

---

## 11. Pattern — Tarefa sem prioridade

### Uso
Quando a tarefa existe, mas não deve carregar nenhuma bandeira nem interferir na leitura de urgência do jogo.

### Payload
```json
{
  "title": "Registrar ideia para revisar depois",
  "projectId": "<PROJECT_ID>",
  "content": "Nota sem urgência nem peso de cobrança.",
  "startDate": "2026-05-03T18:00:00+0000",
  "dueDate": "2026-05-03T18:00:00+0000",
  "timeZone": "America/Sao_Paulo",
  "priority": 0,
  "tags": ["CEO Quest", "Inbox", "Sem prioridade"]
}
```

---

## 12. Pattern — Hábito pessoal

### Uso
Reino 🌱 Pessoal Alf.

### Payload
```json
{
  "name": "Meditação 10 min",
  "type": "Boolean"
}
```

### Fluxo
1. criar hábito
2. fazer check-in diário
3. acompanhar streak no app

### Outros hábitos sugeridos
- Academia
- Leitura matinal
- Caminhada com Lala
- Água às 8h

---

## 13. Pattern — Ritual pessoal curto

### Uso
Mini-ritual sem checklist, focado em corpo/mente.

### Payload
```json
{
  "title": "Ritual pessoal — corpo + mente",
  "projectId": "<PROJECT_ID>",
  "content": "1. Academia ou caminhada\n2. Meditação 10 min\n3. Leitura 15 min\n4. Não pegar celular antes",
  "startDate": "2026-05-04T10:00:00+0000",
  "dueDate": "2026-05-04T11:00:00+0000",
  "timeZone": "America/Sao_Paulo",
  "priority": 3,
  "repeatFlag": "RRULE:FREQ=WEEKLY;BYDAY=SU",
  "tags": ["CEO Quest", "Pessoal Alf"]
}
```

---

## 14. Pattern — Ação CEO (cobrança/verificação que gera streak)

### Uso
Pattern mais importante do CEO Quest no dia a dia.

### Por que é crítico
- toda ação CEO registrada com tag `Ação CEO` é candidata a contar para a streak
- tag da pessoa permite filtrar histórico de cobrança
- tag do reino permite medir onde o Alf está investindo presença
- serve para cobrar, verificar, decidir e destravar

### Payload
```json
{
  "title": "Cobrar Quintela sobre LA Educa",
  "projectId": "<PROJECT_ID>",
  "content": "Cobrança real. Verbo direto: cadê. Prazo: até quinta.",
  "startDate": "2026-05-01T15:00:00+0000",
  "dueDate": "2026-05-02T21:00:00+0000",
  "timeZone": "America/Sao_Paulo",
  "priority": 5,
  "tags": ["CEO Quest", "Ação CEO", "Pedagógico", "Quintela"]
}
```

### Variações
- Cobrar Juliana sobre Jornada do Aluno
- Verificar Krissya sobre relatório de leads
- Destravar Yuri sobre conteúdo pendente
- Decidir com Bianca questão da SonoraMente

---

## 15. Pattern — Task laboratório

### Uso
Testes de payload sem contaminar cards reais.

### Convenção sugerida
- título sempre começa com `LAB TICKTICK —`
- tag `Lab`
- nunca usar em card real

### Payload
```json
{
  "title": "LAB TICKTICK — nome do teste",
  "projectId": "<PROJECT_ID>",
  "content": "Objetivo do teste",
  "priority": 1,
  "tags": ["Lab", "CEO Quest"]
}
```

---

## 16. Pattern — Boss Battle dentro de Campanha

### Uso
Quando um Boss faz parte de uma Campanha maior e precisa carregar esse vínculo no próprio card.

### Exemplo
Boss SonoraMente Jurídico dentro da Campanha SonoraMente.

### Payload
```json
{
  "title": "Boss Battle — SonoraMente Jurídico",
  "projectId": "<PROJECT_ID>",
  "content": "Regularizar estrutura jurídica e regulatória da SonoraMente.",
  "desc": "Boss interno da Campanha SonoraMente",
  "startDate": "2026-05-06T12:00:00+0000",
  "dueDate": "2026-06-15T21:00:00+0000",
  "timeZone": "America/Sao_Paulo",
  "priority": 5,
  "tags": ["CEO Quest", "Boss", "Campanha", "SonoraMente", "Jurídico"],
  "items": [
    {"title": "Contrato social alinhado", "status": 0},
    {"title": "Responsável técnico validado", "status": 0},
    {"title": "Documentação regulatória revisada", "status": 0}
  ]
}
```

### Regra de conexão pai-filho por tag
A Campanha carrega a tag-mãe:
- `Campanha`
- `SonoraMente`

O Boss interno herda:
- `Boss`
- `Campanha`
- `SonoraMente`
- e a frente específica (`Jurídico`, `Marca`, `ERP`, etc.)

---

## 17. Regras de modelagem recomendadas

### Regra 1 — Ritual longo não precisa de checklist por padrão
Usar só `content` + recorrência + reminder + prioridade + tag.

### Regra 2 — Boss Battle combina melhor com checklist
Usar `items[]` desde o nascimento.

### Regra 3 — Não misturar teste com card real
Todo experimento novo deve nascer como `LAB TICKTICK — ...`.

### Regra 4 — Cuidado com update incremental em checklist
Se a tarefa já tem `items[]`, update mal feito pode sobrescrever.

### Regra 5 — Tags são taxonomia do jogo
Tags ajudam a cruzar:
- reino
- boss
- campanha
- cadência
- contexto

---

## 18. Tags sugeridas para o CEO Quest

### Estruturais
- `CEO Quest`
- `Boss`
- `Campanha`
- `Ritual`
- `1:1`
- `Lab`

### Reinos
- `Pessoal Alf`
- `Pedagógico`
- `Operação`
- `Comercial`
- `Marketing`
- `Financeiro`
- `Gente`
- `Tecnologia`
- `Estratégia`

### Campanhas / projetos
- `SonoraMente`
- `LA Educa`
- `Jornada do Aluno`
- `LA Organizer`

---

## 19. Conclusão final

Com essa biblioteca, o Alfredo para de improvisar payload e passa a trabalhar com padrões já validados.

Isso aumenta:
- velocidade
- consistência
- previsibilidade
- resiliência operacional

E reduz:
- retrabalho
- payload torto
- teste burro em card real
- risco de bagunçar estrutura boa

A ideia é simples:

> primeiro padrão, depois automação.

Sem isso, o jogo vira gambiarra.
Com isso, o TickTick vira backend operacional de verdade para o CEO Quest.
