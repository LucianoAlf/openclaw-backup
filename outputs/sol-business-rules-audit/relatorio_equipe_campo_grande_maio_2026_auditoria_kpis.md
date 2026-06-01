# Relatório para equipe — Auditoria dos números de Campo Grande / Maio 2026

## 1. O que estávamos fazendo

Fizemos uma conferência dos números de **Campo Grande em maio/2026**, principalmente:

- alunos ativos;
- alunos pagantes;
- matrículas ativas;
- bolsistas;
- segundos cursos;
- matrículas de banda/projeto.

O objetivo foi entender por que o número de pagantes que aparecia como **475** mudou para **470** depois da revisão.

Essa auditoria não foi para “punir” ninguém. Foi para limpar a base e garantir que a unidade esteja olhando para números reais, sem duplicidade e sem aluno contado errado.

---

## 2. Número atual após a revisão

Depois das correções feitas, o painel atual de Campo Grande / Maio 2026 está assim:

| Indicador | Número atual |
|---|---:|
| Alunos ativos | **496** |
| Alunos pagantes | **470** |
| Matrículas ativas | **561** |
| Matrículas de banda/projeto | **41** |
| Segundo curso | **27** |
| Novas matrículas | **23** |
| Evasões | **13** |


> Correção: a view bruta expõe 65 linhas com `is_segundo_curso=true`, mas esse total inclui 38 matrículas de banda/projeto que já entram no KPI de banda. O card de Gestão de Alunos usa a regra operacional correta: **27 segundos cursos não-banda + 41 banda**.

> Observação: o Marcos foi colocado como **inativo**, porque não estava mais frequentando as aulas. Por isso ele também saiu da base de ativos/matrículas.

---

## 3. Por que caiu de 475 para 470 pagantes?

O número anterior estava inflado por cinco casos que não deveriam estar contando como pagantes.

### 1. Bruna Damasceno

Havia duas entradas para a mesma aluna, com variação no nome:

- Bruna Damasceno Castro;
- Bruna Damasceno de Castro.

Uma entrada estava com valor correto, e outra estava zerada. A entrada duplicada/zerada foi removida/corrigida.

**Impacto:** tirou uma contagem indevida.

---

### 2. Carlos Eduardo Garcia do Nascimento

O Carlos é bolsista integral por uma parceria/permuta com a empresa do pai.

Ele estava correto como bolsista em um curso, mas o outro curso ainda aparecia como se fosse pagante zerado. Isso foi corrigido.

**Status correto:** bolsista integral nos dois cursos.  
**Impacto:** não deve contar como pagante.

---

### 3. Miguel Gomes Biancamano

O Miguel é professor/bolsista.

Estava aparecendo de forma que podia contaminar a contagem de pagantes. Foi corrigido para bolsista integral.

**Status correto:** bolsista integral.  
**Impacto:** não deve contar como pagante.

---

### 4. Matheus Reis da Silva Gaspar

O Matheus é estagiário e bolsista integral.

Estava zerado, mas ainda podia entrar como pagante. Foi corrigido.

**Status correto:** bolsista integral.  
**Impacto:** não deve contar como pagante.

---

### 5. Marcos da Silva Saturnino

O Marcos é professor da escola e tinha bolsa integral para estudar.

Ele não estava pagando e também não estava frequentando as aulas. Primeiro foi corrigido como bolsista; depois foi colocado como inativo.

**Status correto:** inativo / não pagante.  
**Impacto:** não deve contar como pagante nem como aluno ativo.

---

## 4. Resumo da queda

O número de pagantes caiu porque havia alunos/pessoas que estavam entrando como pagantes, mas não eram pagantes reais.

| Caso | Motivo |
|---|---|
| Bruna Damasceno | duplicidade de cadastro/nome |
| Carlos Eduardo | bolsista integral / permuta |
| Miguel Gomes | professor / bolsista integral |
| Matheus Reis | estagiário / bolsista integral |
| Marcos Saturnino | professor / bolsista integral / não frequenta mais |

Por isso o número saiu de **475 pagantes** para **470 pagantes**.

---

## 5. Casos que ainda precisam ser verificados pela equipe

Ainda existem casos que não são para corrigir no escuro. Precisam ser verificados com calma.

### Ana Clara Lima Santos Pinto

A Ana Clara está fazendo aula, mas no LA Report aparece com valor zerado/nulo.

Foi identificado que faturas dela foram removidas/movidas. A equipe precisa verificar o que aconteceu com essas faturas e por que o cadastro ficou sem valor correto.

**Ponto de atenção:** confirmar situação das faturas e corrigir o financeiro/cadastro.

---

### Anna Clara de Souza Iorio Sales

Caso parecido com o da Ana Clara.

Ela também aparece zerada no LA Report, e há indício de faturas removidas/movidas. No Emusys não ficou clara a fatura/pagamento.

**Ponto de atenção:** verificar com a equipe o que aconteceu com as faturas e corrigir o cadastro se necessário.

---

### Sofia Elaile da Silva Campos

Aluna nova de Violino.

Foi matriculada em abril, pagou passaporte, mas não começou em maio. Vai começar em junho e pagar a primeira parcela em junho.

**Ponto de atenção:** não tratar como erro simples. É caso de matrícula feita antes do início real da cobrança mensal.

---

### Sofia Lauermann Silva

Aluna nova de Canto.

Pagou passaporte e começa em junho. A primeira parcela será em junho.

**Ponto de atenção:** mesmo caso da Sofia Elaile: matrícula/passaporte em um mês e mensalidade recorrente no mês seguinte.

---

## 6. O que aprendemos com essa auditoria

O problema não foi só um número errado. A auditoria mostrou que precisamos cruzar melhor as informações entre sistemas.

Os principais tipos de inconsistência encontrados foram:

1. aluno duplicado por diferença no nome;
2. bolsista/professor/estagiário aparecendo como pagante;
3. aluno ativo sem fatura correta;
4. fatura removida ou transferida sem reflexo correto no relatório;
5. aluno matriculado em um mês, mas começando a pagar no mês seguinte;
6. aluno ativo no sistema, mas sem frequência real.

---

## 7. Encaminhamento para a equipe

A equipe precisa revisar principalmente:

1. Ana Clara Lima Santos Pinto — entender faturas removidas/movidas;
2. Anna Clara de Souza Iorio Sales — entender faturas removidas/movidas;
3. garantir que bolsistas/professores/estagiários não entrem como pagantes;
4. evitar duplicidade de cadastro por nome diferente;
5. sinalizar quando aluno pagou passaporte, mas só começa mensalidade no mês seguinte;
6. revisar alunos ativos que não frequentam e não pagam.

---

## 8. Conclusão

O número **470 pagantes** é o número correto no painel após a limpeza dos casos encontrados.

O número **475** estava inflado por inconsistências de cadastro e classificação.

A partir daqui, o ideal é transformar esse tipo de conferência em rotina automática, para que esses problemas sejam apontados antes de afetarem meta, relatório e tomada de decisão.
