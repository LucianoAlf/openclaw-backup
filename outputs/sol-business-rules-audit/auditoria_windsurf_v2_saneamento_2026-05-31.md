# Auditoria Alfredo — Windsurf v2 saneamento ciclo de vida CG/Maio

Data: 2026-05-31
Arquivos auditados:
- `Saneamento-de-Ciclo-de-Vida_Campo_Grande_Maio-2026---7cec49df-740b-4b9a-9438-9878cfa11424.sql`
- `UPDATES-COM-GUARDS_Campo_Grande_Maio_2026---56fad2b2-b51d-454a-9c17-98b69997c535.sql`

## Veredito

**Melhorou muito, mas ainda NÃO aprovar execução.**

Os updates estão perto, mas a simulação e a regra proposta para `recalcular_dados_mensais` ainda têm um blocker sério: `curso_id IS NOT NULL` exclui uma aluna real ativa.

## O que está correto agora

- Preview sem DDL: OK, agora usa SELECT/CTE.
- Update em arquivo separado e comentado: OK.
- Maria 1450 e Ana Julia 1378 separadas de Alan/Leamsi: OK.
- Alan 1375 e Leamsi 1393 sem update, dependendo da regra de banda: OK.
- Emilly id 106 com data correta 2026-03-05: OK.
- Arthur id 47: update só muda status para inativo e mantém data_saida 2026-01-09: OK.
- Maria/Ana/Luciano/Alexandre com corte técnico 2026-05-31: conceitualmente aceitável como saneamento de estoque, sem movimentação retroativa.

## Blockers

### 1) Não aprovar `curso_id IS NOT NULL` como regra de ativos/pagantes/matrículas

Windsurf propôs/mostrou regra:
- `curso_id IS NOT NULL` para ativos/pagantes/matrículas

Isso exclui:
- Alexandre id 1598 — ok, validado pelo Alf como excluído.
- **Giovanna Campos Peixoto Ueoka id 1619 — NÃO validado para excluir.**

Evidência: Giovanna aparece no CSV Emusys de ativos/em andamento:
- Nome: Giovanna Campos Peixoto Ueoka
- Curso: Teclado / Piano
- Prof. Fabricio Oliveira
- Em Andamento, conclusão 10/02/2027
- Mensalidade 447,00

No Supabase, id 1619 está:
- status ativo
- data_matricula 2026-04-15
- data_saida NULL
- valor_parcela 387.0
- tipo_aluno pagante
- curso_id NULL

Conclusão: `curso_id NULL` aqui parece dado incompleto no LA Report, não aluno inexistente. Não pode virar regra de exclusão sem validar/corrigir esse cadastro.

Regra correta por enquanto:
- excluir `cursos.is_projeto_banda = true` de `alunos_ativos`/`alunos_pagantes`;
- não usar `curso_id IS NOT NULL` como filtro global;
- tratar `curso_id NULL` como alerta de qualidade de dados, não exclusão automática.

### 2) Simulação ainda tem bug no Grupo B / Arthur

Na CTE `alunos_virt`, todo registro em `correcoes` com `nova_data_saida IS NULL` vira `data_saida_virt = NULL`.

Isso limpa virtualmente Arthur id 47, mesmo a regra dizendo:
- status -> inativo;
- manter `data_saida = 2026-01-09`.

O update está correto, mas a simulação não representa o update.

O resultado agregado aparenta bater por compensação: exclui Giovanna via `curso_id IS NOT NULL` e inclui Arthur por limpar data virtualmente. Dois erros se anulando parcialmente.

### 3) Preview nominal também pode marcar Arthur incorretamente

A lógica de `no_snapshot_virt` tem `WHEN c.id IS NOT NULL AND c.nova_data_saida IS NULL ... THEN 'SIM'`, que serve para Grupo C, mas também pega Grupo B/F. Precisa considerar `grupo` explicitamente:
- B: manter data_saida atual;
- C: limpar data_saida;
- F: sem update, apenas excluído de ativos/pagantes pela regra banda.

### 4) Updates ainda deveriam ter asserts

O arquivo de update agora tem guards bons, mas apenas imprime `RAISE NOTICE`. Se um guard falhar, o DO block continua.

Recomendado: pré-validar contagens esperadas ou lançar `RAISE EXCEPTION` se o total alterado por grupo não bater:
- Grupo A: 16
- Grupo B: 1
- Grupo C: 5
- Grupo D: 2
- Grupo E: 2

Também seria melhor no Grupo C usar datas esperadas por ID, não só `data_saida IS NOT NULL`.

## Números de referência sem `curso_id IS NOT NULL`

Com a lógica desejada (sem excluir curso_id NULL globalmente; excluir só projeto/banda):

- Atual por data: 515 ativos / 485 pagantes / 582 matrículas / 45 banda
- Após correções dos 28: 500 ativos / 474 pagantes / 567 matrículas / 43 banda
- Após correções + excluir `is_projeto_banda=true` de ativos/pagantes: 495 ativos / 473 pagantes / 567 matrículas / 43 banda

Esses números batem com o resultado final, mas não pelo motivo certo no SQL atual.

## Prompt para Windsurf

```text
Melhorou, mas ainda não aprovar execução.

Blocker principal: NÃO usar `curso_id IS NOT NULL` como regra global para alunos_ativos/pagantes/matrículas.
Isso exclui Giovanna Campos Peixoto Ueoka id 1619, que aparece no CSV Emusys como ativa/em andamento em Teclado/Piano, mensalidade 447, conclusão 10/02/2027.
No Supabase ela está status='ativo', data_saida NULL, tipo pagante, mas curso_id NULL. Isso é dado incompleto, não regra de exclusão.

Regra correta:
- alunos_ativos/pagantes devem excluir `cursos.is_projeto_banda = true`.
- NÃO filtrar `curso_id IS NOT NULL` globalmente.
- `curso_id NULL` deve aparecer como alerta de qualidade/correção cadastral.

Segundo blocker: a simulação virtual ainda limpa data_saida de Arthur id 47, porque `correcoes` tem nova_data_saida NULL e a CTE transforma isso em data_saida_virt NULL.
Mas Arthur deve manter data_saida='2026-01-09' e só mudar status para inativo.
Corrigir `alunos_virt` usando grupo/ação explícita:
- grupo A/D/E: aplicar nova_data_saida
- grupo B/F: manter data_saida atual
- grupo C: limpar data_saida

Corrigir também `no_snapshot_virt` do preview com a mesma lógica por grupo.

No arquivo de updates:
- adicionar asserts/RAISE EXCEPTION por contagem esperada dos grupos: A=16, B=1, C=5, D=2, E=2.
- idealmente Grupo C com guards por data_saida esperada por ID.

Números de referência esperados sem `curso_id IS NOT NULL` global:
- Atual por data: 515 / 485 / 582 / 45
- Após correções dos 28: 500 / 474 / 567 / 43
- Após correções + excluir projeto/banda de ativos/pagantes: 495 / 473 / 567 / 43

Gerar v3 sem executar update/RPC/backfill.
```
