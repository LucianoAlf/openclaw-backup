# Fechamento provisório — CG/Maio 2026: 475 → 470 e papel da Sol

Data: 2026-06-01 UTC
Status: READ-ONLY no Alfredo. Ajustes manuais foram feitos pelo Alf no LA Report/Emusys/Windsurf.

## Veredito atual

O número **475 pagantes** informado pela equipe Campo Grande estava contaminado por inconsistências cadastrais/operacionais.

Após validações e ajustes manuais do Alf, o banco atual mostra:

- **497 alunos ativos**
- **470 alunos pagantes** na `vw_kpis_gestao_mensal`
- **562 matrículas ativas**
- **41 matrículas de banda/projeto**
- **27 segundos cursos**
- **23 novas matrículas**
- **13 evasões**
- **churn 2,77%**


> Correção: a view bruta expõe 65 linhas com `is_segundo_curso=true`, mas esse total inclui 38 matrículas de banda/projeto que já entram no KPI de banda. O card de Gestão de Alunos usa a regra operacional correta: **27 segundos cursos não-banda + 41 banda**.

## Reconciliação da queda 475 → 470

A queda de 5 pagantes é explicada por:

1. **Bruna Damasceno**
   - Havia duplicidade por nome/linha.
   - Linha zerada removida/corrigida.
   - Restou uma Bruna ativa pagante: `Bruna Damasceno Castro`, Guitarra, R$367.

2. **Miguel Gomes Biancamano**
   - Professor/bolsista.
   - Corrigido para Bolsista Integral / `conta_como_pagante=false`.

3. **Matheus Reis da Silva Gaspar**
   - Estagiário/bolsista integral.
   - Corrigido para Bolsista Integral / `conta_como_pagante=false`.

4. **Carlos Eduardo Garcia do Nascimento**
   - Parceria/permuta com empresa do pai.
   - Bolsista integral nos dois cursos.
   - Corrigido para Bolsista Integral nas duas linhas / `conta_como_pagante=false`.

5. **Marcos da Silva Saturnino**
   - Professor da escola.
   - Não está mais frequentando aulas.
   - Consta ativo no Emusys, mas não paga; bolsista integral.
   - Corrigido para Bolsista Integral / `conta_como_pagante=false`.

## Pendências que ainda aparecem com flag pagante sem valor positivo

Após os ajustes, restam quatro casos com `conta_como_pagante=true`, mas sem `valor_parcela > 0`:

1. **Ana Clara Lima Santos Pinto**
   - Faz aula.
   - LA Report está zerado.
   - Gabi removeu 7 faturas; Alf vai perguntar o que houve.
   - Pendente de auditoria com Gabriela.

2. **Anna Clara de Souza Iorio Sales**
   - Mesma natureza da Ana Clara: faturas movidas/removidas pela Gabi.
   - Está zerada no LA Report e sem fatura/pagamento visível no Emusys.
   - Pendente de auditoria com Gabriela.

3. **Sofia Elaile da Silva Campos**
   - Aluna nova de Violino.
   - Matriculada em abril.
   - Não começou em maio; vai começar em junho.
   - Pagou passaporte; primeira parcela em junho.
   - Não deve contar como pagante financeiro de maio, mas pode constar como ativa/contratual conforme regra.

4. **Sofia Lauermann Silva**
   - Aluna nova de Canto.
   - Pagou passaporte.
   - Começa e paga primeira parcela em junho.
   - Não deve contar como pagante financeiro de maio, mas pode constar como ativa/contratual conforme regra.

## O que esta auditoria provou

Não é apenas uma correção de número. O processo revelou cinco classes de inconsistência que a Sol precisa fiscalizar automaticamente:

1. **Duplicidade de pessoa por variação de nome**
   - Ex.: Bruna Damasceno Castro / Bruna Damasceno de Castro.

2. **Bolsista/professor/estagiário marcado como pagante**
   - Ex.: Miguel, Matheus, Marcos, Carlos.

3. **Aluno ativo com faturas removidas/movidas**
   - Ex.: Ana Clara e Anna Clara.

4. **Aluno novo com matrícula/passaporte em um mês e primeira mensalidade no mês seguinte**
   - Ex.: Sofia Elaile, Sofia Lauermann.

5. **Aluno ativo no Emusys sem frequência/pagamento real**
   - Ex.: Marcos faltando muito e ainda constando ativo.

## Regra estrutural necessária

A Sol não pode depender de uma única coluna (`valor_parcela`) nem de uma única flag (`conta_como_pagante`).

Ela precisa cruzar:

- cadastro do aluno;
- tipo de matrícula;
- status/atividade;
- faturas previstas/pagas por competência;
- presença/frequência;
- passaporte/taxa de matrícula;
- data real de início das aulas;
- curso/professor atual;
- duplicidade por nome/telefone/Emusys ID.

## Categorias que a Sol deve separar

- **Ativo operacional:** aluno/matrícula ainda ativo no sistema.
- **Pagante contratual:** contrato/tipo pagante, ainda que primeira parcela futura.
- **Pagante financeiro da competência:** tem fatura/mensalidade positiva prevista ou paga naquele mês.
- **Bolsista/permutado/professor/estagiário:** ativo, mas não pagante.
- **Sujeira operacional:** ativo sem aula/fatura/frequência, duplicidade, curso errado, nome divergente.

## Próximo passo técnico

Antes de migration em `recalcular_dados_mensais`, produzir uma auditoria Sol/LA Report com:

1. ledger nominal de ativos;
2. ledger nominal de pagantes contratuais;
3. ledger nominal de pagantes financeiros da competência;
4. lista de divergências com motivo e responsável provável;
5. alerta para equipe validar/corrigir;
6. só depois gravar snapshot em `dados_mensais`.

---

## Evidência visual — tela Gestão de Alunos CG/Mai 2026

Print enviado pelo Alf: `/root/.openclaw/media/inbound/file_1165---727aed6e-ee11-4e3b-8931-9c7e0272f564.jpg`

A tela confirma visualmente os KPIs atuais da gestão de alunos para **Campo Grande / Mai 2026**:

- Matrículas Ativas: **562**
- Alunos Ativos: **497**
- Pagantes: **470**
- Bolsistas: **27**
- 2º curso: **27**
- Banda: **41**
- Coral: **0**
- Ticket Médio: **R$386**
- Tempo de Permanência: **19,6 meses**

Filtro aplicado na lista: `Marcos da Silva Saturnr`.

Registro exibido:

- **Marcos da Silva Saturnino**
- Tag: **Bolsista**
- Unidade: CG
- Escola: EMLA
- Professor: Joel de Salles Gouveia Filho
- Curso: Violino
- Dia: Terça
- Horário: 13:00
- Parcela: `-`
- Status: Ativo

Conclusão: o print confirma que Marcos foi reclassificado visualmente como Bolsista e que os KPIs visíveis já estão em **497 ativos / 470 pagantes / 562 matrículas**.
