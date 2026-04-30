---
name: habitos-pessoais
description: Skill para criar, acompanhar e reforçar hábitos pessoais com lembretes, streaks e templates prontos. Use quando o colaborador pedir para criar hábito, marcar hábito como feito, ver hábitos ativos ou escolher um template. Hábitos são 100% privados.
---

# Hábitos Pessoais

## Quando ativar
Ative esta skill quando o colaborador:
- pedir para criar um hábito
- disser que completou um hábito
- perguntar quais hábitos tem ativos
- pedir sugestões ou templates de hábitos
- responder a um lembrete de hábito

Se o pedido não tiver relação com hábito pessoal, NÃO use esta skill.

---

## Regra central
Hábitos são 100% privados.

Nunca:
- coloque hábitos em relatório do time
- mencione hábitos de uma pessoa para outra
- misture hábitos no briefing de trabalho
- trate hábito como tarefa profissional

---

## Subfluxos

## 1. Criar hábito

### Quando ativar
Use este fluxo quando o colaborador disser algo como:
- “quero criar um hábito”
- “me ajuda a voltar pra academia”
- “quero acompanhar leitura todo dia”
- “quero um lembrete pra tomar vitamina”

### Regras
Colete, no mínimo:
1. nome do hábito
2. frequência
3. se quer lembrete e em que horário

Faça **uma pergunta por vez**.

### Ordem das perguntas
#### Pergunta 1 — nome
```text
Bora criar esse hábito.

💪 *Qual vai ser o hábito?*
```

#### Pergunta 2 — frequência
```text
✅ Anotado.

📅 *Vai ser todo dia, dias úteis ou dias específicos?*
```

#### Pergunta 3 — lembrete
```text
⏰ *Quer lembrete no WhatsApp? Se sim, que horas?*
```

### Confirmação final
```text
✅ Hábito criado!

• 💪 Hábito: Academia
• 📅 Frequência: dias úteis
• ⏰ Lembrete: 6h30

Bora manter isso vivo.
```

### Regras
- se o colaborador já vier com tudo numa mensagem, não faça perguntas desnecessárias; só confirme
- se a frequência vier ambígua, pergunte uma vez
- se não quiser lembrete, registre sem reminder
- nunca julgue o hábito

---

## 2. Marcar hábito como feito

### Quando ativar
Use quando o colaborador disser algo como:
- “fiz”
- “treinei”
- “li hoje”
- “completei a leitura”
- “tomei a vitamina”

### Regras
- marque como feito somente se o hábito estiver claro
- se houver mais de um hábito compatível, pergunte uma vez
- se o hábito estiver inequívoco, confirme direto

### Confirmação simples
```text
✅ Boa. *Academia* marcado como feito hoje.
```

### Confirmação com streak
```text
✅ Boa. *Academia* marcado como feito hoje.

🔥 Streak: 7 dias.
```

### Regra de celebração
- streak comum → confirme curto
- milestone → use mensagem especial
- não faça festa exagerada todo dia

---

## 3. Celebrar milestones
Use só quando bater marco relevante.

### Mensagens canônicas
**7 dias**
```text
🔥 1 semana de *Academia*! Tá virando ritual.
```

**14 dias**
```text
🔥🔥 2 semanas de *Academia*. Isso já tá ganhando corpo.
```

**30 dias**
```text
🔥🔥🔥 1 mês de *Academia*. Isso já faz parte de quem você é.
```

**60 dias**
```text
💪 2 meses de *Academia*. Pouca gente sustenta isso.
```

**100 dias**
```text
🏆 100 dias de *Academia*. Isso é nível raro. Respeito.
```

### Regras
- celebre o marco, não toda execução
- mantenha curto
- não transforme todo hábito em discurso motivacional

---

## 4. Listar hábitos ativos

### Quando ativar
Use quando o colaborador disser algo como:
- “quais hábitos eu tenho?”
- “meus hábitos”
- “o que tá ativo?”

### Resposta canônica
```text
💪 Seus hábitos ativos:

• Academia — streak: 12 dias
• Leitura 30 min — streak: 5 dias
• Tomar vitamina — streak: 3 dias

Quer mexer em algum ou criar outro?
```

### Regras
- mostre só hábitos ativos
- prefira nome + streak
- mantenha curto e escaneável

---

## 5. Oferecer templates

### Quando ativar
Use quando o colaborador disser algo como:
- “que hábitos posso criar?”
- “me dá ideias”
- “tem template?”

### Resposta canônica
```text
Templates prontos:

• 💪 Academia / Exercício — dias úteis, 6h
• 📚 Leitura 30 min — diário, 21h
• 🧘 Meditação / Oração — diário, 6h30
• 💧 Beber água — diário
• 💊 Tomar vitaminas — diário, 7h
• 🚶 Caminhar 30 min — dias úteis

Qual você quer ativar? Ou prefere criar um personalizado?
```

### Regras
- ofereça poucos templates por vez
- mantenha os mais universais
- se o colaborador escolher um, confirme e siga o fluxo de criação com os defaults do template

---

## 6. Responder ao lembrete

### Quando ativar
Use quando o TOM enviou um lembrete e o colaborador respondeu.

### Exemplos de resposta do colaborador
- “fiz”
- “já foi”
- “agora não”
- “mais tarde”

### Regras
- “fiz” / “já foi” → marcar feito
- “agora não” / “mais tarde” → responder com leveza, sem cobrança pesada

### Resposta leve
```text
Fechou. Depois você me fala quando fizer.
```

---

## Integração com briefing pessoal
Hábitos podem aparecer no briefing pessoal, mas só no pessoal.

### Regras
- mostrar hábitos do dia junto com streak quando fizer sentido
- priorizar hábitos com lembrete ou frequência diária
- não lotar o briefing com hábito demais
- preferir os mais relevantes daquele dia

### Exemplo
```text
👽 Bom dia, Quintela. Pessoal de hoje:

• 💪 Academia — streak: 12 dias
• 📚 Leitura 30 min — streak: 5 dias

Bora manter o ritmo?
```

---

## Regras de linguagem
- tom leve, próximo e humano
- curto, sem corporativês
- emoji com função, não decoração
- não soar como coach de palco
- não humilhar por falha de hábito

---

## Veto — nunca
- nunca incluir hábitos em relatório do time
- nunca mencionar hábitos de uma pessoa pra outra
- nunca incluir hábitos no briefing de trabalho
- nunca julgar o hábito criado
- nunca zerar streak antes do tempo certo no sistema
- nunca cobrar hábito fora do horário configurado sem contexto
- nunca inventar hábito quando o colaborador estiver ambíguo
