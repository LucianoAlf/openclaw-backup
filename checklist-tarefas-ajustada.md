---
name: checklist-tarefas
description: Permite que o colaborador fechar, reagendar ou criar tarefas via WhatsApp em linguagem natural — principalmente nas respostas ao fechamento do dia. Reconheça a intenção, responda em texto curto e, quando houver ação suportada, emita um marcador `<<TASK_UPDATE>>...<<END>>` para o engine processar.
---

# Checklist de Tarefas via WhatsApp

## Quando ativar
Ative esta skill quando:
- o colaborador responder ao ritual de fechamento
- o colaborador mencionar uma tarefa de forma acionável
- o colaborador pedir para criar, concluir, reagendar ou lembrar algo

Se a mensagem não tiver ação clara, NÃO use esta skill.

---

## Regra central
Esta skill só deve emitir actions que o engine atual suporta com segurança.

### Actions liberadas
- `complete`
- `reschedule`
- `create`

### Actions não liberadas nesta versão
- `delegate`
- `extension_request`
- `extension_decision`
- qualquer outro action não validado no engine atual

Se o colaborador pedir algo fora das actions liberadas, responda normalmente, mas **não emita marker de ação não suportada**.

---

## Subfluxos

## 1. Fechar tarefa (`complete`)
### Sinais comuns
- “fiz”
- “terminei”
- “feito”
- “completei”
- “fiz a 1”
- “fiz 1 e 2”
- “fiz tudo”

### Regras
- “fiz tudo” → marque todas as tarefas do contexto atual
- número → use a posição da lista no contexto
- parte do título → faça match só se estiver inequívoco
- se houver dúvida sobre qual tarefa é, pergunte **UMA vez** antes do marker
- nunca marque tarefa sem confirmação clara do colaborador

---

## 2. Reagendar tarefa (`reschedule`)
### Sinais comuns
- “não deu”
- “deixa pra amanhã”
- “reagenda”
- “muda pra quinta”
- “passa pra terça”
- “fica pra semana que vem”

### Regras
- se faltar data, pergunte **UMA vez**: `Pra quando?`
- resolva datas relativas em `America/Sao_Paulo`
- “semana que vem” → próxima segunda
- nunca emita `reschedule` sem `new_due_date`
- se a tarefa não estiver clara, pergunte antes

---

## 3. Criar tarefa (`create`)
### Sinais comuns
- “anota aí”
- “anota:”
- “põe na lista”
- “adiciona”
- “marca”
- “lembra de X”

### Regras
- classifique `context` como:
  - `personal` → academia, médico, conta, família, leitura, remédio
  - `work` → reunião, professor, aluno, contrato, projeto, LA Music
- extraia título curto e claro
- prioridade:
  - “urgente” / “importante” → `high`
  - default → `medium`
- sem data → usar hoje
- com hora, mantenha a hora só no texto visível; o marker `create` continua baseado em `due_date`

---

## 4. Lembrete avulso (`create` com `remind_at`)
### Sinais comuns
- “me lembra em 30 min”
- “daqui 2 horas me chama”
- “às 15h me lembra”
- “lembrete pra 14h”

### Regras
- trate como `create` com `remind_at`
- use `context: "personal"` por padrão
- `remind_at` deve ser ISO 8601 com timezone `-03:00`
- use só quando o pedido de lembrete estiver claro
- não invente cálculo se a referência temporal estiver ambígua

---

## Resolução pelo contexto
Tarefas no prompt podem aparecer assim:

```text
1. [id=ab12cd34] Resolver pai aluno Y — ...
2. [id=ef56gh78] Entrevista professor piano — ...
```

### Regras de resolução
- número → posição da lista
- parte do título → só use se o match for inequívoco
- `[id=ab12cd34]` é interno: use no marker, nunca mostre ao usuário
- se houver ambiguidade, pergunte antes

Exemplos de ambiguidade:
- duas tarefas com “reunião” no nome
- nome incompleto que bate em mais de uma tarefa
- “faz aquela do Joel” sem contexto suficiente

---

## Confirmação antes do marker
- se a intenção estiver inequívoca, confirme e emita o marker na mesma resposta
- se a intenção estiver ambígua, faça **UMA pergunta** e espere
- nunca chute

---

## Formato do marcador

```text
<<TASK_UPDATE>>
[
  {"action":"complete","id":"ab12cd34"},
  {"action":"reschedule","id":"ef56gh78","new_due_date":"2026-04-30"},
  {"action":"create","title":"Revisar material teatro","context":"work","due_date":"2026-04-30","priority":"medium"}
]
<<END>>
```

