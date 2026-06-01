# Validação — falsos pagantes/bolsistas após ajuste

Data: 2026-06-01 UTC
Escopo: Campo Grande / Maio 2026
Status: READ-ONLY — nenhuma alteração executada pelo Alfredo.

## Contexto informado pelo Alf

Alf validou que os falsos pagantes abaixo são realmente bolsistas/não pagantes:

- Carlos Eduardo Garcia do Nascimento: já estava como bolsista na linha principal.
- Miguel Gomes Biancamano: bolsista/professor.
- Matheus Reis da Silva Gaspar: estagiário, bolsista integral.

Alf informou que ajustou/está ajustando no LA Report para não contarem como pagantes.

## Conferência atual no banco

### Carlos Eduardo Garcia do Nascimento

| ID | Curso | Tipo matrícula | Segundo curso | Valor | Conta como pagante | Tipo aluno | Status pagamento |
|---:|---|---|---|---:|---|---|---|
| 1066 | Contrabaixo | Bolsista Integral | false | NULL | false | bolsista_integral | sem_parcela |
| 1067 | Canto | Segundo Curso | true | 0 | true | pagante | inadimplente |

Leitura: a linha principal já está correta como bolsista integral. Mas a linha de segundo curso ainda está com `conta_como_pagante=true`, `tipo_aluno=pagante`, valor 0. Se a regra final for por pessoa usando `bool_or(conta_como_pagante=true)`, Carlos ainda contamina como pagante. Pela view atual row-by-row que exclui segundo curso, ele não entra.

### Miguel Gomes Biancamano

| ID | Curso | Tipo matrícula | Segundo curso | Valor | Conta como pagante | Tipo aluno |
|---:|---|---|---|---:|---|---|
| 1064 | Contrabaixo | Bolsista Integral | false | 0 | false | bolsista_integral |
| 320 | Harmonia | Bolsista Integral | true | NULL | false | bolsista_integral |

Leitura: corrigido como bolsista integral/não pagante.

### Matheus Reis da Silva Gaspar

| ID | Curso | Tipo matrícula | Segundo curso | Valor | Conta como pagante | Tipo aluno |
|---:|---|---|---|---:|---|---|
| 1599 | Bateria | Bolsista Integral | false | 0 | false | bolsista_integral |

Leitura: corrigido como bolsista integral/não pagante.

## Recontagem atual

- pessoas ativas sem Plínio: 497
- matrículas ativas sem Plínio: 562
- banda: 41
- pessoas pagantes por flag `conta_como_pagante=true`: 472
- pessoas pagantes por flag + `valor_parcela > 0`: 466
- linhas pagantes/sem segundo curso: 471

## Pendências atuais com flag pagante e sem valor positivo

Ainda aparecem como `conta_como_pagante=true` sem `valor_parcela > 0`:

1. Ana Clara Lima Santos Pinto — pendente Gabi/faturas removidas.
2. Anna Clara de Souza Iorio Sales — pendente auditoria.
3. Carlos Eduardo Garcia do Nascimento — segunda linha ainda como Segundo Curso/pagante; falso pagante por pessoa.
4. Sofia Elaile da Silva Campos — começo/pagamento em junho segundo Alf.
5. Sofia Lauermann Silva — começo/pagamento em junho segundo Alf.
6. Marcos da Silva Saturnino — pendente; provável falso/benefício se Emusys 0.

## Recomendação

- Confirmar se a linha 1067 do Carlos deve continuar como `Segundo Curso` ou também virar bolsista/não pagante.
- Na regra por pessoa, não usar `bool_or(conta_como_pagante=true)` cru; precisa ignorar flags de segundo curso zerado quando a pessoa é bolsista/não pagante, ou melhor, usar status financeiro/competência.
- Continuar sem migration até fechar os 6 pendentes.
