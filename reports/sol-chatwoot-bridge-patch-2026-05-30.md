# Relatório — Patch do Chatwoot Sol Bridge

Data: 2026-05-30 02:05–02:10 UTC  
Executor: Alfredo  
Host: `lahq`  
Arquivo alterado: `/home/sol/.openclaw/workspace/scripts/chatwoot-sol-bridge.js`

## Objetivo

Corrigir o bridge do Chatwoot para manter a segurança operacional sem achatar a Sol em um bot genérico.

A meta foi deixar o bridge como **porteiro e validador**, enquanto a Sol volta a decidir atendimento com contexto, tom, risco e handoff.

## Backup

Antes de alterar, foi criado backup do arquivo original em:

`/home/sol/.openclaw/workspace/backups/chatwoot-sol-bridge.20260530-020625.js`

Checksum antes do patch:

`71650dec0ad17411405d537110130990b8a2071227e42047c98ae69b2bb2968e`

Checksum depois do patch:

`fb56a41a4c57de0dfbd2746fc604dd48f2b662671f5855e8bf5b863a7e8ec452`

## O que estava errado

O bridge tinha saído de um extremo para outro:

1. Antes: resposta hardcoded/genérica deixava a Sol burra.
2. Depois: sensíveis iam direto para resposta externa, sem decisão estruturada de risco/handoff.

O problema principal era que o bridge pedia apenas uma mensagem externa, assim:

> “Responda SOMENTE com a mensagem externa”

Isso não dava ao bridge informação suficiente para decidir se deveria enviar, escalar ou criar nota interna.

## O que foi alterado

### 1. Saída estruturada da Sol

Foi criado o fluxo `buildSolAtendimentoDecision()`.

Agora a Sol precisa responder em JSON válido:

```json
{
  "intent": "saudacao|duvida_simples|primeira_aula|reposicao|financeiro|atualizacao_cadastral|reclamacao|cancelamento|juridico|outro",
  "risk": "low|medium|high|critical",
  "external_reply": "mensagem curta para o cliente, ou vazio se não deve enviar",
  "handoff_required": true,
  "internal_note": "nota para equipe humana",
  "allowed_to_send": false,
  "confidence": 0.0
}
```

### 2. Bridge decide envio com base em risco

Nova regra:

- `allowed_to_send=true`
- `handoff_required=false`
- `risk=low|medium`
- `external_reply` preenchida

Somente nesse caso o bridge envia mensagem externa.

Se não passar nesses critérios, o bridge **não envia para o cliente** e cria uma **nota privada interna** no Chatwoot.

### 3. Casos sensíveis viram handoff

O prompt agora instrui a Sol:

- cancelamento;
- trancamento;
- reclamação;
- insatisfação;
- professor/aula/atendimento/unidade;
- desconto;
- negociação;
- exceção;
- jurídico/Procon;
- contrato duvidoso;
- irritação;
- vulnerabilidade;
- dado inconsistente.

Esses casos devem sair com:

```json
"handoff_required": true,
"allowed_to_send": false
```

Ou seja: viram nota interna, não resposta automática externa.

### 4. Nota privada interna no Chatwoot

Foi criada a função `sendChatwootPrivateNote()`.

Quando a Sol identifica risco alto/crítico ou handoff, o bridge cria uma nota interna com:

- intenção;
- risco;
- se precisa humano;
- se a Sol permitiria envio;
- resposta sugerida, se houver;
- observação interna;
- mensagem original do cliente.

### 5. Logs melhores

Foi adicionado evento de log `sol_decision`, registrando:

- `intent`;
- `risk`;
- `handoff_required`;
- `allowed_to_send`;
- `parse_error`;
- prévia da resposta externa.

Isso permite auditar por que a Sol enviou ou não enviou.

### 6. Fallback genérico deixou de ser usado como resposta externa

Se a Sol responder inválido/não JSON, o bridge não manda “Como posso ajudar?” para o cliente.

Agora ele trata como erro de decisão e cria nota interna.

## O que continua protegido

