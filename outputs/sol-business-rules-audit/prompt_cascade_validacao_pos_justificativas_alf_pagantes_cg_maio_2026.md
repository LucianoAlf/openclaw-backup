Cascade, vamos fazer uma nova auditoria READ-ONLY depois das justificativas e correções manuais do Alf.

Contexto obrigatório:
- Campo Grande / Maio 2026.
- Nenhuma migration.
- Nenhum RPC.
- Nenhum UPDATE.
- Nenhum backfill.
- Não rodar Barra/Recreio.
- O objetivo é validar a regra e as inconsistências; não corrigir ainda.

O Alf validou nominalmente 5 casos que estavam com `valor_parcela NULL/0` no LA Report e mensalidade positiva no Emusys:

1. Ana Clara Lima Santos Pinto
- Está fazendo aula.
- LA Report ainda está com `valor_parcela=NULL`.
- Gabriela removeu 7 faturas dela; Alf vai perguntar o que houve.
- Classificação: ativa; pagante real pendente de validação das faturas removidas.

2. Sofia Elaile da Silva Campos
- Matriculada em abril.
- Não começou em maio.
- Vai começar em junho.
- Provável problema/adiamento financeiro; por isso está zerada no LA Report.
- Classificação: matriculada/ativa cadastral, mas não pagante financeiro de maio.

3. Sofia Lauermann Silva
- Matriculada no fim de abril/maio.
- Pagou passaporte.
- Começa em junho e primeira parcela será em junho.
- Classificação: matriculada/ativa cadastral, mas não pagante financeiro de maio.

4. Sarah Christina Mendes Silva
- Fazia aula normalmente.
- Tinha fatura de maio paga no Emusys.
- Alf ajustou no LA Report.
- Banco atual mostra `valor_parcela=456.16`.
- Classificação: ativa e pagante de maio.

5. Valkiria Carvalho Baeta
- Alf corrigiu curso de Bateria para Canto.
- Faz Canto com Matheus.
- Paga R$387.
- Matriculou em abril e começou em maio.
- Banco atual mostra curso Canto e `valor_parcela=387`.
- Classificação: ativa e pagante de maio.

Estado read-only atual observado no banco após ajustes manuais:
- pessoas ativas sem Plínio: 497
- matrículas ativas sem Plínio: 562
- linhas banda: 41
- pessoas pagantes por flag `conta_como_pagante=true`: 472
- pessoas pagantes por `conta_como_pagante=true AND valor_parcela > 0`: 466
- `vw_kpis_gestao_mensal`: 497 ativos / 471 pagantes / 41 banda / 65 segundo curso

Tarefa READ-ONLY:

1. Recalcular os números acima diretamente no banco e confirmar ou corrigir.
2. Listar nominalmente as pessoas que ainda têm `conta_como_pagante=true` mas nenhuma linha com `valor_parcela > 0`.
3. Classificar cada uma em uma das categorias:
   - erro/sincronização/fatura removida;
   - matriculada mas cobrança começa em junho;
   - falso pagante/bolsista/zero real;
   - duplicidade/nome;
   - precisa validação manual.
4. Não usar `valor_parcela > 0` como regra final global.
5. Separar conceitualmente:
   - aluno ativo contratual/operacional;
   - aluno pagante contratual;
   - aluno pagante financeiro da competência;
   - falso pagante cadastral.
6. Apontar quais alunos devem contar em maio em cada visão:
   - ativo operacional;
   - pagante contratual;
   - pagante financeiro de maio.
7. Explicar por que a view atual dá 471 pagantes, enquanto a contagem por pessoa/flag dá 472.
8. Explicar o impacto das correções Bruna/Sarah/Valkiria nos números.
9. Entregar uma proposta de regra estrutural para parar de remendar:
   - preferencialmente usar faturas/competência do Emusys ou tabela equivalente;
   - não depender só de `valor_parcela` da tabela `alunos`;
   - não depender só de `conta_como_pagante`;
   - usar identificador Emusys/pessoa para evitar duplicidade por nome.

Saída esperada:
- relatório com tabelas nominais;
- SQL somente SELECT;
- sem DDL/DML;
- sem migration;
- sem RPC;
- sem UPDATE.
