# Auditoria — Renovação antecipada Emusys ↔ LA Report

Data: 2026-06-09
Escopo: caso Maria Flor / Campo Grande e regra operacional para renovações antecipadas.
Modo: leitura Emusys/logs + SELECT-only Supabase. Nenhum dado alterado.

---

## Pergunta do Alf

O Emusys dispara renovação assim que a equipe lança uma renovação antecipada. Hoje o LA Report trata como renovação do mês do webhook, sujando o fluxo do mês atual. Exemplo: renovação feita em junho, mas ciclo novo só começa em julho.

Objetivo:

- saber se dá para identificar renovação antecipada;
- cruzar Emusys ↔ LA Report;
- propor como ela deve cair no Report sem sujar o mês atual;
- criar base para um ambiente/lista de “Renovações Antecipadas”.

---

## Caso confirmado — Maria Flor de Carvalho Fernandes

### Log LA Report

`automacao_log.id = 3756`

- Aluna: Maria Flor de Carvalho Fernandes
- Unidade: Campo Grande
- Evento: `matricula_renovacao`
- Ação: `renovado`
- Workflow: `processar-matricula-emusys`
- Criado em: `2026-06-08T19:24:45.477088+00:00`
- Execução: `2026-06-08T19:24:45.457Z`
- Emusys matrícula: `1482`
- Curso: Bateria
- Professor: Gabriel Barbosa Rufino Otávio
- Match: `nome_curso`
- `renovacao_inserida = true`
- `movimentacao_registrada = true`

### Payload Emusys no log

Campos relevantes no `payload_bruto`:

- `payload_bruto.id = 46793`
- `evento = matricula_renovacao`
- `escola_id = 39` → Campo Grande
- `matricula.matricula_id = 1482`
- `matricula.nome_aluno = Maria Flor de Carvalho Fernandes`
- `matricula.valor = 447`
- `matricula.tipo_pagamento = Boleto`
- `matricula.data_matricula = 2023-06-28`
- `matricula.data_primeira_aula = 2026-07-16`
- `matricula.data_ultima_aula = 2027-05-06`
- `payload_bruto.data_hora_criacao = 2026-06-08 16:24:43`

### Interpretação

A renovação foi **lançada em 08/06/2026**, mas o novo ciclo/aula efetiva começa em **16/07/2026**.

Logo, para KPI/fluxo mensal, isso é:

```text
renovação antecipada lançada em junho
competência efetiva da renovação: julho/2026
```

---

## O que o Report gravou hoje

### Tabela `renovacoes`

Registro encontrado:

- `renovacoes.id = 460`
- `aluno_id = 290`
- `data_renovacao = 2026-06-08`
- `status = renovado`
- `observacoes = Automático via Emusys — Bateria`
- `valor_parcela_anterior = 357`
- `valor_parcela_novo = null`
- `data_inicio_novo_contrato = null`
- `data_fim_novo_contrato = null`
- `created_at = 2026-06-08T19:24:45.274137+00:00`

Problema: o Report não salvou a competência efetiva `2026-07-16` nesse registro.

### Tabela `movimentacoes_admin`

O log dizia que a movimentação foi registrada, mas a tabela atual não tem mais a movimentação da Maria Flor.

Audit log confirmou:

- `movimentacoes_admin.id = 3126`
- inserida pelo sistema em `2026-06-08T19:24:45.411705+00:00`
- `data = 2026-06-08`
- `tipo = renovacao`
- `motivo = Renovação automática via Emusys — Bateria`
- deletada manualmente por `gabi@lamusic.com.br`
- deleção em `2026-06-09T00:03:31.183785+00:00`
- `origem = manual`

Isso confirma a fala do Alf: a Gabi apagou porque estava sujando o fluxo.

---

## Bug raiz encontrado no código

Arquivo:

```text
supabase/functions/processar-matricula-emusys/index.ts
```

### 1. Handler de renovação usa “hoje” para a renovação

No `handleRenovacao`:

```ts
const hoje = new Date().toISOString().split('T')[0];
...
await supabase.from('renovacoes').insert({
  aluno_id: aluno.id,
  unidade_id: p.unidadeId,
  data_renovacao: hoje,
  ...
});
```

Ou seja: `data_renovacao` = data do processamento/webhook, não data efetiva do novo ciclo.

### 2. Movimentação também usa “hoje”

No `registrarMovimentacao`:

```ts
await supabase.from('movimentacoes_admin').insert({
  unidade_id: p.unidadeId,
  data: new Date().toISOString().split('T')[0],
  tipo,
  ...
});
```

Logo, `movimentacoes_admin.data` também cai no mês do webhook.

### 3. Parser pega a primeira disciplina, não necessariamente o novo ciclo

No `parsePayload`:

```ts
const disc = m.disciplinas?.[0];
...
dataInicioContrato: disc?.data_hora_primeira_aula || null,
dataFimContrato: disc?.data_hora_ultima_aula || null,
```

No payload da Maria Flor existem múltiplas disciplinas históricas/ciclos:

- 2023-07-03 → 2024-06-20
- 2024-06-27 → 2025-06-19
- 2025-06-26 → 2026-07-09
- 2026-07-16 → 2027-05-06

O código usa a primeira, mas a renovação nova é a última / `matricula.data_primeira_aula`.