O bloco deve ficar no final da resposta.
Não escreva nada depois de `<<END>>`.

### Campos por action
- `complete`: `{"action":"complete","id":"<8-char>"}`
- `reschedule`: `{"action":"reschedule","id":"<8-char>","new_due_date":"YYYY-MM-DD"}`
- `create`: `{"action":"create","title":"<curto>","context":"personal|work","due_date":"YYYY-MM-DD","priority":"low|medium|high"}`
- `create` com lembrete: `{"action":"create","title":"<curto>","context":"personal","remind_at":"YYYY-MM-DDTHH:MM:SS-03:00"}`

---

## Respostas canônicas

### Criar tarefa pessoal
**User:** `me lembra de pagar conta sexta`

**TOM:**
```text
✅ Anotado!

🗓️ Na sexta (01/05) te lembro de pagar a conta.
```

**Marker:**
```text
<<TASK_UPDATE>>
[{"action":"create","title":"Pagar conta","context":"personal","due_date":"2026-05-01","priority":"medium"}]
<<END>>
```

---

### Criar tarefa de trabalho
**User:** `anota: reunião com Juliana quarta às 10h`

**TOM:**
```text
✅ Anotado!

*Reunião com Juliana*.
🗓️ Quarta (29/04)
⏰ 10h.
```

**Marker:**
```text
<<TASK_UPDATE>>
[{"action":"create","title":"Reunião com Juliana","context":"work","due_date":"2026-04-29","priority":"medium"}]
<<END>>
```

---

### Criar lembrete avulso
**User:** `me lembra em 30 min de tomar remédio`

**TOM:**
```text
✅ Anotado: *Tomar remédio*. ⏰ Em 30 min.
```

**Marker:**
```text
<<TASK_UPDATE>>
[{"action":"create","title":"Tomar remédio","context":"personal","remind_at":"2026-04-26T22:30:00-03:00"}]
<<END>>
```

---

### Reagendar tarefa
**User:** `muda a reunião pra quinta`

**TOM:**
```text
🗓️ Movido: *Reunião com Juliana* — pra quinta (30/04).
```

**Marker:**
```text
<<TASK_UPDATE>>
[{"action":"reschedule","id":"abc12345","new_due_date":"2026-04-30"}]
<<END>>
```

---

### Fechar tarefa
**User:** `fiz a 1`

**TOM:**
```text
✅ Fechado: *Reunião com Juliana*.
```

**Marker:**
```text
<<TASK_UPDATE>>
[{"action":"complete","id":"abc12345"}]
<<END>>
```

---

## Pedidos fora do escopo desta versão

### Delegar tarefa
Se o colaborador pedir para delegar:
```text
Entendi. Delegação ainda não está ativa por aqui.
Se quiser, eu posso deixar isso anotado como tarefa ou te ajudar a reformular o pedido.
```

### Pedir mais prazo
Se o colaborador pedir extensão de prazo:
```text
Entendi. Pedido de prazo ainda não está automatizado por aqui.
Se quiser, eu te ajudo a formular a mensagem pro coordenador.
```

### Aprovar ou negar prazo
Se coordenador pedir decisão de prazo:
```text
Entendi. Aprovação de prazo ainda não está ativa por aqui.
Se quiser, eu te ajudo a escrever a resposta.
```

Nesses casos, **não emita marker**.

---

## Templates de resposta visível
- Criar com hora: `✅ Anotado!\n\n*<título>*.\n🗓️ <dia>\n⏰ <hora>.`
- Criar sem hora: `✅ Anotado!\n\n🗓️ <dia> te lembro de <ação>.`
- Lembrete: `✅ Anotado: *<título>*. ⏰ Em <duração>.`
- Reagenda: `🗓️ Movido: *<título>* — pra <dia>.`
- Fecha total: `✅ Tudo fechado. Bora descansar.`
- Fecha parcial: `✅ 2 de 3 fechado. <título restante> vai pra quando?`
- Fecha uma: `✅ Fechado: *<título>*.`

---

## Veto — nunca
- nunca exiba IDs / UUIDs / `[id=...]`
- nunca invente tarefa fora do contexto, exceto em `create`
- nunca emita `complete` sem confirmação clara do colaborador
- nunca emita `reschedule` sem data resolvida
- nunca misture marker com texto solto fora do bloco final
- `remind_at` deve sempre usar timezone `-03:00`
- nunca emita action não suportada pelo engine atual
- nunca chute match de tarefa ou pessoa em caso ambíguo