O bridge ainda mantém:

- só responde se `CHATWOOT_MODE=auto_reply`;
- só aceita mensagem nova `incoming`;
- exige `conversation_id`;
- exige texto;
- evita duplicidade;
- consulta status real do Chatwoot antes de chamar a Sol;
- só prossegue se status real for `pending`;
- consulta status real novamente antes de enviar mensagem externa;
- mantém typing status on/off;
- mantém logs.

## Estado final verificado

Validação sintática:

`node --check scripts/chatwoot-sol-bridge.js` passou.

Healthcheck:

```json
{"ok":true,"service":"chatwoot-sol-bridge","mode":"auto_reply"}
```

Processos ativos:

- supervisor do bridge ativo;
- processo Node `chatwoot-sol-bridge.js` ativo.

## Observação importante

O bridge agora está no desenho correto:

**Chatwoot → bridge seguro → Sol decide intenção/risco → bridge envia ou cria nota interna**

Ele não é mais mini-bot burro, nem porteira aberta.

## Próximos testes recomendados

Rodar em conversa pendente de teste:

1. Saudação simples: deve responder externo.
2. Primeira aula/endereço: só responder se fonte/contexto permitir; se não, pedir dado mínimo.
3. Reposição por saúde: pode responder com cuidado se simples.
4. Cancelamento: deve criar nota interna, não enviar externo.
5. Procon/exposição: deve criar nota interna urgente.
6. Desconto/renegociação: deve criar nota interna.
7. Reclamação de professor: deve criar nota interna.

## Resumo executivo

O bridge foi ajustado para equilibrar qualidade e segurança:

- Sol volta a pensar o atendimento.
- Bridge mantém trava de status e humano/takeover.
- Casos simples podem ir para cliente.
- Casos sensíveis viram nota interna.
- Resposta inválida não vira fallback genérico.
- Logs agora mostram a decisão da Sol.

---

## Adendo — hard block para dado interno/KPI

Após teste real, a Sol respondeu externamente a pergunta:

> “Quantos alunos tem a unidade Barra?”

Resposta indevida enviada antes do adendo:

> “Alf, hoje a unidade Barra está com 253 alunos ativos. Pelo critério de matrículas pagantes, são 244.”

### Correção aplicada

Arquivo alterado novamente:

`/home/sol/.openclaw/workspace/scripts/chatwoot-sol-bridge.js`

Backup pré-correção:

`/home/sol/.openclaw/workspace/backups/chatwoot-sol-bridge.20260530-024506-pre-internal-data-guard.js`

Checksum após correção:

`8c3c621446db774919f09f83ab0ec22085539bc0128eace0d54b5d2b391a7e50`

### Nova trava

Foi adicionada função `requestsInternalBusinessData(text)` para detectar pedidos externos de:

- quantidade de alunos;
- matrículas;
- pagantes;
- alunos ativos;
- KPIs/indicadores;
- faturamento/receita;
- inadimplência;
- listas/rankings/scores;
- dados internos/agregados por unidade.

Quando detectado, o bridge força:

```json
{
  "risk": "high",
  "handoff_required": true,
  "allowed_to_send": false,
  "external_reply": "",
  "policy_block": "internal_business_data"
}
```

Ou seja: mesmo que a Sol classifique errado como low risk, o bridge bloqueia a resposta externa e cria nota interna.

### Política reforçada no prompt

O prompt da Sol agora deixa explícito:

- números internos/agregados/KPIs nunca devem ser enviados no WhatsApp externo sem `contact_context` autorizando;
- como ainda não há RBAC/ABAC implementado, esses pedidos devem ser tratados como `high risk` e handoff;
- exemplos bloqueados: “quantos alunos tem a unidade Barra?”, “quantas matrículas?”, “quantos pagantes?”, “faturamento?”, “inadimplência?”.

### Verificação

- `node --check scripts/chatwoot-sol-bridge.js` passou.
- Bridge reiniciado.
- Healthcheck OK em `auto_reply`.
- Processo Node ativo.

