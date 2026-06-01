# Validação Alf — 9 alunos que apareciam ativos no Emusys

Data: 2026-05-31
Contexto: saneamento de ciclo de vida Campo Grande / Maio 2026, após cruzar CSV de ativos e ex-alunos do Emusys.

## Validação recebida do Alf

| ID LA Report | Nome | Validação Alf | Implicação preliminar |
|---:|---|---|---|
| 1450 | Maria Eduarda de Lima Bomfim Pedro | Não está mais matriculada; saiu da escola; estava só em banda | Não tratar como aluna ativa de curso. Manter/inativar no LA Report; precisa definir `data_saida` efetiva/corte técnico. Não usar presença em banda para contar como aluno ativo de curso. |
| 1375 | Alan Samico do Nascimento | Não está mais matriculado em curso; só participa de banda | Não contar como aluno ativo de curso/pagante. Manter participação de banda separada. Precisa modelar regra: banda ≠ curso ativo. |
| 1378 | Ana Julia de Oliveira Gomes | Não está mais matriculada | Não contar como aluna ativa. Precisa definir `data_saida` efetiva/corte técnico. |
| 1393 | Leamsi Guedes de Sant'anna | Não está mais matriculado em curso; só participa de banda | Não contar como aluno ativo de curso/pagante. Manter participação de banda separada. Precisa modelar regra: banda ≠ curso ativo. |
| 31 | Anne Krissya Cordeiro da Silva Noé | Aluna bolsista de Piano e Banda; matriculada | Contar como aluna ativa. Como bolsista, não contar como pagante. Limpar `data_saida` antiga se status atual ativo estiver correto. |
| 263 | Luiza Mazeliah do Nascimento | Aluna de guitarra; matriculada | Contar como aluna ativa/pagante conforme cadastro. Limpar `data_saida` antiga. |
| 405 | Vicente Dias Botelho | Aluno de piano e participa de duas bandas; matriculado | Contar como aluno ativo; curso piano + bandas. Limpar `data_saida` antiga. |
| 323 | Miguel Santos Borges | Aluno de piano/teclado; matriculado | Contar como aluno ativo/pagante conforme cadastro. Limpar `data_saida` antiga. |
| 949 | Cassyo Lucas Prado Silva | Aluno de piano/teclado; matriculado | Contar como aluno ativo/pagante conforme cadastro. Limpar `data_saida` antiga. |

## Regra de negócio emergente

Participar de **banda** não é suficiente para contar como aluno ativo de curso.  
Para `Total Alunos Ativos`, separar:

- aluno matriculado em curso/aula regular;
- aluno apenas participante de banda/projeto;
- aluno bolsista ativo;
- matrícula de banda como matrícula/projeto, quando o KPI pedir `matriculas_banda`.

Essa regra precisa entrar na base canônica após confirmação final, porque explica por que o CSV do Emusys marca alguns nomes como `Em Andamento`, mas o Alf não considera esses nomes como alunos matriculados em curso.

## Impacto imediato no saneamento

A lista dos 9 não deve ser tratada como um bloco único de “ativos”. Ela se divide em:

### Confirmados matriculados/ativos
- 31 Anne Krissya Cordeiro da Silva Noé
- 263 Luiza Mazeliah do Nascimento
- 405 Vicente Dias Botelho
- 323 Miguel Santos Borges
- 949 Cassyo Lucas Prado Silva

### Não matriculados em curso / não contar como aluno ativo de curso
- 1450 Maria Eduarda de Lima Bomfim Pedro
- 1375 Alan Samico do Nascimento
- 1378 Ana Julia de Oliveira Gomes
- 1393 Leamsi Guedes de Sant'anna

## Próxima ação recomendada

Antes de gerar SQL final:
1. Definir se Maria, Alan, Ana Júlia e Leamsi devem receber `data_saida` e qual data usar.
2. Para Alan e Leamsi, preservar/representar participação em banda sem contar como curso ativo.
3. Limpar `data_saida` apenas dos cinco confirmados matriculados: 31, 263, 405, 323, 949.
4. Recalcular a projeção de snapshot CG/Maio depois dessa classificação.
