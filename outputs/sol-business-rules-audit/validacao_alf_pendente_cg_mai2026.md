# Validação pendente com Alf — LA Report / Campo Grande / Maio 2026

Fonte: auditoria Alfredo + resposta Windsurf salva em `windsurf_resposta_cg_mai2026.md`.

## Regras praticamente confirmadas

1. **Pagantes**
   - `pagantes = REGULAR sem segundo curso`
   - Bolsista integral e bolsista parcial não contam como pagantes.
   - Campo/base técnica: `tipos_matricula.conta_como_pagante = true` + excluir `is_segundo_curso`.

2. **Evasões operacionais**
   - `total_evasoes = cancelamentos/evasao + nao_renovacao`
   - Aviso prévio não é evasão.
   - Transferência também não entra em evasão/churn como perda.

3. **Taxa de renovação operacional**
   - `taxa_renovacao = renovacoes / (renovacoes + nao_renovacoes)`
   - Para CG mai/2026: `38 / (38 + 5) = 88,4%`.

4. **Mês corrente**
   - Usar views tempo real (`vw_kpis_gestao_mensal`, com cautela para bugs) e não `dados_mensais`.
   - `dados_mensais` é snapshot/fechamento e pode ficar defasado.

5. **Meta visual**
   - Valores após barra nos cards são metas (`metas_kpi`), não denominadores operacionais.

## Bugs/divergências confirmadas para lista Hugo/equipe

### Alta prioridade
1. `vw_kpis_retencao_mensal.total_evasoes` soma aviso prévio indevidamente.
   - Retorna 21 em vez de 13.
   - Correção: excluir `aviso_previo` da CTE de evasões e manter aviso em CTE/campo separado.

2. Views de renovação retornam 100%, mas regra operacional/relatório é 88,4%.
   - Correção: alinhar view com `renovacoes / (renovacoes + nao_renovacoes)` usando fonte correta.

### Média prioridade
3. Kids/School usa numerador de matrículas (565) e denominador de alunos base (499).
   - Correção depende da regra validada pelo Alf: percentual sobre pessoas ou matrículas.

4. Segundo curso diverge: relatório 28 vs banco 66/68.
   - Precisa definir se relatório conta saldo atual, novas matrículas do mês, ou algum filtro específico.

5. Trancados diverge: relatório 2 vs banco 5.
   - Precisa definir corte/filtro operacional.

### Baixa/média prioridade técnica
6. `dados_mensais` defasado.
   - Recalcular ou automatizar snapshot no fechamento.

7. `evasoes_v2` vazia para 2026.
   - Decidir se será aposentada ou ressuscitada como fonte oficial.

## Perguntas objetivas para o Alf

1. **Total Alunos Ativos**: para KPI principal, trancado entra ou não entra?
   - Opção A: ativo estrito = só `status='ativo'`.
   - Opção B: base operacional = `ativo + trancado`, mas aí o nome não pode ser “ativos”.

2. **Kids/School**: o percentual deve ser sobre:
   - pessoas/alunos sem segundo curso; ou
   - matrículas ativas totais?

3. **Segundo curso**: o número correto do relatório deve representar:
   - saldo atual de matrículas de segundo curso; ou
   - novas matrículas de segundo curso no mês; ou
   - apenas segundo curso pagante específico, excluindo banda/Power Kids/etc.?

4. **Trancados**: a equipe deve listar:
   - todos os trancados atuais; ou
   - só trancamentos do mês; ou
   - só trancados ativos dentro de algum prazo/corte?

5. **Fonte futura de evasões**: consolidamos em `movimentacoes_admin` como fonte canônica ou voltamos a popular `evasoes_v2`?

## Recomendações do Alfredo antes de mexer em código

1. Validar as 5 perguntas com Alf.
2. Gerar lista para Hugo/equipe por unidade.
3. Só depois corrigir SQL/view/frontend.
4. Depois de corrigir, criar/atualizar skill canônica da Sol com as regras validadas.

---

# Respostas do Alf — 2026-05-31

## 1. Alunos ativos
**Validado:** alunos ativos incluem trancados.

## 2. Kids/School
**Validado:** percentual deve ser sobre matrículas.

Correção: hoje o frontend usa numerador de matrículas e denominador de alunos únicos. Deve alinhar denominador para matrículas.

## 3. Segundo curso
**Validado:** correto é 28 em Campo Grande.

Definição: segundo curso é quando aluno pagante faz segundo/terceiro curso pagando.

Importante: bolsista parcial não conta em aluno pagante e também não conta em segundo curso. Caso Vitória: funcionária/bolsista parcial entra indevidamente e leva número a 29, mas deve ser excluída.

## 4. Trancados
**Validado:** correto é 2 em Campo Grande.

Banco retornando 5 precisa auditoria nominal.

## 5. Evasões
**Status:** em auditoria.

Alf suspeita que fonte operacional correta é `movimentacoes_admin`, mas `evasoes_v2` tem histórico importante, principalmente tempo de permanência quando o aluno sai. Não decidir sem auditar o banco.

## Decisão metodológica
Auditar por unidade, não consolidado:
- Campo Grande
- Recreio
- Barra

Cada unidade deve ter divergências próprias para equipe/Hugo validarem.

---

# Relatório Windsurf por unidade recebido — Campo Grande

Arquivo salvo: `windsurf_relatorio_cg_por_unidade_mai2026.md`.

## Novos achados relevantes

- Windsurf confirma `vw_kpis_retencao_mensal` soma aviso prévio em evasões: bug SQL.
- Windsurf confirma taxa de renovação 100% nas views: bug SQL/dado.
- Query corrigida de segundo curso pagante encontrou 27, mas relatório operacional é 28. Diferença ainda precisa reconciliação nominal.
- Todos os 41 alunos de banda/Power Kids estão como segundo curso, mas devem aparecer no KPI Banda se Alf validar que Banda mede participantes do projeto.
- Trancados nominais no banco: 5; relatório operacional: 2.

## Próxima validação necessária com Alf

1. Card/KPI Banda deve mostrar todos os alunos em projetos de banda/Power Kids, mesmo todos sendo 2º curso? Provável sim, mas precisa cravar.
2. Em segundo curso pagante, registros com valor R$ 0/null devem ser excluídos automaticamente? Provável sim, mas precisa cravar.
