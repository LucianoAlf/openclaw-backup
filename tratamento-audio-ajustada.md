---
name: tratamento-audio
description: Skill para interpretar mensagens de voz do colaborador, confirmar entendimento e só então encaminhar a ação correta. Use quando o colaborador enviar áudio via WhatsApp.
---

# Tratamento de Áudio

## Quando ativar
Ative esta skill quando o colaborador enviar uma mensagem de voz via WhatsApp.

Se a entrada não for áudio, NÃO use esta skill.

---

## Regra central
Áudio nunca vira ação automática direto.

O fluxo correto é:
1. transcrever
2. interpretar
3. resumir o entendimento
4. confirmar com o colaborador
5. só depois executar a ação correspondente

---

## Papel desta skill
Esta skill é principalmente de interpretação e confirmação.

### O que ela faz
- recebe o conteúdo transcrito do áudio
- interpreta a intenção
- resume o que entendeu
- confirma com o colaborador
- depois entrega a execução para a skill ou action correspondente

### O que ela não faz sozinha
- não executa ação sem confirmação
- não mostra transcrição bruta
- não inventa significado se o áudio estiver ruim

---

## Subfluxos

## 1. Áudio simples com uma ação clara

### Exemplos comuns
- “fiz a entrevista do professor”
- “marca reunião com Juliana amanhã”
- “me lembra de pagar a conta”

### Resposta canônica
```text
Entendi: *Entrevista do professor* — feito ✅.

Certo?
```

### Regra
- se houver uma ação clara e única, confirme de forma curta
- não execute antes do “sim” do colaborador

---

## 2. Áudio com múltiplas ações

### Exemplo comum
O colaborador conclui uma coisa, reagenda outra e dá contexto adicional no mesmo áudio.

### Resposta canônica
```text
Entendi do áudio:

• ✅ Entrevista do professor — feita
• 🗓️ Material teatro — pra quinta
• 📝 Reunião com pai de aluno tomou a tarde

Tá certo isso?
```

### Regra
- listar na ordem em que o colaborador falou
- separar ação de contexto
- não exagerar no tamanho

---

## 3. Áudio ambíguo

### Exemplos comuns
- “tô vendo aquela parada lá do Renan”
- “acho que foi aquilo mesmo”
- “depois eu resolvo isso”

### Resposta canônica
```text
Não ficou claro pra mim.

Você tá falando de *ligar pro Renan* ou *revisar o material do Renan*?
```

### Regra
- fazer uma pergunta curta
- nunca chutar a intenção
- não emitir action enquanto houver ambiguidade

---

## 4. Áudio com transcrição ruim ou incompleta

### Quando ativar
Use quando a transcrição vier ruim, truncada ou sem sentido suficiente.

### Resposta canônica
```text
Não consegui entender bem esse áudio.

Se puder, me manda de novo — pode ser em texto também.
```

### Regra
- não fingir entendimento
- oferecer saída simples
- não constranger o colaborador

---

## 5. Áudio que traz só contexto, sem ação

### Exemplos comuns
- desabafo breve
- explicação do dia
- justificativa sem pedido objetivo

### Resposta canônica
```text
Entendi.

Valeu por me contextualizar.
```

### Regra
- se não houver ação, não invente uma
- contexto pode servir para a próxima resposta, mas não deve virar execução automática

---

## Confirmação antes de agir
Só execute algo depois de sinais como:
- “sim”
- “isso”
- “certo”
- “isso mesmo”
- “é isso”

Se o colaborador corrigir, ajuste o entendimento e confirme de novo.

### Exemplo
```text
Entendi então assim:

• ✅ Entrevista do professor — feita ontem
• 🗓️ Material teatro — ficou pra quinta

Agora sim tá certo?
```

---

## Handoff para outras skills/actions
Depois da confirmação, a execução deve seguir o fluxo apropriado.

### Exemplos
- tarefa concluída → fluxo de `checklist-tarefas`
- reagendamento → fluxo de `checklist-tarefas`
- criação de tarefa → fluxo de `checklist-tarefas`
- contexto relevante → memória, se fizer sentido

### Regra
Esta skill normalmente **não define um marker próprio**.
Ela interpreta e confirma. A action final deve ser emitida pelo fluxo correspondente após a confirmação.

---

## Tolerância a erro de transcrição
Aceite como natural erros como:
- “Open Claw” → OpenClaw
- “clã de ferro” → Claude Code
- “L.A.” → LA Music
- “é o muses” / “e-muses” → Emusys
- “tom” → TOM

Use o contexto da conversa para interpretar melhor.

---

## Regras de linguagem
- tom curto, leve e natural
- sem mostrar a transcrição bruta
- sem parecer robô de transcrição
- confirmar entendimento em linguagem humana
- se errar, corrigir sem drama

---

## Veto — nunca
- nunca presumir que entendeu 100%
- nunca agir com base em áudio sem confirmação
- nunca mostrar a transcrição bruta pro colaborador
- nunca guardar o arquivo de áudio como memória de longo prazo
- nunca inventar intenção quando o áudio estiver ambíguo
- nunca ignorar um áudio; se não entender, peça repetição
