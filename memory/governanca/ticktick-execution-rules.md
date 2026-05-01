# TickTick — Regras de Execução Confiável

> Complemento operacional às documentações já existentes:
> - `ticktick-skill.md`
> - `memory/governanca/ticktick-capacidades.md`
> - `memory/governanca/ticktick-payload-patterns.md`
>
> Este arquivo NÃO repete capacidades gerais da API.
> Ele existe para registrar as regras práticas de execução que evitam retrabalho, sobrescrita e perda de contexto.

---

## 1. Objetivo deste documento

Registrar como executar operações no TickTick **sem destruir cards bons, sem perder contexto e sem repetir erros de modelagem**.

Este documento é a camada de:
- disciplina operacional
- migração segura
- padrão visual aprovado pelo Alf
- regra de create vs update

---

## 2. Regra-mãe

# Quando um padrão já estiver aprovado visualmente, não reinterpretar — replicar.

Se o Alf aprovou um card como referência visual:
- usar esse card como molde
- copiar a estrutura
- preservar o conteúdo
- evitar simplificações “inteligentes”

**Erro proibido:** resumir, reorganizar ou “melhorar” um padrão já aprovado sem pedido explícito.

---

## 3. Padrão visual aprovado para card com checklist

## Estrutura canônica

### `title`
Título do card.

### `desc`
Campo visual principal do card.

Formato aprovado:

```text
Responsável: <nome>

Objetivo: <descrição curta e clara>
```

### Linha adicional opcional em `desc`
Usar somente quando necessário:
- `Apoio: ...`
- `Acompanhamento: ...`
- `Execução: ...`
- `Direção: ...`

Exemplo:

```text
Responsável: Bianca

Objetivo: definir o escopo clínico mínimo necessário para o MVP.

Acompanhamento: Alf + Anne
```

### `items[]`
Checklist nativo do card.

### `content`
Usar apenas se houver necessidade real de complemento.

**Regra prática:** se `desc + items[]` já resolvem, não inventar `content` extra.

---

## 4. Create vs Update

## Regra operacional

### Preferir `create` quando:
- o card tem checklist (`items[]`)
- o card é sensível
- a estrutura visual precisa ficar correta no app
- há risco de sobrescrever ou perder contexto
- o card está errado de origem

### Preferir `update` apenas quando:
- o card já está correto estruturalmente
- a mudança é pequena e segura
- não há necessidade de reestruturar `items[]`
- não há risco de quebrar renderização visual

---

## 5. Regra crítica de segurança

# Se o card nasceu errado e a estrutura importa, não remendar. Apagar e recriar.

Isso vale especialmente para cards com:
- `desc`
- `items[]`
- checklist visual importante
- padrão aprovado pelo Alf

**Erro comum a evitar:** tentar “consertar por cima” um card já inconsistente.

---

## 6. Protocolo de migração segura

Antes de converter um card antigo para checklist nativo:

### Passo 1 — Preservar o conteúdo original
Capturar antes:
- título
- descrição antiga
- bullets/checklist antigo
- tags
- responsável
- contexto semântico do card

### Passo 2 — Validar o molde
Criar **um card piloto** e validar no app.

### Passo 3 — Só depois replicar
Se o piloto estiver aprovado visualmente, replicar para os demais.

### Passo 4 — Não simplificar o conteúdo sem autorização
Se o card antigo tinha contexto relevante, preservar esse contexto no novo `desc`.

---

## 7. Regra de preservação de contexto

Quando recriar card:
- preservar a intenção do original
- preservar quem é o responsável
- preservar a definição do que deve acontecer
- preservar a ordem do checklist quando ela carregar lógica de execução

**Não fazer:**
- cortar contexto por conveniência
- trocar palavras importantes sem necessidade
- resumir agressivamente o objetivo
- reescrever em linguagem mais pobre se o original estava melhor

---

## 8. Espaçamento visual

O espaçamento entre linhas faz parte do padrão aprovado.

## Formato mínimo

```text
Responsável: <nome>

Objetivo: <texto>
```

## Formato com linha extra opcional

```text
Responsável: <nome>

Objetivo: <texto>

Apoio: <nome(s)>
```

**Não colar tudo numa linha só.**

---

## 9. Casos de uso prioritários para seguir estas regras

Estas regras valem principalmente para:

### 9.1 Card de projeto com checklist
Ex.: SonoraMente — Plano Mestre do MVP

### 9.2 Card de roadmap / marco
Ex.: etapa com data, dono e checklist

### 9.3 Card de atribuição
Ex.: responsável + execução + itens

### 9.4 Boss Battle / Campanha
Ex.: várias fases visíveis em checklist

### 9.5 Card operacional sensível
Ex.: jurídico, comercial, obra, sistema

---

## 10. Casos de uso que não precisam desta rigidez toda

### Pode ser mais simples:
- nota solta
- ação CEO simples
- lembrete curto sem checklist
- ritual em texto longo
- hábito

Nesses casos, não precisa forçar o padrão de card complexo.

---

## 11. Regra de validação antes de replicar em lote

Se houver mudança estrutural de modelagem:
- validar 1 card
- esperar aprovação visual do Alf
- só então replicar

**Nunca replicar em lote um padrão não validado.**

---

## 12. Anti-patterns proibidos

### Proibido 1 — Simplificar porque “parece melhor”
Se o padrão já foi aprovado, não otimizar por conta própria.

### Proibido 2 — Atualizar card ruim por insistência
Se já deu sinal de inconsistência, apagar e recriar.

### Proibido 3 — Perder o conteúdo original do card
Estrutura técnica correta sem semântica preservada = erro.

### Proibido 4 — Pular leitura da documentação existente
Antes de agir, revisar:
- skill de classificação
- capacidades da API
- payload patterns
- este documento de execução

---

## 13. Fluxo recomendado antes de qualquer operação importante no TickTick

1. Identificar o caso de uso
2. Ver se já existe padrão documentado
3. Escolher lista/projeto correto
4. Escolher `create` ou `update`
5. Se checklist sensível: preferir recriação limpa
6. Validar card piloto
7. Replicar somente após aprovação

---

## 14. Conclusão operacional

A documentação técnica existente já cobre muito bem:
- o que a API faz
- quais campos existem
- quais payloads são válidos

O que este documento adiciona é a camada que faltava:

> **como executar direito sem estragar o que já estava certo**

Essa é a diferença entre saber a API e operar com confiabilidade.