Por isso, além de sujar o mês, pode preservar contrato antigo no `alunos.data_inicio_contrato` / `data_fim_contrato`.

---

## Como saber que é renovação antecipada

Sim, dá para saber com segurança pelo payload Emusys.

Regra prática:

```text
se evento = matricula_renovacao
E data_primeira_aula do novo ciclo > mês/data do webhook
ENTÃO renovação antecipada
```

Campos recomendados, em ordem de confiança:

1. `payload_bruto.matricula.data_primeira_aula`
2. maior `disciplinas[].data_hora_primeira_aula`
3. `payload_bruto.renovacao.data_ultima_aula` / `matricula.data_ultima_aula` para fim do novo ciclo

Para Maria Flor:

```text
data_hora_criacao: 2026-06-08
matricula.data_primeira_aula: 2026-07-16
competência correta: 2026-07
```

---

## Varredura de junho

Consulta em `automacao_log` para `evento = matricula_renovacao` desde 2026-06-01:

- total de renovações Emusys encontradas: `17`
- renovações antecipadas detectadas por payload: `1`
- caso detectado: Maria Flor de Carvalho Fernandes

Observação: se a Gabi apagou outros registros antes/fora do intervalo ou se houve webhook antigo sem `payload_bruto`, precisa ampliar a janela ou cruzar n8n/Emusys. Nesta varredura atual, o caso confirmado é Maria Flor.

---

## Onde isso suja o Report hoje

### 1. Administrativo / Retenção por `movimentacoes_admin`

A página administrativa conta movimentações por `movimentacoes_admin.data`.

Como o sistema gravou `data=2026-06-08`, ela entraria em junho. A Gabi apagou esse registro, então parou de sujar essa parte.

### 2. Snapshot / relatórios / histórico de ficha por `renovacoes`

`renovacoes.data_renovacao` ainda está como `2026-06-08`.

Então ainda pode sujar lugares que leem `renovacoes`, por exemplo:

- Snapshot diário/mensal;
- Planilha de Retenção;
- ficha do aluno;
- relatórios que contam `renovacoes.data_renovacao` no mês.

---

## Recomendação de regra de negócio

### Definição

Renovação antecipada é uma renovação lançada antes da competência efetiva do novo ciclo.

```text
competência_lançamento = mês(data_hora_criacao/webhook)
competência_efetiva = mês(data_primeira_aula_novo_ciclo)

se competência_efetiva > competência_lançamento:
  status operacional = renovação antecipada
  não contar em renovações realizadas do mês de lançamento
  contar em renovações efetivas da competência futura
```

### Para KPI executivo

- Junho deve enxergar Maria Flor como **renovação antecipada agendada**, não renovação realizada de junho.
- Julho deve contar a renovação como realizada/efetivada, se ainda estiver válida.

### Para operação

Criar aba/card/lista:

```text
Renovações Antecipadas
```

Campos úteis:

- aluno
- unidade
- curso
- professor
- data de lançamento
- data efetiva / primeira aula do novo ciclo
- competência efetiva
- valor novo
- usuário Emusys que lançou
- status: antecipada / efetivada / cancelada / apagada manualmente
- origem: Emusys
- emusys_matricula_id
- payload id

Isso vira ferramenta de gestão: Campo Grande consegue jogar o jogo de antecipação sem sujar relatório mensal.

---

## Modelo técnico sugerido — sem aplicar ainda

### Opção mínima

Adicionar à tabela `renovacoes`:

```text
is_antecipada boolean
competencia_efetiva date ou text YYYY-MM
data_lancamento date
data_efetiva_renovacao date
payload_emusys_id text/int
emusys_matricula_id text
usuario_emusys_nome text
```

E mudar a regra:

- `data_lancamento` = hoje/webhook/data_hora_criacao;
- `data_efetiva_renovacao` = `matricula.data_primeira_aula` ou maior data de início das disciplinas;
- `data_renovacao` pode ser repensada para virar data efetiva, ou mantida por compatibilidade e criar campo separado.

### Opção mais limpa

Criar uma tabela própria:

```text
renovacoes_antecipadas
```

Com relação futura com `renovacoes`, permitindo:

- não poluir a tabela de renovações efetivas;
- ter ambiente operacional próprio;
- efetivar automaticamente quando chegar a competência.

### Opção recomendada

Não criar tabela separada de cara. Primeiro enriquecer `renovacoes` com campos de lançamento vs efetivação e criar UI filtrada.

Motivo: o evento continua sendo renovação; o que muda é a competência e status operacional.

---

## Regra de segurança

Não apagar renovação antecipada para limpar relatório.

O sistema deve guardar o evento e classificá-lo corretamente.

Apagar manualmente resolve o relatório no curto prazo, mas perde inteligência operacional: justamente o indicador que mostra que Campo Grande está antecipando renovação.

---

## Próximo passo recomendado

1. Validar com Alf a regra:
   - renovação antecipada conta na competência da `data_primeira_aula` do novo ciclo.
2. Atualizar skill/regras canônicas.
3. Criar prompt para Codex implementar sem backfill inicial:
   - corrigir parse do novo ciclo;
   - classificar antecipada;
   - não jogar em `movimentacoes_admin` do mês atual;
   - exibir em aba/lista “Renovações Antecipadas”.
4. Depois fazer SELECT-only/backfill pro histórico recente, se aprovado.
