# Prompt Windsurf — Saneamento final dos 28 casos CG/Maio 2026

Você está olhando arquivo desatualizado. As decisões dos 28 casos já foram validadas pelo Alf com:
- auditoria Alfredo/Windsurf;
- CSV Emusys de ativos;
- CSV Emusys de ex-alunos;
- validação visual/foto do Alf.

NÃO executar SQL ainda.
NÃO rodar RPC/backfill ainda.
Gerar SQL final com guards + simulação READ-ONLY.

## Regra nova validada

Participação apenas em banda/projeto NÃO mantém aluno como ativo de curso.

Para `alunos_ativos` e `alunos_pagantes`:
- excluir `alunos.is_segundo_curso = true`;
- excluir cursos onde `cursos.is_projeto_banda = true`;
- pagantes também excluem bolsistas integrais/parciais/não pagantes.

Banda/projeto deve ser contabilizado separadamente em `matriculas_banda`, não em aluno ativo de curso.

Não criar `movimentacoes_admin` retroativas sem evidência. Este saneamento é de estoque/ciclo de vida, não de eventos/churn.

---

## A) Ex-alunos com data real validada — preencher `data_saida`

Gerar SQL com guards (`status='inativo'`, `data_saida IS NULL` quando aplicável, id exato):

```text
id 106  Emilly Souza de Oliveira              data_saida = 2026-03-05  -- validado pelo Alf; não usar 2026-03-07
id 85   Davi Borges da Silva Nascimento       data_saida = 2026-04-25
id 94   Davi Rosendo Chaves Vieira            data_saida = 2026-04-01
id 131  Gabriel Pereira Morais                data_saida = 2026-03-03
id 137  Georgie Jefferson de Mello Basílio    data_saida = 2026-05-07
id 149  Guilherme Gama Clavelario Nunes       data_saida = 2026-05-04
id 165  Heitor Thadeu Caciano                 data_saida = 2026-04-11
id 224  Laura Peres de Souza                  data_saida = 2026-04-02
id 258  Luís Rafael Sousa dos Santos          data_saida = 2026-05-06
id 270  Manuela Piveta Schulz                 data_saida = 2026-04-02
id 327  Murilo Martellote de Assis            data_saida = 2026-03-06
id 354  Pedro Martellote de Assis             data_saida = 2026-03-06
id 384  Sophia Maciel Magalhaes               data_saida = 2026-04-10
id 11   Alexandre Wallace Bispo Oliveira      data_saida = 2026-03-14
id 118  Felipe Marques Gevezier               data_saida = 2026-03-23
id 1377 Alexandre de Sousa Serra              data_saida = 2026-04-01
```

---

## B) Ativo falso — corrigir status, não limpar saída

```text
id 47 Arthur Souza Del Bosco
- Emusys ex-aluno: interrompido em 2026-01-09
- LA Report tem status='ativo' e data_saida='2026-01-09'
- Propor status='inativo'
- NÃO limpar data_saida
```

---

## C) Ativos/matriculados confirmados pelo Alf — limpar `data_saida`

Gerar SQL com guards (`status='ativo'`, `data_saida IS NOT NULL`, id exato):

```text
id 31  Anne Krissya Cordeiro da Silva Noé     limpar data_saida = NULL  -- aluna bolsista de Piano + Banda; ativa, não pagante
id 263 Luiza Mazeliah do Nascimento           limpar data_saida = NULL  -- guitarra
id 405 Vicente Dias Botelho                   limpar data_saida = NULL  -- piano + duas bandas
id 323 Miguel Santos Borges                   limpar data_saida = NULL  -- piano/teclado
id 949 Cassyo Lucas Prado Silva               limpar data_saida = NULL  -- piano/teclado
```

---

## D) Casos que aparecem como Em Andamento no Emusys, mas Alf validou que NÃO são alunos ativos de curso

Não tratar como ativos de curso.
Não contar em `alunos_ativos` nem `alunos_pagantes`.
Preservar/representar banda/projeto separadamente.

```text
id 1450 Maria Eduarda de Lima Bomfim Pedro
- Não está mais matriculada; saiu da escola; estava só em banda.
- Não contar como ativa/pagante.
- Se não houver data real, propor data_saida='2026-05-31' apenas como corte técnico de estoque, sem movimentacao_admin.

id 1375 Alan Samico do Nascimento
- Não está matriculado em curso; só participa de banda.
- Não contar como aluno ativo de curso/pagante.
- Não inventar evasão.
- Preferência: corrigir a regra da função para excluir curso/projeto banda via cursos.is_projeto_banda=true.

id 1378 Ana Julia de Oliveira Gomes
- Não está mais matriculada.
- Não contar como ativa/pagante.
- Se não houver data real, propor data_saida='2026-05-31' apenas como corte técnico de estoque, sem movimentacao_admin.

id 1393 Leamsi Guedes de Sant'anna
- Não está matriculado em curso; só participa de banda.
- Não contar como aluno ativo de curso/pagante.
- Não inventar evasão.
- Preferência: corrigir a regra da função para excluir curso/projeto banda via cursos.is_projeto_banda=true.
```

---

## E) Pendentes resolvidos pelo Alf — excluídos/não matriculados

```text
id 945 Luciano da Silva Bernardino
- Alf validou: aluno excluído, não está matriculado, não está no fluxo ativo.
- Não contar como ativo/pagante.
- Se não houver data real, propor data_saida='2026-05-31' como corte técnico de estoque, sem movimentacao_admin.

id 1598 Alexandre Dos Santos
- Alf validou: aluno excluído do Emusys e está inativo no LA Report.
- Não contar como ativo/pagante.
- Se não houver data real, propor data_saida='2026-05-31' como corte técnico de estoque, sem movimentacao_admin.
```

---

## Entrega esperada

1. Atualizar o arquivo de auditoria local com as decisões acima.
2. Gerar SQL final em modo revisão, com guards.
3. Não executar SQL ainda.
4. Rodar simulação READ-ONLY aplicando virtualmente as correções.
5. Mostrar antes/depois dos 28 casos.
6. Mostrar impacto projetado em:
   - alunos_ativos
   - alunos_pagantes
   - churn_rate
   - matriculas_ativas
   - matriculas_banda
7. Simular também a regra nova:
   - `alunos_ativos` exclui `cursos.is_projeto_banda = true`;
   - `alunos_pagantes` exclui projeto/banda e bolsistas/não pagantes.
8. Só após validação do Alf executar updates.
9. Só após updates + nova simulação bater, executar `recalcular_dados_mensais(2026, 5, Campo Grande)`.
10. Não fazer backfill Jan–Abr, Barra ou Recreio ainda.

Importante: não forçar o número 499. O objetivo agora é composição nominal correta e regra limpa.
