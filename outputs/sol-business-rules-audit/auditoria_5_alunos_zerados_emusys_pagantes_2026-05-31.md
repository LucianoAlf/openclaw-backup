# Auditoria — 5 alunos reais com mensalidade Emusys 447 e valor NULL/0 no LA Report

Data: 2026-05-31
Escopo: Campo Grande / Maio 2026
Status: READ-ONLY — nenhuma alteração executada.

## Alunos auditados

Lista enviada pelo Alf no print:

- Ana Clara Lima Santos Pinto
- Sofia Elaile da Silva Campos
- Sofia Lauermann Silva
- Sarah Christina Mendes Silva
- Valkiria Carvalho Baeta

## Resultado no banco LA Report/Supabase

| Aluno | ID LR | Status | Matrícula | Saída | Curso LR | Tipo | 2º curso | Valor LR | conta_como_pagante | Emusys mensalidade | Curso Emusys | Conta ativo? | Pagante por flag? | Pagante por valor > 0? |
|---|---:|---|---|---|---|---|---|---:|---|---:|---|---|---|---|
| Ana Clara Lima Santos Pinto | 21 | ativo | 2025-05-28 | NULL | Canto | Regular | false | NULL | true | 447 | Canto | sim | sim | não |
| Sofia Elaile da Silva Campos | 1643 | ativo | 2026-04-30 | NULL | Violino | Regular | false | NULL | true | 447 | Violino | sim | sim | não |
| Sofia Lauermann Silva | 1633 | ativo | 2026-04-27 | NULL | Bateria | Regular | false | NULL | true | 447 | Canto | sim | sim | não |
| Sarah Christina Mendes Silva | 1600 | ativo | 2026-04-02 | NULL | Canto | Regular | false | 0 | true | 447 | Canto | sim | sim | não |
| Valkiria Carvalho Baeta | 1624 | ativo | 2026-04-22 | NULL | Bateria | Regular | false | NULL | true | 447 | Canto | sim | sim | não |

## Leitura

Todos os 5 são alunos reais e ativos no LA Report:

- `status='ativo'`
- `data_saida=NULL`
- `tipo_matricula=Regular`
- `conta_como_pagante=true`
- `is_segundo_curso=false`

Mas todos estão sem valor financeiro válido no LA Report:

- Ana Clara: `valor_parcela=NULL`
- Sofia Elaile: `valor_parcela=NULL`
- Sofia Lauermann: `valor_parcela=NULL`
- Sarah: `valor_parcela=0`
- Valkiria: `valor_parcela=NULL`

No Emusys, todos aparecem com mensalidade **R$447,00**.

## Resposta à pergunta operacional

- Como **aluno ativo**: sim, todos contam.
- Como **pagante por flag cadastral** (`conta_como_pagante=true`): sim, todos contam.
- Como **pagante financeiro real usando `valor_parcela > 0` no LA Report**: não, nenhum conta.

Portanto, o problema não é existência do aluno. O problema é que o LA Report está com valor financeiro NULL/0 apesar de o Emusys mostrar mensalidade positiva.

## Inconsistência extra

Além do valor, há divergência de curso em pelo menos dois casos:

- Sofia Lauermann Silva: LA Report = Bateria; Emusys = Canto.
- Valkiria Carvalho Baeta: LA Report = Bateria; Emusys = Canto.

Isso precisa ser validado no Emusys/rotina de sincronização.

## Ação recomendada

Cobrar equipe/saneamento para cada aluno:

1. confirmar contrato ativo no Emusys;
2. confirmar curso correto;
3. confirmar mensalidade correta;
4. atualizar/corrigir `valor_parcela` no LA Report ou corrigir sincronização;
5. reprocessar cálculo somente depois da validação nominal.

## Status

Não executar migration/RPC/backfill ainda.
