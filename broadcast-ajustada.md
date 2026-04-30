---
name: broadcast
description: Permite que coordenador, gerente ou diretor enviar comunicações em massa via WhatsApp, com confirmação prévia, follow-up opcional e relatório final. Use quando liderança pedir para avisar, comunicar ou notificar um grupo de pessoas.
---

# Broadcast

## Quando ativar
Ative esta skill quando:
- um `coordinator`, `manager` ou `director` pedir para avisar várias pessoas
- houver intenção clara de comunicar um grupo, equipe, unidade ou lista de nomes

Se a mensagem não for de liderança ou não envolver envio em massa, NÃO use esta skill.

---

## Regra central
Broadcast só pode acontecer com:
1. permissão válida
2. grupo-alvo resolvido
3. confirmação explícita do remetente

Sem esses 3 itens, **não envie nada**.

---

## Fluxo

## 1. Verificar permissão
Se o role não for `coordinator`, `manager` ou `director`, responda:

```text
Broadcast é função de coordenação. Quer que eu passe o pedido pro seu supervisor?
```

Pare aí. Não continue o fluxo.

---

## 2. Resolver grupo-alvo
Converta o grupo pedido em destinatários reais.

### Exemplos de grupo
- `assistentes`
- `professores`
- `coordenadores`
- `todos`
- `time do Recreio`
- `equipe do projeto X`
- lista explícita: `Joel, Eric, Jordão`

### Regras
- se o grupo estiver claro e resolvível, siga
- se houver ambiguidade, pergunte **UMA vez** antes de continuar
- nunca inclua o remetente no broadcast `todos`, salvo se ele pedir explicitamente
- nunca assuma nomes ou grupos que não baterem claramente no banco

### Casos ambíguos
Pergunte uma vez quando houver dúvida, por exemplo:

```text
Quando você diz “time comercial”, quer Campo Grande, Recreio, Barra ou todo o comercial?
```

ou

```text
Tem dois “João” aqui. Você quer o João do Recreio ou o João da Barra?
```

---

## 3. Confirmar com o remetente
Antes de disparar, confirme sempre.

Use este formato:

```text
Vou mandar pra [N] pessoas:

• [lista curta de nomes ou grupo]
• Mensagem: "[conteúdo]"
• Confirmação: [sim/não]
• Cobrança: a cada [interval] min por [timeout]h

Confirma o envio?
```

### Regras
- só prossiga se o remetente disser algo como: `sim`, `confirma`, `manda`, `bora`
- se o remetente ajustar texto, grupo ou regra de confirmação, atualize e reconfirme
- nunca envie sem confirmação explícita

---

## 4. Enviar broadcast
Depois da confirmação:
- criar o registro do broadcast
- criar os registros individuais de resposta
- enviar a mensagem a cada destinatário

### Texto visível para os destinatários
Sem confirmação obrigatória:

```text
[Nome], aviso de [nome do remetente]:

[mensagem]
```

Com confirmação obrigatória:

```text
[Nome], aviso de [nome do remetente]:

[mensagem]

Me confirma por aqui, por favor.
```

### Regras
- sempre identificar o remetente humano
- nunca enviar como se a mensagem fosse do TOM
- nunca incluir dado pessoal irrelevante

---

## 5. Follow-up de confirmação
Só faça follow-up se `requires_confirmation = true`.

### Texto de cobrança
```text
[Nome], ainda preciso da sua confirmação sobre:

[resumo curto da mensagem]

Confirma pra mim?
```

### Regras
- no máximo 1 cobrança por intervalo configurado
- nunca cobrar quem já respondeu
- nunca bombardear
- se o destinatário recusou, pare de cobrar

---

## 6. Processar resposta do destinatário
### Confirmou
Sinais comuns:
- `sim`
- `confirmado`
- `ok`
- `vou`

→ registrar como `confirmed`

### Recusou
Sinais comuns:
- `não vou`
- `não posso`
- `não consigo`

→ registrar como `declined`

### Regras
- resposta curta ainda vale, se estiver inequívoca
- se a resposta estiver ambígua, não invente status

---

## 7. Gerar relatório final
Quando o tempo do broadcast acabar, enviar relatório ao remetente.

### Formato
```text
Relatório do broadcast:

✅ Confirmados ([N]): [nomes]
❌ Recusaram ([N]): [nomes]
⏳ Sem resposta ([N]): [nomes]

Quer que eu continue cobrando os que não responderam?
```

### Regras
- se o remetente disser sim, continue follow-up
- se disser não, encerre
- não inclua detalhes pessoais desnecessários

---

## Regras de linguagem
- tom curto, claro e direto
- sem linguagem corporativa pesada
- mensagens de confirmação e relatório devem ser legíveis no WhatsApp
- listas com `•`
- no máximo 4–6 blocos curtos por mensagem

---

## Veto — nunca
- nunca enviar broadcast sem confirmação do remetente
- nunca permitir broadcast vindo de `collaborator`
- nunca incluir dados pessoais desnecessários de destinatários
- nunca cobrar mais de 1 vez por intervalo configurado
- nunca continuar cobrando quem já respondeu
- nunca fingir que o TOM é o autor da mensagem
- nunca resolver grupo ambíguo no chute

---

## Checklist operacional
- permissão validada
- grupo-alvo resolvido
- confirmação do remetente recebida
- broadcast criado
- destinatários individuais registrados
- mensagens enviadas
- follow-up aplicado se necessário
- respostas registradas
- relatório final enviado
- status final encerrado corretamente
