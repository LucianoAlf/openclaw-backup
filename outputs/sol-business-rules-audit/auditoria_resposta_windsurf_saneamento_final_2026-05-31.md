# Auditoria da resposta Windsurf — Saneamento final ciclo de vida CG/Maio

Data: 2026-05-31
Arquivos auditados:
- `RelatórioFinal-SaneamentoCiclodeVida_Simulação---2b37c530-8740-4da0-85e4-95cd2a59031d.md`
- `Saneamento-de-Ciclo-de-Vida_Campo_Grande_Maio-2026---88fef523-d182-41f9-8c6d-a0c01da9c2c8.sql`

## Veredito

**Não aprovar ainda.** A direção está correta, mas o SQL/relatório ainda têm inconsistências que precisam ser corrigidas antes de qualquer update/RPC.

## Blockers encontrados

### 1) O SQL não é realmente read-only
O arquivo usa:
- `DROP VIEW IF EXISTS preview_saneamento;`
- `CREATE OR REPLACE VIEW preview_saneamento AS ...`
- `DROP VIEW IF EXISTS validacao_pos_update;`
- `CREATE OR REPLACE VIEW validacao_pos_update AS ...`

Isso altera schema. Para revisão, Windsurf deve entregar `SELECT` com CTEs, ou views temporárias dentro de transaction explicitamente controlada. Não chamar isso de read-only.

### 2) Updates sem guards suficientes
Os updates estão por `WHERE id = ...` apenas. Precisam de guards para evitar sobrescrever estado que tenha mudado:
- `unidade_id = '2ec861f6-023f-4d7b-9927-3960ad8c2a92'`
- grupo A/E: `status='inativo' AND data_saida IS NULL`
- grupo B: `status='ativo' AND data_saida='2026-01-09'`
- grupo C: `status='ativo' AND data_saida = <data antiga esperada>`

### 3) Números do relatório não batem com o SQL atual
Simulação própria em cima do estado atual do banco:

| Cenário | alunos_ativos | alunos_pagantes | matriculas_ativas | matriculas_banda |
|---|---:|---:|---:|---:|
| Atual por data, sem excluir projeto | 515 | 485 | 582 | 45 |
| SQL exato proposto, sem excluir projeto | 502 | 474 | 569 | 45 |
| SQL exato proposto + excluir projeto de ativos/pagantes | 495 | 473 | 569 | 45 |
| SQL + Maria/Ana com corte técnico | 500 | 474 | 567 | 43 |
| SQL + todos os D com corte técnico | 498 | 474 | 565 | 41 |

O relatório do Windsurf fala `DEPOIS A = 503/475/570` e `DEPOIS B = 496/474/570`, então há divergência de +1 em várias métricas.

### 4) Grupo D está conceitualmente misturado
Validação do Alf:
- Maria Eduarda (1450): saiu da escola; estava só em banda.
- Ana Julia (1378): não está mais matriculada.
- Alan (1375): só participa de banda, sem curso.
- Leamsi (1393): só participa de banda, sem curso.

Portanto não são todos iguais:
- Maria e Ana devem sair do snapshot ativo/matrículas se não há data real: usar `data_saida='2026-05-31'` como corte técnico, sem movimentação retroativa.
- Alan e Leamsi podem permanecer como participação de banda/projeto, mas devem ser excluídos de `alunos_ativos`/`alunos_pagantes` pela regra `cursos.is_projeto_banda=true`.

O relatório diz que “todos continuam em matriculas_banda”; isso pode estar errado para Maria/Ana.

### 5) Validação pós-update não aplica nova regra de banda
A view `validacao_pos_update` calcula `alunos_ativos` e `alunos_pagantes` sem join em `cursos` e sem filtro `COALESCE(c.is_projeto_banda,false)=false`.

Ela valida o cenário A, não o cenário B. Precisa corrigir.

### 6) Contagem de pagantes precisa ser explicitada
O SQL usa `tipos_matricula.conta_como_pagante`. O relatório trata Alexandre Dos Santos (id 1598) como não pagante por parcela 0, mas no banco ele está como Regular/tipo pagante. Isso muda contagem. Windsurf precisa explicitar a regra usada:
- pagante por `tipos_matricula.conta_como_pagante`, ou
- pagante por valor/parcela/status financeiro?

A regra validada até aqui: pagantes excluem bolsista integral/parcial/não pagante; segundo curso e banda/projeto têm tratamentos próprios. Parcela zero precisa ser auditada, não inferida automaticamente.

## Prompt recomendado para Windsurf

```text
Não aprovar ainda. Corrigir o relatório/SQL antes de execução.

Problemas encontrados:
1. O SQL não é read-only: DROP/CREATE VIEW alteram schema. Trocar previews/validações por SELECTs com CTEs, sem DDL.
2. Updates precisam de guards por unidade/status/data_saida esperada.
3. Os números do relatório não batem com a simulação do SQL atual.
4. Grupo D está misturado: Maria (1450) e Ana Julia (1378) não estão mais matriculadas; devem receber data_saida técnica se não houver data real. Alan (1375) e Leamsi (1393) são só banda; podem permanecer em matriculas_banda, mas não em alunos_ativos/alunos_pagantes.
5. validacao_pos_update não aplica a regra de excluir cursos.is_projeto_banda de alunos_ativos/alunos_pagantes.
6. Explicitar regra de pagante para parcela zero / tipo_matricula Regular, especialmente id 1598.

Use estes cenários de referência, calculados sobre o banco atual:
- Atual por data: 515 ativos / 485 pagantes / 582 matrículas / 45 banda.
- SQL exato atual, sem regra projeto: 502 ativos / 474 pagantes / 569 matrículas / 45 banda.
- SQL exato atual + excluir projeto de ativos/pagantes: 495 ativos / 473 pagantes / 569 matrículas / 45 banda.
- Se Maria e Ana também receberem data_saida='2026-05-31': 500 ativos / 474 pagantes / 567 matrículas / 43 banda; com exclusão projeto: 495 ativos / 473 pagantes / 567 matrículas / 43 banda.

Entregar nova versão:
- relatório sem textos de raciocínio interno (“wait, let me recount” etc.);
- SQL sem DDL no preview;
- SQL com guards;
- simulação READ-ONLY reproduzível;
- before/after dos 28;
- decisão separada para Maria/Ana vs Alan/Leamsi;
- validação com a nova regra de banda aplicada corretamente.

Não executar update, não executar RPC, não backfill.
```
