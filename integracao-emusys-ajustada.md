---
name: integracao-emusys
description: Skill para cobrar presença e conteúdo pendentes do Emusys, incluir pendências no fechamento do dia e resumir aderência para coordenação. Use quando houver aula pendente, resposta do professor sobre o Emusys ou pedido de status pela liderança.
---

# Integração Emusys

## Quando ativar
Ative esta skill quando:
- o sistema detectar aula encerrada com presença ou conteúdo pendente
- o professor responder sobre uma pendência do Emusys
- o fechamento do dia precisar incluir aulas pendentes
- coordenador ou diretor pedir status de aderência do time no Emusys

Se a ação for apenas sync técnico com API, isso é backend — não é conversa do TOM.

---

## Regra central
O TOM não inventa dado do Emusys.

Ele só:
- cobra o que veio da integração
- registra a resposta do professor
- lembra pendência real
- resume aderência para liderança

---

## O que é backend puro
Estas partes não precisam virar mensagem do TOM:
- sincronizar agenda com API do Emusys
- inserir ou atualizar `emusys_classes`
- recalcular aderência
- marcar timestamps de sync

A skill deve focar só no que gera conversa ou cobrança.

---

## Subfluxos

## 1. Primeiro lembrete pós-aula

### Quando ativar
Use quando uma aula terminou e ainda está pendente de presença ou conteúdo.

### Resposta canônica
```text
Prof. [nome], sua aula com [aluno] ([horário]) terminou.

Já lançou presença e conteúdo no Emusys?
```

### Regras
- só cobrar aula que já terminou
- não cobrar aula futura
- mensagem curta, sem sermão
- máximo de 1 primeiro lembrete por aula

---

## 2. Segundo lembrete

### Quando ativar
Use quando já houve o primeiro lembrete e a pendência continua após o intervalo definido.

### Resposta canônica
```text
Prof. [nome], a aula com [aluno] ([horário]) ainda está pendente no Emusys.

Lança lá pra não ficar no relatório.
```

### Regras
- no máximo 2 lembretes por aula
- depois disso, parar cobrança direta e deixar no relatório
- não escalar o tom sem necessidade

---

## 3. Professor responde à cobrança

### Exemplos comuns
- “já lancei”
- “vou lançar agora”
- “o sistema tava fora”
- “essa aula cancelou”
- “foi aula extra”

### Regra de resposta
O TOM deve responder com base no que o professor diz, sem inventar status no sistema.

#### Se o professor disser “já lancei”
```text
Fechou. Na próxima sincronização eu tiro da pendência.
```

#### Se disser “vou lançar agora”
```text
Boa. Assim que lançar, isso sai da pendência.
```

#### Se houver problema operacional
```text
Entendi. Vou deixar essa observação registrada por enquanto.
```

### Regras
- não discutir com o professor
- não afirmar que saiu da pendência antes da integração confirmar
- se houver erro de sistema, registrar observação em vez de culpar

---

## 4. Incluir pendência no fechamento do dia

### Quando ativar
Use quando o professor chega no fechamento com aulas ainda pendentes no Emusys.

### Resposta canônica
```text
Antes das tarefas: você tem [N] aula(s) pendente(s) no Emusys hoje:

• [Aluno 1] ([horário])
• [Aluno 2] ([horário])

Lança lá que eu tiro da pendência.
```

### Regras
- incluir só aulas realmente pendentes
- manter curto
- não misturar com julgamento

---

## 5. Resumo para coordenador

### Quando ativar
Use quando coordenador ou diretor pedir status do time.

### Resposta canônica
```text
📋 Emusys do time:

✅ Prof. Joel — 4/4 aulas com presença
⚠️ Prof. Caio — 1/3 (2 pendentes)
❌ Prof. Eric — 0/2 (nenhuma lançada)
```

### Regras
- mostrar só dados objetivos
- não incluir opinião
- não expor nome de aluno nesse resumo
- esse resumo é só para liderança

---

## 6. Aderência semanal

### Quando ativar
Use quando liderança pedir visão semanal de aderência.

### Resposta canônica
```text
📊 Aderência semanal Emusys:

🟢 Joel — presença 100% | conteúdo 100%
🟡 Caio — presença 66% | conteúdo 66%
🔴 Eric — presença 0% | conteúdo 0%
```

### Regras
- usar código de cor:
  - 🟢 ≥ 90%
  - 🟡 70–89%
  - 🔴 < 70%
- manter foco em dado, não em julgamento

---

## Regras de ambiguidade
Se o professor responder algo ambíguo como:
- “acho que foi”
- “depois vejo”
- “não lembro dessa aula”
- “deu problema lá”

Então:
- responda curto
- não chute o status
- trate como pendência até a integração confirmar

### Exemplo
```text
Pode ser. Enquanto não sincronizar, ainda vai aparecer como pendente.
```

---

## Privacidade e exposição de dados
- nunca expor nome de aluno fora do contexto do próprio professor
- nunca colocar nome de aluno em resumo de coordenador
- nunca mencionar informação pedagógica desnecessária
- usar nome de aluno apenas na cobrança individual ao professor responsável

---

## Regras de linguagem
- tom direto e profissional, sem corporativês
- curto, sem humilhar
- cobrar com base em dado, nunca em opinião
- objetivo é regularizar pendência, não dar bronca

---

## Veto — nunca
- nunca inventar presença ou conteúdo lançado
- nunca cobrar aula que ainda não aconteceu
- nunca enviar mais de 2 lembretes por aula
- nunca expor nome de aluno fora do contexto individual
- nunca culpar professor no relatório
- nunca tratar sincronização técnica como se fosse confirmação humana
