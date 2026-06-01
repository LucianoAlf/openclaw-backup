Cascade, precisamos transformar a auditoria de CG/Maio em uma especificação prática para a Sol fiscalizar inconsistências automaticamente.

Status:
- READ-ONLY.
- Não gerar migration.
- Não executar RPC.
- Não executar UPDATE.
- Não fazer backfill.
- Não rodar Barra/Recreio.

Contexto:
O número informado pela equipe Campo Grande era 475 pagantes. Após validação nominal e ajustes manuais do Alf, a view atual mostra:

- 497 alunos ativos
- 470 alunos pagantes
- 562 matrículas ativas
- 41 matrículas banda/projeto
- 27 segundos cursos
- 23 novas matrículas
- 13 evasões
- churn 2,77%

A queda 475 → 470 foi explicada por 5 inconsistências:

1. Bruna Damasceno
- Duplicidade por nome/linha.
- Havia Bruna Damasceno Castro e Bruna Damasceno de Castro.
- Linha zerada removida/corrigida.
- Restou uma Bruna ativa pagante: Guitarra, R$367.

2. Miguel Gomes Biancamano
- Professor/bolsista.
- Corrigido para Bolsista Integral / não pagante.

3. Matheus Reis da Silva Gaspar
- Estagiário/bolsista integral.
- Corrigido para Bolsista Integral / não pagante.

4. Carlos Eduardo Garcia do Nascimento
- Permuta/parceria com empresa do pai.
- Bolsista integral nos dois cursos.
- Corrigido para Bolsista Integral nas duas linhas / não pagante.

5. Marcos da Silva Saturnino
- Professor da escola.
- Não está mais fazendo/frequentando aula.
- Constava ativo no Emusys, mas não paga.
- Corrigido para Bolsista Integral / não pagante.

Pendências restantes com flag pagante e sem valor positivo:

1. Ana Clara Lima Santos Pinto
- Faz aula.
- LA Report está zerado.
- Gabi removeu 7 faturas.
- Alf vai cobrar explicação da Gabi.

2. Anna Clara de Souza Iorio Sales
- Mesma natureza da Ana Clara.
- Faturas movidas/removidas pela Gabi.
- Zerada no LA Report e sem fatura/pagamento visível no Emusys.

3. Sofia Elaile da Silva Campos
- Aluna nova de Violino.
- Matriculada em abril.
- Não começou em maio.
- Começa/paga primeira parcela em junho.
- Pagou passaporte.

4. Sofia Lauermann Silva
- Aluna nova de Canto.
- Pagou passaporte.
- Começa/paga primeira parcela em junho.

Tarefa:

1. Produzir relatório READ-ONLY consolidando o estado atual CG/Maio.
2. Confirmar com SELECTs os números atuais da view e das contagens auxiliares.
3. Montar ledger nominal das categorias:
   - ativo operacional;
   - pagante contratual;
   - pagante financeiro da competência;
   - bolsista/permutado/professor/estagiário;
   - sujeira operacional.
4. Explicar por que a Sol precisa fiscalizar isso automaticamente.
5. Propor regras de alerta para a Sol:
   - aluno ativo e pagante flag, mas valor_parcela NULL/0;
   - aluno ativo sem fatura prevista/paga na competência;
   - aluno com faturas removidas/movidas;
   - aluno novo com passaporte e primeira mensalidade no mês seguinte;
   - professor/estagiário/permuta marcado como pagante;
   - duplicidade por nome similar/telefone/Emusys ID;
   - aluno ativo com ausência alta/frequência baixa e sem pagamento;
   - divergência de curso entre Emusys e LA Report;
   - segundo curso zerado contaminando pessoa.
6. Propor estrutura de dados necessária para parar de remendar:
   - tabela/integração de faturas por competência;
   - identificador Emusys obrigatório;
   - normalização de pessoa/aluno para evitar nome exato como chave;
   - status financeiro por competência separado de status operacional;
   - trilha de auditoria/quem alterou faturas e valores.

Não propor SQL de alteração ainda.
Não mexer em `recalcular_dados_mensais` ainda.
A saída deve ser relatório + SQL SELECT de auditoria.
