# Auditoria — 5 alunos do print: zerado x início de pagamento

Data: 2026-05-31
Escopo: Campo Grande / Maio 2026
Status: READ-ONLY

## Pergunta do Alf

Alguns alunos do print podem ser alunos recém-entrados que só começam a pagar em junho. Identificar isso no banco e separar de erro de cadastro/sincronização.

## Estado atual no banco após correções manuais em andamento

| Aluno | ID | Data matrícula LR | Início contrato | Venc. | Valor passaporte | Valor parcela LR atual | Emusys | Leitura |
|---|---:|---|---|---:|---:|---:|---:|---|
| Ana Clara Lima Santos Pinto | 21 | 2025-05-28 | NULL | 5 | NULL | NULL | 447 | Aluna antiga. Não é caso de entrada recente/junho. Valor LR faltando é erro/sincronização. |
| Sofia Elaile da Silva Campos | 1643 | 2026-04-30 | 2026-04-30 | 5 | 325 | NULL | 447 | Recém-entrada fim de abril. Forte candidata a primeira mensalidade regular em junho, com passaporte/entrada em abril/maio. Precisa validar parcelas no Emusys. |
| Sofia Lauermann Silva | 1633 | 2026-04-27 | 2026-04-28 | 5 | 500 | NULL | 447 | Recém-entrada fim de abril. Forte candidata a primeira mensalidade regular em junho, com passaporte/entrada. Precisa validar parcelas no Emusys. |
| Sarah Christina Mendes Silva | 1600 | 2026-04-02 | 2026-04-04 | 5 | NULL | 456.16 | 447 | Não está mais zerada no LR. Foi corrigida ou sincronizada. Deve contar por valor positivo agora. |
| Valkiria Carvalho Baeta | 1624 | 2026-04-22 | 2026-04-29 | 5 | 400 | 387 | 447 | Não está mais zerada no LR. Foi corrigida ou sincronizada. Apesar de ser recente, agora conta por valor positivo. |

## Conclusão

Sim, dá para identificar indícios:

- **Ana Clara**: não é nova; é erro de valor/sincronização.
- **Sofia Elaile** e **Sofia Lauermann**: parecem ser exatamente o caso citado pelo Alf — entraram no fim de abril, têm `valor_passaporte`, vencimento dia 5 e podem começar mensalidade regular em junho. Ainda precisa confirmação das parcelas no Emusys.
- **Sarah** e **Valkiria**: já foram corrigidas no LR e têm `valor_parcela > 0` atualmente.

## Regra importante

No sistema atual, `valor_parcela` zerado/NULL **não impede necessariamente** o aluno de contar como pagante, porque a view/função atual contam pela flag `tipo_matricula.conta_como_pagante`.

Mas em uma regra financeira baseada em `valor_parcela > 0`, alunos zerados/NULL ficam fora. Por isso não dá para usar apenas `valor_parcela > 0` sem saber se o caso é:

1. erro de sincronização/cadastro;
2. aluno novo com cobrança futura;
3. bolsista/falso pagante.

## Decisão de regra pendente

Separar conceitualmente:

- **Aluno pagante contratual/ativo:** plano regular ativo, pode contar mesmo antes da primeira mensalidade recorrente.
- **Aluno pagante financeiro da competência:** só conta se há cobrança/mensalidade positiva naquela competência.

Sem essa separação, `alunos_pagantes` mistura stock operacional com competência financeira.

---

## Evidência visual Sarah Christina — fatura maio paga

Print enviado pelo Alf (`file_1162---9669fffc-bf58-45c3-9c3f-c4d9716e370d.jpg`) mostra **Sarah Christina Mendes Silva**, curso Canto — Módulo 1, Em Andamento.

Faturas visíveis:

- Parcela 06/2026 do curso de Canto — prevista 20/06/2026 — valor 377,00 — em aberto.
- **Parcela 05/2026 do curso de Canto — prevista 20/05/2026 — paga em 21/05/2026 via Pix — valor 456,16.**
- Parcela 04/2026 do curso de Canto — paga em 22/04/2026 — valor 377,00.
- Taxas de matrícula do curso de Canto — pagas.

Conclusão: Sarah é evidência explícita de que um aluno pode estar zerado no LA Report e ainda assim ter fatura paga na competência. Após ajuste feito pelo Alf, o banco já mostra Sarah com `valor_parcela=456.16`, então ela passou a contar também pela regra `valor_parcela > 0`.

## Recontagem após ajustes manuais em andamento

Consulta read-only atual após correções de Bruna/Sarah/Valkiria:

- pessoas ativas sem Plínio: 497
- matrículas ativas sem Plínio: 562
- pagantes por flag `conta_como_pagante=true`: 474
- pagantes por flag + `valor_parcela > 0`: 466

Ainda sem valor positivo no LA Report:

- Ana Clara Lima Santos Pinto — valor NULL
- Anna Clara de Souza Iorio Sales — valor 0
- Carlos Eduardo Garcia do Nascimento — valor 0/NULL, bolsista/falso
- Sofia Elaile da Silva Campos — valor NULL, passaporte 325
- Miguel Gomes Biancamano — valor 0/NULL, falso
- Sofia Lauermann Silva — valor NULL, passaporte 500
- Matheus Reis da Silva Gaspar — valor 0, falso
- Marcos da Silva Saturnino — valor 0, falso
